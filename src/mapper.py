from src.entities import Character, Settings
from src.raiderIO import CharacterResponse, GuildResponse
from src.db import SettingOrm
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


def setting_model_to_entity(instance: SettingOrm) -> Settings:
    return Settings(
        discord_guild_id=instance.discord_guild_id,
        default_realm=instance.default_realm,
        default_region=instance.default_region,
        raider_role_id=instance.raider_role_id,
        admin_role_id=instance.admin_role_id,
    )
