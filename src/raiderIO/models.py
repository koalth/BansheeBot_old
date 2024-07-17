# generated by datamodel-codegen:
#   filename:  char.json
#   timestamp: 2024-07-14T20:31:21+00:00

from __future__ import annotations

from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CorruptionResponse(BaseModel):
    added: int
    resisted: int
    total: int
    cloakRank: int
    spells: List


class SpellResponse(BaseModel):
    id: int
    school: int
    icon: str
    name: str
    rank: None


class AzeritePowersResponse(BaseModel):
    id: int
    spell: SpellResponse
    tier: int


class Corruption1Response(BaseModel):
    added: int
    resisted: int
    total: int


class HeadResponse(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List[Optional[AzeritePowersResponse]]
    corruption: Corruption1Response
    domination_shards: List
    tier: str
    gems: List[int]
    bonuses: List[int]


class NeckResponse(BaseModel):
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List[int]
    bonuses: List[int]


class AzeritePowers1Response(BaseModel):
    id: int
    spell: SpellResponse
    tier: int


class ShoulderResponse(BaseModel):
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List[Optional[AzeritePowers1Response]]
    corruption: Corruption1Response
    domination_shards: List
    tier: str
    gems: List
    bonuses: List[int]


class BackResponse(BaseModel):
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List
    bonuses: List[int]


class AzeritePowers2Response(BaseModel):
    id: int
    spell: SpellResponse
    tier: int


class ChestResponse(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List[Optional[AzeritePowers2Response]]
    corruption: Corruption1Response
    domination_shards: List
    tier: str
    gems: List
    bonuses: List[int]


class WaistResponse(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List[int]
    bonuses: List[int]


class WristResponse(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List[int]
    bonuses: List[int]


class HandsResponse(BaseModel):
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    tier: str
    gems: List
    bonuses: List[int]


class LegsResponse(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    tier: str
    gems: List
    bonuses: List[int]


class FeetResponse(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List
    bonuses: List[int]


class Finger1Response(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List
    bonuses: List[int]


class Finger2Response(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List[int]
    bonuses: List[int]


class Trinket1Response(BaseModel):
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List
    bonuses: List[int]


class Trinket2Response(BaseModel):
    item_id: int
    item_level: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List
    bonuses: List[int]


class MainhandResponse(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List
    bonuses: List[int]


class OffhandResponse(BaseModel):
    item_id: int
    item_level: int
    enchant: int
    icon: str
    name: str
    item_quality: int
    is_legendary: bool
    is_azerite_armor: bool
    azerite_powers: List
    corruption: Corruption1Response
    domination_shards: List
    gems: List
    bonuses: List[int]


class ItemsResponse(BaseModel):
    head: Optional[HeadResponse]
    neck: Optional[NeckResponse]
    shoulder: Optional[ShoulderResponse]
    back: Optional[BackResponse]
    chest: Optional[ChestResponse]
    waist: Optional[WaistResponse]
    wrist: Optional[WristResponse]
    hands: Optional[HandsResponse]
    legs: Optional[LegsResponse]
    feet: Optional[FeetResponse]
    finger1: Optional[Finger1Response]
    finger2: Optional[Finger2Response]
    trinket1: Optional[Trinket1Response]
    trinket2: Optional[Trinket2Response]
    mainhand: Optional[MainhandResponse]
    offhand: Optional[OffhandResponse]


class GearResponse(BaseModel):
    updated_at: str
    item_level_equipped: int
    item_level_total: int
    artifact_traits: int
    corruption: CorruptionResponse
    items: ItemsResponse


class GuildResponse(BaseModel):
    name: str
    realm: str
    region: Optional[str] = None
    faction: Optional[str] = None
    last_crawled_at: Optional[datetime] = None
    profile_url: Optional[str] = None


class CharacterResponse(BaseModel):
    name: str
    race: str
    character_class: str = Field(alias="class")
    active_spec_name: str
    active_spec_role: str
    gender: str
    faction: str
    achievement_points: int
    honorable_kills: int
    thumbnail_url: str
    region: str
    realm: str
    last_crawled_at: datetime
    profile_url: str
    profile_banner: str
    gear: Optional[GearResponse] = None
    guild: Optional[GuildResponse] = None