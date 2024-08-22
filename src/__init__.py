from loguru import logger
from src.bot import BansheeBot
from src.config import config

def main():

    if config.DEBUG:
        logger.debug("Debugging is enabled")
    try:
        bot = BansheeBot()
        bot.run()
    except Exception:
        logger.exception("Error in main")


if __name__ == "__init__":
    main()
