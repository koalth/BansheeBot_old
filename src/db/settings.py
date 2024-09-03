from typing import List, Optional, Any
from src.db import SettingOrm, sessionmanager
from src.entities import Settings
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


def setting_model_to_entity(instance: SettingOrm) -> Settings:
    return Settings(
        discord_guild_id=instance.discord_guild_id,
        default_realm=instance.default_realm,
        default_region=instance.default_region,
        raider_role_id=instance.raider_role_id,
        admin_role_id=instance.admin_role_id,
    )


class SettingsRepository:

    @staticmethod
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

    @staticmethod
    async def add_setting(discord_guild_id: str) -> Optional[Settings]:
        async with sessionmanager.session() as session:
            model = SettingOrm(discord_guild_id=discord_guild_id)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return setting_model_to_entity(model)

    @staticmethod
    async def update_setting(
        discord_guild_id: str, setting_attr: str, attr_value: Any
    ) -> Optional[Settings]:
        async with sessionmanager.session() as session:
            model = (
                await session.execute(
                    select(SettingOrm).where(
                        SettingOrm.discord_guild_id == discord_guild_id
                    )
                )
            ).scalar_one_or_none()

            if model is None:
                raise NoResultFound

            if hasattr(model, setting_attr):
                setattr(model, setting_attr, attr_value)
            else:
                raise AttributeError

            session.add(model)
            await session.commit()
            await session.refresh(model)
            return setting_model_to_entity(model)
