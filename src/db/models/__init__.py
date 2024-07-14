from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    Mapped,
    mapped_column,
)
from datetime import datetime

from typing import List


class Base(DeclarativeBase):
    pass


class WowGuild(Base):
    __tablename__ = "wowguild"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    region: Mapped[str]
    realm: Mapped[str]

    discord_guild_id: Mapped[int]

    wow_characters: Mapped[List["WowCharacter"]] = relationship(
        back_populates="wow_guild", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<WowGuild(id={self.id}, name={self.name})>"


class WowCharacter(Base):
    __tablename__ = "wowcharacter"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    region: Mapped[str]
    realm: Mapped[str]

    discord_user_id: Mapped[int]
    thumbnail_url: Mapped[str]
    item_level: Mapped[str]
    last_crawled_at: Mapped[datetime]

    wow_guild_id: Mapped[int] = mapped_column(ForeignKey("wowguild.id"))
    wow_guild: Mapped[WowGuild] = relationship(back_populates="wow_characters")

    def __repr__(self) -> str:
        return f"<WowCharacter(id={self.id}, name={self.name})>"
