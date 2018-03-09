import unittest
import copy
from datetime import datetime
from .helpers import BotMock, NetworkMock
from ethogram.monitor import Monitor
from ethogram.models import Rig


class MonitorTests(unittest.TestCase):
    def test_monitoring(self):
        rig1a = Rig("abcdef", {
            "rack_loc": "testing",
            "hash": 1234,
            "temp": "50 60 70",
            "server_time": datetime.utcnow().timestamp(),
            "uptime": 630,
            "miner_secs": 404,
        })

        rig1b = copy.deepcopy(rig1a)
        rig1b.timestamp.boot_delta = 60

        rig2 = Rig("123456", {
            "rack_loc": "another",
            "hash": 4444,
            "temp": "44 44 44",
            "server_time": datetime.utcnow().timestamp(),
            "uptime": 90,
            "miner_secs": 30,
        })

        bot = BotMock()
        network = bot.network

        monitor = Monitor("chat_id", bot)
        monitor.update()

        self.assertEqual(bot.tables, [])
        self.assertEqual(bot.messages, [])
        bot.clear()

        network.all_rigs["panel"].append(rig2)
        monitor.panels.append("panel")

        monitor.update()
        self.assertEqual(bot.tables, [])
        self.assertEqual(bot.messages, [("another has been added!", "chat_id")])
        bot.clear()

        network.all_rigs["panel"].remove(rig2)
        network.all_rigs["panel"].append(rig1a)

        monitor.update()
        self.assertEqual(bot.tables, [])
        self.assertEqual(bot.messages, [
            (("another has been removed"
            + "\ntesting has been added!"), "chat_id")
        ])
        bot.clear()

        network.all_rigs["panel"].remove(rig1a)
        network.all_rigs["panel"].append(rig1b)

        monitor.update()
        self.assertEqual(bot.tables, [([["testing", "0s 1m 6m"]], "chat_id")])
        self.assertEqual(bot.messages, [
            ("testing: Rig seems to have rebooted!", "chat_id")
        ])
