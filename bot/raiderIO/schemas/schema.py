from marshmallow import Schema, fields, post_load, EXCLUDE
from ..models.character import Character, Guild, Item, Gear


class GuildSchema(Schema):
    name = fields.Str()
    realm = fields.Str()

    class Meta:
        unknown = EXCLUDE

    def load(self, *args, **kwargs) -> Guild:
        data = super().load(*args, **kwargs)
        return Guild(**data)


class ItemSchema(Schema):
    item_id = fields.Int()
    item_level = fields.Int()
    icon = fields.Str()
    name = fields.Str()
    item_quality = fields.Int()
    is_legendary = fields.Bool()
    gems = fields.List(fields.Int(), allow_none=True)
    enchant = fields.Integer(allow_none=True)
    tier = fields.Str(allow_none=True)

    class Meta:
        unknown = EXCLUDE

    def load(self, *args, **kwargs) -> Item:
        data = super().load(*args, **kwargs)
        return Item(**data)


class GearSchema(Schema):
    updated_at = fields.Str()
    item_level_equipped = fields.Int()
    item_level_total = fields.Int()
    items = fields.Dict(keys=fields.Str(), values=fields.Nested(ItemSchema))

    class Meta:
        unknown = EXCLUDE

    def load(self, *args, **kwargs) -> Gear:
        data = super().load(*args, **kwargs)
        return Gear(**data)


class CharacterSchema(Schema):
    name = fields.Str()
    race = fields.Str()
    c_class = fields.Str(data_key="class")
    faction = fields.Str()
    region = fields.Str()
    realm = fields.Str()
    gear = fields.Nested(GearSchema)
    guild = fields.Nested(GuildSchema)

    class Meta:
        unknown = EXCLUDE

    def load(self, *args, **kwargs) -> Character:
        data = super().load(*args, **kwargs)
        return Character(**data)
