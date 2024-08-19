from src.db import GuildRepository
from src.services import GuildService
from src.entities import Guild
import pytest


@pytest.mark.asyncio
async def test_guild_service(mocker):
    mock_response = Guild(name="fake", realm="Dalaran", region="us")
    repo = GuildRepository()
    mocker.patch.object(repo, "get_by_guild_name_and_realm", return_value=mock_response)
    _sut = GuildService(repo)

    assert await _sut.get_by_guild_name_and_realm("fake", "Dalaran") == mock_response
