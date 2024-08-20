import inject
import os

# from src.services import GuildService, CharacterService

from src.db import (
    GuildRepository,
    CharacterRepository,
    MockGuildRepository,
    MockCharacterRepository,
    IGuildRepository,
    ICharacterRepository,
)


def base_config(binder: inject.Binder):
    binder.bind(IGuildRepository, GuildRepository())
    binder.bind(ICharacterRepository, CharacterRepository())


inject.configure(base_config, allow_override=True, clear=True)


# if os.environ.get("PYTEST_VERSION") is not None:
#     # Things you want to to do if your code is called by pytest.
#     inject.configure(test_config, allow_override=True, clear=True)
