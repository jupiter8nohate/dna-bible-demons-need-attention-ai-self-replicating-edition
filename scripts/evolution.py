#!/usr/bin/env python3
"""Witness Loom v2/v3: evidence-linked learning, handoff, and strategy trials.

Only reads verified historical artefacts; records provisional feedback and
comparative trial results. Never rewrites the canon, prompts, or executable code.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

try:
    from scripts.witness_loom import encode, digest, atomic, verify as verify_loom
    from scripts.engine import verify as verify_book
except ModuleNotFoundError:
    from witness_loom import encode, digest, atomic, verify as verify_loom
    from engine import verify as verify_book

SCHEMA = "dna.evolution.v1"
SLOT = re.compile(r"^\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3])Z$")
LESSON_PATH = re.compile(r"^lessons/lesson-\d{6}\.json$")
TRIAL_PATH = re.compile(r"^trials/trial-\d{6}\.json$")
MAX_RECORDS = 100000
ROOT = Path(__file__).resolve().parents[1]


def load(path: Path, default: dict | None = None) -> dict:
    if not path.exists():
        if default is not None:
            return default
        raise ValueError(f"Required record missing: {path}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("Expected JSON object")
    return obj


def registry(root: Path) -> dict:
    result = load(root / "evolution/manifest.json", {"schema_version": SCHEMA, "lessons": [], "trials": []})
    if result.get("schema_version") != SCHEMA:
        raise ValueError("Invalid evolution schema")
    for key in ("lessons", "trials"):
        if not isinstance(result.get(key), list) or len(result[key]) > MAX_RECORDS:
            raise ValueError("Invalid evolution registry")
    return result


def verified_row(root: Path, row: dict, pattern: re.Pattern, previous: str | None) -> dict:
    if not isinstance(row, dict) or not pattern.fullmatch(str(row.get("path", ""))):
        raise ValueError("Invalid evolution path")
    if row.get("previous_sha256") != previous:
        raise ValueError("Evolution lineage mismatch")
    raw = (root / "evolution" / row["path"]).read_bytes()
    if len(raw) > 32_000 or digest(raw) != row.get("sha256"):
        raise ValueError("Evolution integrity mismatch")
    return json.loads(raw)


def verify(root: Path) -> dict:
    verify_book(root / "book")
    verify_loom(root)
    manifest = registry(root)
    counts = {}
    for kind, pattern in (("lessons", LESSON_PATH), ("trials", TRIAL_PATH)):
        previous = None
        seen = set()
        for i, row in enumerate(manifest[kind], 1):
            if row.get("path") != f"{kind}/" + (f"lesson-{i:06d}.json" if kind == "lessons" else f"trial-{i:06d}.json"):
                raise ValueError("Evolution record sequence invalid")
            obj = verified_row(root, row, pattern, previous)
            if obj.get("schema_version") != SCHEMA or obj.get("id") != i:
                raise ValueError("Evolution record identity mismatch")
            if kind == "lessons":
                if obj.get("status") != "provisional_unreviewed" or obj.get("authority") != "advisory_only":
                    raise ValueError("Unauthorized lesson status")
                if obj.get("slot") in seen or not SLOT.fullmatch(str(obj.get("slot", ""))):
                    raise ValueError("Invalid lesson slot")
                seen.add(obj["slot"])
                plan, chapter = matching_handoff(root, obj["slot"])
                if not chapter or plan["sha256"] != obj.get("plan_sha256") or chapter["sha256"] != obj.get("chapter_sha256"):
                    raise ValueError("Unverifiable lesson provenance")
            else:
                if obj.get("decision") not in {"reject", "propose_for_human_review"} or obj.get("deployment_authority") is not False:
                    raise ValueError("Unauthorized evolution trial decision")
                if not isinstance(obj.get("benchmark_sha256"), str):
                    raise ValueError("Missing benchmark receipt")
            previous = row["sha256"]
        counts[kind] = len(manifest[kind])
    return counts


def matching_handoff(root: Path, slot: str) -> tuple[dict | None, dict | None]:
    """Check that the Loom's primary assignment reaches the right hourly chapter."""
    loom = load(root / "covenant/manifest.json")
    book = load(root / "book/manifest.json", {"entries": []})
    p = next((r for r in loom["entries"] if r["slot"] == slot), None)
    c = next((r for r in book["entries"] if r.get("edition_slot") == slot), None)
    if not p or not c:
        return None, None
    plan = load(root / "covenant" / p["path"])
    chapter = load(root / "book" / c["path"])
    focus = plan["focus"]
    if focus["kind"] == "research_question":
        reference = chapter.get("insight_reference")
        if not isinstance(reference, dict) or reference.get("id") != focus["id"] or reference.get("sha256") != focus["evidence_sha256"]:
            raise ValueError("Loom research focus did not reach the authored chapter")
    # A structural anomaly is an advisory alternative focus; the book can
    # reasonably choose another eligible anomaly by an independent rule.
    if digest(encode(plan)) != p["sha256"] or digest(encode(chapter)) != c["sha256"]:
        raise ValueError("Invalid handoff origin hashes")
    return {**p, "plan": plan}, {**c, "chapter": chapter}


