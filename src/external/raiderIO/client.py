from typing import Optional
from .models import CharacterResponse, GuildResponse
from .interface import APIClient
from abc import ABC, abstractmethod

from loguru import logger


class IRaiderIOClient(ABC):

    @abstractmethod
    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> Optional[CharacterResponse]:
        raise NotImplementedError()

    @abstractmethod
    async def getGuildProfile(
        self, name: str, realm: str, region: str
    ) -> Optional[GuildResponse]:
        raise NotImplementedError()


class RaiderIOClient(IRaiderIOClient, APIClient):

    def __init__(self, api_url: str):
        super().__init__(api_url=api_url)

    async def getCharacterProfile(
        self, name: str, realm: str = "Dalaran", region="us"
    ) -> Optional[CharacterResponse]:
        try:
            params = {
                "region": region,
                "realm": realm,
                "name": name,
                "fields": "gear",
            }

            response = await self._get("characters/profile", params, CharacterResponse)

            if response is None:
                logger.debug("getCharacterProfile :: response was none")
                return None

            return response
        except Exception:
            logger.exception(f"There was an error in getCharacterProfile")
            return None

    async def getGuildProfile(
        self, name: str, realm: str, region: str
    ) -> GuildResponse | None:
        try:
            params = {
                "region": region,
                "realm": realm,
                "name": name,
            }

            response = await self._get("guilds/profile", params, GuildResponse)

            if response is None:
                logger.debug("getGuildProfile :: response was none")
                return None

            return response
        except Exception:
            logger.exception(f"There was an error in getGuildProfile")
            return None


class MockRaiderIOClient(IRaiderIOClient):

    character_response: Optional[CharacterResponse]
    guild_response: Optional[GuildResponse]

    def __init__(
        self,
        character_response: Optional[CharacterResponse] = None,
        guild_response: Optional[GuildResponse] = None,
    ):
        self.character_response = character_response
        self.guild_response = guild_response

    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> Optional[CharacterResponse]:

        return self.character_response

    async def getGuildProfile(
        self, name: str, realm: str, region: str
    ) -> GuildResponse | None:
        return self.guild_response
