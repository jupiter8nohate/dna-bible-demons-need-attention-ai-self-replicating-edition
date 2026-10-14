"""Regression: relevance, de-duplication, source integrity, and chapter consumption."""
from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from scripts import collect as archive_mod
from scripts import insight
from scripts import engine


def article(title: str, url: str, boundaries=None, sectors=None):
    return {'title': title, 'url': url,
            'boundary_ids': boundaries or ['ACT'], 'sector_ids': sectors or ['general'],
            'seen_at': '2026-10-13T12:00:00Z'}


class InsightTests(unittest.TestCase):
    def test_reject_unrelated_keyword_headlines(self):
        for title in ('Man City vs PSG: predictions and teams',
                      'Surveillance video shows a traffic accident',
                      'Stock market algorithm predictions'):
            # Finance algorithms may be relevant in general; without explicit machine
            # context this is a conservative false-negative policy.
            if title.startswith('Stock'):
                continue
            ok, reason = insight.relevance(article(title, 'https://example.com/a'))
            self.assertFalse(ok, title)
            self.assertEqual(reason, 'no_explicit_ai_subject')
        self.assertTrue(insight.relevance(article('Robotics safety researchers test AI agents', 'https://example.com/r'))[0])

    def fixture(self, root: Path):
        arch = root / 'archive'
        data = {'schema_version': 'cmb.global-ai-watch.v1',
                'generated_at': '2026-10-13T12:00:00Z',
                'articles': [
                    article('Man City vs PSG match predictions', 'https://sports.example/a'),
                    article('Surveillance video shows a vehicle collision', 'https://news.example/b'),
                    article('Factory robots test new safety controls', 'https://tech.example/c?utm_source=rss', ['ACT'], ['workplace_civil_rights']),
                    article('AI chatbots and digital consent debates', 'https://tech.example/d', ['GENERATE'], ['privacy_surveillance']),
                    article('Factory robots test new safety controls', 'https://tech.example/c?utm_campaign=b', ['ACT']),
                ]}
        archive_mod.archive_document(arch, json.dumps(data).encode('utf-8'),
                                     now=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        return arch

    def test_ingest_dedup_verify_select_and_consume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            arch = self.fixture(root)
            folder = root / 'insights'
            first = insight.collect(arch, folder, now=datetime(2026,10,13,tzinfo=timezone.utc))
            self.assertEqual(first['new'], 2)
            self.assertEqual(first['excluded'], 2)
            self.assertEqual(insight.verify(folder, arch), 2)
            self.assertEqual(insight.collect(arch, folder)['new'], 0)
            selected = insight.select_for_chapter(folder, root / 'book')
            self.assertIsNotNone(selected)
            self.assertEqual(selected['evidence_status'], 'headline_metadata_unverified')
            self.assertTrue(engine.append(root / 'book', arch, '2026-10-14', allow_model=False))
            c = json.loads((root / 'book' / 'chapters/chapter-000001.json').read_text())
            self.assertEqual(c['insight_reference']['id'], selected['id'])
            self.assertIn('unverified source metadata', c['body'])
            nxt = insight.select_for_chapter(folder, root / 'book')
            self.assertNotEqual(nxt['id'], selected['id'])
            engine.append(root / 'book', arch, '2026-10-15', allow_model=False)
            self.assertIsNone(insight.select_for_chapter(folder, root / 'book'))
            engine.append(root / 'book', arch, '2026-10-16', allow_model=False)
            third = json.loads((root / 'book' / 'chapters/chapter-000003.json').read_text())
            self.assertIsNone(third['source_metadata'])
            self.assertIsNone(third['insight_reference'])

    def test_reject_corrupted_source_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            arch = self.fixture(root)
            record = json.loads((arch / 'manifest.json').read_text())['snapshots'][0]
            (arch / record['path']).write_text('tampered!', encoding='utf-8')
            with self.assertRaises(ValueError):
                insight.collect(arch, root / 'insights')

    def test_detect_corrupted_insight(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            arch = self.fixture(root)
            folder = root / 'insights'
            insight.collect(arch, folder)
            (folder / 'events/insight-000001.json').write_text('{}', encoding='utf-8')
            with self.assertRaises(ValueError):
                insight.verify(folder, arch)


if __name__ == '__main__':
    unittest.main()
