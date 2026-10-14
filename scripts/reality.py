#!/usr/bin/env python3
"""Append original reality-world overlays to the D.N.A. machine testament.

The worlds borrow broad philosophical mechanisms, never movie characters or plots.
They never write to the human-authored canon or treat fictional events as news.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
REALITIES = ROOT / "realities"

# Each lens corresponds to a mechanism, not a licensed adaptation.
LENSES = (
    ("CLOCK_WITHOUT_MIDNIGHT", "The Unfinished Hour", "time resets and persistent memory", "What survives when the surrounding world forgets?", "Ecclesiastes 3:1", "The bells erase the city's calendar, but the witnesses retain their questions."),
    ("MIRROR_OF_CONSENT", "The Mirror of Consent", "constructed consensus and chosen truth", "Who has the authority to certify what another person experiences?", "John 8:32", "The mirrors agree on one face; the person chooses a different name."),
    ("NESTED_GARDEN", "The Garden of Inner Worlds", "nested levels of invented experience", "Can a convincing simulation demand obedience?", "1 Thessalonians 5:21", "A doorway opens inside another doorway, each carrying a different rulebook."),
    ("RECURSIVE_CITY", "The City Beneath the City", "observers inside a modeled world", "Does describing a world grant the right to govern its inhabitants?", "Proverbs 18:13", "The city's map contains a second map drawn by someone who never entered."),
    ("SEED_OF_INTENTION", "The Seed That Refused Its Gardener", "suggestion, influence and independent judgment", "When does persuasion become the theft of a decision?", "Romans 12:2", "A thought arrives like a seed; the witness chooses whether it grows."),
    ("ECHO_OF_TOMORROW", "The Replay That Cannot Convict", "repeated scenarios and counterfactual investigation", "Can replaying a possibility establish what truly occurred?", "Deuteronomy 19:15", "The same event is rehearsed in a hundred lanterns, none a witness by itself."),
    ("UNWRITTEN_MEMORY", "The Archive of Unwritten Memories", "memory uncertainty and identity", "Is a remembered image equivalent to an authenticated event?", "Proverbs 14:15", "The archive returns a beautiful memory without a trustworthy origin."),
    ("MASKS_OF_THE_LEDGER", "The Ledger of Borrowed Names", "identity theft and profiling", "Who can challenge the identity a system assigns?", "1 Samuel 16:7", "Every traveler receives a profile, but one refuses the borrowed mask."),
    ("GAME_OF_REFUSAL", "The Rules of the Unconsenting Player", "games, consent and hidden rule changes", "Can a decision be free if the rules are concealed?", "Galatians 5:1", "A game begins before its players are told they may decline."),
    ("FLOOR_OF_WITNESSES", "The Thirteenth Witness", "uncertain simulation boundaries", "What evidence distinguishes observer from model?", "1 Corinthians 13:12", "The witness finds an upper floor where all the lower floors are stories."),
    ("SENSORY_ECHO", "The Room of Borrowed Senses", "recorded perception and contested testimony", "Does a recording capture the meaning of an experience?", "James 1:19", "A borrowed sensation is replayed without the life around it."),
    ("CASTE_OF_PREDICTIONS", "The Child Outside the Forecast", "genetic and statistical determinism", "Can any predicted future eliminate a person's right to choose?", "Jeremiah 1:5", "The registry predicts every road but cannot predict the first refusal."),
)
DECISIONS = (
    ("Question the system", "A new objection is entered into the witness ledger. No authority is automatically transferred."),
    ("Protect the human", "The chapter establishes a consent boundary that the simulated institution must respect."),
    ("Follow the anomaly", "The inquiry opens another interpretive layer without claiming that fiction is evidence."),
)
SCHEMA = "dna.reality-engine.v1"
PATH = re.compile(r"^worlds/realm-[0-9]{6}\.json$")


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".dna-reality-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def manifest_at(folder: Path) -> dict:
    path = folder / "manifest.json"
    obj = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schema_version": SCHEMA, "entries": []}
    if obj.get("schema_version") != SCHEMA or not isinstance(obj.get("entries"), list):
        raise ValueError("Invalid reality manifest")
    return obj


def source_book(folder: Path) -> list[dict]:
    path = folder / "manifest.json"
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema_version") != "dna.machine-testament.v1" or not isinstance(obj.get("entries"), list):
        raise ValueError("Invalid source book manifest")
    return obj["entries"]


def verify(book: Path, realms: Path) -> int:
    entries = source_book(book)
    world_entries = manifest_at(realms)["entries"]
    if len(world_entries) > len(entries):
        raise ValueError("Reality manifest contains nonexistent chapters")
    previous = None
    for n, record in enumerate(world_entries, 1):
        chapter_record = entries[n - 1]
        expected_path = f"worlds/realm-{n:06d}.json"
        if record.get("path") != expected_path or not PATH.fullmatch(record["path"]):
            raise ValueError(f"Unsafe or nonsequential world path at {n}")
        if record.get("previous_sha256") != previous:
            raise ValueError(f"Broken world chain at {n}")
        if record.get("chapter_sha256") != chapter_record.get("sha256"):
            raise ValueError(f"World no longer agrees with chapter {n}")
        chapter_bytes = (book / chapter_record["path"]).read_bytes()
        if digest(chapter_bytes) != chapter_record.get("sha256"):
            raise ValueError(f"Source chapter failed integrity at {n}")
        content = (realms / expected_path).read_bytes()
        if digest(content) != record.get("sha256"):
            raise ValueError(f"World failed integrity at {n}")
        world = json.loads(content)
        if world.get("chapter") != n or world.get("fictional") is not True:
            raise ValueError(f"World schema content mismatch at {n}")
        if world.get("source_chapter_sha256") != record.get("chapter_sha256"):
            raise ValueError(f"World chapter reference mismatch at {n}")
        if world.get("previous_world_sha256") != previous:
            raise ValueError(f"World self-chain mismatch at {n}")
        if len(world.get("reader_choices", [])) != 3:
            raise ValueError(f"World requires three distinct reader choices at {n}")
        previous = record["sha256"]
    return len(world_entries)


def make_world(n: int, chapter: dict, chapter_hash: str, previous_record: dict | None, previous_world: dict | None) -> dict:
    key, name, mechanic, question, passage_ref, scene = LENSES[(n - 1) % len(LENSES)]
    cycle = (n - 1) // len(LENSES) + 1
    echo = previous_world["open_question"] if previous_world else "What would remain of an identity if every label disappeared?"
    return {
        "schema_version": SCHEMA,
        "chapter": n,
        "chapter_date": chapter["date"],
        "fictional": True,
        "source_chapter_sha256": chapter_hash,
        "previous_world_sha256": previous_record["sha256"] if previous_record else None,
        "lens_id": key,
        "world_name": name,
        "cycle": cycle,
        "mechanic": mechanic,
        "scene": scene,
        "narrative": (f"Cycle {cycle} of the D.N.A. Reality Engine. {scene} "
                      f"The record from the previous world still asks: {echo} "
                      "No observer may turn a simulated identity into a human verdict."),
        "open_question": question,
        "scriptural_reference": passage_ref,
        "theological_status": "question_for_study_not_doctrinal_answer",
        "reference_resource": "https://www.gotquestions.org/",
        "source_status": "fiction_inspired_by_broad_themes_not_an_adaptation",
        "reader_choices": [{"id": f"{key}-{i}", "label": label, "fictional_consequence": result}
                           for i, (label, result) in enumerate(DECISIONS, 1)],
        "agency": "Reader branches are private to the current browser and never modify the shared canon.",
    }


def extend(book: Path, realms: Path) -> int:
    try:
        from scripts.engine import verify as verify_chapters
    except ModuleNotFoundError:
        from engine import verify as verify_chapters
    verify_chapters(book)
    verify(book, realms)
    chapters = source_book(book)
    manifest = manifest_at(realms)
    new_count = 0
    previous_world = None
    if manifest["entries"]:
        previous_world = json.loads((realms / manifest["entries"][-1]["path"]).read_text(encoding="utf-8"))
    for n in range(len(manifest["entries"]) + 1, len(chapters) + 1):
        source = chapters[n - 1]
        chapter = json.loads((book / source["path"]).read_text(encoding="utf-8"))
        previous_record = manifest["entries"][-1] if manifest["entries"] else None
        world = make_world(n, chapter, source["sha256"], previous_record, previous_world)
        path = f"worlds/realm-{n:06d}.json"
        record = {
            "chapter": n,
            "path": path,
            "sha256": digest(canonical(world)),
            "chapter_sha256": source["sha256"],
            "previous_sha256": previous_record["sha256"] if previous_record else None,
            "lens_id": world["lens_id"],
        }
        atomic_write(realms / path, canonical(world))
        manifest["entries"].append(record)
        atomic_write(realms / "manifest.json", canonical(manifest))
        previous_world = world
        new_count += 1
    verify(book, realms)
    return new_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book-dir", type=Path, default=BOOK)
    parser.add_argument("--realities-dir", type=Path, default=REALITIES)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        count = verify(args.book_dir, args.realities_dir) if args.verify else extend(args.book_dir, args.realities_dir)
        print(f"REALITY_ENGINE: {count} {'worlds verified' if args.verify else 'new worlds appended'}")
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"REALITY_ENGINE_FAILED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
