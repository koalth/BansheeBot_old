import inject
from src.config import config
from src.raiderIO import IRaiderIOClient, RaiderIOClient

from src.services import (
    ISettingsService,
    SettingsService,
    IGuildService,
    ICharacterService,
    GuildService,
    CharacterService,
)


def base_config(binder: inject.Binder):

    binder.bind(
        IRaiderIOClient,
        RaiderIOClient(
            config.API_URL,
        ),
    )

    binder.bind(ISettingsService, SettingsService())
    binder.bind(ICharacterService, CharacterService())
    binder.bind(IGuildService, GuildService())


inject.configure(base_config, allow_override=True, clear=True)
