from datetime import datetime


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
