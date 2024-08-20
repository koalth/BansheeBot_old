import inject
import os
from src.config import Config

# from src.services import GuildService, CharacterService

from src.db import (
    GuildRepository,
    CharacterRepository,
    MockGuildRepository,
    MockCharacterRepository,
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
            Config.API_URL,
            Config.CALLS,
            Config.RATE_LIMIT,
            Config.TIMEOUT,
            Config.RETRIES,
            Config.BACKOFF_FACTOR,
        ),
    )


inject.configure(base_config, allow_override=True, clear=True)


# if os.environ.get("PYTEST_VERSION") is not None:
#     # Things you want to to do if your code is called by pytest.
#     inject.configure(test_config, allow_override=True, clear=True)
