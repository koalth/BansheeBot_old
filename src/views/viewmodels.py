from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GuildViewModel:
    name: str
    region: str
    realm: str


@dataclass
class CharacterViewModel:
    name: str
    region: str
    realm: str
    faction: Optional[str] = None

    race: Optional[str] = None
    char_class: Optional[str] = None
    spec_name: Optional[str] = None
    role: Optional[str] = None

    profile_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    item_level: Optional[int] = None
