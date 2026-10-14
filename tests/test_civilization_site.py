import unittest
from pathlib import Path

class LivingCivilizationWebsiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.html = (cls.root / 'civilization/index.html').read_text(encoding='utf-8')
        cls.js = (cls.root / 'civilization/reader.js').read_text(encoding='utf-8')

    def test_story_opens_from_day_one(self):
        for value in ('Day One', 'GitHub Town', 'God Zeus', 'Goddess Hera', 'Jupiter', 'Mercury', 'Thoth', '666'):
            self.assertIn(value, self.html)

    def test_chronological_reader(self):
        for value in ('id="day-list"', 'id="story-body"', 'id="day-title"'):
            self.assertIn(value, self.html)
        self.assertIn('choose(indexFromUrl())', self.js)

    def test_browser_checks_story_fingerprint(self):
        self.assertIn("crypto.subtle.digest('SHA-256', raw)", self.js)
        self.assertIn("verifiedDay(record.path, record.sha256)", self.js)

    def test_untrusted_prose_not_rendered_as_html(self):
        self.assertNotIn('innerHTML', self.js)
        self.assertIn('textContent', self.js)

    def test_signature_and_no_em_dash(self):
        self.assertIn('♃ ⚡︎⚡︎˖ ࣪⏻ᯤ', self.html)
        self.assertNotIn(chr(0x2014), self.js)
        self.assertNotIn(chr(0x2014), self.html)

if __name__ == '__main__':
    unittest.main()
