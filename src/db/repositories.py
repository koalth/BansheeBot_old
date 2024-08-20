from typing import Optional
from sqlalchemy import select, and_

from .database import get_session
from .interfaces import ICharacterRepository, IGuildRepository

from src.mapper import (
    character_entity_to_model,
    character_model_to_entity,
    guild_entity_to_model,
    guild_model_to_entity,
)

from src.entities import Character, Guild
from .models import GuildOrm, CharacterOrm


class GuildRepository(IGuildRepository):

    def _get_entity(self, instance: Optional[GuildOrm]) -> Optional[Guild]:
        if instance is None:
            return None
        return guild_model_to_entity(instance)

    async def get_by_id(self, id: int) -> Optional[Guild]:
        async with get_session() as session:
            result = await session.execute(select(GuildOrm).where(GuildOrm.id == id))
            return self._get_entity(result.scalar_one_or_none())

    async def get_by_discord_guild_id(self, discord_guild_id: int) -> Optional[Guild]:
        async with get_session() as session:
            result = await session.execute(
                select(GuildOrm).where(GuildOrm.discord_guild_id == discord_guild_id)
            )
            return self._get_entity(result.scalar_one_or_none())

    async def get_by_guild_name_and_realm(
        self, name: str, realm: str
    ) -> Optional[Guild]:
        async with get_session() as session:
            result = await session.execute(
                select(GuildOrm).where(
                    and_(GuildOrm.name == name, GuildOrm.realm == realm)
                )
            )
            return self._get_entity(result.scalar_one_or_none())

    async def add(self, entity: Guild) -> Optional[Guild]:
        async with get_session() as session:
            model = guild_entity_to_model(entity)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._get_entity(model)


class CharacterRepository(ICharacterRepository):

    def _get_entity(self, instance: Optional[CharacterOrm]) -> Optional[Character]:
        if instance is None:
            return None
        return character_model_to_entity(instance)

    async def get_by_discord_user_id(self, discord_user_id: int) -> Optional[Character]:
        async with get_session() as session:
            result = await session.execute(
                select(CharacterOrm).where(
                    CharacterOrm.discord_user_id == discord_user_id
                )
            )

            return self._get_entity(result.scalar_one_or_none())

    async def get_by_name_and_realm(self, name: str, realm: str) -> Optional[Character]:
        async with get_session() as session:
            result = await session.execute(
                select(CharacterOrm).where(
                    and_(CharacterOrm.name == name, CharacterOrm.realm == realm)
                )
            )

            return self._get_entity(result.scalar_one_or_none())

    async def add(self, entity: Character) -> Optional[Character]:
        async with get_session() as session:
            model = character_entity_to_model(entity)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._get_entity(model)
