from typing import Union
from uuid import UUID

from app.db.models.base import BaseModel
from fastapi import FastAPI


def register_exception_handler(app: FastAPI):
    app.add_exception_handler(ObjectDoesNotExistException, object_does_not_exist_exception_handler)


class ApplicationBaseException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ObjectDoesNotExistException(ApplicationBaseException):
    def __init__(self, model: BaseModel, object_id: Union[UUID, str, int]):
        msg = f"{model.__name__} object id {object_id} not found"
        super().__init__(msg)
