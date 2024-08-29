import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from typing import List, Optional


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid5)


class SettingOrm(Base):
    __tablename__ = "settings"

    discord_guild_id: Mapped[str] = mapped_column(index=True)

    default_region: Mapped[Optional[str]] = mapped_column(nullable=True)
    default_realm: Mapped[Optional[str]] = mapped_column(nullable=True)

    admin_role_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    raider_role_id: Mapped[Optional[str]] = mapped_column(nullable=True)
