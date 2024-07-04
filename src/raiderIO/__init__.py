import ssl
from tqdm import tqdm
import re
import asyncio
from typing import List, Optional
from ratelimit import limits, sleep_and_retry
import httpx
from marshmallow import ValidationError

from src.raiderIO.models.character import Character
from src.raiderIO.schemas.schema import CharacterSchema

API_URL = "https://raider.io/api/v1/"
CALLS = 200
RATE_LIMIT = 60
TIMEOUT = 10
RETRIES = 5
BACKOFF_FACTOR = 2


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def get_character(name: str, realm="Dalaran", region="us") -> Optional[Character]:
    for retry in range(RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    API_URL
                    + f"characters/profile?region={region}&realm={realm}&name={name}&fields=guild,gear",
                    timeout=TIMEOUT,
                )
                if response.status_code == 200:

                    character_schema = CharacterSchema()

                    try:
                        character_io = character_schema.load(response.json())
                    except ValidationError as err:
                        print("Validation Error: ", err)
                        raise err

                    return character_io
                else:
                    print(response.status_code)
                    print(f"Error: API Error. {response.status_code}")
                    return None
        except (httpx.TimeoutException, httpx.ReadTimeout, ssl.SSLWantReadError):
            if retry == RETRIES - 1:
                raise
            else:
                await asyncio.sleep(BACKOFF_FACTOR * (2**retry))

        except Exception as exception:
            print(exception)
            return None
