import os
from dotenv import load_dotenv

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import DiscordGuild, DiscordGuildMember, DiscordGuildMemberLink

load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class BansheeBotDB:
    def __init__(self):
        print("---- BansheeBot Database Initializing ---------")
        self.sqlite_file_name = f"{SQLALCHEMY_DATABASE_URI}"
        self.sqlite_url = f"sqlite+aiosqlite:///{self.sqlite_file_name}"
        self.engine = create_async_engine(self.sqlite_url, echo=True)
        print("---- BansheeBot Database Initialized ---------")

    async def init(self):
        async with self.engine.begin() as session:
            await session.run_sync(SQLModel.metadata.create_all)
            print("Database created")

    # async def addDiscordUser(self, discord_id: int, discord_username: str):
    #     async with AsyncSession(self.engine) as session:
    #         discord_user = await session.exec(
    #             select(DiscordUser).where(DiscordUser.discord_id == discord_id)
    #         )
    #         try:
    #             discord_user = discord_user.one()
    #             print("Discord user already exists.")
    #         except NoResultFound:
    #             discord_user = DiscordUser(
    #                 discord_id=discord_id, discord_username=discord_username
    #             )
    #             session.add(discord_user)
    #             await session.commit()
    #             await session.refresh(discord_user)
    #         except Exception:
    #             print("Something went wrong with addDiscordUser")


db = BansheeBotDB()
