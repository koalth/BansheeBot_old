import discord
from typing import List, Optional
from src.entities import Character


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
