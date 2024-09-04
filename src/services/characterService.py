import inject
from loguru import logger
from src.entities import Character, CharacterCreate, CharacterUpdate
from src.external import IRaiderIOClient, CharacterResponse
from .base import GenericService, IGenericService
from src.db import ICharacterRepository, CharacterOrm
from abc import abstractmethod, ABCMeta
from uuid import UUID
from typing import List, Optional


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
