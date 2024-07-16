from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import StrEnum
from datetime import datetime

from src.db.models import GuildOrm, CharacterOrm
from src.raiderIO.models import CharacterResponse, GuildResponse


class Faction(StrEnum):
    alliance = "alliance"
    horde = "horde"


class Role(StrEnum):
    HEAL = "heal"
    DPS = "dps"
    TANK = "tank"


class Region(StrEnum):
    US = "us"
    EU = "eu"
    TW = "tw"
    KR = "kr"
    CN = "cn"


@dataclass
class GuildDTO:
    name: str
    realm: str
    region: Region

    discord_guild_id: Optional[int] = None

    characters: List["CharacterDTO"] = field(default_factory=lambda: [])


@dataclass
class CharacterDTO:
    name: str
    realm: str
    region: Region

    item_level: int
    class_name: str
    profile_url: str
    thumbnail_url: str

    last_crawled_at: datetime

    discord_user_id: Optional[int] = None
    guild_id: Optional[int] = None


def createCharacterDTOFromOrm(character_orm: CharacterOrm) -> CharacterDTO:
    return CharacterDTO(
        name=character_orm.name,
        realm=character_orm.realm,
        region=Region(character_orm.region),
        discord_user_id=character_orm.discord_user_id,
        item_level=character_orm.item_level,
        class_name=character_orm.class_name,
        profile_url=character_orm.profile_url,
        thumbnail_url=character_orm.thumbnail_url,
        last_crawled_at=character_orm.last_crawled_at,
        guild_id=character_orm.guild_id,
    )


def createGuildDTOFromOrm(guild_orm: GuildOrm) -> GuildDTO:
    return GuildDTO(
        name=guild_orm.name,
        realm=guild_orm.realm,
        region=Region(guild_orm.region),
        discord_guild_id=guild_orm.discord_guild_id,
        characters=[
            createCharacterDTOFromOrm(character) for character in guild_orm.characters
        ],
    )


def createCharacterDTOFromResponse(
    character_response: CharacterResponse,
) -> CharacterDTO:

    dto = CharacterDTO(
        name=character_response.name,
        realm=character_response.realm,
        region=Region(character_response.region),
        item_level=(
            character_response.gear.item_level_equipped
            if character_response.gear is not None
            else 0
        ),
        class_name=character_response.active_spec_name,
        profile_url=character_response.profile_url,
        thumbnail_url=character_response.thumbnail_url,
        last_crawled_at=character_response.last_crawled_at,
    )

    return dto


def createGuildDTOFromResponse(guild_response: GuildResponse) -> GuildDTO:

    dto = GuildDTO(
        name=guild_response.name,
        realm=guild_response.realm,
        region=Region(guild_response.region),
    )

    return dto
