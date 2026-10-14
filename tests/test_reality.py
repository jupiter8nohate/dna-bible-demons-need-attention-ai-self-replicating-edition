"""Verify the add-on world engine does not rewrite canon or source chapters."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.engine import append
from scripts.reality import LENSES, extend, verify


class RealityTests(unittest.TestCase):
    def test_twelve_distinct_lenses(self):
        self.assertEqual(len(LENSES), 12)
        self.assertEqual(len({row[0] for row in LENSES}), 12)

    def test_generates_hash_chained_worlds_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book, archive, realms = [root / p for p in ('book', 'archive', 'realities')]
            self.assertTrue(append(book, archive, '2026-10-13', allow_model=False))
            self.assertTrue(append(book, archive, '2026-10-14', allow_model=False))
            before = (book / 'manifest.json').read_bytes()
            self.assertEqual(extend(book, realms), 2)
            self.assertEqual(extend(book, realms), 0)
            self.assertEqual(before, (book / 'manifest.json').read_bytes())
            self.assertEqual(verify(book, realms), 2)
            manifest = json.loads((realms / 'manifest.json').read_text())
            self.assertEqual(manifest['entries'][1]['previous_sha256'], manifest['entries'][0]['sha256'])
            world = json.loads((realms / 'worlds/realm-000001.json').read_text())
            self.assertTrue(world['fictional'])
            self.assertEqual(len(world['reader_choices']), 3)
            self.assertEqual(world['theological_status'], 'question_for_study_not_doctrinal_answer')
            self.assertEqual(world['cycle'], 1)

    def test_detect_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book, archive, realms = [root / p for p in ('book', 'archive', 'realities')]
            append(book, archive, '2026-10-13', allow_model=False)
            extend(book, realms)
            (realms / 'worlds/realm-000001.json').write_text('{}')
            with self.assertRaises(ValueError):
                verify(book, realms)

    def test_continuity_across_twelfth_world(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book, archive, realms = [root / p for p in ('book', 'archive', 'realities')]
            for day in range(1, 14):
                append(book, archive, f'2026-09-{day:02d}', allow_model=False)
            extend(book, realms)
            self.assertEqual(verify(book, realms), 13)
            first = json.loads((realms / 'worlds/realm-000001.json').read_text())
            thirteenth = json.loads((realms / 'worlds/realm-000013.json').read_text())
            self.assertEqual(first['lens_id'], thirteenth['lens_id'])
            self.assertEqual(thirteenth['cycle'], 2)


if __name__ == '__main__':
    unittest.main()
