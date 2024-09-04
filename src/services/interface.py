from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Optional, List, Generic, TypeVar, Type
from sqlalchemy import select, delete
from src.db import sessionmanager, Base, IGenericRepository

ModelType = TypeVar("ModelType", bound=Base)
EntityType = TypeVar("EntityType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class IGenericService(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, EntityType]
):
    repository: IGenericRepository

    async def create(self, create_entity: CreateSchemaType) -> EntityType:
        return await self.repository.create(create_entity)

    async def get(self, id: uuid.UUID) -> EntityType:
        return await self.repository.get(id)

    async def get_all(self, *filter_conditions) -> List[EntityType]:
        return await self.repository.get_all(*filter_conditions)

    async def update(
        self, id: uuid.UUID, update_entity: UpdateSchemaType
    ) -> EntityType:
        return await self.repository.update(id, update_entity)

    async def delete(self, id: uuid.UUID) -> bool:
        return await self.repository.delete(id)
