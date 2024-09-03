from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


@dataclass
class _BaseEntity:
    id: UUID


@dataclass
class _CreateBaseEntity:
    pass


@dataclass
class _UpdateBaseEntity:
    pass


@dataclass
class _CharacterBase:
    name: str
    realm: str
    region: str

    discord_user_id: str
    guild_id: Optional[UUID]

    on_raid_roster: bool

    item_level: int
    class_name: str
    spec_name: str

    profile_url: str
    thumbnail_url: str
    last_crawled_at: datetime


@dataclass
class CharacterCreate(_CharacterBase, _CreateBaseEntity):
    pass


@dataclass
class Character(_CharacterBase, _BaseEntity):
    pass


@dataclass
class _GuildBase:
    name: str
    realm: str
    region: str

    discord_guild_id: str

    item_level_requirement: Optional[int]


@dataclass
class GuildCreate(_GuildBase, _CreateBaseEntity):
    pass


@dataclass
class Guild(_GuildBase, _BaseEntity):
    characters: List[Character]


@dataclass
class _SettingsBase:
    discord_guild_id: str
    default_region: Optional[str]
    default_realm: Optional[str]
    admin_role_id: Optional[str]
    raider_role_id: Optional[str]


@dataclass
class SettingsCreate(_SettingsBase, _CreateBaseEntity):
    pass


@dataclass
class Settings(_SettingsBase, _BaseEntity):
    pass
