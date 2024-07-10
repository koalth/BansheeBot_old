from pydantic import BaseModel, Field

from typing import List, Optional


class WowCharacterDTO(BaseModel):
    id: int
    name: str
    region: str
    realm: str
    discord_user_id: int
    class_name: str
    thumbnail_url: str


class WowGuildDTO(BaseModel):
    id: int
    name: str
    region: str
    realm: str

    discord_guild_id: int
