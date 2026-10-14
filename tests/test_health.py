"""Verify stalls, archive integrity and honest model labeling."""
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from scripts import engine, reality, branching, health

class HealthTests(unittest.TestCase):
    def build(self, root):
        engine.append(root/"book",root/"archive","2026-10-14",allow_model=False,edition_slot="2026-10-14T01Z")
        reality.extend(root/"book",root/"realities")
        branching.extend(root/"book",root/"realities",root/"interactive")

    def test_fresh_and_stalled(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.build(root)
            fresh=health.report(root,datetime(2026,10,14,2,tzinfo=timezone.utc))
            stale=health.report(root,datetime(2026,10,14,6,tzinfo=timezone.utc))
            self.assertEqual(fresh["status"],"operational")
            self.assertEqual(stale["status"],"stalled")
            self.assertEqual(fresh["chapters"],1)
            self.assertFalse(fresh["model_generation_verified"])

    def test_corrupt_source_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.build(root)
            (root/"book/chapters/chapter-000001.json").write_text("{}")
            with self.assertRaises(ValueError):
                health.report(root,datetime(2026,10,14,2,tzinfo=timezone.utc))
