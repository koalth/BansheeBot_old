from pydantic import BaseModel, Field
import datetime
from typing import List, Optional, Dict


class GuildResponse(BaseModel):
    name: str
    realm: str
    faction: str
    region: str
    last_crawled_at: datetime.datetime
    profile_url: str


class ItemResponse(BaseModel):
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    gems: List[int]
    enchant: Optional[int]
    tier: Optional[str]


class GearResponse(BaseModel):
    updated_at: datetime.datetime
    item_level_equipped: int
    item_level_total: int
    items: Dict[str, ItemResponse]


class CharacterResponse(BaseModel):
    name: str
    race: str
    class_name: str = Field(alias="class")
    spec_name: str = Field(alias="active_spec_name")
    role: str = Field(alias="active_spec_role")
    faction: str
    region: str
    realm: str
    gear: GearResponse
    guild: GuildResponse

    profile_url: str
    thumbnail_url: str

    last_crawled_at: datetime.datetime
