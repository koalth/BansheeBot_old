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

from src.models import (
    GuildDTO,
    CharacterDTO,
    Region,
)
from src.raiderIO.models import CharacterResponse, GuildResponse
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
    except ValidationError as err:
        logger.debug(err.json())
        logger.error(f"Validation error in getCharacterProfile: {err}")
        return None
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

            response = await get("characters/profile", params, CharacterResponse)

            if response is None:
                logger.debug("Response was none")
                return None

            return CharacterDTO(
                name=response.name,
                realm=response.realm,
                region=Region(response.region),
                class_name=response.character_class,
                profile_url=response.profile_url,
                last_crawled_at=response.last_crawled_at,
                item_level=0,  # will need to be updated
                thumbnail_url=response.thumbnail_url,
            )
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
            response = await get("guilds/profile", params, GuildResponse)

            if response is None:
                logger.debug("Response was none")
                return None
            return GuildDTO(
                name=response.name, region=Region(response.region), realm=response.realm
            )
        except ValidationError as err:
            logger.error(f"Validation error in getGuildProfile: {err}")
            return None
        except Exception as err:
            logger.error(f"There was an error in getGuildProfile: {err}")
            return None
