import unittest
import os
from ethogram.storage import Storage


class StorageTests(unittest.TestCase):

    def test_storage(self):
        storage = Storage("tmp/test.json")
        storage.clear()
        self.assertFalse(os.path.exists(storage.filepath))
        self.assertEqual(storage.contents, {})

        val1 = [1, 2, 3]
        val2 = {"a": "test", "b": 444}
        storage.set("key1", val1)
        storage.set("key2", val2)

        self.assertEqual(storage.get("key1"), val1)
        self.assertEqual(storage.get("key2"), val2)
        self.assertEqual(storage.get("key3"), None)

        storage.clear()
