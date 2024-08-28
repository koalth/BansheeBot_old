from loguru import logger
import inject
from typing import Optional
from src.db import get_db_session
from src.entities import Settings


class SettingsService:

    async def get_settings(self, discord_guild_id: str) -> Optional[Settings]:
        pass
