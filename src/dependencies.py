import inject
from src.config import config
from src.external import IRaiderIOClient, RaiderIOClient
from src.db import (
    ISettingRepository,
    SettingRepository,
    IGuildRepository,
    GuildRepository,
    ICharacterRepository,
    CharacterRepository,
)

from src.services import (
    ISettingService,
    SettingService,
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

    binder.bind(ISettingRepository, SettingRepository())
    binder.bind(IGuildRepository, GuildRepository())
    binder.bind(ICharacterRepository, CharacterRepository())

    binder.bind(ISettingService, SettingService())
    binder.bind(ICharacterService, CharacterService())
    binder.bind(IGuildService, GuildService())


inject.configure(base_config, allow_override=True, clear=True)
