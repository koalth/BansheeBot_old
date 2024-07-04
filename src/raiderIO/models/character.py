import datetime
from typing import List, Optional, Dict


class Guild:
    name: str
    realm: str

    def __init__(self, name: str, realm: str):
        self.name = name
        self.realm = realm


class Item:
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    gems: List[int]
    enchant: Optional[int]
    tier: Optional[str]

    def __init__(
        self,
        item_id: int,
        item_level: int,
        icon: str,
        name: str,
        item_quality: int,
        is_legendary: bool,
        gems: List[int],
        enchant: Optional[int] = [],
        tier: Optional[str] = [],
    ):
        self.item_id = item_id
        self.item_level = item_level
        self.icon = icon
        self.name = name
        self.item_quality = item_quality
        self.is_legendary = is_legendary
        self.gems = gems
        self.enchant = enchant
        self.tier = tier


class Gear:
    updated_at: datetime
    item_level_equipped: int
    item_level_total: int
    items: Dict[str, Item]

    def __init__(
        self,
        updated_at: datetime,
        item_level_equipped: int,
        item_level_total: int,
        items: Dict[str, Item],
    ):
        self.updated_at = updated_at
        self.item_level_equipped = item_level_equipped
        self.item_level_total = item_level_total
        self.items = items


class Character:
    name: str
    race: str
    class_name: str
    spec_name: str
    role: str
    faction: str
    region: str
    realm: str
    gear: Gear
    guild: Guild

    profile_url: str
    thumbnail_url: str

    def __init__(
        self,
        name: str,
        race: str,
        class_name: str,
        spec_name: str,
        role: str,
        faction: str,
        region: str,
        realm: str,
        gear: Gear,
        guild: Guild,
        profile_url: str,
        thumbnail_url: str,
    ):
        self.name = name
        self.race = race
        self.class_name = class_name
        self.spec_name = spec_name
        self.role = role
        self.faction = faction
        self.region = region
        self.realm = realm
        self.gear = gear
        self.guild = guild
        self.profile_url = profile_url
        self.thumbnail_url = thumbnail_url

    def __repr__(self) -> str:
        return f"<Character(name={self.name}, realm={self.realm})>"
