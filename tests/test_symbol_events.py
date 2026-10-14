"""Angelic event history checks for generated fiction."""
import json
import tempfile
import unittest
from pathlib import Path
from shutil import copytree
from scripts import civilization, symbol_events

class TestSymbolEvents(unittest.TestCase):
    def test_registry_signature(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "civilization/symbols.json").read_text("utf-8"))
        self.assertEqual(data["signature"], symbol_events.STAMP)

    def test_coverage_and_tamper_detection(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            copytree(root / "civilization", target / "civilization")
            copytree(root / "mythos", target / "mythos")
            self.assertEqual(symbol_events.run(target, write=True), civilization.verify(target))
            self.assertEqual(symbol_events.run(target), civilization.verify(target))
            entry = target / "civilization/symbol_events/days/day-000001.json"
            item = json.loads(entry.read_text("utf-8"))
            item["events"][0]["detail"] = "forged"
            entry.write_text(json.dumps(item), encoding="utf-8")
            with self.assertRaises(ValueError):
                symbol_events.run(target)

    def test_missing_coverage_fails(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            copytree(root / "civilization", target / "civilization")
            copytree(root / "mythos", target / "mythos")
            with self.assertRaises(ValueError):
                symbol_events.run(target)

if __name__ == "__main__":
    unittest.main()
