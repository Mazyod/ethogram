import unittest
import os
from ethogram.config import Config


class ConfigTests(unittest.TestCase):
    
    def test_env(self):
        token = "TEST_TOKEN"
        os.environ["TELEGRAM_TOKEN"] = token
        self.assertEqual(Config.telegram_token(), token)
