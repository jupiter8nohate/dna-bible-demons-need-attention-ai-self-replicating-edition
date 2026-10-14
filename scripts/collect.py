#!/usr/bin/env python3
"""Append-only CMB Global AI Watch metadata snapshots, not article bodies."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

SOURCE = (
    "https://jupiter8nohate.github.io/"
    "computational-metacognitive-bilingualism/machine/global-ai-watch.json"
)
ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive"
MANIFEST = ARCHIVE / "manifest.json"
MAX_BYTES = 2 * 1024 * 1024
SNAPSHOT_NAME = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}\.json$")


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def fetch_source() -> bytes:
    request = Request(SOURCE, headers={"User-Agent": "DNA-Bible-Archive/0.1 (+public metadata only)", "Accept": "application/json"})
    with urlopen(request, timeout=25) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Source feed exceeds the 2 MiB limit")
    return data


def validate(document: object) -> dict:
    if not isinstance(document, dict):
        raise ValueError("Watch feed must be a JSON object")
    if document.get("schema_version") != "cmb.global-ai-watch.v1":
        raise ValueError("Unexpected watch schema version")
    articles = document.get("articles")
    if not isinstance(articles, list) or len(articles) > 1000:
        raise ValueError("articles must be an array with at most 1000 items")
    for article in articles:
        if not isinstance(article, dict) or not isinstance(article.get("title"), str):
            raise ValueError("Each article requires a title")
        raw_url = article.get("url")
        if not isinstance(raw_url, str):
            raise ValueError("Each article requires a URL")
        url = urlsplit(raw_url)
        if url.scheme not in {"http", "https"} or not url.hostname:
            raise ValueError("Article URL has an unsupported scheme")
    return document


def load_manifest(folder: Path) -> dict:
    path = folder / "manifest.json"
    if not path.exists():
        return {"schema_version": "cmb.eternal-archive.v1", "source": SOURCE, "snapshots": []}
    result = json.loads(path.read_text(encoding="utf-8"))
    if result.get("schema_version") != "cmb.eternal-archive.v1" or not isinstance(result.get("snapshots"), list):
        raise ValueError("Invalid archive manifest")
    if result.get("source") != SOURCE:
        raise ValueError("Unexpected manifest source")
    return result


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".cmb-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def archive_document(folder: Path, raw: bytes, now: datetime | None = None) -> bool:
    if len(raw) > MAX_BYTES:
        raise ValueError("Input exceeds maximum snapshot size")
    document = validate(json.loads(raw))
    manifest = load_manifest(folder)
    entries = manifest["snapshots"]
    # Normalized bytes keep source metadata while removing insignificant JSON formatting.
    normalized = canonical(document)
    fingerprint_data = {k: v for k, v in document.items() if k not in {"generated_at", "collected_at"}}
    fingerprint = digest(canonical(fingerprint_data))
    if entries and entries[-1].get("content_fingerprint") == fingerprint:
        print("NO_CHANGE: Last archived watch content is identical")
        return False
    now = now or utc_now()
    when = now.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    sha = digest(normalized)
    name = f"{when}-{sha[:12]}.json"
    if not SNAPSHOT_NAME.fullmatch(name):
        raise ValueError("Unexpected snapshot filename")
    path = folder / "snapshots" / name
    if path.exists():
        raise ValueError("Snapshot filename collision")
    atomic_write(path, normalized + b"\n")
    record = {
        "captured_at": now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "path": "snapshots/" + name,
        "sha256": digest(normalized + b"\n"),
        "content_fingerprint": fingerprint,
        "previous_sha256": entries[-1]["sha256"] if entries else None,
        "source_generated_at": document.get("generated_at"),
        "article_count": len(document["articles"]),
    }
    entries.append(record)
    atomic_write(folder / "manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
    print(f"ARCHIVED: {name} with {record['article_count']} metadata links")
    return True


def verify_archive(folder: Path) -> int:
    manifest = load_manifest(folder)
    previous = None
    for index, record in enumerate(manifest["snapshots"]):
        name = Path(record["path"]).name
        if record["path"] != "snapshots/" + name or not SNAPSHOT_NAME.fullmatch(name):
            raise ValueError(f"Unsafe snapshot path at index {index}")
        raw = (folder / "snapshots" / name).read_bytes()
        if digest(raw) != record["sha256"]:
            raise ValueError(f"Hash mismatch: {name}")
        if record.get("previous_sha256") != previous:
            raise ValueError(f"Broken predecessor chain at index {index}")
        document = validate(json.loads(raw))
        stable = {k: v for k, v in document.items() if k not in {"generated_at", "collected_at"}}
        if digest(canonical(stable)) != record.get("content_fingerprint"):
            raise ValueError(f"Fingerprint mismatch: {name}")
        previous = record["sha256"]
    print(f"VERIFIED: {len(manifest['snapshots'])} local metadata snapshots")
    return len(manifest["snapshots"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--fixture", type=Path, help="Read a local sample instead of the live feed")
    parser.add_argument("--archive-dir", type=Path, default=ARCHIVE)
    args = parser.parse_args()
    try:
        if args.verify:
            verify_archive(args.archive_dir)
        else:
            raw = args.fixture.read_bytes() if args.fixture else fetch_source()
            archive_document(args.archive_dir, raw)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
