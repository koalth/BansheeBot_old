from datetime import datetime
import discord
from discord.ui.item import Item
from src.entities import (
    Setting,
    SettingCreate,
    SettingUpdate,
    CharacterUpdate,
    CharacterCreate,
)
import inject
from src.services import ISettingService, ICharacterService, IGuildService
from loguru import logger
from typing import List, cast, Optional
import uuid


region_options = [
    discord.SelectOption(label="US", value="us"),
    discord.SelectOption(label="EU", value="eu"),
]


class SettingsShowEmbed(discord.Embed):

    settingsService: ISettingService = inject.attr(ISettingService)

    def __init__(
        self,
        region: Optional[str],
        realm: Optional[str],
        admin_role: Optional[str],
        raider_role: Optional[str],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.title = "Settings"
        self.description = "The server's current settings"

        self.add_field(
            name="Default Region",
            value=(region if region is not None else "Not set"),
        )
        self.add_field(
            name="Default Realm",
            value=realm if realm is not None else "Not set",
        )

        self.add_field(
            name="Admin Role",
            value=(admin_role if admin_role is not None else "Not set"),
        )
        self.add_field(
            name="Raider Role",
            value=(raider_role if raider_role is not None else "Not set"),
        )


def get_select_option(
    selected_value, options: List[discord.SelectOption]
) -> discord.SelectOption:
    for option in options:
        if option.value == selected_value:
            return option

    raise Exception("Option does not exist")


class SettingsView(discord.ui.View):
    discord_guild_id: str
    settingsService: ISettingService = inject.attr(ISettingService)

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

        update_obj = SettingUpdate(
            discord_guild_id=self.discord_guild_id, default_region=selected_option.value
        )

        settings = await self.settingsService.get_by_discord_guild_id(
            discord_guild_id=self.discord_guild_id
        )
        await self.settingsService.update(settings.id, update_obj)

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

        update_obj = SettingUpdate(
            discord_guild_id=self.discord_guild_id,
            raider_role_id=str(selected_value.id),
        )

        settings = await self.settingsService.get_by_discord_guild_id(
            discord_guild_id=self.discord_guild_id
        )

        await self.settingsService.update(settings.id, update_obj)

        await interaction.response.edit_message(
            content=f"Raider role set to: `{selected_value.name}`",
            delete_after=10,
            view=None,
        )


class SettingsRaiderRoleMemberSelectModal(discord.ui.Modal):

    settingsService: ISettingService = inject.attr(ISettingService)
    characterService: ICharacterService = inject.attr(ICharacterService)

    def __init__(
        self, guild_id: uuid.UUID, discord_guild_id: str, *args, **kwargs
    ) -> None:
        self.guild_id = guild_id
        self.discord_guild_id = discord_guild_id

        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Character Name", required=True))

    async def callback(self, interaction: discord.Interaction):

        settings = await self.settingsService.get_by_discord_guild_id(
            discord_guild_id=self.discord_guild_id
        )

        if settings.default_region is None:
            return await interaction.response.send_message("There was an error")

        if settings.default_realm is None:
            return await interaction.response.send_message("There was an error")

        character_name = self.children[0].value

        if character_name is None:
            return await interaction.response.send_message("There was an error")

        character = await self.characterService.get_character_from_raider_io(
            character_name, settings.default_realm, settings.default_region
        )

        if character is None:
            return await interaction.response.send_message("There was an error")

        if interaction.user is None:
            return await interaction.response.send_message("There was an error")

        character_create_obj = CharacterCreate(
            discord_user_id=str(interaction.user.id),
            on_raid_roster=True,
            guild_id=self.guild_id,
            name=character.name,
            realm=character.realm,
            region=character.region,
            item_level=character.gear.item_level_equipped,
            class_name=character.character_class,
            spec_name=character.active_spec_name,
            profile_url=character.profile_url,
            thumbnail_url=character.thumbnail_url,
            last_crawled_at=character.last_crawled_at,
        )

        created_character = await self.characterService.create(character_create_obj)

        embed = discord.Embed(
            title=f"You have added `{created_character.name}`-`{created_character.realm}` to the guild's raid roster!"
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
