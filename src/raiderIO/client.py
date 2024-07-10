import ssl
from tqdm import tqdm
import asyncio
from ratelimit import limits, sleep_and_retry
import httpx
from typing import List, Optional, Dict
import urllib.parse

import logging

logger = logging.getLogger("RaiderIOClient")
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


from httpx import Response

from src.raiderIO.models.character import Character
from src.raiderIO.schemas.schema import CharacterSchema

from src.raiderIO.models.guild import Guild, GuildSchema

from marshmallow import ValidationError


API_URL = "https://raider.io/api/v1"
CALLS = 200
RATE_LIMIT = 60
TIMEOUT = 10
RETRIES = 5
BACKOFF_FACTOR = 2


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def get(endpoint: str, params: Dict[str, str]) -> Response:
    for retry in range(RETRIES):
        try:
            async with httpx.AsyncClient() as client:

                if len(params) > 0:
                    endpoint = f"{endpoint}?{urllib.parse.urlencode(params)}"

                logger.debug(f"{endpoint}")

                response = await client.get(f"{API_URL}/{endpoint}")

                if response.status_code != 200:
                    logger.error(f"Response error: {response.status_code}")
                    return None

                return response

        except (httpx.TimeoutException, httpx.ReadTimeout, ssl.SSLWantReadError):
            if retry == RETRIES - 1:
                logger.info(f"Request timeout, retrying...")
                raise
            else:
                await asyncio.sleep(BACKOFF_FACTOR * (2**retry))

        except Exception as err:
            logger.error(
                f"There was an error requesting endpoint: {endpoint} with params: {params}. Error: {err}"
            )
            return None


class RaiderIOClient:

    async def getCharacterProfile(
        name: str, realm="Dalaran", region="us"
    ) -> Optional[Character]:
        try:
            params = {
                "region": region,
                "realm": realm,
                "name": name,
                "fields": "guild,gear",
            }
            response = await get("characters/profile", params)

            character_schema = CharacterSchema()
            try:
                character_io = character_schema.load(response.json())
            except ValidationError as err:
                logger.error(f"Error during validation: {err}")
                raise err

            return character_io

        except Exception as err:
            logger.error(f"There was an error in getCharacterProfile: {err}")
            return None

    async def getGuildProfile(
        name: str, realm: str = "Dalaran", region: str = "us"
    ) -> Optional[Guild]:
        try:
            params = {"region": region, "realm": realm, "name": name}
            response = await get("guilds/profile", params)
            guild_schema = GuildSchema()
            try:
                guild_io = guild_schema.load(response.json())
            except ValidationError as err:
                logger.error(f"Error during validation: {err}")
                raise err

            return guild_io
        except Exception as err:
            logger.error(f"There was an error in getGuildProfile: {err}")
            return None
