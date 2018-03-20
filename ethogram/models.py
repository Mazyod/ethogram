"""
Contains basic models classes, with zero dependency on other files
"""

from datetime import datetime
from .util import Util

###
# Metrics
#

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
        if self.hashrate <= 0.01 and old_metric.hashrate <= 0.01:
            return None
        if old_metric.hashrate <= 0.01 \
            or (self.hashrate / old_metric.hashrate) > 1.1:
            return "Hashrate increased!"
        if (self.hashrate / old_metric.hashrate) < 0.9:
            return "Hashrate dropped!"
        return None

class TimestampMetric:
    def __init__(self, payload):
        now = datetime.utcnow()
        server_time = datetime.fromtimestamp(payload["server_time"])

        self.update_delta = (now - server_time).seconds
        self.boot_delta = int(payload["uptime"] or 0)
        self.mine_delta = int(payload["miner_secs"] or 0)

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


###
# Rig
#

class Rig:
    def __init__(self, uid, payload):
        self.uid = uid
        self.name = payload.get("rack_loc") or uid
        self.hashrate = HashrateMetric(int(payload["hash"]))
        self.gpu_temps = TemperatureMetric(*Util.min_max_from_seq(payload["temp"]))
        self.timestamp = TimestampMetric(payload)

    def all_metrics(self):
        return [self.hashrate, self.gpu_temps, self.timestamp]

    def row(self, included):
        return [self.name] + [str(getattr(self, a)) for a in included]
