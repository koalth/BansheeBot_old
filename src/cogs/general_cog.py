from loguru import logger
import discord
from discord import guild_only
from discord.ext import commands
import inject
from src.bot import BansheeBot
from src.services import ICharacterService, ISettingService, IGuildService


class General(commands.Cog):

    characterService: ICharacterService = inject.attr(ICharacterService)
    settingService: ISettingService = inject.attr(ISettingService)
    guildService: IGuildService = inject.attr(IGuildService)

    def __init__(self, bot: BansheeBot) -> None:
        self.bot = bot

    def _get_guild_id(self, ctx: discord.ApplicationContext) -> str:
        assert ctx.guild
        return str(ctx.guild.id)

    async def _check_guild_exist(self, ctx: discord.ApplicationContext) -> bool:
        guild_id = self._get_guild_id(ctx)

        return (
            await self.guildService.does_guild_settings_exist(discord_guild_id=guild_id)
        ) is True

    @discord.slash_command(
        name="add",
        description="Add your World of Warcraft character to be tracked and viewed by your guild",
    )
    async def add_character(
        self, ctx: discord.ApplicationContext, name: str, realm: str
    ):
        if not await self._check_guild_exist(ctx):
            return await ctx.respond(
                f"There isn't a guild to be linked. Yell at your server admin"
            )

        if await self.characterService.has_character(str(ctx.author.id)):
            return await ctx.respond(
                f"You already have a character tied to the guild. There can only be one!"
            )

        guild = await self.guildService.get_by_discord_guild_id(
            discord_guild_id=self._get_guild_id(ctx)
        )

        character = await self.characterService.add_character(
            name, realm, guild.region, str(ctx.author.id), guild.id
        )

        return await ctx.respond(
            f"{character.name}-{character.realm} has been added!", ephemeral=True
        )

    @discord.slash_command(
        name="get",
        description="Get your World of Warcraft character currently associated in the discord guild",
    )
    async def get_character(self, ctx: discord.ApplicationContext):

        if not self._check_guild_exist(ctx):
            return await ctx.respond(
                f"There isn't a guild to be linked. Yell at your server admin"
            )

        character = await self.characterService.get_by_did(
            discord_id=str(ctx.author.id)
        )

        embed = discord.Embed(
            title=f"{character.name}",
            colour=discord.Colour.blurple(),
            thumbnail=character.thumbnail_url,
        )

        embed.set_footer(text="Data from Raider.io")
        embed.add_field(name="Name", value=character.name)
        embed.add_field(name="Item Level", value=str(character.item_level))
        embed.add_field(
            name="Class/Spec", value=f"{character.class_name}/{character.spec_name}"
        )

        return await ctx.respond(embed=embed)

    async def cog_command_error(
        self, ctx: discord.ApplicationContext, error: Exception
    ) -> None:
        logger.error(f"There was a problem in General cog: {error}")
        await ctx.respond("Something went wrong :(")
        return await super().cog_command_error(ctx, error)


def setup(bot: BansheeBot) -> None:
    bot.add_cog(General(bot))
    logger.debug("General cog has loaded successfully")
