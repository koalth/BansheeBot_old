import pytest
from src.external.raiderIO import IRaiderIOClient, MockRaiderIOClient, CharacterResponse
from src.services import CharacterService
from src.mapper import character_response_to_entity
import inject


@pytest.fixture
def mockCharacterResponse(dataset) -> CharacterResponse:
    data = dataset["test_data"]
    return CharacterResponse(**data)


@pytest.fixture
def mock_raiderioclient(
    mockCharacterResponse: CharacterResponse,
) -> IRaiderIOClient:
    return MockRaiderIOClient(mockCharacterResponse)


@pytest.fixture
def setup_mock_injector(mock_raiderioclient: IRaiderIOClient):
    def tests_config(binder: inject.Binder):
        binder.bind(IRaiderIOClient, mock_raiderioclient)

    inject.configure(tests_config, allow_override=True, clear=True)


@pytest.mark.asyncio
async def test_get_character_valid(setup_mock_injector, mockCharacterResponse):
    _sut = CharacterService()
    result = await _sut.get_character(
        mockCharacterResponse.name,
        mockCharacterResponse.realm,
        mockCharacterResponse.region,
    )
    assert result is not None
    assert result == character_response_to_entity(mockCharacterResponse)


@pytest.mark.asyncio
async def test_get_character_invalid(setup_mock_injector, mockCharacterResponse):
    _sut = CharacterService()
    result = await _sut.get_character(
        "not a name",
        "not a realm",
        "not a region",
    )
    assert result is None
