import logging
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.embeds import Embed
from src import BansheeBot
from src.views import AdminRoleSelectView
from src.services import GuildService, CharacterService


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

    @admin.command(
        name="add_character_to_guild",
        description="Adds a wow character to the server's wow guild",
    )
    @commands.has_permissions(administrator=True)
    async def add_character_to_guild(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        realm: str = "Dalaran",
        region: str = "us",
    ):

        wow_char = await CharacterService().add_character_to_guild(
            name, realm, region, ctx.author.id, ctx.guild_id
        )

        if wow_char is None:
            await ctx.respond(f"Something went wrong adding character to guild")
            return

        await ctx.respond(f"`{wow_char.name}` was added")

    @admin.command(
        name="get_guild_summary",
        description="Gets a short summary of the guild member's and their item levels",
    )
    @commands.has_permissions(administrator=True)
    async def get_guild_summary(self, ctx: discord.ApplicationContext):

        wow_guild = await GuildService().get_by_discord_guild_id(ctx.guild_id)

        if wow_guild is None:
            await ctx.respond(f"No guild was found")
            return

        title = f"{wow_guild.name} Summary"
        embed = discord.Embed(
            title=title,
            description="Small summary of all characters registered in the guild\n",
        )

        embed.set_author(name="BansheeBot")

        for character in wow_guild.characters:
            field_value = f"> Item Lv: {character.item_level}"
            embed.add_field(name=character.name, value=field_value)

        embed.set_footer(text="Data from Raider.IO")

        await ctx.respond(embed=embed)

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem: {error}")
        await ctx.respond("Something weng wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(Admin(bot))
    logger.info("Admin cog has loaded successfully")
