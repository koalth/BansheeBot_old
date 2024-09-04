import pytest
from src.external.raiderIO import (
    IRaiderIOClient,
    MockRaiderIOClient,
    CharacterResponse,
    GuildResponse,
)
from src.services import CharacterService, ICharacterService
import inject


@pytest.fixture
def mockCharacterResponse_valid(dataset) -> CharacterResponse:
    data = dataset["raider_io_character"]
    return CharacterResponse(**data)


@pytest.fixture
def mockGuildResponse_valid(dataset) -> GuildResponse:
    data = dataset["raider_io_guild"]
    return GuildResponse(**data)


@pytest.fixture
def mock_raiderioclient_returns_none() -> IRaiderIOClient:
    return MockRaiderIOClient()


@pytest.fixture
def mock_raiderioclient_returns_valid(
    mockCharacterResponse_valid: CharacterResponse,
    mockGuildResponse_valid: GuildResponse,
) -> IRaiderIOClient:
    return MockRaiderIOClient(mockCharacterResponse_valid, mockGuildResponse_valid)


@pytest.fixture
def setup_mock_injector_client_returns_valid(
    mock_raiderioclient_returns_valid: IRaiderIOClient,
):
    def tests_config(binder: inject.Binder):
        binder.bind(IRaiderIOClient, mock_raiderioclient_returns_valid)

    inject.configure(tests_config, allow_override=True, clear=True)


@pytest.fixture
def setup_mock_injector_client_returns_none(
    mock_raiderioclient_returns_none: IRaiderIOClient,
):
    def tests_config(binder: inject.Binder):
        binder.bind(IRaiderIOClient, mock_raiderioclient_returns_none)

    inject.configure(tests_config, allow_override=True, clear=True)


@pytest.mark.asyncio
async def test_get_character_valid(
    setup_mock_injector_client_returns_valid, mockCharacterResponse_valid
):
    _sut = CharacterService()
    result = await _sut.get_character_from_raider_io(
        mockCharacterResponse_valid.name,
        mockCharacterResponse_valid.realm,
        mockCharacterResponse_valid.region,
    )
    assert result is not None
    assert result == mockCharacterResponse_valid


@pytest.mark.asyncio
async def test_get_character_none(setup_mock_injector_client_returns_none):
    _sut = CharacterService()
    result = await _sut.get_character_from_raider_io(
        "not a name",
        "not a realm",
        "not a region",
    )
    assert result is None
