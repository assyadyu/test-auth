from typing import TypeVar

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.sessions import async_session
from app.interfaces.repositories.base import IBaseRepository

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class SQLAlchemyBaseRepository(IBaseRepository):
    session: AsyncSession
    _MODEL: MODEL

    def __init__(self, *, session: async_session = Depends()):
        self.session = session

    async def create(self, obj: MODEL) -> MODEL:
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def create_from_data(self, data: BaseModel, *args, **kwargs) -> MODEL:
        obj = self._MODEL(**data.model_dump(exclude_none=True))
        return await self.create(obj=obj)
