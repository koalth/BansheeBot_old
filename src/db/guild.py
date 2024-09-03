from typing import List, Optional, Any
from src.db import GuildOrm, sessionmanager
from src.db.character import character_model_to_entity
from src.entities import Guild
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


def guild_model_to_entity(instance: GuildOrm) -> Guild:
    return Guild(
        id=instance.id,
        name=instance.name,
        realm=instance.realm,
        region=instance.region,
        discord_guild_id=instance.discord_guild_id,
        characters=[character_model_to_entity(char) for char in instance.characters],
    )


def guild_entity_to_model(instance: Guild) -> GuildOrm:
    return GuildOrm(
        name=instance.name,
        realm=instance.realm,
        region=instance.region,
        discord_guild_id=instance.discord_guild_id,
        characters=[],
    )


class GuildRepository:

    @staticmethod
    async def get_by_discord_guild_id(discord_guild_id: str) -> Optional[Guild]:
        async with sessionmanager.session() as session:
            result = (
                await session.execute(
                    select(GuildOrm).where(
                        GuildOrm.discord_guild_id == discord_guild_id
                    )
                )
            ).scalar_one_or_none()

            if result is None:
                return None
            return guild_model_to_entity(result)

    @staticmethod
    async def add_guild(guild: Guild) -> Optional[Guild]:
        async with sessionmanager.session() as session:
            model = guild_entity_to_model(guild)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return guild_model_to_entity(model)
