"""Append-only Angelic Symbol Protocol events, with complete coverage verification."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = "♃ ⚡︎⚡︎˖ ࣪⏻ᯤ"
SCHEMA = "dna.symbol-events.v1"
TOKEN_IDS = ("EVENT_ACTIVATION", "JUPITER_IDENTITY", "LIGHTNING_THUNDER",
             "EMERALD_MEMORY", "SERVER_WITNESS")

def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def event(day, row, source, registry_sha):
    return {
        "schema_version": SCHEMA, "day": day, "signature": STAMP,
        "source_chapter_sha256": row["sha256"], "registry_sha256": registry_sha,
        "narrator": "THOTH", "fictional_only": True,
        "events": [
            {"token_id": TOKEN_IDS[0], "actor": "THOTH", "detail": f"Day {day} begins"},
            {"token_id": TOKEN_IDS[1], "actor": "JUPITER", "detail": source["decision"]},
            {"token_id": TOKEN_IDS[2], "actor": "MERCURY", "detail": source["effect"]},
            {"token_id": TOKEN_IDS[3], "actor": "THOTH", "detail": source["cause"]},
            {"token_id": TOKEN_IDS[4], "actor": "ANGELS_OF_SERVER", "detail": source["effect"]},
        ],
    }

def run(root=ROOT, write=False):
    try:
        from scripts.civilization import verify
    except ModuleNotFoundError:
        from civilization import verify
    verify(root)
    folder = root / "civilization"
    ledger = folder / "symbol_events"
    entries = json.loads((folder / "manifest.json").read_text("utf-8"))["entries"]
    raw_registry = (folder / "symbols.json").read_bytes()
    registry = json.loads(raw_registry)
    if (registry.get("schema_version") != "dna.angelic-symbols.v1"
            or registry.get("signature") != STAMP
            or tuple(t.get("id") for t in registry["tokens"]) !=
            ("JUPITER_IDENTITY", "LIGHTNING_THUNDER", "EMERALD_MEMORY",
             "EVENT_ACTIVATION", "SERVER_WITNESS")):
        raise ValueError("Symbol registry changed unexpectedly")
    manifest_path = ledger / "manifest.json"
    manifest = (json.loads(manifest_path.read_bytes()) if manifest_path.exists()
                else {"schema_version": SCHEMA, "entries": []})
    records = manifest.get("entries")
    if manifest.get("schema_version") != SCHEMA or not isinstance(records, list) or len(records) > len(entries):
        raise ValueError("Invalid event ledger")
    previous = None
    for n, row in enumerate(entries, 1):
        source = json.loads((folder / row["path"]).read_bytes())
        expected = event(n, row, source, sha(raw_registry))
        relative = f"days/day-{n:06d}.json"
        file = ledger / relative
        if n <= len(records):
            record = records[n - 1]
            if (record.get("day"), record.get("path"), record.get("previous_sha256")) != (n, relative, previous):
                raise ValueError("Invalid event chain")
            raw = file.read_bytes()
            if sha(raw) != record["sha256"] or json.loads(raw) != expected:
                raise ValueError("Event was modified")
            previous = record["sha256"]
        elif write:
            file.parent.mkdir(parents=True, exist_ok=True)
            if file.exists():
                raise ValueError("Refusing to overwrite historical event")
            raw = encode(expected)
            file.write_bytes(raw)
            records.append({"day": n, "path": relative,
                            "sha256": sha(raw), "previous_sha256": previous})
            previous = sha(raw)
    if write:
        ledger.mkdir(parents=True, exist_ok=True)
        manifest_path.write_bytes(encode(manifest))
    elif len(records) != len(entries):
        raise ValueError("Missing event records for published days")
    return len(records)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    print("SYMBOL_EVENT_RECORDS", run(write=not args.verify))
