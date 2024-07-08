from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class DiscordGuild(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    discord_guild_id: int = Field(index=True)
    discord_guild_name: str

    wow_guild: Optional["WowGuild"] = Relationship(back_populates="discord_guild")


# World of Warcraft tables
class WowGuild(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wow_guild_name: str = Field(index=True)
    region: str
    realm: str

    discord_guild_id: int | None = Field(default=None, foreign_key="discordguild.id")
    discord_guild: DiscordGuild | None = Relationship(back_populates="wow_guild")


class WowCharacter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wow_character_name: str = Field(index=True)
    wow_character_id: int
    region: str
    realm: str
    discord_user_id: int
