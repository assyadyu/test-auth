from abc import abstractmethod, ABC
from typing import TypeVar

from pydantic import BaseModel

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class IBaseRepository(ABC):

    @abstractmethod
    async def create(self, obj: MODEL) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def create_from_data(self, data: BaseModel, *args, **kwargs) -> MODEL:
        raise NotImplementedError
