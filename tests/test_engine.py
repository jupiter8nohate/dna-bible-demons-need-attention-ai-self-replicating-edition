"""Tests for the 666-agent bounded living-manuscript engine."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts.engine import GUILDS, append, load_manifest, roster, run_agents, verify


class EngineTests(unittest.TestCase):
    def test_666_unique_agents_all_execute(self):
        agents = roster()
        self.assertEqual(len(agents), 666)
        self.assertEqual(len(set(agents)), 666)
        ballots, counts = run_agents(1, 10)
        self.assertEqual([x["id"] for x in ballots], agents)
        self.assertEqual(counts, {guild: 111 for guild in GUILDS})
        self.assertTrue(all(x["status"] == "complete" for x in ballots))

    def test_append_idempotent_chained_and_tamper_detected(self):
        with tempfile.TemporaryDirectory() as book, tempfile.TemporaryDirectory() as archive:
            folder = Path(book)
            self.assertTrue(append(folder, Path(archive), "2026-10-13", allow_model=False))
            self.assertFalse(append(folder, Path(archive), "2026-10-13", allow_model=False))
            self.assertTrue(append(folder, Path(archive), "2026-10-14", allow_model=False))
            self.assertEqual(verify(folder), 2)
            manifest = load_manifest(folder)
            self.assertEqual(manifest["entries"][1]["previous_sha256"], manifest["entries"][0]["sha256"])
            path = folder / manifest["entries"][0]["path"]
            chapter = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(chapter["mode"], "deterministic_code_poetry")
            self.assertEqual(chapter["agent_count"], 666)
            path.write_text("tampered", encoding="utf-8")
            with self.assertRaises(ValueError):
                verify(folder)

    def test_reject_untrusted_archive_path(self):
        with tempfile.TemporaryDirectory() as book, tempfile.TemporaryDirectory() as archive:
            archive_path = Path(archive)
            (archive_path / "manifest.json").write_text(json.dumps({"snapshots": [{"path": "../README.md", "sha256": "fake"}]}))
            with self.assertRaises(ValueError):
                append(Path(book), archive_path, "2026-10-13", allow_model=False)


if __name__ == "__main__":
    unittest.main()
