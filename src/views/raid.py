import discord
from typing import List, Optional
from src.entities import Character
from src.services import ISettingService, ICharacterService
from src.entities import CharacterCreate
import inject
from uuid import UUID


class RaidRosterShowEmbed(discord.Embed):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = "Raid Roster"
        self.set_footer(text="Data from Raider.IO")

    def item_level_check(self, character: Character, item_level_required: int) -> bool:
        return character.item_level >= item_level_required

    def add_characters(
        self, characters: List[Character], item_level_required: Optional[int]
    ):

        item_levels = []
        if item_level_required is not None:
            item_levels_pre = []
            for character in characters:
                item_levels_pre.append(
                    f"{str(character.item_level)} {'✅' if character.item_level >= item_level_required else '❌'}"
                )

            item_levels = "\n".join(item_levels_pre)
        else:
            item_levels = "\n".join(
                [f"{str(character.item_level)}" for character in characters]
            )
        names = "\n".join([character.name for character in characters])
        class_spec_names = "\n".join(
            [f"{char.class_name}/{char.spec_name}" for char in characters]
        )
        self.add_field(name="Members", value=names, inline=True)
        self.add_field(name="Item Level", value=item_levels, inline=True)
        self.add_field(name="Class/Spec", value=class_spec_names, inline=True)


class LinkCharacterModal(discord.ui.Modal):

    def __init__(self, view: "RaidRosterMemberLinkCharacterView") -> None:
        super().__init__(
            discord.ui.InputText(label="Character Name", max_length=99),
            title="Link Character",
        )
        self.view = view

    async def callback(self, interaction: discord.Interaction) -> None:
        settings = await self.view.settingsService.get_by_discord_guild_id(
            discord_guild_id=self.view.discord_guild_id
        )

        if settings.default_region is None:
            await interaction.response.send_message("There was an error")
            return

        if settings.default_realm is None:
            await interaction.response.send_message("There was an error")
            return

        character_name = self.children[0].value

        if character_name is None:
            await interaction.response.send_message("There was an error")
            return

        character = await self.view.characterService.get_character_from_raider_io(
            character_name, settings.default_realm, settings.default_region
        )

        if character is None:
            await interaction.response.send_message("There was an error")
            return

        if interaction.user is None:
            await interaction.response.send_message("There was an error")
            return

        character_create_obj = CharacterCreate(
            discord_user_id=str(interaction.user.id),
            on_raid_roster=True,
            guild_id=self.view.guild_id,
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

        created_character = await self.view.characterService.create(
            character_create_obj
        )

        embed = discord.Embed(
            title=f"You have added `{created_character.name}`-`{created_character.realm}` to the guild's raid roster!"
        )
        await interaction.response.send_message(embed=embed)


class RaidRosterMemberLinkCharacterView(discord.ui.View):

    discord_guild_id: str
    guild_id: UUID
    settingsService: ISettingService = inject.attr(ISettingService)
    characterService: ICharacterService = inject.attr(ICharacterService)

    def __init__(self, discord_guild_id: str, guild_id: UUID):
        self.discord_guild_id = discord_guild_id
        self.guild_id = guild_id
        super().__init__(timeout=3600, disable_on_timeout=True)

    @discord.ui.button(label="Link Character", style=discord.ButtonStyle.blurple)
    async def link_character(self, _, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(LinkCharacterModal(self))
