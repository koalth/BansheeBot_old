from datetime import datetime
from .models import *

# Create mock data for ItemResponse
mock_item_response = ItemResponse(
    item_id=12345,
    item_level=300,
    enchant=5678,
    icon="icon_url",
    name="Sword of Mockery",
    item_quality=4,
    is_legendary=False,
    is_azerite_armor=False,
    gems=[123, 456],
    tier="Epic",
    bonuses=[1, 2, 3],
)

# Create mock data for ItemsResponse
mock_items_response = ItemsResponse(
    head=mock_item_response,
    neck=None,
    shoulder=mock_item_response,
    back=mock_item_response,
    chest=mock_item_response,
    waist=None,
    wrist=mock_item_response,
    hands=mock_item_response,
    legs=mock_item_response,
    feet=None,
    finger1=mock_item_response,
    finger2=mock_item_response,
    trinket1=mock_item_response,
    trinket2=mock_item_response,
    mainhand=mock_item_response,
    # offhand=mock_item_response  # Uncomment if needed
)

# Create mock data for GearResponse
mock_gear_response = GearResponse(
    updated_at="2024-08-25T12:00:00Z",
    item_level_equipped=320,
    item_level_total=330,
    items=mock_items_response,
)

# Create mock data for GuildResponse (if needed)
mock_guild_response = GuildResponse(
    name="Mock Guild",
    realm="Mock Realm",
    region="US",
    faction="Alliance",
    last_crawled_at=datetime.now(),
    profile_url="https://example.com/profile",
)

# Create mock data for CharacterResponse
mock_character_response = CharacterResponse(
    name="MockCharacter",
    race="Human",
    character_class="Warrior",
    active_spec_name="Fury",
    active_spec_role="DPS",
    gender="Male",
    faction="Alliance",
    achievement_points=12345,
    honorable_kills=6789,
    thumbnail_url="https://example.com/thumbnail.jpg",
    region="US",
    realm="Stormrage",
    last_crawled_at=datetime.now(),
    profile_url="https://example.com/character-profile",
    profile_banner="https://example.com/banner.jpg",
    gear=mock_gear_response,
)
