import os
from dotenv import load_dotenv
from src import BansheeBot

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def main():
    bot = BansheeBot()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
