from abc import abstractmethod, ABC
from pydantic import BaseModel, ValidationError
from typing import Dict, Optional, TypeVar
from aiolimiter import AsyncLimiter
import urllib.parse
import aiohttp
from loguru import logger


ModelType = TypeVar("ModelType", bound=BaseModel)


class APIClient:

    API_URL: str

    RATE_LIMIT: int = 100
    TIMEOUT: int
    RETRIES: int
    BACKOFF_FACTOR: int

    def __init__(self, api_url: str):
        self.API_URL = api_url

    async def _get(
        self, endpoint: str, params: Dict[str, str], model_cls: type[ModelType]
    ) -> Optional[ModelType]:
        try:
            async with AsyncLimiter(self.RATE_LIMIT):
                async with aiohttp.ClientSession() as client:
                    if len(params) > 0:
                        endpoint = f"{endpoint}?{urllib.parse.urlencode(params)}"
                    async with client.get(f"{self.API_URL}/{endpoint}") as response:
                        response.raise_for_status()
                        json_data = await response.json()
                        return model_cls(**json_data)
        except ValidationError as err:
            logger.exception(f"Validation error in APIClient")
            return None
        except Exception as err:
            logger.error(
                f"There was an error requesting endpoint: {endpoint} with params: {params}. Error: {err}"
            )
            return None