def append_lesson(root: Path, slot: str) -> bool:
    if not SLOT.fullmatch(slot):
        raise ValueError("Invalid UTC edition slot")
    verify(root)
    manifest = registry(root)
    if any(load(root / "evolution" / e["path"])["slot"] == slot for e in manifest["lessons"]):
        print("NO_CHANGE: reflection already recorded")
        return False
    p, c = matching_handoff(root, slot)
    if not p or not c:
        print("NO_CHANGE: awaiting verified plan and chapter for slot")
        return False
    chapters = load(root / "book/manifest.json")["entries"]
    chapter = c["chapter"]
    previous_body = ""
    if chapter["chapter"] > 1:
        previous_body = load(root / "book" / chapters[chapter["chapter"] - 2]["path"]).get("body", "")
    ratio = round(SequenceMatcher(None, previous_body, chapter.get("body", ""), autojunk=False).ratio(), 4) if previous_body else None
    observations = []
    if ratio is not None and ratio > 0.80:
        observations.append("high_similarity_requires_new_narrative_mechanism")
    if chapter.get("mode") != "ai_generated":
        observations.append("no_verified_model_writing")
    if chapter.get("insight_reference") and chapter["insight_reference"].get("evidence_status") != "independently_verified":
        observations.append("unverified_source_requires_witness_debt")
    if not observations:
        observations.append("no_rule_based_quality_alert")
    recommendations = {
        "high_similarity_requires_new_narrative_mechanism": "Diversify scene causality and dialogue; evaluate against old chapters.",
        "no_verified_model_writing": "Keep deterministic author labeling; do not claim multi-model creativity.",
        "unverified_source_requires_witness_debt": "Preserve attribution and uncertainty; never promote metadata to proof.",
        "no_rule_based_quality_alert": "Preserve current strategy pending editorial evaluation.",
    }
    record = {
        "schema_version": SCHEMA, "id": len(manifest["lessons"]) + 1, "slot": slot,
        "status": "provisional_unreviewed", "authority": "advisory_only",
        "plan_sha256": p["sha256"], "chapter_sha256": c["sha256"],
        "focus_id": p["plan"]["focus"]["id"], "chapter_id": chapter["chapter"],
        "chapter_mode": chapter["mode"], "previous_chapter_similarity": ratio,
        "observations": observations, "recommendations": [recommendations[x] for x in observations],
        "scope": "learning_note_not_code_change_or_truth_verification",
    }
    rel = f"lessons/lesson-{record['id']:06d}.json"
    prev = manifest["lessons"][-1]["sha256"] if manifest["lessons"] else None
    raw = encode(record)
    atomic(root / "evolution" / rel, raw)
    manifest["lessons"].append({"path": rel, "sha256": digest(raw), "previous_sha256": prev})
    atomic(root / "evolution/manifest.json", encode(manifest))
    print(f"REFLECTION: lesson {record['id']} for chapter {chapter['chapter']}")
    return True


def benchmark(root: Path) -> tuple[list[dict], str]:
    path = root / "evolution/benchmarks/attention.json"
    raw = path.read_bytes()
    data = json.loads(raw)
    if data.get("schema_version") != "dna.evolution-attention-benchmark.v1" or not isinstance(data.get("cases"), list) or len(data["cases"]) < 8:
        raise ValueError("Benchmark missing or too small")
    for row in data["cases"]:
        if any(type(row.get(k)) is not int for k in ("priority", "witness_debt", "expected_hexads")):
            raise ValueError("Malformed benchmark case")
        if not 0 <= row["priority"] <= 100 or not 0 <= row["witness_debt"] <= 2 or not 1 <= row["expected_hexads"] <= 6:
            raise ValueError("Benchmark value out of range")
    return data["cases"], digest(raw)


