from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator
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


class ItemDTO(BaseModel):
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    gems: List[int] = []
    enchant: Optional[int] = None
    tier: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class GearDTO(BaseModel):
    updated_at: datetime
    item_level_equipped: int
    item_level_total: int
    items: Dict[str, ItemDTO]

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class GuildDTO(BaseModel):
    name: str
    realm: str
    faction: Optional[Faction] = None
    region: Optional[Region] = None
    profile_url: Optional[str] = None
    last_crawled_at: Optional[datetime] = None

    characters: List["CharacterDTO"] = []

    @field_validator("characters", mode="before")
    @classmethod
    def map_characters(cls, characters: list) -> list["CharacterDTO"]:
        return [CharacterDTO.model_validate(char) for char in characters]

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class CharacterDTO(BaseModel):
    name: str
    race: str
    class_name: str = Field(alias="class")
    spec_name: str = Field(alias="active_spec_name")
    role: str = Field(alias="active_spec_role")
    faction: str
    region: str
    realm: str
    gear: Optional[GearDTO]
    guild: Optional[GuildDTO]

    profile_url: str
    thumbnail_url: str

    @computed_field
    @property
    def item_level(self) -> Optional[int]:
        if self.gear is None:
            return None
        else:
            return self.gear.item_level_equipped

    last_crawled_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")
