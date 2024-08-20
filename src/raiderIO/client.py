from aiolimiter import AsyncLimiter
from typing import Optional, Dict, TypeVar
import urllib.parse
import aiohttp
from pydantic import BaseModel, ValidationError
from loguru import logger
from .models import CharacterResponse, GuildResponse

T = TypeVar("T", bound=BaseModel)


class RaiderIOClient:

    api_url: str
    calls: int
    rate_limit: int
    timeout: int
    retries: int
    backoff_factor: int

    def __init__(
        self,
        api_url: str,
        calls: int,
        rate_limit: int,
        timeout: int,
        retries: int,
        backoff_factor: int,
    ):
        self.api_url = api_url
        self.calls = calls
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor

    async def _get(
        self, endpoint: str, params: Dict[str, str], content: type[T]
    ) -> Optional[T]:
        try:
            async with AsyncLimiter(100):
                async with aiohttp.ClientSession() as client:
                    if len(params) > 0:
                        endpoint = f"{endpoint}?{urllib.parse.urlencode(params)}"
                    async with client.get(f"{self.api_url}/{endpoint}") as response:
                        response.raise_for_status()
                        json_data = await response.json()
                        return content(**json_data)
        except ValidationError as err:
            logger.debug(err.json())
            logger.error(f"Validation error in getCharacterProfile: {err}")
            return None
        except Exception as err:
            logger.error(
                f"There was an error requesting endpoint: {endpoint} with params: {params}. Error: {err}"
            )
            return None

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
                logger.debug("Response was none")
                return None

            return response
        except ValidationError as err:
            logger.error(f"Validation error in getCharacterProfile: {err}")
            return None
        except Exception as err:
            logger.error(f"There was an error in getCharacterProfile: {err}")
            return None

    async def getGuildProfile(
        self, name: str, realm: str = "Dalaran", region: str = "us"
    ) -> Optional[GuildResponse]:
        try:
            params = {"region": region, "realm": realm, "name": name}
            response = await self._get("guilds/profile", params, GuildResponse)

            if response is None:
                logger.debug("Response was none")
                return None
            return response
        except ValidationError as err:
            logger.error(f"Validation error in getGuildProfile: {err}")
            return None
        except Exception as err:
            logger.error(f"There was an error in getGuildProfile: {err}")
            return None
