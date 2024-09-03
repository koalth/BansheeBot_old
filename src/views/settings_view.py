import discord
from discord.ui.item import Item
import inject
from src.services import ISettingsService, ICharacterService, IGuildService
from loguru import logger
from typing import List, cast
import uuid


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


class SettingsView(discord.ui.View):
    discord_guild_id: str
    settingsService: ISettingsService = inject.attr(ISettingsService)

    def __init__(
        self,
        discord_guild_id: str,
        *items: Item,
        timeout: float | None = 180,
        disable_on_timeout: bool = False,
    ):
        self.discord_guild_id = discord_guild_id
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)


class SettingsSelectRegion(SettingsView):

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


class SettingsRaiderRoleSelect(SettingsView):

    @discord.ui.role_select(
        placeholder="Choose the role for your raiders", min_values=1, max_values=1
    )
    async def select_callback(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ):
        select_values = cast(List[discord.Role], select.values)
        selected_value = select_values[0]

        await self.settingsService.update_setting(
            discord_guild_id=self.discord_guild_id,
            setting_attr="raider_role_id",
            attr_value=str(selected_value.id),
        )

        await interaction.response.edit_message(
            content=f"Raider role set to: `{selected_value.name}`",
            delete_after=10,
            view=None,
        )


class SettingsRaiderRoleMemberSelectModal(discord.ui.Modal):

    settingsService: ISettingsService = inject.attr(ISettingsService)
    characterService: ICharacterService = inject.attr(ICharacterService)

    def __init__(
        self, guild_id: uuid.UUID, discord_guild_id: str, *args, **kwargs
    ) -> None:
        self.guild_id = guild_id
        self.discord_guild_id = discord_guild_id

        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Character Name", required=True))

    async def callback(self, interaction: discord.Interaction):

        settings = await self.settingsService.get_settings(
            discord_guild_id=self.discord_guild_id
        )
        if settings is None:
            return await interaction.response.send_message("There was an error")

        if settings.default_region is None:
            return await interaction.response.send_message("There was an error")

        if settings.default_realm is None:
            return await interaction.response.send_message("There was an error")

        character_name = self.children[0].value

        if character_name is None:
            return await interaction.response.send_message("There was an error")

        character = await self.characterService.get_character(
            character_name, settings.default_realm, settings.default_region
        )

        if character is None:
            return await interaction.response.send_message("There was an error")

        if interaction.user is None:
            return await interaction.response.send_message("There was an error")

        await self.characterService.add_character_to_guild(
            character=character,
            discord_user_id=str(interaction.user.id),
            guild_id=self.guild_id,
        )

        embed = discord.Embed(
            title=f"You have added {character_name} to the guild's raid roster!"
        )
        await interaction.response.send_message(embed=embed)


class SettingsRaiderRoleMemberSelectView(SettingsView):

    def __init__(
        self,
        guild_id: uuid.UUID,
        discord_guild_id: str,
        *items: Item,
        timeout: float | None = 180,
        disable_on_timeout: bool = False,
    ):
        self.guild_id = guild_id
        super().__init__(
            discord_guild_id,
            *items,
            timeout=timeout,
            disable_on_timeout=disable_on_timeout,
        )

    @discord.ui.button(label="Add Character", style=discord.ButtonStyle.primary)
    async def button_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.disable_all_items()
        await interaction.response.send_modal(
            SettingsRaiderRoleMemberSelectModal(
                title="Add your wow character!",
                discord_guild_id=self.discord_guild_id,
                guild_id=self.guild_id,
            )
        )
