from src.entities import Character
from src.raiderIO import CharacterResponse, GuildResponse
import pytz
from datetime import datetime, timezone


def convert_datetime(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc)


def character_response_to_entity(instance: CharacterResponse) -> Character:
    return Character(
        name=instance.name,
        realm=instance.realm,
        region=instance.region,
        item_level=instance.gear.item_level_equipped,
        class_name=instance.character_class,
        spec_name=instance.active_spec_name,
        profile_url=instance.profile_url,
        thumbnail_url=instance.thumbnail_url,
        last_crawled_at=convert_datetime(instance.last_crawled_at),
    )
