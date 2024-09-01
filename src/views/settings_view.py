import discord
from discord.ui.item import Item
import inject
from src.services import ISettingsService

region_options = [
    discord.SelectOption(label="US", value="us", default=True),
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
        selected_value = select.options[0].value
        await self.settingsService.update_setting(
            discord_guild_id=self.discord_guild_id,
            setting_attr="default_region",
            attr_value=selected_value,
        )
        return await interaction.response.send_message(
            f"Default Region set to `{selected_value}`", ephemeral=True
        )
