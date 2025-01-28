from abc import ABC, abstractmethod

import bcrypt
import jwt
from fastapi import Depends

from app.common import settings
from app.common.exceptions.exceptions import InvalidTokenException, ObjectDoesNotExistException
from app.db.models import UserModel
from app.interfaces.repositories.users import IUserRepository
from app.users.schemas import (
    UserSignupSchema,
    UserSigninSchema,
    UserSchema,
    TokenSchema,
    TokenPayload,
)


class IUserService(ABC):
    """
    User service for basic operations of user registration and authentication
    """
    repo: IUserRepository

    def __init__(self, repo: IUserRepository = Depends()):
        self.repo = repo

    @staticmethod
    @abstractmethod
    async def hash_password(password) -> bytes:
        """
        Generate hash for password to save in database
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def validate_password(password: str, db_password: bytes) -> bool:
        """
        Check password with saved hashed password
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def generate_token(db_user: UserModel) -> TokenSchema:
        """
        Generate access token for user
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def decode_token(encoded_token: str) -> TokenPayload:
        """
        Decode access token to extract user data
        :param encoded_token: encoded token
        :return: decoded user data
        """
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, data: UserSignupSchema) -> UserSchema:
        """
        Create new user base on data
        :param self:
        :param data:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def signin_user(self, data: UserSigninSchema) -> TokenSchema:
        """
        Signin user based on data
        :param data: user credentials
        :return: token for authentication
        """
        raise NotImplementedError

    @abstractmethod
    async def validate_token(self, data: TokenSchema) -> TokenPayload:
        """
        Decrypt token to get encoded user data
        :param data: encoded token
        :return: decoded user data
        """
        raise NotImplementedError


class UserService(IUserService):

    @staticmethod
    async def get_response_schema(obj: UserModel) -> UserSchema:
        """
        Convert DB object to DTO
        :param obj: user object
        :return: user schema
        """
        return UserSchema(
            uuid=obj.uuid,
            username=obj.username,
            email=obj.email,
            fullname=obj.fullname,
            is_active=obj.is_active,
            role=obj.role,
        )

    @staticmethod
    async def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    async def validate_password(password: str, db_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), db_password)

    @staticmethod
    async def generate_token(db_user: UserModel) -> TokenSchema:
        payload = TokenPayload(
            uuid=str(db_user.uuid),
            username=db_user.username,
            role=db_user.role,
            is_active=db_user.is_active,
        )
        return TokenSchema(
            access_token=jwt.encode(payload.__dict__, settings.SECRET_KEY, algorithm='HS256'),
            token_type="Bearer",
        )

    @staticmethod
    async def decode_token(encoded_token: str) -> TokenPayload:
        try:
            return jwt.decode(encoded_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            raise InvalidTokenException()

    async def create_user(self, data: UserSignupSchema) -> UserSchema:
        hashed_password = await self.hash_password(data.password)
        obj = await self.repo.create_from_data(data, hashed_password=hashed_password)
        return await self.get_response_schema(obj)

    async def signin_user(self, data: UserSigninSchema) -> TokenSchema:
        db_user = await self.repo.get_by_username(data.username)
        if db_user and await self.validate_password(data.password, db_user.hashed_password):
            return await self.generate_token(db_user)
        raise ObjectDoesNotExistException(self.repo._MODEL, object_id=data.username)

    async def validate_token(self, data: TokenSchema) -> TokenPayload:
        return await self.decode_token(data.access_token)
