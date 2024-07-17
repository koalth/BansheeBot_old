from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import StrEnum
from datetime import datetime


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
