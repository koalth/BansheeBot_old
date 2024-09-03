import uuid
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from typing import List, Optional


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class SettingOrm(Base):
    __tablename__ = "settings"

    discord_guild_id: Mapped[str] = mapped_column(index=True)

    default_region: Mapped[Optional[str]] = mapped_column(nullable=True)
    default_realm: Mapped[Optional[str]] = mapped_column(nullable=True)

    admin_role_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    raider_role_id: Mapped[Optional[str]] = mapped_column(nullable=True)


class GuildOrm(Base):
    __tablename__ = "guilds"

    discord_guild_id: Mapped[str] = mapped_column(index=True)

    name: Mapped[str] = mapped_column(index=True)
    region: Mapped[str]
    realm: Mapped[str]

    characters: Mapped[List["CharacterOrm"]] = relationship(
        back_populates="guild", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<GuildOrm(id={self.id}, name={self.name})>"


class CharacterOrm(Base):
    __tablename__ = "characters"

    name: Mapped[str] = mapped_column(index=True)
    region: Mapped[str]
    realm: Mapped[str]

    discord_user_id: Mapped[str] = mapped_column(index=True)

    item_level: Mapped[int]
    class_name: Mapped[str]
    spec_name: Mapped[str]
    profile_url: Mapped[str]
    thumbnail_url: Mapped[str]

    last_crawled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    guild_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("guilds.id"))
    guild: Mapped[GuildOrm] = relationship(back_populates="characters")

    def __repr__(self) -> str:
        return f"<CharacterOrm(id={self.id}, name={self.name})>"
