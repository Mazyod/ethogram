"""
Persistence storage service implementation
"""
import os
import json


class Storage:
    def __init__(self, filepath):
        self.filepath = filepath

    @property
    def contents(self):
        if not os.path.exists(self.filepath):
            return {}

        with open(self.filepath) as f:
            return json.loads(f.read())

    def write_contents(self, obj):
        with open(self.filepath, "w+") as f:
            f.write(json.dumps(obj))

    def set(key, value):
        # TODO - thread safety
        store = self.contents
        store[key] = value
        self.write_contents(store)

    def get(key):
        return self.contents.get(key)

    def clear(self):
        try:
            os.remove(self.filepath)
        except:
            pass
