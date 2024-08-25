import inject
from src.config import config

from src.raiderIO import RaiderIOClient


def base_config(binder: inject.Binder):

    binder.bind(
        RaiderIOClient,
        RaiderIOClient(
            config.API_URL,
        ),
    )


inject.configure(base_config, allow_override=True, clear=True)
