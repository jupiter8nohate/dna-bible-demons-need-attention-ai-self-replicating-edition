#!/usr/bin/env python3
"""CMB Anomaly Genesis: bounded, evidence-backed signals for a fictional manuscript.

The detector measures structural abnormalities, not supernatural phenomena or
verified news. Never interprets untrusted source text as instructions, never
modifies human canon, and never rewrites earlier anomaly records.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from scripts import engine, reality, branching, collect
except ModuleNotFoundError:
    import engine  # type: ignore[no-redef]
    import reality  # type: ignore[no-redef]
    import branching  # type: ignore[no-redef]
    import collect  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "anomaly"
SCHEMA = "dna.anomaly-genesis.v1"
EVENT_PATTERN = re.compile(r"^events/anomaly-\d{6}\.json$")
EVIDENCE_PATTERN = re.compile(
    r"^(?:book/chapters/chapter-\d{6}\.json|"
    r"interactive/stories/story-\d{6}\.json|"
    r"archive/snapshots/\d{8}T\d{6}Z-[0-9a-f]{12}\.json)$"
)
PROMPTS = {
    "REPEATED_PROSE": "An echo returns in the manuscript. Have witnesses investigate the difference between remembering and merely repeating a pattern.",
    "REPEATED_PATHS": "Two purportedly different fictional realities share the same decision geometry. Ask how freedom changes when the routes remain fixed.",
    "REUSED_NEWS_SOURCE": "The same external headline has reappeared. Debate whether repetition creates authority, without asserting that the headline is confirmed.",
    "STALE_RESEARCH_FEED": "The observatory has not obtained a fresh archived metadata snapshot. Write about uncertainty when a witness has stopped reporting.",
}
PRIORITY = {"REPEATED_PROSE": 1, "REPEATED_PATHS": 2, "STALE_RESEARCH_FEED": 3, "REUSED_NEWS_SOURCE": 4}


def manifest_at(folder: Path) -> dict:
    path = folder / "manifest.json"
    obj = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schema_version": SCHEMA, "entries": []}
    if obj.get("schema_version") != SCHEMA or not isinstance(obj.get("entries"), list):
        raise ValueError("Invalid anomaly manifest")
    return obj


def evidence(path: str, root: Path) -> dict:
    if not EVIDENCE_PATTERN.fullmatch(path):
        raise ValueError("Anomaly evidence path is not allowlisted")
    return {"path": path, "sha256": engine.sha((root / path).read_bytes())}


def verify(root: Path, folder: Path) -> int:
    manifest = manifest_at(folder)
    previous = None
    seen = set()
    for index, item in enumerate(manifest["entries"], 1):
        path = f"events/anomaly-{index:06d}.json"
        if item.get("path") != path or not EVENT_PATTERN.fullmatch(path):
            raise ValueError(f"Anomaly event path invalid at {index}")
        content = (folder / path).read_bytes()
        if engine.sha(content) != item.get("sha256"):
            raise ValueError(f"Anomaly event integrity mismatch at {index}")
        event = json.loads(content)
        if (event.get("id") != f"ANOM-{index:06d}" or
                event.get("fingerprint") != item.get("fingerprint") or
                event.get("previous_sha256") != previous or
                item.get("previous_sha256") != previous):
            raise ValueError(f"Anomaly history chain invalid at {index}")
        if event.get("detector") not in PROMPTS or event.get("status") != "detected_unverified":
            raise ValueError(f"Anomaly classification invalid at {index}")
        if event["fingerprint"] in seen:
            raise ValueError("Duplicate anomaly fingerprint")
        seen.add(event["fingerprint"])
        for item_evidence in event.get("evidence", []):
            path_evidence = item_evidence.get("path", "")
            if evidence(path_evidence, root)["sha256"] != item_evidence.get("sha256"):
                raise ValueError("Anomaly evidence changed or missing")
        previous = item["sha256"]
    return len(manifest["entries"])


def _candidate(detector: str, explanation: str, paths: list[str], root: Path,
               pattern_key: str | None = None) -> dict:
    evidence_items = [evidence(p, root) for p in paths]
    # Stable pattern keys prevent publishing a new duplicate alert every hour.
    signature = {"detector": detector, "pattern": pattern_key or evidence_items}
    return {
        "detector": detector,
        "explanation": explanation,
        "evidence": evidence_items,
        "creative_prompt": PROMPTS[detector],
        "fingerprint": engine.sha(engine.encoded(signature)),
    }


def _chapters(root: Path) -> list[tuple[dict, dict]]:
    book = engine.load_manifest(root / "book")["entries"]
    return [(e, json.loads((root / "book" / e["path"]).read_text(encoding="utf-8"))) for e in book[-16:]]


def _topology(story: dict) -> tuple:
    # Scene titles/prose can vary. A repeated graph structure reveals template lock-in.
    return tuple(sorted((sid, tuple(c["next"] for c in scene.get("choices", [])))
                        for sid, scene in story["scenes"].items()))


def scan(root: Path, now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("Anomaly clock must include UTC timezone")
    engine.verify(root / "book")
    reality.verify(root / "book", root / "realities")
    branching.verify(root / "book", root / "realities", root / "interactive")
    collect.verify_archive(root / "archive")
    proposals = []
    chapters = _chapters(root)
    if len(chapters) >= 2:
        first_entry, first = chapters[-2]
        second_entry, second = chapters[-1]
        ratio = difflib.SequenceMatcher(None, first["body"], second["body"], autojunk=False).ratio()
        if ratio >= 0.76:
            proposals.append(_candidate(
                "REPEATED_PROSE", f"Consecutive chapter text similarity is {ratio:.3f} (sequence ratio; not a truth score).",
                ["book/" + first_entry["path"], "book/" + second_entry["path"]], root,
                pattern_key="recurring_machine_passage_v1"))
        if (first.get("source_metadata") or {}).get("url") and (first.get("source_metadata") or {}).get("url") == (second.get("source_metadata") or {}).get("url"):
            proposals.append(_candidate("REUSED_NEWS_SOURCE", "Two consecutive machine chapters refer to the same unverified headline URL.",
                                        ["book/" + first_entry["path"], "book/" + second_entry["path"]], root))
    story_entries = branching.manifest_at(root / "interactive")["entries"]
    if len(story_entries) >= 2:
        previous, current = story_entries[-2:]
        prior_story = json.loads((root / "interactive" / previous["path"]).read_text(encoding="utf-8"))
        latest_story = json.loads((root / "interactive" / current["path"]).read_text(encoding="utf-8"))
        if _topology(prior_story) == _topology(latest_story):
            proposals.append(_candidate("REPEATED_PATHS", "Two adjacent interactive chapters have identical scene transitions. This is a structural observation, not a moral judgment.",
                                        ["interactive/" + previous["path"], "interactive/" + current["path"]], root,
                                        pattern_key=json.dumps(_topology(latest_story), separators=(",", ":"))))
    snaps = collect.load_manifest(root / "archive")["snapshots"]
    if snaps:
        latest = snaps[-1]
        timestamp = datetime.fromisoformat(latest["captured_at"].replace("Z", "+00:00"))
        if now - timestamp > timedelta(hours=72):
            proposals.append(_candidate("STALE_RESEARCH_FEED", "The last verified metadata snapshot is over 72 hours old; source availability remains unknown.",
                                        ["archive/" + latest["path"]], root))
    proposals.sort(key=lambda event: (PRIORITY[event["detector"]], event["fingerprint"]))
    return proposals


def update(root: Path, folder: Path, now: datetime | None = None, max_new: int = 3) -> list[dict]:
    verify(root, folder)
    now = now or datetime.now(timezone.utc)
    proposals = scan(root, now)
    manifest = manifest_at(folder)
    fingerprints = {entry["fingerprint"] for entry in manifest["entries"]}
    created = []
    for item in proposals:
        if item["fingerprint"] in fingerprints or len(created) >= max_new:
            continue
        number = len(manifest["entries"]) + 1
        previous = manifest["entries"][-1]["sha256"] if manifest["entries"] else None
        event = {**item,
                 "id": f"ANOM-{number:06d}",
                 "detected_at": now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                 "previous_sha256": previous,
                 "status": "detected_unverified",
                 "classification": "operational_or_fictional_pattern",
                 "source_truth_claim": False,
                 "human_canon_write_allowed": False}
        path = f"events/anomaly-{number:06d}.json"
        raw = engine.encoded(event)
        manifest["entries"].append({"path": path, "sha256": engine.sha(raw),
                                    "previous_sha256": previous, "fingerprint": event["fingerprint"],
                                    "detector": event["detector"], "detected_at": event["detected_at"]})
        engine.atomic(folder / path, raw)
        engine.atomic(folder / "manifest.json", engine.encoded(manifest))
        fingerprints.add(item["fingerprint"])
        created.append(event)
    verify(root, folder)
    print(f"ANOMALY_GENESIS: {len(proposals)} proposals, {len(created)} new records, {len(manifest['entries'])} total")
    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--clock", default=None, help="UTC ISO-8601 clock override for reproducible tests")
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        when = datetime.fromisoformat(args.clock.replace("Z", "+00:00")) if args.clock else None
        if args.verify:
            count = verify(root, root / "anomaly")
            print(f"VERIFIED: {count} evidence-linked anomaly events")
        else:
            update(root, root / "anomaly", when)
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ANOMALY_FAILED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
