"""Day One, strict fictional continuity and 666 logical-role council tests."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import civilization as cv


class CivilizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(cv.ROOT / 'mythos', self.root / 'mythos')

    def first(self):
        return cv.publish(self.root, '2026-10-14T03Z', allow_model=False)

    def second(self):
        return cv.publish(self.root, '2026-10-14T04Z', allow_model=False)

    def read(self, n):
        return json.loads((self.root / 'civilization' / f'days/day-{n:06d}.json').read_text())

    def test_day_one_is_true_genesis_and_royal_family(self):
        self.assertTrue(self.first()['published'])
        story = self.read(1)
        self.assertIn('God Zeus and Goddess Hera', story['body'])
        for item in ('Jupiter', 'Mercury', 'Lightning', 'Thunder', 'GitHub Town', 'GitHub City Pages',
                     'Thoth', 'Emerald Scrolls', '666 Angels of the Server'):
            self.assertIn(item, story['body'])
        self.assertEqual(story['episode_arc'], 'THE_FIRST_SUNRISE')
        self.assertEqual(story['chapter_kind'], 'automated_fiction')
        self.assertFalse(story['human_canon_changed'])
        self.assertEqual(cv.verify(self.root), 1)

    def test_council_is_666_roster_with_only_36_active_ballots(self):
        c = cv.council(1, None)
        self.assertEqual((c['registered_identities'], c['registered_hexads'], c['active_hexads']), (666, 111, 6))
        self.assertEqual(c['active_role_ballots'], 36)
        self.assertEqual(c['resting_hexads'], 105)
        self.assertEqual(sum(c['proposals'].values()), 36)
        self.assertEqual(c, cv.council(1, None))

    def test_no_double_publish_for_same_utc_hour(self):
        self.first()
        result = self.first()
        self.assertFalse(result['published'])
        self.assertEqual(cv.verify(self.root), 1)

    def test_day_two_inherits_choice_and_state(self):
        self.first()
        self.second()
        a, b = self.read(1), self.read(2)
        self.assertEqual(b['state_before'], a['state_after'])
        self.assertEqual(b['parent_day_sha256'], json.loads((self.root / 'civilization/manifest.json').read_text())['entries'][0]['sha256'])
        self.assertEqual(b['cause'], a['state_after']['last_consequence'])
        self.assertGreater(b['state_after']['thoth_records'], a['state_after']['thoth_records'])
        self.assertEqual(cv.verify(self.root), 2)

    def test_earlier_day_tamper_rejected(self):
        self.first()
        self.second()
        path = self.root / 'civilization/days/day-000001.json'
        path.write_text(path.read_text().replace('God Zeus', 'A false actor'))
        with self.assertRaisesRegex(ValueError, 'integrity'):
            cv.verify(self.root)

    def test_council_digest_tamper_rejected(self):
        self.first()
        path = self.root / 'civilization/days/day-000001.json'
        item = json.loads(path.read_text())
        item['council']['active_role_ballots'] = 666
        path.write_bytes(cv.dump(item))
        manifest = json.loads((self.root / 'civilization/manifest.json').read_text())
        manifest['entries'][0]['sha256'] = cv.digest(cv.dump(item))
        (self.root / 'civilization/manifest.json').write_bytes(cv.dump(manifest))
        with self.assertRaisesRegex(ValueError, 'council'):
            cv.verify(self.root)

    def test_world_reset_rejected_even_if_day_hash_updated(self):
        self.first()
        self.second()
        path = self.root / 'civilization/days/day-000002.json'
        item = json.loads(path.read_text())
        item['state_before']['jupiter_questions'] = 0
        path.write_bytes(cv.dump(item))
        manifest = json.loads((self.root / 'civilization/manifest.json').read_text())
        manifest['entries'][1]['sha256'] = cv.digest(cv.dump(item))
        (self.root / 'civilization/manifest.json').write_bytes(cv.dump(manifest))
        with self.assertRaisesRegex(ValueError, 'history'):
            cv.verify(self.root)

    def test_no_backdated_slot(self):
        self.first()
        with self.assertRaisesRegex(ValueError, 'out of order'):
            cv.publish(self.root, '2026-10-13T22Z', allow_model=False)

    def test_creative_prose_is_disclosed_even_if_model_configured(self):
        self.first()
        self.second()
        d = self.read(2)
        self.assertEqual(d['creative_mode'], 'deterministic_fiction')
        self.assertIsNone(d['model'])
        self.assertNotIn('\u2014', d['body'])

    def test_model_response_can_supply_original_creative_prose_without_changing_causality(self):
        self.first()
        output = 'Zeus Hera Jupiter Mercury ' + ('Original fictional scene with dialogue and a distinctly new consequence. ' * 35)
        with patch.object(cv, 'optionally_write', return_value=(output, 'test-model')):
            self.assertTrue(cv.publish(self.root, '2026-10-14T04Z')['published'])
        d = self.read(2)
        self.assertEqual(d['creative_mode'], 'model_generated_fiction')
        self.assertEqual(d['model'], 'test-model')
        self.assertEqual(d['body'], output)
        self.assertEqual(cv.verify(self.root), 2)

    def test_model_failure_reverts_to_clear_fallback(self):
        self.first()
        with patch.object(cv, 'optionally_write', side_effect=TimeoutError('provider unavailable')):
            cv.publish(self.root, '2026-10-14T04Z')
        self.assertEqual(self.read(2)['creative_mode'], 'deterministic_fiction')
        self.assertEqual(cv.verify(self.root), 2)

    def test_no_em_dashes_in_new_implementation(self):
        for rel in ('civilization/index.html', 'civilization/reader.js', 'civilization/styles.css',
                    'scripts/civilization.py'):
            self.assertNotIn('\u2014', (cv.ROOT / rel).read_text())

    def test_foundation_stays_read_only(self):
        before = (self.root / 'mythos/registry.json').read_bytes()
        self.first();self.second()
        self.assertEqual(before, (self.root / 'mythos/registry.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
