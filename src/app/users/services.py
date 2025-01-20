from abc import ABC
from http.client import HTTPException

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
    repo: IUserRepository

    def __init__(self, repo: IUserRepository = Depends()):
        self.repo = repo


class UserService(IUserService):

    @staticmethod
    async def get_response_schema(obj: UserModel) -> UserSchema:
        return UserSchema(
            uuid=obj.uuid,
            username=obj.username,
            email=obj.email,
            fullname=obj.fullname,
            is_active=obj.is_active,
            role=obj.role,
        )

    @staticmethod
    async def hash_password(password) -> bytes:
        """
        Generates hash for password to save in database
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    async def validate_password(password: str, db_password: bytes) -> bool:
        """
        Checks password with saved hashed password
        """
        return bcrypt.checkpw(password.encode(), db_password)

    @staticmethod
    async def generate_token(db_user: UserModel) -> TokenSchema:
        """
        Generates access token for user
        """
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
        else:
            raise ObjectDoesNotExistException(self._MODEL, object_id=data.username)

    async def validate_token(self, data: TokenSchema) -> TokenPayload:
        return await self.decode_token(data.access_token)