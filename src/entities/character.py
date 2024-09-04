from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List
from datetime import datetime


class CharacterBase(BaseModel):
    name: str
    realm: str
    region: str

    discord_user_id: str

    on_raid_roster: bool

    item_level: int
    class_name: str
    spec_name: str

    profile_url: str
    thumbnail_url: str
    last_crawled_at: datetime


class CharacterCreate(CharacterBase):
    pass


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    realm: Optional[str] = None
    region: Optional[str] = None

    discord_user_id: Optional[str] = None

    on_raid_roster: Optional[bool] = None

    item_level: Optional[int] = None
    class_name: Optional[str] = None
    spec_name: Optional[str] = None

    profile_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    last_crawled_at: Optional[datetime] = None


class Character(CharacterBase):
    id: UUID
    guild_id: UUID
    model_config = ConfigDict(from_attributes=True)
