"""
Simple object that can run a callback at fixed intervals
"""

import time
from threading import Thread


class Scheduler:

    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.running = False

    def start(self):
        self.running = True

        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        while self.running:
            try:
                self.callback()
                time.sleep(self.interval)
            except Exception as e:
                print(e)
                time.sleep(self.interval * 0.1)
