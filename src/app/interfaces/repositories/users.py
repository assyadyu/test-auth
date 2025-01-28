from abc import ABC, abstractmethod

from app.interfaces.repositories.base import (
    IBaseRepository,
    MODEL,
)
from app.users.schemas import UserSignupSchema


class IUserRepository(IBaseRepository, ABC):
    """
    Implementation of base repository interface for users
    """

    @abstractmethod
    async def get_by_username(self, username: str) -> MODEL:
        """
        Get user by username
        :param username: username to search for
        :return: object of MODEL type corresponding to username
        """
        raise NotImplementedError

    @abstractmethod
    async def validate_new_user(self, data: UserSignupSchema) -> None:
        """
        Check if username and email are valid, i.e. not used already
        If error occurs, raise corresponding exception
        :param data: user data
        :return: None
        """
        raise NotImplementedError
