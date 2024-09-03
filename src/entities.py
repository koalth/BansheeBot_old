from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid


@dataclass
class _CharacterBase:
    name: str
    realm: str
    region: str

    discord_user_id: str
    guild_id: Optional[uuid.UUID]

    on_raid_roster: bool

    item_level: int
    class_name: str
    spec_name: str

    profile_url: str
    thumbnail_url: str
    last_crawled_at: datetime


@dataclass
class CharacterCreate(_CharacterBase):
    pass


@dataclass
class Character(_CharacterBase):
    id: Optional[uuid.UUID]
    guild_id: Optional[uuid.UUID]


@dataclass
class _GuildBase:
    name: str
    realm: str
    region: str

    discord_guild_id: str


@dataclass
class GuildCreate(_GuildBase):
    pass


@dataclass
class Guild(_GuildBase):
    id: uuid.UUID
    characters: List[Character]


@dataclass
class _SettingsBase:
    discord_guild_id: str
    default_region: Optional[str]
    default_realm: Optional[str]
    admin_role_id: Optional[str]
    raider_role_id: Optional[str]


@dataclass
class SettingsCreate(_SettingsBase):
    pass


@dataclass
class Settings(_SettingsBase):
    id: Optional[uuid.UUID]
