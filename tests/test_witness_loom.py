"""Unit and adversarial tests for the original Witness Loom-666 protocol."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts.witness_loom import create_plan, verify, events, encode, digest, hexad


class WitnessLoomTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def add_insight(self, identifier, score=70):
        folder = self.root / "insights"
        (folder / "events").mkdir(parents=True, exist_ok=True)
        path = folder / "manifest.json"
        m = json.loads(path.read_text()) if path.exists() else {"schema_version": "dna.insight-queue.v1", "entries": []}
        n = len(m["entries"]) + 1
        data = {"id": identifier, "evidence_status": "headline_metadata_unverified", "priority_score": score,
                "question": "What authority must remain human?"}
        blob = encode(data)
        rel = f"events/insight-{n:06d}.json"
        (folder / rel).write_bytes(blob)
        m["entries"].append({"path": rel, "sha256": digest(blob), "previous_sha256": m["entries"][-1]["sha256"] if m["entries"] else None})
        path.write_bytes(encode(m))
        return folder / rel

    def test_plan_six_role_hexads_and_dormant_budget(self):
        for i in range(8):
            self.add_insight(f"DNA-INSIGHT-{i+1:06d}", 80-i)
        self.assertTrue(create_plan(self.root, "2026-10-13T22Z"))
        self.assertEqual(verify(self.root), 1)
        p = json.loads((self.root/"covenant/plans/plan-000001.json").read_text())
        self.assertEqual((p["registered_cells"], p["active_hexads"], p["active_cell_seats"], p["resting_hexads"]), (666, 6, 36, 105))
        self.assertEqual(p["missions"][0]["cells"], ["SEEKER-001","WITNESS-001","SCRIBE-001","SKEPTIC-001","GUARDIAN-001","ARCHIVIST-001"])
        self.assertEqual(p["focus"]["id"], "DNA-INSIGHT-000001")
        self.assertIs(p["human_canon_write_allowed"], False)
        self.assertEqual(p["model_calls_authorized"], 0)

    def test_idempotence_chain_and_tamper_detection(self):
        self.add_insight("I-1")
        self.assertTrue(create_plan(self.root, "2026-10-13T22Z"))
        self.assertFalse(create_plan(self.root, "2026-10-13T22Z"))
        self.assertTrue(create_plan(self.root, "2026-10-13T23Z"))
        self.assertEqual(verify(self.root), 2)
        (self.root/"covenant/plans/plan-000001.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "integrity"):
            verify(self.root)

    def test_corrupt_source_not_promoted(self):
        source = self.add_insight("I-1")
        source.write_text("{}")
        with self.assertRaisesRegex(ValueError, "Corrupted"):
            create_plan(self.root, "2026-10-13T22Z")

    def test_unsafe_event_path_rejected(self):
        folder=self.root/"insights"
        folder.mkdir()
        (folder/"manifest.json").write_bytes(encode({"entries":[{"path":"../private.json","previous_sha256":None,"sha256":"x"}]}))
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            create_plan(self.root, "2026-10-13T22Z")

    def test_no_sources_emits_fictional_continuity_not_fake_news(self):
        create_plan(self.root, "2026-10-13T22Z")
        p=json.loads((self.root/"covenant/plans/plan-000001.json").read_text())
        self.assertEqual(p["focus"]["evidence_status"], "fictional_only")
        self.assertEqual(p["active_cell_seats"], 6)

    def test_attention_budget_hard_cap(self):
        with self.assertRaises(ValueError):
            create_plan(self.root, "2026-10-13T22Z", 111)
        with self.assertRaises(ValueError):
            create_plan(self.root, "2026-10-13T22Z", -1)
        with self.assertRaises(ValueError):
            hexad(112, {"id":"a", "evidence_sha256":"b"})

    def test_plan_no_code_mutation_or_model_invocations(self):
        self.add_insight("I-1")
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        create_plan(self.root, "2026-10-13T22Z")
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual({k:after[k] for k in before}, before)
        self.assertTrue(set(after)-set(before) <= {"covenant/manifest.json", "covenant/plans/plan-000001.json"})

if __name__ == "__main__":
    unittest.main()
