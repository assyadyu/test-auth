from fastapi import FastAPI

from app.db.sessions import (
    async_session,
    session_factory,
)
from app.interfaces.repositories.base import IBaseRepository
from app.interfaces.repositories.users import IUserRepository
from app.repositories.sqlalchemy.base import SQLAlchemyBaseRepository
from app.repositories.sqlalchemy.users import UserRepository
from app.users.services import (
    UserService,
    IUserService,
)


def bind_dependencies(app: FastAPI, db_url: str):
    app.dependency_overrides[async_session] = session_factory(db_url)

    app.dependency_overrides[IBaseRepository] = SQLAlchemyBaseRepository
    app.dependency_overrides[IUserRepository] = UserRepository

    app.dependency_overrides[IUserService] = UserService
