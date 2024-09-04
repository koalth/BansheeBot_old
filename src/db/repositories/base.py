from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Optional, List, Generic, TypeVar, Type
from sqlalchemy import select, delete
from src.db import sessionmanager, Base
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
    async def update(self, id: uuid.UUID, obj_in: UpdateSchemaType) -> EntityType:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> bool:
        raise NotImplementedError()


class GenericRepository(
    IGenericRepository[ModelType, CreateSchemaType, UpdateSchemaType, EntityType]
):
    def __init__(self, model: Type[ModelType], entity: Type[EntityType]):
        self.model = model
        self.entity = entity

    async def create(self, obj_in: CreateSchemaType) -> EntityType:
        db_obj = self.model(**obj_in.model_dump())
        async with sessionmanager.session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return self.entity.model_validate(db_obj)

    async def get(self, id: uuid.UUID) -> EntityType:
        stmt = select(self.model).where(self.model.id == id)
        async with sessionmanager.session() as session:
            results = await session.execute(stmt)
            obj = results.scalar_one()
            return self.entity.model_validate(obj)

    async def get_all(self, *filter_conditions) -> List[EntityType]:
        stmt = select(self.model)
        if filter_conditions:
            stmt = stmt.where(*filter_conditions)
        async with sessionmanager.session() as session:
            results = await session.execute(stmt)
            return [self.entity.model_validate(obj) for obj in results.scalars().all()]

    async def update(self, id: uuid.UUID, obj_in: UpdateSchemaType) -> EntityType:
        stmt = select(self.model).where(self.model.id == id)
        async with sessionmanager.session() as session:
            results = await session.execute(stmt)
            db_obj = results.scalar_one()
            update_data = obj_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            await session.commit()
            await session.refresh(db_obj)
            return self.entity.model_validate(db_obj)

    async def delete(self, id: uuid.UUID) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        async with sessionmanager.session() as session:
            results = await session.execute(stmt)
            await session.commit()
            return results.rowcount > 0


class GenericService(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, EntityType]
):
    repository: GenericRepository

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
