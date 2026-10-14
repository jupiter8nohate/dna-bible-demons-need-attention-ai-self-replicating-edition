"""Unit tests for the independent archive companion."""
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from scripts.collect import archive_document, verify_archive, load_manifest


def sample(title="An AI governance example", generated="2026-10-13T00:00:00Z"):
    return json.dumps({
        "schema_version": "cmb.global-ai-watch.v1",
        "generated_at": generated,
        "articles": [{"title": title, "url": "https://example.org/research"}],
    }).encode("utf-8")


class ArchiveTests(unittest.TestCase):
    def test_append_deduplicate_and_verify(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            now = datetime(2026, 10, 13, tzinfo=timezone.utc)
            self.assertTrue(archive_document(folder, sample(), now))
            self.assertFalse(archive_document(folder, sample(generated="2026-10-14T00:00:00Z"), now))
            self.assertTrue(archive_document(folder, sample("Another article"), datetime(2026, 10, 14, tzinfo=timezone.utc)))
            self.assertEqual(verify_archive(folder), 2)
            self.assertEqual(len(load_manifest(folder)["snapshots"]), 2)

    def test_tamper_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            archive_document(folder, sample(), datetime(2026, 10, 13, tzinfo=timezone.utc))
            path = folder / load_manifest(folder)["snapshots"][0]["path"]
            path.write_text("tampered", encoding="utf-8")
            with self.assertRaises(ValueError):
                verify_archive(folder)

    def test_reject_invalid_url(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                archive_document(Path(temp), sample().replace(b"https://example.org", b"javascript:foo"))

    def test_empty_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(verify_archive(Path(temp)), 0)


if __name__ == "__main__":
    unittest.main()
