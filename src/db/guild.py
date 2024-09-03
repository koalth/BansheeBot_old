from typing import List, Optional, Any
from src.db import GuildOrm, sessionmanager
from src.db.character import character_model_to_entity
from src.entities import Guild, GuildCreate
from sqlalchemy import select


def guild_model_to_entity(instance: GuildOrm) -> Guild:
    return Guild(
        id=instance.id,
        name=instance.name,
        realm=instance.realm,
        region=instance.region,
        discord_guild_id=instance.discord_guild_id,
        item_level_requirement=0,
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


def guild_create_entity_to_model(instance: GuildCreate) -> GuildOrm:
    return GuildOrm(
        name=instance.name,
        realm=instance.realm,
        region=instance.region,
        discord_guild_id=instance.discord_guild_id,
    )


class GuildRepository:

    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Guild:
        async with sessionmanager.session() as session:
            result = (
                await session.execute(
                    select(GuildOrm).where(
                        GuildOrm.discord_guild_id == discord_guild_id
                    )
                )
            ).scalar_one()

            return guild_model_to_entity(result)

    async def add_guild(self, guild: GuildCreate) -> Guild:
        async with sessionmanager.session() as session:
            model = guild_create_entity_to_model(guild)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return guild_model_to_entity(model)
