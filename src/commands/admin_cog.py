import logging
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from src import BansheeBot
from src.views import AdminRoleSelectView
from src.services import GuildService


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class Admin(commands.Cog):

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    admin = SlashCommandGroup(name="admin", description="Admin commands")

    @admin.command(name="set_role", description="Set the role you would like to track")
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx: discord.ApplicationContext):
        view = AdminRoleSelectView()
        await ctx.respond("Select roles: ", view=view, ephemeral=True)

    @admin.command(
        name="delete_last_messages",
        description="Delete the last n messages in the current channel",
    )
    @commands.has_permissions(administrator=True)
    async def delete_last_messages(
        self, ctx: discord.ApplicationContext, amount: int
    ) -> None:

        if ctx.channel is None:
            raise Exception("Channel was none")

        messages = await ctx.channel.history(limit=amount).flatten()  # type: ignore
        for msg in messages:
            await msg.delete()

        await ctx.send("Deleted messages")

    @admin.command(
        name="set_wow_guild",
        description="Set this servers World of Warcraft guild",
    )
    @commands.has_permissions(administrator=True)
    async def set_wow_guild(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: str = "Dalaran",
        region: str = "us",
    ):

        # discord is already tied to a wow guild
        guildExist = await GuildService().is_discord_already_linked(ctx.guild_id)
        if guildExist:
            await ctx.respond(f"`{ctx.guild.name} is already tied to a wow guild`")
            return

        # wow_guild is already tied to discord
        wowGuildAlreadyLinked = await GuildService().is_wow_guild_already_linked(
            name, realm
        )
        if wowGuildAlreadyLinked:
            await ctx.respond(f"`{name}-{realm} is already tied to a discord server`")
            return

        # wow guild cannot be found
        # TODO add something

        # everything good

        wow_guild = await GuildService().add_wow_guild(
            name, realm, region, ctx.guild_id
        )

        if wow_guild is None:
            await ctx.respond(f"`{name}-{realm} was not found.`")
            return

        await ctx.respond(
            f"Guild `{wow_guild.name}-{wow_guild.realm}` was added to `{ctx.guild.name}`"
        )

    # @admin.command(
    #     name="add_character_to_guild",
    #     description="Adds a WoW character to the server's WoW guild",
    # )
    # @commands.has_permissions(administrator=True)
    # async def add_character_to_guild(
    #     self,
    #     ctx: discord.ApplicationContext,
    #     name: str,
    #     realm: str = "Dalaran",
    #     region: str = "us",
    # ):
    #     character_io = await RaiderIOClient.getCharacterProfile(name, realm)

    #     if character_io is None:
    #         await ctx.respond(
    #             f"Character {name}-{realm} was not found or does not exist"
    #         )
    #         return

    #     if ctx.guild is None:
    #         await ctx.respond(f"No valid guild in discord")
    #         return

    #     wow_guild = await self.bot.db.getWowGuildByDiscordGuildId(ctx.guild.id)

    #     if wow_guild is None:
    #         await ctx.respond(f"Guild {name}-{realm} was not found or does not exist")
    #         return

    #     character_io.discord_user_id = ctx.author.id
    #     character_io.guild_id = wow_guild.id
    #     wow_character = await self.bot.db.createWowCharacter(character_io)

    #     if wow_character is None or wow_character.guild_id is None:
    #         raise Exception("add_character_to_guild wasn't working")

    #     await ctx.respond(f"`{wow_character.name}` was added to `{wow_guild.name}`")

    # @admin.command(
    #     name="get_guild_summary",
    #     description="Get a summary of the current guild",
    # )
    # @commands.has_permissions(administrator=True)
    # async def get_guild_summary(self, ctx: discord.ApplicationContext):
    #     if ctx.guild is None:
    #         await ctx.respond(f"No valid guild in discord")
    #         return

    #     wow_guild = await self.bot.db.getWowGuild(ctx.guild.id)

    #     if wow_guild is None or len(wow_guild.characters) == 0:
    #         await ctx.respond(f"get guild summary had a problem")
    #         return

    #     guild_vm = CharacterVie

    #     embed = GuildViews.getGuildSummary(wow_guild, wow_guild.characters)

    #     await ctx.respond(embed=embed)

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem: {error}")
        await ctx.respond("Something weng wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Admin(bot))
    logger.info("Admin cog has loaded successfully")
