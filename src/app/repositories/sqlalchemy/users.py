import sqlalchemy as sa

from app.common.exceptions.exceptions import (
    ObjectDoesNotExistException,
    UsernameAlreadyRegisteredException,
    EmailAlreadyRegisteredException,
)
from app.db.models import UserModel
from app.interfaces.repositories.users import IUserRepository
from app.repositories.sqlalchemy.base import (
    SQLAlchemyBaseRepository,
    MODEL,
)
from app.users.schemas import UserSignupSchema


class UserRepository(IUserRepository, SQLAlchemyBaseRepository):
    _MODEL: MODEL = UserModel

    async def validate_new_user(self, data: UserSignupSchema) -> None:
        stmt = sa.select(self._MODEL).filter_by(username=data.username)
        resp = await self.session.execute(stmt)
        if resp.scalar():
            raise UsernameAlreadyRegisteredException(username=data.username)
        stmt = sa.select(self._MODEL).filter_by(email=data.email)
        resp = await self.session.execute(stmt)
        if resp.scalar():
            raise EmailAlreadyRegisteredException(email=data.email)

    async def create_from_data(self, data: UserSignupSchema, *args, **kwargs) -> MODEL:
        """
        Creates new user from given data replacing str password with hashed one
        :param data: input data from request
        :param kwargs: contains hashed_password
        :return: User object
        """
        await self.validate_new_user(data)
        obj = self._MODEL(**data.model_dump(exclude={"password", }))
        obj.hashed_password = kwargs["hashed_password"]
        return await self.create(obj=obj)

    async def get_by_username(self, username: str) -> MODEL:
        """
        Called during signin to check if username exists and to validate password
        :param username: username of user trying to sign in
        :return: existing User object or raises ObjectDoesNotExistException
        """
        stmt = sa.select(self._MODEL).filter_by(username=username)
        resp = await self.session.execute(stmt)
        res = resp.scalar()
        if res:
            return res
        else:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=username)
