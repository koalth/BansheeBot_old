from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List
from datetime import datetime


class SettingBase(BaseModel):
    discord_guild_id: str
    default_region: Optional[str]
    default_realm: Optional[str]
    admin_role_id: Optional[str]
    raider_role_id: Optional[str]


class SettingCreate(SettingBase):
    pass


class SettingUpdate(BaseModel):
    discord_guild_id: Optional[str] = None
    default_region: Optional[str] = None
    default_realm: Optional[str] = None
    admin_role_id: Optional[str] = None
    raider_role_id: Optional[str] = None


class Setting(SettingBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
