import logging
from src import BansheeBot

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    try:
        bot = BansheeBot()
        bot.run()
    except Exception as err:
        logger.error("Error running main: ", err)


if __name__ == "__main__":
    main()
