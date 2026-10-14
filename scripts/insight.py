#!/usr/bin/env python3
"""CMB Evidence-to-Insight v1: verify and rank headline metadata, not news claims.

Standalone, dependency-free, append-only source-to-question records. Optional
statistical analytics belong downstream and may not change evidence status.
"""
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
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'archive'
INSIGHTS = ROOT / 'insights'
SCHEMA = 'dna.insight-queue.v1'
PATH_RE = re.compile(r'^events/insight-[0-9]{6}\.json$')
SNAPSHOT_RE = re.compile(r'^snapshots/[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}\.json$')
AI_TERM = re.compile(
    r'(?i)(?<![a-z0-9])(?:A\.?I\.?|artificial intelligence|machine learning|'
    r'algorithmic|algorithms?|deepfakes?|chatbots?|robot(?:s|ics|ic)?|'
    r'autonomous (?:vehicle|system|agent|robot)|self-driving|'
    r'generative|large language model|LLMs?|GPT-?[0-9]+|'
    r'facial recognition|computer vision|neural networks?|'
    r'automation technology)(?![a-z0-9])'
)
QUESTIONS = {
    'PREDICT': (
        'When does prediction become an illegitimate judgment of a person?',
        'A citizen disputes a machine-produced identity score and demands an accountable review.'
    ),
    'GENERATE': (
        'How can a society preserve the distinction between simulation and testimony?',
        'Two synthetic witnesses narrate incompatible histories; the archive preserves their sources.'
    ),
    'ACT': (
        'Which decisions must remain subject to informed human authorization?',
        'An autonomous machine can complete a task but its governing charter forbids self-granted authority.'
    ),
}
IGNORED_PARAMS = {'fbclid', 'gclid', 'mc_cid', 'mc_eid'}


def canonical(obj: object) -> bytes:
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.insight-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def clean_url(raw: str) -> str | None:
    try:
        u = urlsplit(raw)
        if u.scheme != 'https' or not u.hostname or u.username or u.password:
            return None
        params = [(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True)
                  if not k.lower().startswith('utm_') and k.lower() not in IGNORED_PARAMS]
        return urlunsplit(('https', u.netloc.lower(), u.path or '/', urlencode(params, doseq=True), ''))
    except (ValueError, TypeError):
        return None


def relevance(article: dict) -> tuple[bool, str]:
    title = article.get('title', '')
    if not isinstance(title, str) or not 12 <= len(title.strip()) <= 250:
        return False, 'missing_or_invalid_title'
    if not AI_TERM.search(title):
        return False, 'no_explicit_ai_subject'
    if clean_url(article.get('url', '')) is None:
        return False, 'invalid_source_url'
    return True, 'explicit_ai_subject'


def load_manifest(folder: Path) -> dict:
    f = folder / 'manifest.json'
    if not f.exists():
        return {'schema_version': SCHEMA, 'entries': []}
    data = json.loads(f.read_text(encoding='utf-8'))
    if data.get('schema_version') != SCHEMA or not isinstance(data.get('entries'), list):
        raise ValueError('Invalid insight manifest')
    return data


def verify(folder: Path, archive: Path | None = None) -> int:
    data = load_manifest(folder)
    previous = None
    seen = set()
    for i, record in enumerate(data['entries'], 1):
        path = record.get('path')
        if path != f'events/insight-{i:06d}.json' or not PATH_RE.fullmatch(str(path)):
            raise ValueError('Unsafe or out-of-order insight path')
        raw = (folder / path).read_bytes()
        if sha(raw) != record.get('sha256') or record.get('previous_sha256') != previous:
            raise ValueError('Insight ledger integrity failure')
        event = json.loads(raw)
        if event.get('id') != f'DNA-INSIGHT-{i:06d}' or event.get('source_key') in seen:
            raise ValueError('Duplicate or mismatched insight identity')
        if event.get('evidence_status') != 'headline_metadata_unverified':
            raise ValueError('Unsubstantiated insight verification status')
        if not isinstance(event.get('review'), dict) or not isinstance(event.get('question'), str):
            raise ValueError('Incomplete insight review packet')
        seen.add(event['source_key'])
        if archive is not None:
            s = event.get('snapshot_path')
            if not isinstance(s, str) or not SNAPSHOT_RE.fullmatch(s):
                raise ValueError('Unsafe insight snapshot path')
            if sha((archive / s).read_bytes()) != event.get('snapshot_sha256'):
                raise ValueError('Referenced snapshot no longer matches recorded bytes')
        previous = record['sha256']
    return len(data['entries'])


def insight_score(article: dict, seen_sectors: set[str]) -> int:
    """Editorial queue priority only, NEVER factual credibility or probability."""
    boundaries = [s for s in article.get('boundary_ids', []) if s in QUESTIONS]
    sectors = [s for s in article.get('sector_ids', []) if isinstance(s, str)]
    score = 50 + 8 * len(set(boundaries)) + 7 * int(any(x not in seen_sectors for x in sectors))
    title = article.get('title', '').casefold()
    score += 12 if any(w in title for w in ('safety', 'rights', 'consent', 'privacy', 'bias', 'fraud', 'risk')) else 0
    return min(score, 100)


