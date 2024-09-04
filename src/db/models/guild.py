import uuid
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from typing import List, Optional
from ..base import Base


class GuildOrm(Base):
    __tablename__ = "guilds"

    discord_guild_id: Mapped[str] = mapped_column(index=True)

    name: Mapped[str] = mapped_column(index=True)
    region: Mapped[str]
    realm: Mapped[str]

    item_level_requirement: Mapped[Optional[int]] = mapped_column(nullable=True)

    characters: Mapped[List["CharacterOrm"]] = relationship(  # type: ignore
        back_populates="guild", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<GuildOrm(id={self.id}, name={self.name})>"
