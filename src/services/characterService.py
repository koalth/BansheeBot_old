from loguru import logger
import inject
from typing import Optional
from src.entities import Character
from src.raiderIO import IRaiderIOClient
from src.mapper import character_response_to_entity
from src.db import CharacterRepository
import uuid
from abc import abstractmethod, ABCMeta


class ICharacterService(metaclass=ABCMeta):

    @abstractmethod
    async def get_character(
        self, name: str, realm: str, region: str
    ) -> Optional[Character]:
        raise NotImplementedError()

    @abstractmethod
    async def add_character_to_guild(
        self,
        character: Character,
        discord_user_id: str,
        guild_id: uuid.UUID,
    ):
        raise NotImplementedError()


class CharacterService(ICharacterService):

    raiderIOClient: IRaiderIOClient = inject.attr(IRaiderIOClient)

    async def get_character(
        self, name: str, realm: str, region: str
    ) -> Optional[Character]:

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

    async def add_character_to_guild(
        self,
        character: Character,
        discord_user_id: str,
        guild_id: uuid.UUID,
    ):
        try:
            result = await CharacterRepository.get_by_discord_user_id(discord_user_id)
            if result is not None:
                return None

            character.guild_id = guild_id

            return await CharacterRepository.add_character(character=character)
        except Exception:
            logger.exception("There was problem in CharacterService")
            raise
