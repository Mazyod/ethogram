"""
Just a wrapper around the available configurations for ethogram
"""

import os

class Config:
    @classmethod
    def env(cls, key):
        return os.environ[key]

    @classmethod
    def telegram_token(cls):
        return cls.env("TELEGRAM_TOKEN")
