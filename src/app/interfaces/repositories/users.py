from abc import ABC, abstractmethod
from uuid import UUID

from app.interfaces.repositories.base import (
    IBaseRepository,
    MODEL,
)


class IUserRepository(IBaseRepository, ABC):

    @abstractmethod
    async def get_by_username(self, username: str) -> MODEL:
        raise NotImplementedError
