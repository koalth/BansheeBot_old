from loguru import logger
from src.bot import BansheeBot
from src.config import Config, config
from typing import Optional


def create_bot(alt_config: Optional[Config] = None) -> BansheeBot:

    bot = BansheeBot()

    if alt_config is not None:
        logger.debug("Using alternative config")
        bot.set_config(alt_config)
    else:
        logger.debug("Using default config")
        bot.set_config(config)

    return bot


def main():
    bot = create_bot()
    bot.run()


if __name__ == "__init__":
    main()
