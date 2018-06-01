"""
Just a wrapper around the available configurations for ethogram
"""

import os
import json


class Config:
    def __init__(self):
        config_filepath = os.environ.get('ETHOGRAM_ROOT', ".")
        config_filepath = os.path.join(config_filepath, "ethogram.json")

        with open(config_filepath) as f:
            self.config = json.loads(f.read())

    @property
    def telegram_token(self):
        return self.config["TELEGRAM_TOKEN"]

    @property
    def webhook_host(self):
        return self.config["WEBHOOK_HOST"]

    @property
    def webhook_port(self):
        return self.config.get("WEBHOOK_PORT", 8443)