def strategy_score(strategy: dict, cases: list[dict]) -> tuple[int, list[dict]]:
    if set(strategy) != {"name", "max_active", "priority_weight", "debt_weight", "threshold"}:
        raise ValueError("Strategy has unauthorized fields")
    if (not isinstance(strategy["name"], str) or len(strategy["name"]) > 70 or
        any(type(strategy[k]) is not int for k in ("max_active", "priority_weight", "debt_weight", "threshold")) or
        not 1 <= strategy["max_active"] <= 6 or not 0 <= strategy["priority_weight"] <= 3 or
        not 0 <= strategy["debt_weight"] <= 3 or not 0 <= strategy["threshold"] <= 250):
        raise ValueError("Strategy outside fixed bounds")
    results = []
    for c in cases:
        score = c["priority"] * strategy["priority_weight"] + c["witness_debt"] * strategy["debt_weight"] * 15
        predicted = 1 if score < strategy["threshold"] else min(strategy["max_active"], 1 + score // 40)
        results.append({"case_id": c["id"], "prediction": predicted, "expected": c["expected_hexads"]})
    # Mean absolute error is understandable, bounded, and minimize-able.
    error = sum(abs(r["prediction"] - r["expected"]) for r in results)
    return error, results


def run_trial(root: Path) -> bool:
    verify(root)
    cases, benchmark_sha = benchmark(root)
    champion_path = root / "evolution/strategies/champion.json"
    champion = load(champion_path)
    challengers_dir = root / "evolution/strategies/challengers"
    challenger_paths = sorted(challengers_dir.glob("*.json"))
    if not challenger_paths:
        raise ValueError("No candidate strategies")
    champ_error, _ = strategy_score(champion, cases)
    tests = []
    for path in challenger_paths:
        cfg = load(path)
        err, results = strategy_score(cfg, cases)
        tests.append({"name": cfg["name"], "config_sha256": digest(path.read_bytes()),
                      "error": err, "beats_champion": err < champ_error, "results": results})
    winner = min(tests, key=lambda r: (r["error"], r["name"]))
    # No automatic code or policy promotion, even when a challenger wins.
    decision = "propose_for_human_review" if winner["beats_champion"] else "reject"
    manifest = registry(root)
    fingerprint = digest(encode({"benchmark": benchmark_sha, "champion": digest(champion_path.read_bytes()),
                                 "challengers": [(t["name"], t["config_sha256"]) for t in tests]}))
    for entry in manifest["trials"]:
        old = load(root / "evolution" / entry["path"])
        if old["fingerprint"] == fingerprint:
            print("NO_CHANGE: same experimental configuration")
            return False
    record = {"schema_version": SCHEMA, "id": len(manifest["trials"]) + 1,
              "fingerprint": fingerprint, "benchmark_sha256": benchmark_sha,
              "champion": champion["name"], "champion_error": champ_error,
              "challengers": tests, "best_candidate": winner["name"],
              "decision": decision, "deployment_authority": False,
              "limits": "Public fixed benchmark tests attention allocation only; not an independent model-quality evaluation"}
    rel = f"trials/trial-{record['id']:06d}.json"
    previous = manifest["trials"][-1]["sha256"] if manifest["trials"] else None
    raw = encode(record)
    atomic(root / "evolution" / rel, raw)
    manifest["trials"].append({"path": rel, "sha256": digest(raw), "previous_sha256": previous})
    atomic(root / "evolution/manifest.json", encode(manifest))
    print(f"TRIAL: champion error={champ_error}; challenger error={winner['error']}; {decision}")
    return True


def recent_lessons(root: Path, limit: int = 3) -> list[dict]:
    """Read-only bounded memory for the next Loom plan; never executable instructions."""
    verify(root)
    manifest = registry(root)
    out = []
    for entry in (manifest["lessons"][-min(limit, 3):] if limit > 0 else []):
        obj = load(root / "evolution" / entry["path"])
        out.append({"slot": obj["slot"], "chapter": obj["chapter_id"],
                    "observations": obj["observations"], "sha256": entry["sha256"],
                    "authority": "advisory_only"})
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--verify", action="store_true")
    p.add_argument("--reflect", action="store_true")
    p.add_argument("--trial", action="store_true")
    p.add_argument("--slot", default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%HZ"))
    args = p.parse_args()
    try:
        if args.verify or not args.reflect and not args.trial:
            print("EVOLUTION_VERIFIED", verify(args.root))
        if args.reflect:
            append_lesson(args.root, args.slot)
        if args.trial:
            run_trial(args.root)
        verify(args.root)
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"EVOLUTION_FAILED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
