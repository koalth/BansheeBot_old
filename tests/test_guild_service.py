from src.services import GuildService
from src.entities import Guild
import pytest


@pytest.mark.asyncio
async def test_guild_service():
    mock_response = Guild(name="fake", realm="Dalaran", region="us")
    _sut = GuildService()

    assert await _sut.get_by_guild_name_and_realm("fake", "Dalaran") == mock_response
