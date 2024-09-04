from pydantic import BaseModel
import uuid
from typing import List, Generic, TypeVar
from src.db import Base
from abc import ABCMeta, abstractmethod


ModelType = TypeVar("ModelType", bound=Base)
EntityType = TypeVar("EntityType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class IGenericRepository(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, EntityType],
    metaclass=ABCMeta,
):

    @abstractmethod
    async def create(self, obj_in: CreateSchemaType) -> EntityType:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, id: uuid.UUID) -> EntityType:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self, *filter_conditions) -> List[EntityType]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_filters(self, *filter_conditions) -> EntityType:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, id: uuid.UUID, obj_in: UpdateSchemaType) -> EntityType:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> bool:
        raise NotImplementedError()


class ICharacterRepository(
    IGenericRepository[ModelType, CreateSchemaType, UpdateSchemaType, EntityType],
    metaclass=ABCMeta,
):
    pass


class IGuildRepository(
    IGenericRepository[ModelType, CreateSchemaType, UpdateSchemaType, EntityType],
    metaclass=ABCMeta,
):
    pass


class ISettingRepository(
    IGenericRepository[ModelType, CreateSchemaType, UpdateSchemaType, EntityType],
    metaclass=ABCMeta,
):
    pass


class IMockRepository(
    IGenericRepository[ModelType, CreateSchemaType, UpdateSchemaType, EntityType],
    metaclass=ABCMeta,
):
    pass
