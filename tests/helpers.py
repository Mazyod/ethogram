
from collections import defaultdict


class BotMock:
    def __init__(self):
        self.network = NetworkMock()
        self.storage = StorageMock()
        self.tables = []
        self.messages = []

    def clear(self):
        self.tables = []
        self.messages = []

    def send_table(self, table, chat_id):
        self.tables.append((table, chat_id))

    def send_message(self, message, chat_id):
        self.messages.append((message, chat_id))


class NetworkMock:
    def __init__(self):
        self.all_rigs = defaultdict(lambda: [])

    def fetch_rigs(self, panel_id):
        return self.all_rigs[panel_id]


class StorageMock:
    def __init__(self):
        self.sets = []
        self.gets = {}

    def set(self, key, value):
        self.sets.append((key, value))

    def get(self, key):
        return self.gets.get(key)
