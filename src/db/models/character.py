from uuid import UUID
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from typing import List, Optional
from ..base import Base


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

    on_raid_roster: Mapped[bool] = mapped_column(default=False)

    last_crawled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    guild_id: Mapped[UUID] = mapped_column(ForeignKey("guilds.id"))
    guild: Mapped["GuildOrm"] = relationship(back_populates="characters")  # type: ignore

    def __repr__(self) -> str:
        return f"<CharacterOrm(id={self.id}, name={self.name})>"
