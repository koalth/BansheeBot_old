from typing import List
from src.db import (
    IGuildRepository,
    ICharacterRepository,
    MockGuildRepository,
    MockCharacterRepository,
)
from src.services import GuildService
from src.entities import Guild
import pytest
from src.injector import inject, base_config


@pytest.fixture
def mock_guilds() -> List[Guild]:
    guilds = [
        Guild(name="fake1", realm="Dalaran", region="us"),
        Guild(name="fake2", realm="Dalaran", region="us"),
        Guild(name="fake3", realm="Arthas", region="us"),
    ]
    return guilds


@pytest.fixture
def setup_injector(mock_guilds):

    def test_config(binder: inject.Binder):
        binder.install(base_config)

        # override dependencies
        binder.bind(IGuildRepository, MockGuildRepository(mock_guilds))
        binder.bind(ICharacterRepository, MockCharacterRepository())

    inject.configure(test_config, allow_override=True, clear=True)


@pytest.mark.asyncio
async def test_guild_service_get_by_guild_name_and_realm(setup_injector, mock_guilds):
    mock_response = mock_guilds[0]
    _sut = GuildService()

    assert (
        await _sut.get_by_guild_name_and_realm(
            name=mock_response.name, realm=mock_response.realm
        )
        == mock_response
    )
