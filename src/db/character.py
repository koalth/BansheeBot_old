from typing import List, Optional, Any
from src.db import CharacterOrm, sessionmanager
from src.entities import Character
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


def character_model_to_entity(instance: CharacterOrm) -> Character:
    return Character(
        id=instance.id,
        name=instance.name,
        region=instance.region,
        realm=instance.realm,
        item_level=instance.item_level,
        discord_user_id=instance.discord_user_id,
        guild_id=instance.guild_id,
        spec_name=instance.spec_name,
        profile_url=instance.profile_url,
        class_name=instance.class_name,
        thumbnail_url=instance.thumbnail_url,
        last_crawled_at=instance.last_crawled_at,
    )


def character_entity_to_model(instance: Character) -> CharacterOrm:
    return CharacterOrm(
        name=instance.name,
        region=instance.region,
        realm=instance.realm,
        item_level=instance.item_level,
        discord_user_id=instance.discord_user_id,
        guild_id=instance.guild_id,
        spec_name=instance.spec_name,
        profile_url=instance.profile_url,
        class_name=instance.class_name,
        thumbnail_url=instance.thumbnail_url,
        last_crawled_at=instance.last_crawled_at,
    )


class CharacterRepository:

    @staticmethod
    async def get_by_discord_user_id(discord_user_id: str) -> Optional[Character]:
        async with sessionmanager.session() as session:
            result = (
                await session.execute(
                    select(CharacterOrm).where(
                        CharacterOrm.discord_user_id == discord_user_id
                    )
                )
            ).scalar_one_or_none()

            if result is None:
                return None
            return character_model_to_entity(result)

    @staticmethod
    async def add_character(character: Character) -> Optional[Character]:
        async with sessionmanager.session() as session:
            model = character_entity_to_model(character)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return character_model_to_entity(model)
