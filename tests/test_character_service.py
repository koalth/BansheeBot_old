import pytest
from src.external.raiderIO import (
    IRaiderIOClient,
    MockRaiderIOClient,
    CharacterResponse,
    GuildResponse,
)
from typing import List
import uuid
from src.db import CharacterOrm, CharacterMockRepository, ICharacterRepository
from src.entities import Character, CharacterCreate, CharacterUpdate
from src.services import CharacterService, ICharacterService
import inject
from unittest.mock import AsyncMock


from faker import Faker

fake = Faker()
from faker.providers import BaseProvider


class CharacterProvider(BaseProvider):
    def character(self) -> Character:
        return Character(
            id=fake.u,
            name=fake.name(),
            realm=fake.color(),
            region=fake.region_code(),
            guild_id=fake.uid(),
            discord_user_id=fake.uid(),
            item_level=int(fake.rd_number()),
            class_name=fake.color(),
            spec_name=fake.color(),
            profile_url=fake.url(),
            thumbnail_url=fake.url(),
            on_raid_roster=fake.boolean(50),
            last_crawled_at=fake.date_time(),
        )


class TestCharacterService_Client:

    @pytest.fixture
    def mockCharacterResponse_valid(self, dataset) -> CharacterResponse:
        data = dataset["raider_io_character"]
        return CharacterResponse(**data)

    @pytest.fixture
    def mockGuildResponse_valid(self, dataset) -> GuildResponse:
        data = dataset["raider_io_guild"]
        return GuildResponse(**data)

    @pytest.fixture
    def mock_raiderioclient_returns_none(self) -> IRaiderIOClient:
        return MockRaiderIOClient()

    @pytest.fixture
    def mock_raiderioclient_returns_valid(
        self,
        mockCharacterResponse_valid: CharacterResponse,
        mockGuildResponse_valid: GuildResponse,
    ) -> IRaiderIOClient:
        return MockRaiderIOClient(mockCharacterResponse_valid, mockGuildResponse_valid)

    @pytest.fixture
    def setup_mock_injector_client_returns_valid(
        self,
        mock_raiderioclient_returns_valid: IRaiderIOClient,
    ):
        def tests_config(binder: inject.Binder):
            binder.bind(IRaiderIOClient, mock_raiderioclient_returns_valid)

        inject.configure(tests_config, allow_override=True, clear=True)

    @pytest.fixture
    def setup_mock_injector_client_returns_none(
        self,
        mock_raiderioclient_returns_none: IRaiderIOClient,
    ):
        def tests_config(binder: inject.Binder):
            binder.bind(IRaiderIOClient, mock_raiderioclient_returns_none)

        inject.configure(tests_config, allow_override=True, clear=True)

    @pytest.mark.asyncio
    async def test_get_character_valid(
        self, setup_mock_injector_client_returns_valid, mockCharacterResponse_valid
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
    async def test_get_character_none(self, setup_mock_injector_client_returns_none):
        _sut = CharacterService()
        result = await _sut.get_character_from_raider_io(
            "not a name",
            "not a realm",
            "not a region",
        )
        assert result is None


class TestCharacterService_Repository:

    @pytest.fixture
    def mock_character_entities(self) -> List[Character]:

        return [
            Character(
                id=fake.uid(),
                name="character",
                realm="dalaran",
            )
        ]

    @pytest.fixture
    def mock_character_repository(self) -> ICharacterRepository:
        return CharacterMockRepository()

    @pytest.fixture
    def setup_mock_injector(self, mock_character_repository: ICharacterRepository):
        def tests_config(binder: inject.Binder):
            binder.bind(ICharacterRepository, mock_character_repository)

        inject.configure(tests_config, allow_override=True, clear=True)

    @pytest.mark.asyncio
    async def test_get_characters_with_raid_role(setup_mock_injector):

        _sut = CharacterService()
