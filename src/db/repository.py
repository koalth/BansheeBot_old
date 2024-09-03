from uuid import UUID
from dataclasses import asdict
from typing import Generic, TypeVar, Type, List, Optional, Any, Callable
from sqlalchemy import select
from sqlalchemy.sql.expression import delete

from .models import Base
from .session import sessionmanager
from src.entities import _BaseEntity, _CreateBaseEntity, _UpdateBaseEntity

ModelType = TypeVar("ModelType", bound=Base)
EntityType = TypeVar("EntityType", bound=_BaseEntity)
CreateSchemaType = TypeVar("CreateSchemaType", bound=_CreateBaseEntity)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=_UpdateBaseEntity)


class GenericRepository(
    Generic[ModelType, EntityType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(
        self,
        model: Type[ModelType],
        entity: Type[EntityType],
        model_to_entity: Callable[[ModelType], EntityType],
        entity_to_model: Callable[[Type[EntityType]], Type[ModelType]],
    ) -> None:
        self.model = model
        self.entity = entity
        self.model_to_entity = model_to_entity
        self.entity_to_model = entity_to_model

    async def get(self, id: UUID) -> EntityType:
        stmt = select(self.model).where(self.model.id == id)
        async with sessionmanager.session() as session:
            result = await session.execute(stmt)
            obj = result.scalar_one()
            return self.model_to_entity(obj)

    async def get_all(self, *filter_conditions) -> List[EntityType]:
        stmt = select(self.model)
        if filter_conditions:
            stmt = stmt.where(*filter_conditions)
        async with sessionmanager.session() as session:
            results = await session.execute(stmt)
            return [self.model_to_entity(result) for result in results.scalars().all()]

    async def create(self, obj_in: CreateSchemaType) -> EntityType:
        async with sessionmanager.session() as session:
            db_obj = self.model(**asdict(obj_in))
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return self.model_to_entity(db_obj)

    async def update(self, id: UUID, obj_in: UpdateSchemaType) -> EntityType:
        stmt = select(self.model).where(self.model.id == id)
        async with sessionmanager.session() as session:
            results = await session.execute(stmt)
            db_obj = results.scalar_one()
            for key, value in asdict(obj_in).items():
                setattr(db_obj, key, value)
            await session.commit()
            await session.refresh(db_obj)
            return self.model_to_entity(db_obj)

    async def delete(self, id: UUID) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        async with sessionmanager.session() as session:
            results = await session.execute(stmt)
            await session.commit()
            return results.rowcount > 0