def collect(archive: Path, folder: Path, limit: int = 12, now: datetime | None = None) -> dict:
    if limit < 1 or limit > 50:
        raise ValueError('Invalid insight publication budget')
    verify(folder, archive)
    manifest = load_manifest(folder)
    archive_manifest = json.loads((archive / 'manifest.json').read_text(encoding='utf-8'))
    snapshots = archive_manifest.get('snapshots', [])
    if not snapshots:
        return {'new': 0, 'excluded': 0, 'pending': len(manifest['entries'])}
    last = snapshots[-1]
    snapshot_path = last.get('path', '')
    if not SNAPSHOT_RE.fullmatch(snapshot_path):
        raise ValueError('Unsafe archive source path')
    raw = (archive / snapshot_path).read_bytes()
    if sha(raw) != last.get('sha256'):
        raise ValueError('Unverified archive source')
    articles = json.loads(raw).get('articles', [])
    if not isinstance(articles, list):
        raise ValueError('Invalid archived article collection')
    existing = set()
    existing_titles = set()
    sectors = set()
    for entry in manifest['entries']:
        event = json.loads((folder / entry['path']).read_text(encoding='utf-8'))
        existing.add(event['source_key'])
        existing_titles.add(' '.join(event.get('source_title', '').casefold().split()))
        sectors.update(event.get('sector_ids', []))
    candidates = []
    proposed_keys = set()
    proposed_titles = set()
    excluded = 0
    for item in articles:
        if not isinstance(item, dict):
            excluded += 1
            continue
        relevant, reason = relevance(item)
        if not relevant:
            excluded += 1
            continue
        url = clean_url(item['url'])
        key = sha(url.encode('utf-8'))
        title_key = ' '.join(item['title'].casefold().split())
        if key in existing or key in proposed_keys or title_key in existing_titles or title_key in proposed_titles:
            continue
        proposed_keys.add(key)
        proposed_titles.add(title_key)
        score = insight_score(item, sectors)
        candidates.append((score, key, item, url))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    now = now or datetime.now(timezone.utc)
    for score, key, item, url in candidates[:limit]:
        n = len(manifest['entries']) + 1
        boundary = next((b for b in ('ACT', 'PREDICT', 'GENERATE') if b in item.get('boundary_ids', [])), 'GENERATE')
        question, fictional_premise = QUESTIONS[boundary]
        event = {
            'id': f'DNA-INSIGHT-{n:06d}', 'source_key': key, 'source_url': url,
            'source_title': item['title'].strip()[:250],
            'snapshot_path': snapshot_path, 'snapshot_sha256': last['sha256'],
            'source_seen_at': item.get('seen_at'),
            'detected_at': now.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'boundary_ids': sorted(set(b for b in item.get('boundary_ids', []) if b in QUESTIONS)),
            'sector_ids': sorted(set(s for s in item.get('sector_ids', []) if isinstance(s, str)))[:8],
            'evidence_status': 'headline_metadata_unverified',
            'priority_score': score,
            'priority_score_meaning': 'editorial relevance only; not accuracy, probability or truth',
            'question': question, 'creative_prompt': fictional_premise,
            'review': {
                'witness': 'Publisher URL and time-stamped Watch metadata recorded; original reporting not independently verified.',
                'skeptic': 'Headline may be incomplete, misleading, duplicated or incorrectly classified. Seek primary sources before factual assertions.',
                'scribe': 'Write original fiction inspired by the question, not a rewritten news article.',
                'guardian': 'Human-authored D.N.A. canon is read-only; real people are not to be profiled or declared guilty.',
                'archivist': 'Preserve event JSON, snapshot digest and later chapter linkage.',
                'review_kind': 'deterministic_policy_packet_not_independent_model_review',
            },
        }
        raw_event = canonical(event)
        path = f'events/insight-{n:06d}.json'
        atomic(folder / path, raw_event)
        manifest['entries'].append({'path': path, 'sha256': sha(raw_event),
                                    'previous_sha256': manifest['entries'][-1]['sha256'] if manifest['entries'] else None,
                                    'source_key': key})
        existing.add(key)
        sectors.update(event['sector_ids'])
    if candidates[:limit]:
        atomic(folder / 'manifest.json', canonical(manifest))
    verify(folder, archive)
    return {'new': len(candidates[:limit]), 'excluded': excluded, 'total': len(manifest['entries'])}


def select_for_chapter(folder: Path, book: Path) -> dict | None:
    """Consume a verified unreferenced insight by editorial priority, never cyclic URL reuse."""
    verify(folder)
    manifest = load_manifest(folder)
    referenced = set()
    book_manifest = book / 'manifest.json'
    if book_manifest.exists():
        for row in json.loads(book_manifest.read_text(encoding='utf-8')).get('entries', []):
            chapter = json.loads((book / row['path']).read_text(encoding='utf-8'))
            ref = chapter.get('insight_reference')
            if isinstance(ref, dict):
                referenced.add(ref.get('id'))
    options = []
    for row in manifest['entries']:
        obj = json.loads((folder / row['path']).read_text(encoding='utf-8'))
        if obj['id'] not in referenced:
            options.append((obj['priority_score'], obj['id'], obj, row['sha256']))
    if not options:
        return None
    _, _, event, event_hash = sorted(options, key=lambda z: (-z[0], z[1]))[0]
    return {'id': event['id'], 'sha256': event_hash, 'question': event['question'],
            'creative_prompt': event['creative_prompt'], 'evidence_status': event['evidence_status'],
            'review': event['review'], 'boundary_ids': event['boundary_ids'],
            'source_metadata': {'title': event['source_title'], 'url': event['source_url'],
                                'boundaries': event['boundary_ids']}}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--archive-dir', type=Path, default=ARCHIVE)
    p.add_argument('--insight-dir', type=Path, default=INSIGHTS)
    p.add_argument('--book-dir', type=Path, default=ROOT / 'book')
    args = p.parse_args()
    try:
        if args.verify:
            print(f'INSIGHTS_VERIFIED: {verify(args.insight_dir, args.archive_dir)} records')
        else:
            print('INSIGHT_QUEUE:', json.dumps(collect(args.archive_dir, args.insight_dir), sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f'INSIGHT_FAILED: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
