from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
import datetime


class WowGuild(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    region: str
    realm: str
    discord_guild_id: int

    wow_characters: list["WowCharacter"] = Relationship(
        back_populates="wow_guild", sa_relationship_kwargs={"lazy": "joined"}
    )


class WowCharacter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    region: str
    realm: str
    discord_user_id: int
    thumbnail_url: str
    item_level: int
    last_updated_at: datetime.datetime

    wow_guild_id: int | None = Field(default=None, foreign_key="wowguild.id")
    wow_guild: WowGuild | None = Relationship(
        back_populates="wow_characters", sa_relationship_kwargs={"lazy": "joined"}
    )
