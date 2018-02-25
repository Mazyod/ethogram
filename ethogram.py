#!/usr/bin/env python3

import os
import json
from urllib.request import urlopen
from telegram import Bot as TelegramBot
from telegram.ext import Updater, CommandHandler


class Config:
    @classmethod
    def env(cls, key):
        return os.environ[key]

    @classmethod
    def telegram_token(cls):
        return cls.env("TELEGRAM_TOKEN")

    @classmethod
    def chat_group_id(cls):
        return cls.env("TELEGRAM_GROUP_CHAT_ID")

    @classmethod
    def ethos_panel_id(cls):
        return cls.env("ETHOS_PANEL_ID")


class Rig:
    @classmethod
    def all(cls):
        ethos_response_raw = urlopen("http://%s.ethosdistro.com/?json=yes" % (Config.ethos_panel_id()))
        ethos_response = json.loads(ethos_response_raw.read().decode())
        return [Rig(p) for p in ethos_response["rigs"].values()]

    def __init__(self, payload):
        self.name = payload["rack_loc"]
        self.hashrate = payload["hash"]


class Bot:
    INSTANCE = None

    @classmethod
    def shared(cls):
        if not cls.INSTANCE:
            cls.INSTANCE = Bot()
        return cls.INSTANCE

    def __init__(self):
        self.telbot = TelegramBot(Config.telegram_token())

        self.commands = [
            CommandHandler("hashrates", lambda *_: self.send_hashrates()),
        ]

    def send_message(self, text):
        self.telbot.send_message(text=text, chat_id=Config.chat_group_id())

    def send_hashrates(self):
        print("hashrates requested...")
        text = []
        for rig in Rig.all():
            text.append("{name}: {hrate} H/s".format(
                name=rig.name, hrate=rig.hashrate))
        text = "\n".join(text)
        self.send_message(text)

def main():

    bot = Bot.shared()
    bot.send_message(text="ethogram bot launched!")

    updater = Updater(Config.telegram_token())
    [updater.dispatcher.add_handler(c) for c in bot.commands]

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
