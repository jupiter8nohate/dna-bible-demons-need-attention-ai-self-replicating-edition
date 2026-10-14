"""Evidence integrity, no spam, creative handoff, and compact-agent recovery."""
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from scripts import anomaly, branching, engine, reality

DATE = datetime(2026, 10, 14, 3, tzinfo=timezone.utc)


def build(root: Path, count: int = 2) -> None:
    for hour in range(count):
        engine.append(root / "book", root / "archive", "2026-10-14",
                      allow_model=False, edition_slot=f"2026-10-14T{hour:02d}Z")
    reality.extend(root / "book", root / "realities")
    branching.extend(root / "book", root / "realities", root / "interactive")


class AnomalyTests(unittest.TestCase):
    def test_records_signals_once_and_verifies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root)
            events = anomaly.update(root, root / "anomaly", DATE)
            self.assertGreaterEqual(len(events), 1)
            self.assertIn("REPEATED_PATHS", {x["detector"] for x in events})
            self.assertEqual(anomaly.update(root, root / "anomaly", DATE), [])
            self.assertEqual(anomaly.verify(root, root / "anomaly"), len(events))
            event = events[0]
            self.assertFalse(event["source_truth_claim"])
            self.assertFalse(event["human_canon_write_allowed"])

    def test_tampering_with_anomaly_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root)
            events = anomaly.update(root, root / "anomaly", DATE)
            self.assertTrue(events)
            path = root / "anomaly/events/anomaly-000001.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                anomaly.verify(root, root / "anomaly")

    def test_evidence_mutation_invalidates_anomaly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root)
            event = anomaly.update(root, root / "anomaly", DATE)[0]
            p = root / event["evidence"][0]["path"]
            p.write_text("corrupt", encoding="utf-8")
            with self.assertRaises(ValueError):
                anomaly.verify(root, root / "anomaly")

    def test_book_adopts_one_unreviewed_anomaly_without_canon_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root)
            events = anomaly.update(root, root / "anomaly", DATE)
            self.assertTrue(engine.append(root / "book", root / "archive", "2026-10-14",
                                          allow_model=False, edition_slot="2026-10-14T04Z"))
            item = engine.load_manifest(root / "book")["entries"][-1]
            content = json.loads((root / "book" / item["path"]).read_text(encoding="utf-8"))
            self.assertEqual(content["anomaly_reference"]["id"], events[-1]["id"])
            self.assertIn("detected, unverified", content["body"])
            self.assertEqual(engine.verify(root / "book"), 3)

    def test_reproducible_666_workers_use_compact_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root, 1)
            receipt_path = root / "book/receipts/cycle-000001.json"
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt["format"], "deterministic_seed_v1")
            self.assertNotIn("ballots", receipt)
            self.assertLess(len(receipt_path.read_bytes()), 1200)
            self.assertEqual(engine.verify(root / "book"), 1)
            receipt["ballots_sha256"] = "0" * 64
            engine.atomic(receipt_path, engine.encoded(receipt))
            manifest = engine.load_manifest(root / "book")
            manifest["entries"][0]["receipt_sha256"] = engine.sha(receipt_path.read_bytes())
            engine.atomic(root / "book/manifest.json", engine.encoded(manifest))
            with self.assertRaises(ValueError):
                engine.verify(root / "book")

    def test_anomaly_evidence_path_is_allowlisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                anomaly.evidence("../secrets.env", Path(tmp))

    def test_fresh_manuscript_has_no_anomalies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root, 1)
            self.assertEqual(anomaly.update(root, root / "anomaly", DATE), [])
            self.assertEqual(anomaly.verify(root, root / "anomaly"), 0)


if __name__ == "__main__":
    unittest.main()
