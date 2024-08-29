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


@dataclass
class Settings:
    discord_guild_id: str
    default_region: Optional[str]
    default_realm: Optional[str]
    admin_role_id: Optional[str]
    raider_role_id: Optional[str]
