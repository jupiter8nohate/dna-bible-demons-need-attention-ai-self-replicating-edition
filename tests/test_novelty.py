"""Deterministic fallback originality checks."""
import difflib
import unittest
from scripts.engine import STORY_SEEDS, deterministic_passage

class NoveltyTests(unittest.TestCase):
    def test_twelve_distinct_fictional_worlds(self):
        self.assertEqual(len(STORY_SEEDS), 12)
        self.assertEqual(len(set(s[0] for s in STORY_SEEDS)), 12)

    def test_adjacent_chapters_do_not_clone_each_other(self):
        texts=[deterministic_passage(i,f"Chapter {i}",f"Theme {i}",None) for i in range(1,14)]
        for a,b in zip(texts,texts[1:]):
            ratio=difflib.SequenceMatcher(None,a,b,autojunk=False).ratio()
            self.assertLess(ratio,0.76)

    def test_fictional_signal_remains_unverified(self):
        text=deterministic_passage(3,"Chapter 3","Test",None,{"story_premise":"A clock diverged."})
        self.assertIn("detected, unverified",text)
        self.assertIn("not proof",text)
