from sqlmodel import Field, SQLModel, Relationship


class DiscordGuildMemberLink(SQLModel, table=True):
    discord_guild_id: int | None = Field(
        default=None, foreign_key="discordguild.id", primary_key=True
    )
    discord_member_id: int | None = Field(
        default=None, foreign_key="discordguildmember.id", primary_key=True
    )

    is_admin: bool = False

    discord_guild: "DiscordGuild" = Relationship(back_populates="discord_member_links")
    discord_member: "DiscordGuildMember" = Relationship(
        back_populates="discord_guild_links"
    )


class DiscordGuild(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    discord_guild_id: int = Field(index=True)
    discord_guild_name: str

    discord_member_links: list[DiscordGuildMemberLink] = Relationship(
        back_populates="discord_guild"
    )

    wow_guild_id: int | None = Field(default=None, foreign_key="wowguild.id")
    wow_guild: "WowGuild" = Relationship(back_populates="discord_guild")


class DiscordGuildMember(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    discord_user_id: int = Field(index=True)
    discord_user_name: int

    discord_guild_links: list[DiscordGuildMemberLink] = Relationship(
        back_populates="discord_member"
    )

    wow_character_id: int | None = Field(default=None, foreign_key="wowcharacter.id")
    wow_character: "WowCharacter" = Relationship(back_populates="discord_guild_member")


# World of Warcraft tables
class WowGuild(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wow_guild_name: str = Field(index=True)
    wow_guild_id: int
    region: str
    realm: str

    wow_characters: list["WowCharacter"] = Relationship(back_populates="wow_guild")

    discord_guild_id: int | None = Field(default=None, foreign_key="discordguild.id")
    discord_guild: DiscordGuild | None = Relationship(back_populates="wow_guild")


class WowCharacter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wow_character_name: str = Field(index=True)
    wow_character_id: int
    region: str
    realm: str

    wow_guild_id: int | None = Field(default=None, foreign_key="wowguild.id")
    wow_guild: WowGuild | None = Relationship(back_populates="wow_characters")

    discord_guild_member_id: int | None = Field(
        default=None, foreign_key="discordguildmember.id"
    )
    discord_guild_member: DiscordGuildMember | None = Relationship(
        back_populates="wow_character"
    )


# Discord World of Warcraft Link
