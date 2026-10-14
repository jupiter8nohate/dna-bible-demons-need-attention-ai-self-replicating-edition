"""Contract tests for the Angelic Symbol Protocol."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AngelicSymbolsTest(unittest.TestCase):
    def test_registry(self):
        data = json.loads((ROOT / "civilization/symbols.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "dna.angelic-symbols.v1")
        self.assertEqual(data["signature"], "♃ ⚡︎⚡︎˖ ࣪⏻ᯤ")
        self.assertEqual(len(data["tokens"]), 5)
        self.assertEqual(data["usage"]["agent_identities"], 666)
        self.assertIn("not cryptographic", data["disclaimer"])
        self.assertTrue(any("must never be rewritten" in rule for rule in data["rules"]))

    def test_reader(self):
        text = (ROOT / "civilization/reader.js").read_text(encoding="utf-8")
        self.assertIn("requestJson('symbols.json')", text)
        self.assertIn("symbols.schema_version", text)
        self.assertNotIn("innerHTML =", text)


if __name__ == "__main__":
    unittest.main()
