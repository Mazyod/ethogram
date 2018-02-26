#!/usr/bin/env python3

import os
import json
import time
from threading import Thread
from datetime import datetime
from urllib.request import urlopen
from telegram import Bot as TelegramBot
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
from tabulate import tabulate


class Scheduler:

    @classmethod
    def start(cls, callback):
        thread = Thread(target=cls.run, args=(callback,))
        thread.daemon = True
        thread.start()

    @classmethod
    def run(cls, callback):
        while True:
            callback()
            time.sleep(5 * 60)


class Monitor:
    def __init__(self):
        self.rigs = Rig.all()

    def update(self):
        old_rigs = self.rigs
        new_rigs = Rig.all()

        all_rows = []
        alerts = []
        for old_rig, new_rig in zip(old_rigs, new_rigs):
            row = []
            for old_met, new_met in zip(old_rig.all_metrics(), new_rig.all_metrics()):
                alert = new_met.alert(old_met)
                if alert:
                    alerts.append(alert)
                    row.append(str(metric))
            if row:
                row = [new_rig.name] + row
                all_rows += row

        if all_rows:
            bot = Bot.shared()
            bot.send_table(all_rows)
            bot.send_message("\n".join(alerts))

        self.rigs = new_rigs


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
    def min_max_from_seq(cls, string):
        nums = [int(s) for s in string.split(" ")]
        return (min(nums), max(nums))

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


class TemperatureMetric:
    def __init__(self, high, low):
        self.high = high
        self.low = low

    def __str__(self):
        return "{} - {} C".format(self.low, self.high)

    def alert(self, old_metric):
        if self.high > 75 and self.high > old_metric.high:
            return "High temperature detected!"
        if self.low < 35 and self.low < old_metric.low:
            return "Low temperature detected!"
        return None

class HashrateMetric:
    def __init__(self, hashrate):
        self.hashrate = hashrate

    def __str__(self):
        return "{} H/s".format(self.hashrate)

    def alert(self, old_metric):
        if (self.hashrate / old_metric.hashrate) < 0.9:
            return "Hashrate dropped!"
        if (self.hashrate / old_metric.hashrate) > 1.1:
            return "Hashrate increased!"
        return None

class TimestampMetric:
    def __init__(self, payload):
        now = datetime.utcnow()
        server_time = datetime.utcfromtimestamp(payload["server_time"])

        self.update_delta = (now - server_time).seconds
        self.boot_delta = int(payload["uptime"])
        self.mine_delta = int(payload["miner_secs"])

    def __str__(self):
        deltas = [self.update_delta, self.boot_delta, self.mine_delta]
        return " ".join(map(Util.time_ago, deltas))

    def alert(self, old_metric):
        if self.update_delta > (8 * 60) and old_metric.update_delta < (8 * 60):
            return "Rig seems offline!"
        if self.boot_delta < old_metric.boot_delta:
            return "Rig seems to have rebooted!"
        if self.mine_delta < old_metric.mine_delta:
            return "Miner seems to have restarted!"
        return None


class Rig:
    @classmethod
    def all(cls):
        ethos_response_raw = urlopen("http://%s.ethosdistro.com/?json=yes" % (Config.ethos_panel_id()))
        ethos_response = json.loads(ethos_response_raw.read().decode())
        return sorted([Rig(p) for p in ethos_response["rigs"].values()], key=lambda r: r.name)

    def __init__(self, payload):
        self.name = payload["rack_loc"]
        self.hashrate = HashrateMetric(int(payload["hash"]))
        self.gpu_temps = TemperatureMetric(*Util.min_max_from_seq(payload["temp"]))
        self.timestamp = TimestampMetric(payload)

    def all_metrics(self):
        return [self.hashrate, self.gpu_temps, self.timestamp]

    def row(self, included=["timestamp", "hashrate", "gpu_temps"]):
        return [self.name] + [str(getattr(self, a)) for a in included]


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
        text = "```\n" + text + "\n```" if code else text
        self.telbot.send_message(
            text=text, chat_id=Config.chat_group_id(),
            parse_mode=ParseMode.MARKDOWN)

    def send_timestamp(self):
        print("timestamp requested...")
        table = [r.row(included=["timestamp"]) for r in Rig.all()]
        self.send_table(table)

    def send_hashrates(self):
        print("hashrates requested...")
        table = [r.row(included=["hashrate"]) for r in Rig.all()]
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
    monitor = Monitor()

    updater = Updater(Config.telegram_token())
    [updater.dispatcher.add_handler(c) for c in bot.commands]

    Scheduler.start(monitor.update)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
