import discord
from discord.ui.item import Item
import inject
from src.services import ISettingsService
from loguru import logger

region_options = [
    discord.SelectOption(label="US", value="us"),
    discord.SelectOption(label="EU", value="eu"),
]


class SettingsSelectRegion(discord.ui.View):

    discord_guild_id: str

    def __init__(
        self,
        discord_guild_id: str,
        *items: Item,
        timeout: float | None = 180,
        disable_on_timeout: bool = False,
    ):
        self.discord_guild_id = discord_guild_id
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)

    settingsService: ISettingsService = inject.attr(ISettingsService)

    @discord.ui.select(
        placeholder="Choose your default region",
        options=region_options,
        min_values=1,
        max_values=1,
    )
    async def select_callback(
        self, select: discord.SelectMenu, interaction: discord.Interaction
    ):

        self.disable_all_items()
        self.timeout = 10
        logger.debug(f"interaction data: {interaction.data}")
        logger.debug(f"Selected: {select.options[0].value}")
        selected_value = select.options[0].value

        await self.settingsService.update_setting(
            discord_guild_id=self.discord_guild_id,
            setting_attr="default_region",
            attr_value=selected_value,
        )

        await interaction.response.edit_message(
            content=f"Default region set to `{selected_value}`",
            view=self,
            delete_after=10,
        )

        # await interaction.respond(f"Default region set to `{selected_value}`")
        # await interaction.response.edit_message(view=self)

        # return await interaction.response.send_message(
        #     f"Default Region set to `{selected_value}`", ephemeral=True
        # )
