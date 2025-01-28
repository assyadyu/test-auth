from abc import abstractmethod, ABC
from typing import TypeVar

from pydantic import BaseModel

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class IBaseRepository(ABC):
    """
    Simplified base repository to create objects in repository
    """

    @abstractmethod
    async def create(self, obj: MODEL) -> MODEL:
        """
        Create object of MODEL type in repository
        :param obj: object to be created in repository
        :return: created object of MODEL type
        """
        raise NotImplementedError

    @abstractmethod
    async def create_from_data(self, data: BaseModel, *args, **kwargs) -> MODEL:
        """
        Create object of MODEL type in repository from DTO
        :param data: DTO
        :param args: additional arguments
        :param kwargs: additional keyword arguments
        :return: created object of MODEL type
        """
        raise NotImplementedError
