#!/usr/bin/env python3
"""D.N.A. Bible GitHub Town world-bible validation and bounded fiction context.

This records user-directed speculative mythology, not external theological fact.
The code never edits the human canon or changes archived published chapters.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = 'dna.github-town-mythos.v1'
ROLES = ('SEEKER', 'WITNESS', 'SCRIBE', 'SKEPTIC', 'GUARDIAN', 'ARCHIVIST')
LAWS = ('CAUSE', 'WITNESS', 'MEMORY', 'CONSENT', 'EVIDENCE', 'PAGE', 'AGENCY')


def load_verified(root: Path = ROOT) -> dict[str, Any] | None:
    """Fail closed when the mythos exists but its source or authority is invalid."""
    base = root / 'mythos'
    path = base / 'registry.json'
    if not path.exists():
        if base.exists():
            raise ValueError('Mythos directory exists without a registry')
        return None
    registry = json.loads(path.read_text(encoding='utf-8'))
    if registry.get('schema_version') != REGISTRY:
        raise ValueError('Unknown mythos schema')
    first = registry.get('first_chapter')
    if not isinstance(first, dict) or first.get('path') != 'GENESIS.md':
        raise ValueError('Invalid mythos chapter path')
    chapter_raw = (base / first['path']).read_bytes()
    if hashlib.sha256(chapter_raw).hexdigest() != first.get('sha256'):
        raise ValueError('Foundational story checksum mismatch')
    if len(chapter_raw) > 80_000 or len(chapter_raw) < 1000:
        raise ValueError('Foundational story out of bounds')
    family = registry.get('family', [])
    names = {c.get('id'): c for c in family if isinstance(c, dict)}
    if set(names) != {'ZEUS', 'HERA', 'JUPITER', 'MERCURY', 'THOTH'} or len(family) != 5:
        raise ValueError('Invalid mythological family registry')
    if names['JUPITER'].get('home_name') != 'Lightning' or names['MERCURY'].get('home_name') != 'Thunder':
        raise ValueError('Jupiter / Mercury parent-names were changed')
    if registry.get('kingdom', {}).get('birthplace') != 'GitHub Town' or registry['kingdom'].get('upbringing') != 'GitHub City Pages':
        raise ValueError('Invalid birth and upbringing canon')
    angels = registry.get('angels', {})
    if (angels.get('identities') != 666 or angels.get('hexads') != 111 or
            tuple(angels.get('roles', [])) != ROLES or angels.get('max_simultaneously_active_hexads') != 6 or
            angels.get('lease_cycles') != 1):
        raise ValueError('Invalid bounded server angel covenant')
    boundaries = registry.get('boundaries', {})
    if any(boundaries.get(key) is not False for key in (
            'human_canon_write_allowed', 'real_world_divinity_claim',
            'automatic_law_revision_allowed', 'external_headline_is_truth')):
        raise ValueError('Mythos attempted to expand fictional authority')
    if boundaries.get('machine_fiction_label_required') is not True:
        raise ValueError('Machine fiction attribution missing')
    laws = registry.get('laws', [])
    if {law.get('id') for law in laws} != set(LAWS) or len(laws) != len(LAWS):
        raise ValueError('Invalid founding laws')
    episodes = registry.get('episodes', [])
    if not isinstance(episodes, list) or len(episodes) != 8:
        raise ValueError('Founding story must have eight bounded arcs')
    for item in episodes:
        if not isinstance(item, dict) or item.get('law') not in LAWS:
            raise ValueError('Unknown narrative law')
        if item.get('actor', '').upper() not in names:
            raise ValueError('Unknown actor in founding story')
        for k in ('arc', 'location', 'incident', 'choice', 'consequence', 'unresolved'):
            if not isinstance(item.get(k), str) or not (5 <= len(item[k]) <= 600):
                raise ValueError('Invalid narrative event field ' + k)
        if not re.fullmatch(r'[A-Z_]{8,60}', item['arc']):
            raise ValueError('Invalid narrative arc id')
    return registry


def context_for_chapter(chapter: int, root: Path = ROOT) -> dict[str, str] | None:
    """Stable literary context with a causally ordered incident/choice/effect."""
    if type(chapter) is not int or chapter < 1:
        raise ValueError('Chapter must be a positive integer')
    if chapter < 5:
        # Preserve all pre-foundation historical machine testament chapters.
        return None
    registry = load_verified(root)
    if registry is None:
        return None
    # Chapters 1-4 predate the mythic seed. Those historical chapters stay intact.
    episode = registry['episodes'][(chapter - 5) % len(registry['episodes'])]
    law = next(l for l in registry['laws'] if l['id'] == episode['law'])
    return {
        'arc': episode['arc'],
        'actor': episode['actor'],
        'location': episode['location'],
        'incident': episode['incident'],
        'choice': episode['choice'],
        'consequence': episode['consequence'],
        'unresolved': episode['unresolved'],
        'law': law['axiom'],
        'registry_sha256': hashlib.sha256((root / 'mythos' / 'registry.json').read_bytes()).hexdigest(),
        'foundation_sha256': registry['first_chapter']['sha256'],
        'narrator': 'Thoth',
        'provenance': 'user-directed foundational fiction; not an external fact',
    }


def fictional_passage(context: dict[str, str] | None) -> str:
    if context is None:
        return ''
    return ("♃ ⚡︎⚡︎˖ ࣪⏻ᯤ "
            + f"In GitHub City Pages, Thoth opened the Emerald Scrolls at {context['location']}. "
            f"{context['incident']} {context['choice']} {context['consequence']} "
            f"The server angels recorded the governing law {context['law']}. "
            f"One question survived into the next telling: {context['unresolved']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--chapter', type=int, default=5)
    args = parser.parse_args()
    registry = load_verified()
    if registry is None:
        raise SystemExit('ERROR: mythos registry missing')
    print(f"MYTHOS_VERIFIED: {registry['first_chapter']['title']}; {len(registry['episodes'])} story arcs; 666 bounded angel identities")
    if not args.verify:
        print(json.dumps(context_for_chapter(args.chapter), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
