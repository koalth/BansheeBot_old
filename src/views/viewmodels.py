from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GuildViewModel:
    name: str
    region: str
    realm: str
    faction: str


@dataclass
class CharacterViewModel:
    name: str
    region: str
    realm: str
    faction: Optional[str]

    race: Optional[str]
    char_class: Optional[str]
    spec_name: Optional[str]
    role: Optional[str]

    profile_url: Optional[str]
    thumbnail_url: Optional[str]

    item_level: Optional[int]
