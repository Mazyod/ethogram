import unittest
from datetime import datetime
from ethogram.models import *


class ModelTests(unittest.TestCase):
    # TODO - need to refine temperature alert triggers
    def test_temperature_metric(self):
        met1 = TemperatureMetric(90, 0)
        met2 = TemperatureMetric(80, 0)
        self.assertEqual(str(met1), "0 - 90 C")
        self.assertEqual(met1.alert(met2), "High temperature detected!")
        met3 = TemperatureMetric(91, 1)
        self.assertEqual(met1.alert(met3), "Low temperature detected!")

    def test_hashrate_metric(self):
        met1 = HashrateMetric(5000)
        met2 = HashrateMetric(4000)
        self.assertEqual(str(met1), "5000 H/s")
        self.assertEqual(met1.alert(met2), "Hashrate increased!")
        met3 = HashrateMetric(6000)
        self.assertEqual(met1.alert(met3), "Hashrate dropped!")
        met0 = HashrateMetric(0)
        self.assertEqual(met1.alert(met0), "Hashrate increased!")
        self.assertEqual(met0.alert(met0), None)
        self.assertEqual(met0.alert(met1), "Hashrate dropped!")

    def test_timestamp_metric(self):
        payload = {
            "server_time": datetime.utcnow().timestamp(),
            "uptime": 99999,
            "miner_secs": 99999,
        }

        normal_met = TimestampMetric(payload)

        offline = payload.copy()
        offline["server_time"] = datetime.utcnow().timestamp() - 10 * 60
        offline_met = TimestampMetric(offline)

        reboot = payload.copy()
        reboot["uptime"] = 3000
        reboot_met = TimestampMetric(reboot)

        self.assertIn("offline", offline_met.alert(normal_met))
        self.assertIn("reboot", reboot_met.alert(normal_met))
