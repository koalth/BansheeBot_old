from pydantic import BaseModel
from enum import StrEnum


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


class GuildDTO(BaseModel):
    name: str
    faction: Faction
    region: Region
    realm: str
    profile_url: str


class CharacterDTO(BaseModel):
    name: str
    race: str
    class_name: str
    spec_name: str
    role: Role
    faction: Faction
    region: Region
    realm: str

    profile_url: str
    thumbnail_url: str

    item_level: int
