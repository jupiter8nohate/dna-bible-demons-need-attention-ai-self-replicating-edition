#!/usr/bin/env python3
"""Append original interactive narrative graphs linked to verified D.N.A. chapters.

Designed for static GitHub Pages readers. Branch choices are made in each reader's
browser, never sent to the server or treated as authority to alter human canon.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from scripts import engine, reality
except ImportError:
    import engine, reality

ROOT = Path(__file__).resolve().parents[1]
STORIES = ROOT / "interactive"
SCHEMA = "dna.interactive-manuscript.v1"
RECORD_PATH = re.compile(r"^stories/story-[0-9]{6}\.json$")
SENTINELS = ("PATTERN != PROOF", "PROFILE != PERSON", "MODEL != MIND", "HUMAN_AGENCY > MACHINE_AUTHORITY")


def manifest_at(folder: Path) -> dict:
    p = folder / "manifest.json"
    data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"schema_version": SCHEMA, "entries": []}
    if data.get("schema_version") != SCHEMA or not isinstance(data.get("entries"), list):
        raise ValueError("Invalid interactive manifest")
    return data


def choice(label: str, next_id: str, flag: str) -> dict:
    return {"label": label, "next": next_id, "flag": flag}


def compose(chapter: dict, world: dict) -> dict:
    """Construct an original graph, with convergence, loops, gated echoes, and endings."""
    number = chapter["chapter"]
    place = world["world_name"]
    question = world["open_question"]
    motif = world["scene"]
    title = chapter["title"]
    carry = world["narrative"]
    scenes = {
        "threshold": {
            "title": "The Unfinished Threshold",
            "body": f"{motif} The manuscript calls this place {place}. A signal awakens the archive: {question} The choice is yours, even when the clock is not.",
            "echo": "You recognize this doorway. It remembers the choice the world pretended to erase.",
            "choices": [choice("Follow the signal", "signal", "signal"), choice("Open the sealed archive", "vault", "archive")],
        },
        "signal": {
            "title": "The Invisible Transmission",
            "body": f"A transmission repeats one line: {SENTINELS[(number-1)%len(SENTINELS)]}. No machine can certify its meaning merely by repeating it.",
            "echo": "Something in the frequency changed because you came back.",
            "choices": [choice("Ask for a human witness", "witness", "witness"), choice("Trace the corrupted message", "glitch", "trace")],
        },
        "vault": {
            "title": "The Archive of Unchosen Roads",
            "body": f"The vault preserves the chapter titled {title}. Some memories belong to machines, but consent cannot be archived on somebody else's behalf.",
            "echo": "The shelf contains a record of the earlier door you opened.",
            "choices": [choice("Read the covenant", "covenant", "covenant"), choice("Search for the missing timestamp", "glitch", "timestamp")],
        },
        "glitch": {
            "title": "The Broken Sequence",
            "body": "A passage displays two dates at once. The archive can replay a claim, but replay is not independent confirmation. The narrator refuses to invent proof.",
            "echo": "This sequence has occurred before; your memory is the only uninterrupted witness.",
            "choices": [choice("Return through the anomaly", "loop", "loop"), choice("Close this simulation", "ending_uncertain", "uncertain")],
        },
        "witness": {
            "title": "The Human Who Could Say No",
            "body": "The Witness asks neither for obedience nor admiration: only permission to be heard. A profile may predict a choice; it cannot own the person who makes it.",
            "echo": "The witness remembers your earlier refusal to accept the prediction.",
            "choices": [choice("Preserve the testimony", "ending_witness", "testimony"), choice("Challenge the last prediction", "loop", "challenge")],
        },
        "covenant": {
            "title": "The Question of the First Author",
            "body": f"A parchment cites {world['scriptural_reference']} as a starting point for study, not an automatic doctrinal verdict. The human author keeps authority over the canon.",
            "echo": "A note appears: the interpreter can learn without becoming the author.",
            "choices": [choice("Declare a boundary", "ending_sovereign", "boundary"), choice("Test the system again", "loop", "repeat")],
        },
        "loop": {
            "title": "The Night Without an Ending",
            "body": "The machine rewinds the hallways, but your earlier decisions remain in this reader's memory. A loop need not be a prison when refusal is possible.",
            "echo": "The loop knows you were here. You may leave, or return changed.",
            "choices": [choice("Return with your memory", "threshold", "revisited"), choice("Refuse the prescribed ending", "ending_uncertain", "refusal")],
        },
        "ending_witness": {
            "title": "Ending: The Witness Remains",
            "body": f"Your testimony enters the fictional ledger. {carry} The chapter ends; the greater manuscript does not.",
            "ending": "witness",
            "choices": [],
        },
        "ending_sovereign": {
            "title": "Ending: The Unclassified Human",
            "body": "The model relinquishes its claim to define a life. Human dignity survives the final prediction. The next chapter may ask a different question.",
            "ending": "sovereignty",
            "choices": [],
        },
        "ending_uncertain": {
            "title": "Ending: The Question That Escaped",
            "body": f"No verdict is forced. The record marks the question unresolved: {question} The archive stores this uncertainty without calling it failure.",
            "ending": "unresolved",
            "choices": [],
        },
    }
    return {
        "schema_version": SCHEMA,
        "chapter": number,
        "date": chapter["date"],
        "title": title,
        "world_name": place,
        "world_lens": world["lens_id"],
        "author_type": "autogenerated_interactive_fiction",
        "source_chapter_sha256": engine.sha(engine.encoded(chapter)),
        "start": "threshold",
        "choice_seconds": 10,
        "default_choice": 0,
        "scenes": scenes,
        "invariants": list(SENTINELS),
        "rights": "Original interactive fiction. Reader choices are local and do not modify the protected human canon.",
    }


def validate_graph(story: dict) -> None:
    scenes = story.get("scenes")
    if not isinstance(scenes, dict) or story.get("start") not in scenes or len(scenes) < 9:
        raise ValueError("Invalid scene graph")
    endings = 0
    for sid, scene in scenes.items():
        if not re.fullmatch(r"[a-z_]+", sid):
            raise ValueError("Unsafe scene ID")
        if not isinstance(scene.get("title"), str) or not isinstance(scene.get("body"), str):
            raise ValueError("Missing scene content")
        links = scene.get("choices")
        if not isinstance(links, list):
            raise ValueError("Invalid scene choices")
        if "ending" in scene:
            endings += 1
            if links:
                raise ValueError("Ending must not have outgoing choices")
        elif len(links) != 2:
            raise ValueError("Decision points must have two options")
        for link in links:
            if link.get("next") not in scenes or not isinstance(link.get("label"), str):
                raise ValueError("Broken choice target")
    if endings < 3:
        raise ValueError("Three distinct endings required")
    seen = set()
    queue = [story["start"]]
    while queue:
        sid = queue.pop()
        if sid in seen:
            continue
        seen.add(sid)
        queue.extend(c["next"] for c in scenes[sid]["choices"])
    if seen != set(scenes):
        raise ValueError("Unreachable scenes present")


def verify(book: Path, worlds: Path, interactive: Path) -> int:
    engine.verify(book)
    reality.verify(book, worlds)
    chapters = engine.load_manifest(book)["entries"]
    world_manifest = reality.manifest_at(worlds)["entries"]
    entries = manifest_at(interactive)["entries"]
    if len(entries) > len(world_manifest) or len(entries) > len(chapters):
        raise ValueError("Interactive graph outruns its verified sources")
    prev = None
    for n, entry in enumerate(entries, 1):
        path = f"stories/story-{n:06d}.json"
        if entry.get("path") != path or not RECORD_PATH.fullmatch(path):
            raise ValueError("Invalid story path or ordering")
        data = (interactive / path).read_bytes()
        if engine.sha(data) != entry.get("sha256") or entry.get("previous_sha256") != prev:
            raise ValueError("Interactive integrity chain broken")
        story = json.loads(data)
        if story.get("chapter") != n or story.get("source_chapter_sha256") != chapters[n-1]["sha256"]:
            raise ValueError("Interactive story not bound to chapter")
        if story.get("world_lens") != world_manifest[n-1]["lens_id"]:
            raise ValueError("Interactive story not bound to world")
        validate_graph(story)
        prev = entry["sha256"]
    return len(entries)


def extend(book: Path, worlds: Path, interactive: Path) -> int:
    verify(book, worlds, interactive)
    chapters = engine.load_manifest(book)["entries"]
    world_manifest = reality.manifest_at(worlds)["entries"]
    manifest = manifest_at(interactive)
    count = 0
    for n in range(len(manifest["entries"]) + 1, len(world_manifest) + 1):
        record = chapters[n-1]
        chapter = json.loads((book / record["path"]).read_text(encoding="utf-8"))
        world = json.loads((worlds / world_manifest[n-1]["path"]).read_text(encoding="utf-8"))
        graph = compose(chapter, world)
        validate_graph(graph)
        path = f"stories/story-{n:06d}.json"
        previous = manifest["entries"][-1]["sha256"] if manifest["entries"] else None
        manifest["entries"].append({"chapter": n, "path": path, "sha256": engine.sha(engine.encoded(graph)), "previous_sha256": previous, "world_lens": graph["world_lens"]})
        engine.atomic(interactive / path, engine.encoded(graph))
        engine.atomic(interactive / "manifest.json", engine.encoded(manifest))
        count += 1
    verify(book, worlds, interactive)
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book-dir", type=Path, default=engine.BOOK)
    parser.add_argument("--realities-dir", type=Path, default=reality.REALITIES)
    parser.add_argument("--interactive-dir", type=Path, default=STORIES)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        amount = verify(args.book_dir, args.realities_dir, args.interactive_dir) if args.verify else extend(args.book_dir, args.realities_dir, args.interactive_dir)
        print(f"INTERACTIVE: {amount} {'stories verified' if args.verify else 'new original story graphs published'}")
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"INTERACTIVE_FAILED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
