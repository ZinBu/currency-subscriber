import typing
from abc import ABC, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import SQLModel


class BaseOrmCrudTool(ABC):

    @property
    @abstractmethod
    def model(self) -> SQLModel:
        ...

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_all(self) -> list:
        result = await self._db_session.execute(select(self.model))
        return typing.cast(list, result.scalars().all())

    async def retrieve(self, obj_id: int) -> Optional[SQLModel]:
        return await self._db_session.get(self.model, obj_id)

    async def create(self, obj: Union[dict, BaseModel, SQLModel]) -> SQLModel:
        model_object = obj if isinstance(obj, SQLModel) else self.model(**self._extract_model(obj))
        self._db_session.add(model_object)  # todo add_all
        await self._db_session.commit()
        await self._db_session.refresh(model_object)
        return model_object

    async def bulk_create(self, objs: list[Union[dict, BaseModel, SQLModel]]) -> None:
        if isinstance(objs[0], SQLModel):
            model_objects = objs
        else:
            model_objects = [self.model(**self._extract_model(obj)) for obj in objs]
        self._db_session.add_all(model_objects)
        await self._db_session.commit()

    async def update(self, obj_id: int, obj: Union[dict, BaseModel]) -> Optional[SQLModel]:
        update_construction = update(self.model).where(self.model.id == obj_id).values(**self._extract_model(obj))
        await self._db_session.execute(update_construction)
        await self._db_session.commit()
        updated_result = await self._db_session.execute(select(self.model).where(self.model.id == obj_id))
        return updated_result.scalars().first()

    @staticmethod
    def _extract_model(obj: Union[dict, BaseModel]) -> dict:
        return obj if isinstance(obj, dict) else obj.dict()
