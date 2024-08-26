from typing import Optional
from .models import CharacterResponse
from .interface import APIClient
from abc import ABC, abstractmethod

from loguru import logger


class IRaiderIOClient(ABC):

    @abstractmethod
    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> Optional[CharacterResponse]:
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


class MockRaiderIOClient(IRaiderIOClient):

    response: CharacterResponse

    def __init__(self, response: CharacterResponse):
        self.response = response

    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> Optional[CharacterResponse]:

        if (
            self.response.name == name
            and self.response.realm == realm
            and self.response.region == region
        ):
            return self.response
        else:
            return None
