import discord
from discord.ui.item import Item
import inject
from src.services import ISettingsService
from loguru import logger
from typing import List


region_options = [
    discord.SelectOption(label="US", value="us"),
    discord.SelectOption(label="EU", value="eu"),
]


def get_select_option(
    selected_value, options: List[discord.SelectOption]
) -> discord.SelectOption:
    for option in options:
        if option.value == selected_value:
            return option

    raise Exception("Option does not exist")


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
        self, select: discord.ui.Select, interaction: discord.Interaction
    ):
        self.disable_all_items()
        self.timeout = 10

        selected_option = get_select_option(select.values[0], select.options)

        await self.settingsService.update_setting(
            discord_guild_id=self.discord_guild_id,
            setting_attr="default_region",
            attr_value=selected_option.value,
        )

        await interaction.response.edit_message(
            content=f"Default region set to `{selected_option.label}`",
            delete_after=10,
            view=None,
        )
