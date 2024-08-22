import contextlib
from typing import Any, AsyncIterator, Optional
from src.config import config

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from .models import Base


class DatabaseSessionManager:

    def __init__(self, database_url: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(database_url, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            expire_on_commit=False, bind=self._engine
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not intialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None
