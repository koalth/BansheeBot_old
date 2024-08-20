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

    # binder.bind(GuildService, GuildService())
    # binder.bind(CharacterService, CharacterService())


def test_config(binder: inject.Binder):
    binder.install(base_config)

    # override dependencies
    binder.bind(IGuildRepository, MockGuildRepository)
    binder.bind(ICharacterRepository, MockCharacterRepository)


inject.configure(base_config, allow_override=True, clear=True)

# if os.environ.get("PYTEST_VERSION") is not None:
#     # Things you want to to do if your code is called by pytest.
#     inject.configure(test_config, clear=True)
