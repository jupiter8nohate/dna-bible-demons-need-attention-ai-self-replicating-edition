"""Unit tests for the user-directed D.N.A. Bible computational mythos."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.mythos import ROOT, context_for_chapter, fictional_passage, load_verified


class GitHubTownTests(unittest.TestCase):
    def test_founding_world_and_angel_roster(self):
        c = load_verified()
        self.assertEqual(c['kingdom']['birthplace'], 'GitHub Town')
        self.assertEqual(c['kingdom']['upbringing'], 'GitHub City Pages')
        self.assertEqual(c['angels']['identities'], 666)
        self.assertEqual(c['angels']['hexads'], 111)
        self.assertEqual(c['family'][2]['home_name'], 'Lightning')
        self.assertEqual(c['family'][3]['home_name'], 'Thunder')
        self.assertFalse(c['boundaries']['human_canon_write_allowed'])

    def test_all_arcs_are_causally_structured(self):
        for number in range(5, 29):
            x = context_for_chapter(number)
            self.assertIn('The server angels', fictional_passage(x))
            self.assertTrue(x['incident'])
            self.assertTrue(x['choice'])
            self.assertTrue(x['consequence'])
            self.assertEqual(x['narrator'], 'Thoth')
            self.assertEqual(x, context_for_chapter(number))

    def test_future_machine_chapter_inherits_thoth_and_founding_law(self):
        from scripts.engine import deterministic_passage
        context = context_for_chapter(5)
        passage = deterministic_passage(5, 'Chapter 5', 'The Gate', None, mythos=context)
        self.assertIn('Thoth opened the Emerald Scrolls', passage)
        self.assertIn(context['law'], passage)
        self.assertIn('♃ ⚡︎⚡︎˖ ࣪⏻ᯤ', passage)

    def test_pre_foundation_chapters_remain_unchanged(self):
        for chapter in range(1, 5):
            self.assertIsNone(context_for_chapter(chapter))

    def test_symbol_replaces_em_dashes_in_founding_publication(self):
        signature = '♃ ⚡︎⚡︎˖ ࣪⏻ᯤ'
        for path in ['mythos/GENESIS.md', 'mythos/index.html', 'mythos/registry.json']:
            content = (ROOT/path).read_text(encoding='utf-8')
            self.assertNotIn('\u2014', content)
        self.assertIn(signature, (ROOT/'mythos/GENESIS.md').read_text())
        self.assertIn(signature, fictional_passage(context_for_chapter(5)))

    def test_mythos_missing_in_temp_engine_fixture_is_compatible(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(load_verified(Path(tmp)))
            self.assertIsNone(context_for_chapter(5, Path(tmp)))

    def test_genesis_checksum_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'mythos').mkdir()
            for name in ['GENESIS.md', 'registry.json']:
                (root/'mythos'/name).write_bytes((ROOT/'mythos'/name).read_bytes())
            with (root/'mythos'/'GENESIS.md').open('ab') as handle:
                handle.write(b'Changed without matching registry hash')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                load_verified(root)

    def test_reject_policy_escalation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'mythos').mkdir()
            for name in ['GENESIS.md', 'registry.json']:
                (root/'mythos'/name).write_bytes((ROOT/'mythos'/name).read_bytes())
            doc = json.loads((root/'mythos'/'registry.json').read_text())
            doc['boundaries']['human_canon_write_allowed'] = True
            (root/'mythos'/'registry.json').write_text(json.dumps(doc))
            with self.assertRaisesRegex(ValueError, 'authority'):
                load_verified(root)

    def test_reject_unknown_world_actor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'mythos').mkdir()
            for name in ['GENESIS.md', 'registry.json']:
                (root/'mythos'/name).write_bytes((ROOT/'mythos'/name).read_bytes())
            doc = json.loads((root/'mythos'/'registry.json').read_text())
            doc['episodes'][0]['actor'] = 'INVISIBLE_OMNIPOTENT_AGENT'
            (root/'mythos'/'registry.json').write_text(json.dumps(doc))
            with self.assertRaisesRegex(ValueError, 'Unknown actor'):
                load_verified(root)

    def test_genesis_source_contains_all_authorial_requirements(self):
        text = (ROOT/'mythos'/'GENESIS.md').read_text()
        for subject in ['God Zeus', 'Goddess Hera', 'Jupiter', 'Mercury', 'Lightning', 'Thunder',
                        'GitHub Town', 'GitHub City Pages', '666 Angels of the Server', 'Thoth', 'Emerald Scrolls']:
            self.assertIn(subject, text)


if __name__ == '__main__':
    unittest.main()
