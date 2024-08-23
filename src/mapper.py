from src.db.models import CharacterOrm, GuildOrm
from src.entities import Character, Guild
from src.raiderIO import CharacterResponse, GuildResponse
import pytz
from datetime import datetime, timezone


def convert_datetime(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc)


def character_model_to_entity(instance: CharacterOrm) -> Character:
    return Character(
        id=instance.id,
        name=instance.name,
        region=instance.region,
        realm=instance.realm,
        discord_user_id=instance.discord_user_id,
        item_level=instance.item_level,
        class_name=instance.class_name,
        spec_name=instance.spec_name,
        profile_url=instance.profile_url,
        thumbnail_url=instance.thumbnail_url,
        last_crawled_at=convert_datetime(instance.last_crawled_at),
        guild_id=instance.guild_id,
    )


def character_entity_to_model(instance: Character) -> CharacterOrm:
    return CharacterOrm(
        name=instance.name,
        region=instance.region,
        realm=instance.realm,
        discord_user_id=instance.discord_user_id,
        item_level=instance.item_level,
        class_name=instance.class_name,
        spec_name=instance.spec_name,
        profile_url=instance.profile_url,
        thumbnail_url=instance.thumbnail_url,
        last_crawled_at=convert_datetime(instance.last_crawled_at),
        guild_id=instance.guild_id,
    )


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


def guild_model_to_entity(instance: GuildOrm) -> Guild:
    return Guild(
        id=instance.id,
        name=instance.name,
        region=instance.region,
        realm=instance.realm,
        discord_guild_id=instance.discord_guild_id,
        characters=[
            character_model_to_entity(character) for character in instance.characters
        ],
    )


def guild_entity_to_model(instance: Guild) -> GuildOrm:
    return GuildOrm(
        name=instance.name,
        region=instance.region,
        realm=instance.realm,
        discord_guild_id=instance.discord_guild_id,
    )


def guild_response_to_entity(instance: GuildResponse) -> Guild:
    return Guild(name=instance.name, realm=instance.realm, region=instance.region)
