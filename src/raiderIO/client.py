from typing import Optional
from .models import CharacterResponse
from .interface import APIClient

from loguru import logger


class RaiderIOClient(APIClient):

    def __init__(self, api_url: str):
        super().__init__(api_url=api_url)

    async def getCharacterProfile(
        self, name: str, realm="Dalaran", region="us"
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
