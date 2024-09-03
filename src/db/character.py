from typing import List, Optional, Any
from src.db import CharacterOrm, sessionmanager
from src.entities import Character, CharacterCreate
from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound
from abc import ABCMeta, abstractmethod
import uuid


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
        on_raid_roster=instance.on_raid_roster,
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
        on_raid_roster=instance.on_raid_roster,
        spec_name=instance.spec_name,
        profile_url=instance.profile_url,
        class_name=instance.class_name,
        thumbnail_url=instance.thumbnail_url,
        last_crawled_at=instance.last_crawled_at,
    )


def character_create_entity_to_model(instance: CharacterCreate) -> CharacterOrm:
    return CharacterOrm(
        name=instance.name,
        region=instance.region,
        realm=instance.realm,
        item_level=instance.item_level,
        discord_user_id=instance.discord_user_id,
        guild_id=instance.guild_id,
        spec_name=instance.spec_name,
        on_raid_roster=instance.on_raid_roster,
        profile_url=instance.profile_url,
        class_name=instance.class_name,
        thumbnail_url=instance.thumbnail_url,
        last_crawled_at=instance.last_crawled_at,
    )


class CharacterRepository:

    async def get_by_discord_user_id(self, discord_user_id: str) -> Character:
        async with sessionmanager.session() as session:
            result = (
                await session.execute(
                    select(CharacterOrm).where(
                        CharacterOrm.discord_user_id == discord_user_id
                    )
                )
            ).scalar_one()

            return character_model_to_entity(result)

    async def does_exist(self, discord_user_id: str) -> bool:
        try:
            return (
                await self.get_by_discord_user_id(discord_user_id=discord_user_id)
            ) is not None
        except NoResultFound:
            return False
        except Exception:
            raise

    async def add_character(self, character: CharacterCreate) -> Character:
        async with sessionmanager.session() as session:
            model = character_create_entity_to_model(character)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return character_model_to_entity(model)

    async def get_characters_on_raider_role(
        self, guild_id: uuid.UUID
    ) -> List[Character]:
        async with sessionmanager.session() as session:
            results = (
                (
                    await session.execute(
                        select(CharacterOrm).where(
                            and_(
                                CharacterOrm.guild_id == guild_id,
                                CharacterOrm.on_raid_roster == True,
                            )
                        )
                    )
                )
                .scalars()
                .all()
            )

            return [character_model_to_entity(result) for result in results]
