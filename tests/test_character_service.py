import pytest
from typing import Optional
from src.raiderIO import RaiderIOClient, CharacterResponse
from src.services import CharacterService
from src.mapper import character_response_to_entity
import inject
import json


class MockRaiderIOClient(RaiderIOClient):

    response: CharacterResponse

    def __init__(self, response: CharacterResponse):
        self.response = response
        super().__init__("")

    async def getCharacterProfile(
        self, name: str, realm="Dalaran", region="us"
    ) -> Optional[CharacterResponse]:
        return self.response


@pytest.fixture
def mockCharacterResponse(dataset) -> CharacterResponse:
    data = dataset["test_data"]
    return CharacterResponse(**data)


@pytest.fixture
def mock_raiderioclient(
    mockCharacterResponse: CharacterResponse,
) -> RaiderIOClient:
    return MockRaiderIOClient(mockCharacterResponse)


@pytest.fixture
def setup_mock_injector(mock_raiderioclient: RaiderIOClient):
    def tests_config(binder: inject.Binder):
        binder.bind(RaiderIOClient, mock_raiderioclient)

    inject.configure(tests_config, allow_override=True, clear=True)


@pytest.mark.asyncio
async def test_get_character(setup_mock_injector, mockCharacterResponse):
    _sut = CharacterService()
    result = await _sut.get_character(
        mockCharacterResponse.name,
        mockCharacterResponse.realm,
        mockCharacterResponse.region,
    )
    assert result is not None
    assert result == character_response_to_entity(mockCharacterResponse)
