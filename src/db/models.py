from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime

from typing import List


class Base(AsyncAttrs, DeclarativeBase):
    pass


class GuildOrm(Base):
    __tablename__ = "guilds"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(index=True)
    region: Mapped[str]
    realm: Mapped[str]

    discord_guild_id: Mapped[int]

    characters: Mapped[List["CharacterOrm"]] = relationship(
        back_populates="guild", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<GuildOrm(id={self.id}, name={self.name})>"


class CharacterOrm(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(index=True)
    region: Mapped[str]
    realm: Mapped[str]

    discord_user_id: Mapped[int]

    item_level: Mapped[int]
    class_name: Mapped[str]
    profile_url: Mapped[str]
    thumbnail_url: Mapped[str]

    last_crawled_at: Mapped[datetime]

    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id"))
    guild: Mapped[GuildOrm] = relationship(back_populates="characters")

    def __repr__(self) -> str:
        return f"<CharacterOrm(id={self.id}, name={self.name})>"
