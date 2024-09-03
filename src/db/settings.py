from typing import List, Optional, Any
from src.db import SettingOrm, sessionmanager
from src.entities import Settings, SettingsCreate
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


def setting_model_to_entity(instance: SettingOrm) -> Settings:
    return Settings(
        id=instance.id,
        discord_guild_id=instance.discord_guild_id,
        default_realm=instance.default_realm,
        default_region=instance.default_region,
        raider_role_id=instance.raider_role_id,
        admin_role_id=instance.admin_role_id,
    )


class SettingsRepository:

    async def get_by_discord_guild_id(self, discord_guild_id: str) -> Settings:
        async with sessionmanager.session() as session:
            result = (
                await session.execute(
                    select(SettingOrm).where(
                        SettingOrm.discord_guild_id == discord_guild_id
                    )
                )
            ).scalar_one()

            return setting_model_to_entity(result)

    async def add_setting(self, discord_guild_id: str) -> Settings:
        async with sessionmanager.session() as session:
            model = SettingOrm(discord_guild_id=discord_guild_id)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return setting_model_to_entity(model)

    async def update_setting(
        self, discord_guild_id: str, setting_attr: str, attr_value: Any
    ) -> Settings:
        async with sessionmanager.session() as session:
            model = (
                await session.execute(
                    select(SettingOrm).where(
                        SettingOrm.discord_guild_id == discord_guild_id
                    )
                )
            ).scalar_one()

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
