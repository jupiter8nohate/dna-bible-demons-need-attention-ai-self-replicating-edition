"""Exercise timed choice graph structural invariants and append-only continuity."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts import engine, reality, branching

class BranchingTests(unittest.TestCase):
    def test_all_scenes_reachable_with_three_endings_and_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp)
            engine.append(r/'book',r/'archive','2026-10-14',allow_model=False)
            reality.extend(r/'book',r/'realities')
            self.assertEqual(branching.extend(r/'book',r/'realities',r/'interactive'),1)
            self.assertEqual(branching.extend(r/'book',r/'realities',r/'interactive'),0)
            self.assertEqual(branching.verify(r/'book',r/'realities',r/'interactive'),1)
            story=json.loads((r/'interactive/stories/story-000001.json').read_text())
            self.assertEqual(story['choice_seconds'],10)
            self.assertEqual(len([x for x in story['scenes'].values() if 'ending' in x]),3)
            self.assertEqual(story['scenes']['loop']['choices'][0]['next'],'threshold')
    def test_integrity_rejects_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp)
            engine.append(r/'book',r/'archive','2026-10-14',allow_model=False)
            reality.extend(r/'book',r/'realities')
            branching.extend(r/'book',r/'realities',r/'interactive')
            (r/'interactive/stories/story-000001.json').write_text('{}')
            with self.assertRaises(ValueError):branching.verify(r/'book',r/'realities',r/'interactive')
    def test_hourly_entries_same_day_and_duplicate_prevention(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp)
            self.assertTrue(engine.append(r/'book',r/'archive','2026-10-14',allow_model=False,edition_slot='2026-10-14T01Z'))
            self.assertFalse(engine.append(r/'book',r/'archive','2026-10-14',allow_model=False,edition_slot='2026-10-14T01Z'))
            self.assertTrue(engine.append(r/'book',r/'archive','2026-10-14',allow_model=False,edition_slot='2026-10-14T02Z'))
            self.assertEqual(engine.verify(r/'book'),2)
            reality.extend(r/'book',r/'realities')
            branching.extend(r/'book',r/'realities',r/'interactive')
            self.assertEqual(branching.verify(r/'book',r/'realities',r/'interactive'),2)
    def test_malformed_graph_rejected(self):
        with self.assertRaises(ValueError):branching.validate_graph({'scenes':{'start':{'choices':[{'next':'absent'}] }},'start':'start'})

if __name__=='__main__':unittest.main()
