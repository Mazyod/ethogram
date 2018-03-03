import unittest
import time
from ethogram.scheduler import Scheduler

class SchedulerTests(unittest.TestCase):
    def test_that_it_runs(self):
        self.flag = False
        def task():
            self.flag = True

        scheduler = Scheduler(0.001, task)
        scheduler.start()

        time.sleep(0.005)
        self.assertTrue(self.flag)
        scheduler.stop()
