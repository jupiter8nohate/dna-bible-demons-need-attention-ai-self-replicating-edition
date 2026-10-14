#!/usr/bin/env python3
"""Operational publication health and manuscript novelty report.

Pure checks inspect only local published records. The status is a report, not an
independent attestation or proof of uptime, and a failed status never edits canon.
"""
from __future__ import annotations

import argparse
import difflib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from scripts import engine, anomaly, collect, reality, branching, insight
except ModuleNotFoundError:
    import engine  # type: ignore[no-redef]
    import anomaly  # type: ignore[no-redef]
    import collect  # type: ignore[no-redef]
    import reality  # type: ignore[no-redef]
    import branching  # type: ignore[no-redef]
    import insight  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parents[1]


def latest_instant(entry: dict) -> datetime:
    slot = entry.get('edition_slot')
    if isinstance(slot, str) and slot:
        return datetime.strptime(slot, '%Y-%m-%dT%HZ').replace(tzinfo=timezone.utc)
    return datetime.strptime(entry['date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)


def report(root: Path, now: datetime | None = None, max_age_hours: int = 3) -> dict:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None or max_age_hours < 1:
        raise ValueError('Use an aware time and a positive freshness threshold')
    now = now.astimezone(timezone.utc)
    chapters = engine.verify(root / 'book')
    worlds = reality.verify(root / 'book', root / 'realities')
    stories = branching.verify(root / 'book', root / 'realities', root / 'interactive')
    archives = collect.verify_archive(root / 'archive')
    anomalies = anomaly.verify(root, root / 'anomaly')
    insights = insight.verify(root / 'insights', root / 'archive')
    entries = engine.load_manifest(root / 'book')['entries']
    latest = latest_instant(entries[-1]) if entries else None
    age_hours = round((now - latest).total_seconds() / 3600, 3) if latest else None
    if latest is not None and latest > now + timedelta(minutes=1):
        raise ValueError('Latest manuscript publication is future-dated')
    status = 'operational' if latest is not None and age_hours <= max_age_hours else 'stalled'
    last_mode = entries[-1].get('mode') if entries else None
    chapters_data = [json.loads((root / 'book' / row['path']).read_text(encoding='utf-8')) for row in entries[-2:]]
    similarity = (round(difflib.SequenceMatcher(None, chapters_data[0]['body'], chapters_data[1]['body'], autojunk=False).ratio(), 4)
                  if len(chapters_data) == 2 else None)
    return {
        'schema_version': 'dna.operational-health.v1',
        'observed_at': now.isoformat().replace('+00:00', 'Z'),
        'status': status,
        'freshness_target_hours': max_age_hours,
        'last_chapter_at': latest.isoformat().replace('+00:00', 'Z') if latest else None,
        'hours_since_last_chapter': age_hours,
        'chapters': chapters, 'worlds': worlds, 'interactive_stories': stories,
        'archive_snapshots': archives, 'anomaly_records': anomalies, 'research_insights': insights,
        'last_prose_mode': last_mode,
        'model_generation_verified': last_mode == 'ai_generated',
        'recent_text_similarity': similarity,
        'repetition_warning': similarity is not None and similarity >= 0.76,
        'workers_per_cycle': 666,
        'worker_type': 'bounded_deterministic_software',
        'limitation': 'GitHub-derived self-report; not independent external monitoring or competitor benchmarking.',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=None)
    parser.add_argument('--check-freshness', action='store_true')
    parser.add_argument('--max-age-hours', type=int, default=3)
    args = parser.parse_args()
    try:
        status = report(args.root, max_age_hours=args.max_age_hours)
        if args.output:
            engine.atomic(args.output, engine.encoded(status))
        print(json.dumps(status, sort_keys=True))
        return 1 if args.check_freshness and status['status'] != 'operational' else 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f'HEALTH_CHECK_FAILED: {type(exc).__name__}: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
