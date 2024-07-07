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


class DiscordGuildMember(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    discord_user_id: int = Field(index=True)
    discord_user_name: int

    disocrd_guild_links: list[DiscordGuildMemberLink] = Relationship(
        back_populates="discord_member"
    )
