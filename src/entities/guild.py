from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List


class GuildBase(BaseModel):
    name: str
    realm: str
    region: str
    discord_guild_id: str
    item_level_requirement: Optional[int]


class GuildCreate(GuildBase):
    pass


class GuildUpdate(BaseModel):
    name: Optional[str] = None
    realm: Optional[str] = None
    region: Optional[str] = None
    discord_guild_id: Optional[str] = None
    item_level_requirement: Optional[int] = None


class Guild(GuildBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
