import inject
from src.config import config
from src.db import (
    GuildRepository,
    CharacterRepository,
    IGuildRepository,
    ICharacterRepository,
)

from src.raiderIO import RaiderIOClient


def base_config(binder: inject.Binder):
    binder.bind(IGuildRepository, GuildRepository())
    binder.bind(ICharacterRepository, CharacterRepository())

    binder.bind(
        RaiderIOClient,
        RaiderIOClient(
            config.API_URL,
            config.CALLS,
            config.RATE_LIMIT,
            config.TIMEOUT,
            config.RETRIES,
            config.BACKOFF_FACTOR,
        ),
    )


inject.configure(base_config, allow_override=True, clear=True)
