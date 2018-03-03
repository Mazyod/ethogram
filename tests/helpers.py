
from collections import defaultdict


class BotMock:
    def __init__(self):
        self.tables = []
        self.messages = []

    def clear(self):
        self.tables = []
        self.messages = []

    def send_table(self, table):
        self.tables.append(table)

    def send_message(self, message):
        self.messages.append(message)


class NetworkMock:
    def __init__(self):
        self.all_rigs = defaultdict(lambda: [])

    def fetch_rigs(self, panel_id):
        return self.all_rigs[panel_id]
