from datetime import datetime
from marshmallow import Schema, fields, post_load, EXCLUDE


class Guild:
    name: str
    faction: str
    region: str
    realm: str
    profile_url: str

    def __init__(
        self,
        name: str,
        faction: str,
        region: str,
        realm: str,
        profile_url: str,
    ) -> None:
        self.name = name
        self.faction = faction
        self.region = region
        self.realm = realm
        self.profile_url = profile_url


class GuildSchema(Schema):
    name = fields.Str()
    faction = fields.Str()
    region = fields.Str()
    realm = fields.Str()
    profile_url = fields.Str()

    class Meta:
        unknown = EXCLUDE

    def load(self, *args, **kwargs) -> Guild:
        data = super().load(*args, **kwargs)
        return Guild(**data)
