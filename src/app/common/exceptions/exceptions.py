from typing import Union
from uuid import UUID

from app.db.models.base import BaseModel


class ApplicationBaseException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ObjectDoesNotExistException(ApplicationBaseException):
    def __init__(self, model: BaseModel, object_id: Union[UUID, str, int]):
        msg = f"{model.__name__} object id {object_id} not found"
        super().__init__(msg)


class UsernameAlreadyRegisteredException(ApplicationBaseException):
    def __init__(self, username: str):
        msg = f"User with this username {username} already exists"
        super().__init__(msg)


class EmailAlreadyRegisteredException(ApplicationBaseException):
    def __init__(self, email: str):
        msg = f"User with this email {email} already exists"
        super().__init__(msg)


class InvalidTokenException(ApplicationBaseException):
    def __init__(self):
        msg = "Token is not valid"
        super().__init__(msg)
