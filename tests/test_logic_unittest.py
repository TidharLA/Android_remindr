import tempfile
import unittest
from pathlib import Path

from logic import MemoryStore, parse_query, parse_store, process_text


class LogicTests(unittest.TestCase):
    def test_parse_store(self):
        self.assertEqual(parse_store("I put the map in the closet"), ("map", "closet"))

    def test_parse_query(self):
        self.assertEqual(parse_query("Where is the map?"), "map")

    def test_process_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / "mem.db"
            store = MemoryStore(str(db))
            self.assertIn("Saved", process_text("I put the keys in drawer", store))
            self.assertIn("drawer", process_text("Where is the keys?", store))
            self.assertIn("No memory found", process_text("Where is the keys?", store))
            store.close()


if __name__ == "__main__":
    unittest.main()

