from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from enum import StrEnum
import datetime


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


class ItemDTO(BaseModel):

    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    gems: List[int]
    enchant: Optional[int]
    tier: Optional[str]

    model_config = ConfigDict(extra="ignore")


class GearDTO(BaseModel):
    updated_at: datetime.datetime
    item_level_equipped: int
    item_level_total: int
    items: Dict[str, ItemDTO]

    model_config = ConfigDict(extra="ignore")


class GuildDTO(BaseModel):
    name: str
    faction: Faction
    region: Region
    realm: str
    profile_url: str
    last_crawled_at: datetime.datetime

    model_config = ConfigDict(extra="ignore")


class CharacterDTO(BaseModel):
    name: str
    race: str
    class_name: str = Field(alias="class")
    spec_name: str = Field(alias="active_spec_name")
    role: str = Field(alias="active_spec_role")
    faction: str
    region: str
    realm: str
    gear: GearDTO
    guild: GuildDTO

    profile_url: str
    thumbnail_url: str

    last_crawled_at: datetime.datetime

    model_config = ConfigDict(extra="ignore")
