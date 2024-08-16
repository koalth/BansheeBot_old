import unittest
from unittest.mock import MagicMock
from src.services import GuildService
from src.db import GuildRepository, GuildOrm

class GuildServiceTests(unittest.TestCase):

    guildService: GuildService


    def setUp(self):
        self.guildRepository = GuildRepository()
        self.guildRepository.get_by_discord_guild_id = MagicMock(return_value=)
        self.guildService = GuildService()

    def test_