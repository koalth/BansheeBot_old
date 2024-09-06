import inject
from loguru import logger
from src.entities import Character, CharacterCreate, CharacterUpdate
from src.external import IRaiderIOClient, CharacterResponse
from .base import IGenericService
from src.db import ICharacterRepository, CharacterOrm
from abc import abstractmethod, ABCMeta
from uuid import UUID
from typing import List, Optional
from sqlalchemy.exc import NoResultFound


class ICharacterService(
    IGenericService[CharacterOrm, CharacterCreate, CharacterUpdate, Character]
):

    @abstractmethod
    async def get_characters_with_raid_role(self, guild_id: UUID) -> List[Character]:
        raise NotImplementedError

    @abstractmethod
    async def get_character_from_raider_io(
        self, name: str, realm: str, region: str
    ) -> CharacterResponse:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_did(self, discord_id: str) -> Character:
        raise NotImplementedError()

    @abstractmethod
    async def has_character(self, discord_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def add_character(
        self, name: str, realm: str, region: str, discord_user_id: str, guild_id: UUID
    ) -> Character:
        raise NotImplementedError()


class CharacterService(
    ICharacterService,
):

    raiderioClient: IRaiderIOClient = inject.attr(IRaiderIOClient)
    repository: ICharacterRepository = inject.attr(ICharacterRepository)

    async def get_characters_with_raid_role(self, guild_id: UUID) -> List[Character]:
        return await self.repository.get_all(
            CharacterOrm.guild_id == guild_id, CharacterOrm.on_raid_roster == True
        )

    async def get_character_from_raider_io(
        self, name: str, realm: str, region: str
    ) -> Optional[CharacterResponse]:
        try:
            character_io = await self.raiderioClient.getCharacterProfile(
                name, realm, region
            )

            return character_io
        except Exception:
            return None

    async def get_by_did(self, discord_id: str) -> Character:
        return await self.repository.get_by_filters(
            CharacterOrm.discord_user_id == discord_id
        )

    async def has_character(self, discord_id: str) -> bool:
        try:
            result = await self.get_by_did(discord_id)
            return result is not None
        except NoResultFound:
            return False

    async def add_character(
        self, name: str, realm: str, region: str, discord_user_id: str, guild_id: UUID
    ) -> Character:

        character_io = await self.get_character_from_raider_io(name, realm, region)

        if character_io is None:
            raise ValueError("No character from raider io")

        create_obj = CharacterCreate(
            name=character_io.name,
            realm=character_io.realm,
            region=character_io.region,
            discord_user_id=discord_user_id,
            guild_id=guild_id,
            on_raid_roster=True,
            item_level=character_io.gear.item_level_equipped,
            class_name=character_io.character_class,
            spec_name=character_io.active_spec_name,
            profile_url=character_io.profile_url,
            thumbnail_url=character_io.thumbnail_url,
            last_crawled_at=character_io.last_crawled_at,
        )

        return await self.repository.create(create_obj)
