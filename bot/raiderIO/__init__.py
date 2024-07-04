import ssl
from tqdm import tqdm
import re
import asyncio
from typing import List, Optional
from ratelimit import limits, sleep_and_retry
import httpx

from bot.raiderIO.models.character import Character


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
                    if response.json()["guild"] is None:
                        guild_name = None
                    else:
                        guild_name = response.json()["guild"]["name"]
                    faction = response.json()["faction"]
                    role = response.json()["active_spec_role"]
                    spec_name = response.json()["active_spec_name"]
                    player_class = response.json()["class"]
                    achievement_points = response.json()["achievement_points"]
                    item_level = response.json()["gear"]["item_level_equipped"]

                    character = Character(
                        name=name,
                        realm=realm,
                        guild_name=guild_name,
                        faction=faction,
                        role=role,
                        spec_name=spec_name,
                        class_name=player_class,
                        achievement_points=achievement_points,
                        item_level=item_level,
                        score=0,
                    )
                    return character
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
