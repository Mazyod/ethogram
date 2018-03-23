import unittest
import os
from ethogram.config import Config


class ConfigTests(unittest.TestCase):
    
    def test_fong(self):
        os.environ["ETHOGRAM_ROOT"] = os.path.dirname(__file__)

        config = Config()
        self.assertEqual(config.telegram_token, "token")
        self.assertEqual(config.webhook_host, "host")
        self.assertEqual(config.webhook_port, 8443)
