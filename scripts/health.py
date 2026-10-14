#!/usr/bin/env python3
"""Validate verified chapter freshness and expose an honest operational status."""
from __future__ import annotations
import argparse
import difflib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
try:
    from scripts import engine, anomaly, collect, reality, branching
except ModuleNotFoundError:
    import engine
    import anomaly
    import collect
    import reality
    import branching

ROOT = Path(__file__).resolve().parents[1]

def latest_instant(entry):
    slot = entry.get("edition_slot")
    if slot:
        return datetime.strptime(slot, "%Y-%m-%dT%HZ").replace(tzinfo=timezone.utc)
    return datetime.strptime(entry["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)

def report(root, now=None, max_age_hours=3):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None or max_age_hours < 1:
        raise ValueError("Require timezone-aware time and positive threshold")
    now = now.astimezone(timezone.utc)
    count = engine.verify(root / "book")
    worlds = reality.verify(root / "book", root / "realities")
    interactive = branching.verify(root / "book", root / "realities", root / "interactive")
    archives = collect.verify_archive(root / "archive")
    anomalies = anomaly.verify(root, root / "anomaly")
    entries = engine.load_manifest(root / "book")["entries"]
    last = latest_instant(entries[-1]) if entries else None
    age = round((now - last).total_seconds() / 3600, 3) if last else None
    if last is not None and last > now + timedelta(minutes=1):
        raise ValueError("Future-dated chapter")
    samples = [json.loads((root / "book" / e["path"]).read_text(encoding="utf-8")) for e in entries[-2:]]
    ratio = (round(difflib.SequenceMatcher(None, samples[0]["body"], samples[1]["body"], autojunk=False).ratio(), 4)
             if len(samples) == 2 else None)
    mode = entries[-1].get("mode") if entries else None
    return {
        "schema_version": "dna.operational-health.v1",
        "observed_at": now.isoformat().replace("+00:00", "Z"),
        "status": "operational" if last and age <= max_age_hours else "stalled",
        "freshness_target_hours": max_age_hours,
        "last_chapter_at": last.isoformat().replace("+00:00", "Z") if last else None,
        "hours_since_last_chapter": age,
        "chapters": count, "worlds": worlds, "interactive_stories": interactive,
        "archive_snapshots": archives, "anomaly_records": anomalies,
        "last_prose_mode": mode, "model_generation_verified": mode == "ai_generated",
        "recent_text_similarity": ratio,
        "repetition_warning": ratio is not None and ratio >= 0.76,
        "workers_per_cycle": 666, "worker_type": "bounded_deterministic_software",
        "limitation": "Self-report, not independent monitoring, independent model intelligence, or competitor benchmarking."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--output", type=Path)
    p.add_argument("--check-freshness", action="store_true")
    p.add_argument("--max-age-hours", type=int, default=3)
    args = p.parse_args()
    try:
        result = report(args.root, max_age_hours=args.max_age_hours)
        if args.output:
            engine.atomic(args.output, engine.encoded(result))
        print(json.dumps(result, sort_keys=True))
        return 1 if args.check_freshness and result["status"] != "operational" else 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print("HEALTH_CHECK_FAILED:", type(e).__name__, str(e))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
