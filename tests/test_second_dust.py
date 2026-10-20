"""Second Dust regression tests: accessible links, source boundaries, and canon guard."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "second-dust"

class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.scrolls = [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.append(a["id"])
        if tag == "a" and "href" in a: self.hrefs.append(a["href"])
        if tag == "section" and a.get("class") == "scroll": self.scrolls.append(a.get("id"))

class SecondDustTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (DIRECTORY / "index.html").read_text(encoding="utf-8")
        cls.manifest = json.loads((DIRECTORY / "manifest.json").read_text(encoding="utf-8"))
        cls.research = json.loads((DIRECTORY / "research.json").read_text(encoding="utf-8"))
        cls.reader = Reader()
        cls.reader.feed(cls.html)

    def test_seven_complete_scrolls(self):
        expected = ["scroll-" + x for x in ("i", "ii", "iii", "iv", "v", "vi", "vii")]
        self.assertEqual(self.reader.scrolls, expected)
        self.assertEqual([s["id"] for s in self.manifest["scrolls"]], expected)
        self.assertEqual(len(self.reader.ids), len(set(self.reader.ids)))
        for slug in expected:
            self.assertIn("#" + slug, self.reader.hrefs)
            body = self.html.split('id="' + slug + '"', 1)[1].split("</section>", 1)[0]
            self.assertGreaterEqual(body.count("<p>"), 6)

    def test_evidence_is_classified(self):
        classes = {r["type"] for r in self.research["items"]}
        self.assertEqual(classes, {"documented","documented_projection","fictional_extrapolation","open_question"})
        for item in self.research["items"]:
            if item["type"].startswith("documented"):
                self.assertTrue(item["source"].startswith("https://"))
                self.assertRegex(item["date"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertIn("Conscious uploaded people", self.html)
        self.assertIn("fiction", self.html.lower())

    def test_authority_remains_human(self):
        self.assertFalse(self.manifest["authority"]["modify_separate_human_canon"])
        self.assertFalse(self.manifest["authority"]["allow_autonomous_rewrite"])
        self.assertTrue(self.manifest["authority"]["require_review_for_additions"])
        mythos = json.loads((ROOT / "mythos/registry.json").read_text(encoding="utf-8"))
        self.assertFalse(mythos["boundaries"]["human_canon_write_allowed"])
        self.assertEqual(mythos["angels"]["identities"], 666)

    def test_links_and_static_accessibility(self):
        self.assertIn('href="second-dust/"', (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn('href="../second-dust/"', (ROOT / "civilization/index.html").read_text(encoding="utf-8"))
        self.assertNotIn("<script", self.html.lower())
        self.assertNotIn("\u2014", self.html)
        self.assertIn('class="skip"', self.html)
        for href in self.reader.hrefs:
            if href.startswith("#"): self.assertIn(href[1:], self.reader.ids)

if __name__ == "__main__":
    unittest.main()
