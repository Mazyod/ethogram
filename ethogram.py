#!/usr/bin/env python3

import os
import json
from datetime import datetime
from urllib.request import urlopen
from telegram import Bot as TelegramBot
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
from tabulate import tabulate

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


class Util:
    @classmethod
    def range_from_string_seq(cls, string):
        nums = [int(s) for s in string.split(" ")]
        return "{min} - {max}".format(min=min(nums), max=max(nums))

    @classmethod
    def time_ago(cls, timestamp):
        s = int(timestamp)
        days, remainder = divmod(s, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        if days >= 1:
            return str(days) + "d"
        if hours >= 1:
            return str(hours) + "h"

        return str(minutes) + "m"

class Rig:
    @classmethod
    def all(cls):
        ethos_response_raw = urlopen("http://%s.ethosdistro.com/?json=yes" % (Config.ethos_panel_id()))
        ethos_response = json.loads(ethos_response_raw.read().decode())
        return [Rig(p) for p in ethos_response["rigs"].values()]

    def __init__(self, payload):
        self.name = payload["rack_loc"]
        self.hashrate = payload["hash"]
        self.gpu_temps = Util.range_from_string_seq(payload["temp"])

        update_delta = datetime.now() - datetime.utcfromtimestamp(payload["server_time"])
        self.timestamp = "{update} {boot} {mine}".format(
            update=Util.time_ago(update_delta.seconds),
            boot=Util.time_ago(payload["uptime"]),
            mine=Util.time_ago(payload["miner_secs"])
        )

    def row(self, included=["timestamp", "hashrates", "gpu_temps"]):
        row = [self.name]

        if "hashrates" in included:
            row.append(str(self.hashrate) + " H/s")
        if "gpu_temps" in included:
            row.append(str(self.gpu_temps) + " C")
        if "timestamp" in included:
            row.append(str(self.timestamp))

        return row


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
            CommandHandler("all_stats", lambda *_: self.send_all_stats()),
            CommandHandler("hashrates", lambda *_: self.send_hashrates()),
            CommandHandler("gpu_temps", lambda *_: self.send_gpu_temps()),
            CommandHandler("timestamp", lambda *_: self.send_timestamp()),
        ]

    def send_table(self, table):
        text = str(tabulate(table))
        self.send_message(text, code=True)

    def send_message(self, text, code=False):
        text = "```\n" + text + "\n``` ." if code else text
        self.telbot.send_message(
            text=text, chat_id=Config.chat_group_id(),
            parse_mode=ParseMode.MARKDOWN)

    def send_timestamp(self):
        print("timestamp requested...")
        table = [r.row(included=["timestamp"]) for r in Rig.all()]
        self.send_table(table)

    def send_hashrates(self):
        print("hashrates requested...")
        table = [r.row(included=["hashrates"]) for r in Rig.all()]
        self.send_table(table)

    def send_gpu_temps(self):
        print("gpu temps requested...")
        table = [r.row(included=["gpu_temps"]) for r in Rig.all()]
        self.send_table(table)

    def send_all_stats(self):
        print("all stats requested...")
        table = [r.row() for r in Rig.all()]
        self.send_table(table)

def main():

    bot = Bot.shared()
    bot.send_all_stats()

    updater = Updater(Config.telegram_token())
    [updater.dispatcher.add_handler(c) for c in bot.commands]

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
