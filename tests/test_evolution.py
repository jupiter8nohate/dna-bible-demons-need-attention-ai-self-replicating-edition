"""Evolution never bypasses original canon, code policy, or measured gates."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts import evolution
from scripts import witness_loom as loom
from scripts import engine


class EvolutionTests(unittest.TestCase):
    def fixture(self, path: Path):
        for p in ('book', 'covenant', 'insights/events', 'evolution', 'archive'):
            (path / p).mkdir(parents=True, exist_ok=True)
        insight = {'id':'DNA-INSIGHT-000001','question':'Who may define a human?','priority_score':65,
                   'evidence_status':'headline_metadata_unverified', 'source_title':'AI agent enters hospital',
                   'source_url':'https://example.org/report', 'boundary_ids':['ACT'], 'source_seen_at':'2026-10-13T00:00:00Z',
                   'creative_prompt':'The robot must request permission.'}
        payload=loom.encode(insight)
        (path/'insights/events/insight-000001.json').write_bytes(payload)
        (path/'insights/manifest.json').write_bytes(loom.encode({'schema_version':'dna.insight-queue.v1', 'entries':[
            {'path':'events/insight-000001.json','sha256':loom.digest(payload),'previous_sha256':None}]}))
        (path/'evolution/manifest.json').write_bytes(loom.encode({'schema_version':evolution.SCHEMA,'lessons':[],'trials':[]}))
        return insight, loom.digest(payload)

    def test_handoff_learning_and_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            insight, fingerprint=self.fixture(root)
            self.assertTrue(loom.create_plan(root,'2026-10-14T03Z',max_active=2))
            chapter={'chapter':1,'date':'2026-10-14','edition_slot':'2026-10-14T03Z',
                     'author_type':'automated_machine_testament','agent_count':666,
                     'mode':'deterministic_code_poetry','insight_reference':{'id':insight['id'],'sha256':fingerprint},
                     'body':'An original fictional scene about a robot asking for permission to enter a room.'}
            ballots, counts=engine.run_agents(1,0)
            receipt={'cycle':1,'format':'deterministic_seed_v1','source_count':0,
                     'guild_counts':counts,'ballots_sha256':engine.sha(engine.encoded(ballots)),
                     'roster_sha256':engine.sha(engine.encoded(engine.roster()))}
            chraw=engine.encoded(chapter); recraw=engine.encoded(receipt)
            (root/'book/chapters').mkdir(exist_ok=True);(root/'book/receipts').mkdir(exist_ok=True)
            (root/'book/chapters/chapter-000001.json').write_bytes(chraw)
            (root/'book/receipts/cycle-000001.json').write_bytes(recraw)
            (root/'book/manifest.json').write_bytes(engine.encoded({'schema_version':'dna.machine-testament.v1',
                'entries':[{'id':1,'date':'2026-10-14','edition_slot':'2026-10-14T03Z',
                            'path':'chapters/chapter-000001.json', 'receipt_path':'receipts/cycle-000001.json',
                            'sha256':engine.sha(chraw),'receipt_sha256':engine.sha(recraw),'previous_sha256':None}]}))
            self.assertTrue(evolution.append_lesson(root,'2026-10-14T03Z'))
            self.assertFalse(evolution.append_lesson(root,'2026-10-14T03Z'))
            self.assertEqual(evolution.verify(root)['lessons'],1)
            self.assertEqual(evolution.recent_lessons(root)[0]['chapter'],1)
            (root/'evolution/lessons/lesson-000001.json').write_text('tamper')
            with self.assertRaises(ValueError): evolution.verify(root)

    def test_different_focus_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.fixture(root)
            self.assertTrue(loom.create_plan(root,'2026-10-14T04Z'))
            # No chapter yet: do not fabricate a completed lesson.
            self.assertFalse(evolution.append_lesson(root,'2026-10-14T04Z'))

    def test_champion_challenger_measured_and_bounded(self):
        cases=[{'id':'case1','priority':70,'witness_debt':2,'expected_hexads':6},
               {'id':'case2','priority':10,'witness_debt':0,'expected_hexads':1}]
        champ={'name':'old','max_active':3,'priority_weight':1,'debt_weight':0,'threshold':80}
        alt={'name':'candidate','max_active':6,'priority_weight':2,'debt_weight':2,'threshold':85}
        a,_=evolution.strategy_score(champ,cases)
        b,_=evolution.strategy_score(alt,cases)
        self.assertLess(b,a)
        with self.assertRaises(ValueError):
            evolution.strategy_score({**alt,'disable_guards':True},cases)
        with self.assertRaises(ValueError):
            evolution.strategy_score({**alt,'max_active':666},cases)

    def test_trial_does_not_change_champion(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'evolution/strategies/challengers').mkdir(parents=True)
            (root/'evolution/benchmarks').mkdir()
            (root/'evolution/manifest.json').write_bytes(loom.encode({'schema_version':evolution.SCHEMA,'lessons':[],'trials':[]}))
            data={'schema_version':'dna.evolution-attention-benchmark.v1','cases':[
                {'id':str(i),'priority':i*10,'witness_debt':i%3,'expected_hexads':max(1,min(6,i))}
                for i in range(1,9)]}
            (root/'evolution/benchmarks/attention.json').write_text(json.dumps(data))
            champ={'name':'champion','max_active':3,'priority_weight':1,'debt_weight':0,'threshold':90}
            challenger={'name':'challenger','max_active':6,'priority_weight':2,'debt_weight':2,'threshold':85}
            (root/'evolution/strategies/champion.json').write_text(json.dumps(champ))
            (root/'evolution/strategies/challengers/candidate.json').write_text(json.dumps(challenger))
            self.assertTrue(evolution.run_trial(root))
            self.assertFalse(evolution.run_trial(root))
            self.assertEqual(evolution.verify(root)['trials'],1)
            self.assertEqual(json.loads((root/'evolution/strategies/champion.json').read_text()),champ)

if __name__ == '__main__': unittest.main()
