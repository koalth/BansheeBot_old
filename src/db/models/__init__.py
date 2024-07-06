from sqlmodel import Field, SQLModel, Relationship


# Discord related tables
class DiscordUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    discord_id: int = Field(unique=True, index=True)
    discord_username: str

    discord_guild_members: list["DiscordGuildMember"] = Relationship(
        back_populates="discord_user"
    )

    wow_characters: list["WowCharacter"] = Relationship(back_populates="discord_user")


class DiscordGuild(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    discord_guild_id: int = Field(unique=True, index=True)
    discord_guild_name: str
    discord_guild_owner_id: int = Field(foreign_key="discorduser.id")

    discord_guild_members: list["DiscordGuildMember"] = Relationship(
        back_populates="discord_guild"
    )


class DiscordGuildMemberRoleLink(SQLModel, table=True):
    discord_guild_member_id: int | None = Field(
        default=None, foreign_key="discordguildmember.id", primary_key=True
    )
    discord_guild_member_role_id: int | None = Field(
        default=None, foreign_key="discordguildmemberrole.id", primary_key=True
    )


class DiscordGuildMember(SQLModel, table=True):
    id: int = Field(primary_key=True)
    is_admin: bool = Field(default=False)

    discord_guild_id: int = Field(foreign_key="discordguild.id")
    discord_guild: DiscordGuild | None = Relationship(
        back_populates="discord_guild_members"
    )

    discord_user_id: int = Field(foreign_key="discorduser.id")
    discord_user: DiscordUser | None = Relationship(
        back_populates="discord_guild_members"
    )

    discord_guild_member_roles: list["DiscordGuildMemberRole"] = Relationship(
        back_populates="discord_guild_members", link_model=DiscordGuildMemberRoleLink
    )


class DiscordGuildMemberRole(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    discord_guild_members: list["DiscordGuildMember"] = Relationship(
        back_populates="discord_guild_member_roles",
        link_model=DiscordGuildMemberRoleLink,
    )


# World of Warcraft related tables
class WowGuildMember(SQLModel, table=True):
    wow_character_id: int | None = Field(
        default=None, foreign_key="wowcharacter.id", primary_key=True
    )
    wow_guild_id: int | None = Field(
        default=None, foreign_key="wowcharacter.id", primary_key=True
    )

    wow_character: "WowCharacter" = Relationship(back_populates="wow_guild_member_link")
    wow_guild: "WowGuild" = Relationship(back_populates="wow_guild_members_link")


class WowGuild(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    faction: str
    region: str
    realm: str
    raiderio_url: str

    wow_guild_members_link: list["WowGuildMember"] = Relationship(
        back_populates="wow_guild_link"
    )


class WowCharacter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    character_class: str
    region: str
    realm: str
    raiderio_url: str

    discord_user_id: int = Field(foreign_key="discorduser.id")
    discord_user: DiscordUser | None = Relationship(back_populates="wow_characters")

    wow_guild_member_id: int = Field(foreign_key="wowguildmember.id")
    wow_guild_member_link: WowGuildMember | None = Relationship(
        back_populates="wow_character"
    )


# class WowGuildMember(SQLModel, table=True):
#     wow_character_id: int | None = Field(
#         default=None, foreign_key="wowcharacter.id", primary_key=True
#     )
#     wow_guild_id: int | None = Field(
#         default=None, foreign_key="wowcharacter.id", primary_key=True
#     )

#     wow_character: "WowCharacter" = Relationship(back_populates="wow_guild_member_link")
#     wow_guild: "WowGuild" = Relationship(back_populates="wow_guild_members_link")
