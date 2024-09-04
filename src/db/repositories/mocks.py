from pydantic import BaseModel
import uuid
from src.db import Base
from unittest.mock import AsyncMock

from .interfaces import IMockRepository
from typing import List, Generic, TypeVar, Type

ModelType = TypeVar("ModelType", bound=Base)
EntityType = TypeVar("EntityType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class MockGenericRepository(
    IMockRepository[ModelType, CreateSchemaType, UpdateSchemaType, EntityType],
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, EntityType],
):
    def __init__(self, model: Type[ModelType], entity: Type[EntityType]):
        self.model = model
        self.entity = entity

    async def get(self, id: uuid.UUID) -> EntityType:
        return AsyncMock()()

    async def get_all(self, *filter_conditions) -> List[EntityType]:
        return AsyncMock()()

    async def get_by_filters(self, *filter_conditions) -> EntityType:
        return AsyncMock()()

    async def update(self, id: uuid.UUID, obj_in: UpdateSchemaType) -> EntityType:
        return AsyncMock()()

    async def delete(self, id: uuid.UUID) -> bool:
        return AsyncMock()()
