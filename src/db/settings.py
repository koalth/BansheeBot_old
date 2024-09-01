from typing import List, Optional
from src.db import SettingOrm, sessionmanager
from src.entities import Settings
from sqlalchemy import select


def setting_model_to_entity(instance: SettingOrm) -> Settings:
    return Settings(
        discord_guild_id=instance.discord_guild_id,
        default_realm=instance.default_realm,
        default_region=instance.default_region,
        raider_role_id=instance.raider_role_id,
        admin_role_id=instance.admin_role_id,
    )


async def get_by_discord_guild_id(discord_guild_id: str) -> Optional[Settings]:
    async with sessionmanager.session() as session:
        result = (
            await session.execute(
                select(SettingOrm).where(
                    SettingOrm.discord_guild_id == discord_guild_id
                )
            )
        ).scalar_one_or_none()

        if result is None:
            return None
        return setting_model_to_entity(result)


async def add_setting(discord_guild_id: str) -> Optional[Settings]:
    async with sessionmanager.session() as session:
        model = SettingOrm(discord_guild_id=discord_guild_id)
        session.add(model)
        await session.commit()
        await session.refresh(model)
        return setting_model_to_entity(model)
