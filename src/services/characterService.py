from loguru import logger
import inject
from typing import Optional, List
from src.entities import Character, CharacterCreate
from src.raiderIO import IRaiderIOClient, CharacterResponse
from datetime import datetime, timezone
from src.db import CharacterRepository
import uuid
from abc import abstractmethod, ABCMeta


class ICharacterService(metaclass=ABCMeta):

    @abstractmethod
    async def get_character_from_raider_io(
        self, name: str, realm: str, region: str
    ) -> Optional[Character]:
        raise NotImplementedError()

    @abstractmethod
    async def add_character_to_guild(
        self,
        character: Character,
        discord_user_id: str,
        on_raider_role: bool,
        guild_id: uuid.UUID,
    ):
        raise NotImplementedError()

    @abstractmethod
    async def get_characters_on_raid_role(self, guild_id: uuid.UUID) -> List[Character]:
        raise NotImplementedError()


def convert_datetime(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc)


def character_response_to_entity(instance: CharacterResponse) -> CharacterCreate:
    return CharacterCreate(
        name=instance.name,
        realm=instance.realm,
        region=instance.region,
        discord_user_id="",
        guild_id=None,
        on_raid_roster=False,
        item_level=instance.gear.item_level_equipped,
        class_name=instance.character_class,
        spec_name=instance.active_spec_name,
        profile_url=instance.profile_url,
        thumbnail_url=instance.thumbnail_url,
        last_crawled_at=convert_datetime(instance.last_crawled_at),
    )


class CharacterService(ICharacterService):

    characterRepository: CharacterRepository = inject.attr(CharacterRepository)
    raiderIOClient: IRaiderIOClient = inject.attr(IRaiderIOClient)

    async def get_character_from_raider_io(
        self, name: str, realm: str, region: str
    ) -> Optional[CharacterCreate]:

        try:
            character = await self.raiderIOClient.getCharacterProfile(
                name, realm, region
            )

            if character == None:
                return None

            return character_response_to_entity(character)
        except Exception:
            logger.exception("There was problem in CharacterService")
            raise

    async def get_characters_on_raid_role(self, guild_id: uuid.UUID) -> List[Character]:
        return await self.characterRepository.get_characters_on_raider_role(guild_id)

    async def add_character_to_guild(
        self,
        character: CharacterCreate,
        discord_user_id: str,
        on_raider_role: bool,
        guild_id: uuid.UUID,
    ):
        try:
            if await self.characterRepository.does_exist(discord_user_id):
                return None

            character.discord_user_id = discord_user_id
            character.guild_id = guild_id
            character.on_raid_roster = on_raider_role

            return await self.characterRepository.add_character(character=character)
        except Exception:
            logger.exception("There was problem in CharacterService")
            raise
