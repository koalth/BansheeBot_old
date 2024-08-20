from loguru import logger
from src.bot import BansheeBot


def main():
    logger.debug("This is a test message")
    try:
        bot = BansheeBot()
        bot.run()
    except Exception as err:
        logger.error("Error running main: ", err)


if __name__ == "__init__":
    main()
