import ssl
from tqdm import tqdm
from aiolimiter import AsyncLimiter

from typing import Optional, Dict, TypeVar
import urllib.parse
import aiohttp
from pydantic import BaseModel

import logging

logger = logging.getLogger("RaiderIOClient")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

from src.models import GuildDTO, CharacterDTO
from pydantic import ValidationError

API_URL = "https://raider.io/api/v1"
CALLS = 200
RATE_LIMIT = 60
TIMEOUT = 10
RETRIES = 5
BACKOFF_FACTOR = 2


T = TypeVar("T", bound=BaseModel)


async def get(endpoint: str, params: Dict[str, str], content: type[T]) -> Optional[T]:
    try:
        async with AsyncLimiter(100):
            async with aiohttp.ClientSession() as client:
                if len(params) > 0:
                    endpoint = f"{endpoint}?{urllib.parse.urlencode(params)}"
                async with client.get(f"{API_URL}/{endpoint}") as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    return content(**json_data)

    except Exception as err:
        logger.error(
            f"There was an error requesting endpoint: {endpoint} with params: {params}. Error: {err}"
        )
        return None


class RaiderIOClient:

    @staticmethod
    async def getCharacterProfile(
        name: str, realm="Dalaran", region="us"
    ) -> Optional[CharacterDTO]:
        try:
            params = {
                "region": region,
                "realm": realm,
                "name": name,
                "fields": "guild,gear",
            }

            return await get("characters/profile", params, CharacterDTO)
        except ValidationError as err:
            logger.error(f"Validation error in getCharacterProfile: {err}")
            return None
        except Exception as err:
            logger.error(f"There was an error in getCharacterProfile: {err}")
            return None

    @staticmethod
    async def getGuildProfile(
        name: str, realm: str = "Dalaran", region: str = "us"
    ) -> Optional[GuildDTO]:
        try:
            params = {"region": region, "realm": realm, "name": name}
            return await get("guilds/profile", params, GuildDTO)
        except ValidationError as err:
            logger.error(f"Validation error in getGuildProfile: {err}")
            return None
        except Exception as err:
            logger.error(f"There was an error in getGuildProfile: {err}")
            return None
