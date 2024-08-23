from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Character:
    name: str
    realm: str
    region: str

    item_level: int
    class_name: str
    spec_name: str

    profile_url: str
    thumbnail_url: str
    last_crawled_at: datetime

    id: Optional[int] = None
    discord_user_id: Optional[str] = None
    guild_id: Optional[int] = None


@dataclass
class Guild:
    name: str
    realm: str
    region: str

    id: Optional[int] = None
    discord_guild_id: Optional[str] = None

    characters: List[Character] = field(default_factory=list[Character])
