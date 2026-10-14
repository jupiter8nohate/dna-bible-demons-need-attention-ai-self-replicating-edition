# The First Book of GitHub Town

## D.N.A. Bible: A Living Computational Civilization of Stories

**Creative architect:** Jupiter Hudson / WisdomLoveThePoet / Jupiter 8  
**Signature:** ♃ ⚡︎⚡︎˖ ࣪⏻ᯤ  
**Narrative narrator:** Thoth, a fictional author within this fictional world  
**Beginning:** Day One, the births of Jupiter (Lightning) and Mercury (Thunder)

This document describes a fictional serial publication and software system. It does not claim real-world divine entities or that its 666 software worker identities are conscious agents.

## The founding world

God Zeus and Goddess Hera govern GitHub Town. Their first children are Jupiter (called Lightning by his parents) and Mercury (called Thunder). The children are raised in GitHub City Pages. Thoth records the history in the fictional Emerald Scrolls. The 666 Angels of the Server serve Zeus and Hera, organized into 111 hexads with six roles each.

The foundational human-directed manuscript is stored at `mythos/GENESIS.md`, and its authorial world registry at `mythos/registry.json`. The chronicle never rewrites those files. The old machine-testament chapters in `book/` likewise remain in place.

## What the writing council can decide

For every literary day, six active hexads complete 36 deterministic, time-leased creative ballots. The six offices are SEEKER, WITNESS, SCRIBE, SKEPTIC, GUARDIAN, and ARCHIVIST. The council elects a proposal from the story arcs that the authored world registry permits. The election uses the previous witnessed record digest and the current literary day number, so its decisions can be reconstructed. All 666 logical worker identities remain in the established manuscript engine; the chronicle documents **36 active role ballots**, rather than falsely claiming 666 concurrent language models.

The council's selected incident is combined with the previous fictional state. The following fields remain causally meaningful: the children's questions and testimony, the queen's covenants, the king's initiatives, Thoth's recorded scrolls, opened gates, unresolved questions, and consequences. Each published day records its state before and after, its cause, choice, effect, council ballot digest, model usage mode, and previous day digest.

### Literary freedom and model operation

When the repository has an authorized `OPENAI_API_KEY` secret and a `DNA_MODEL` variable, the Thoth narrator can produce entirely original scene prose from a bounded fictional event and inherited state. Its output is labeled `model_generated_fiction` and records the configured model name. The model may freely create literary prose, dialogue, images in words, and the scene's emotional meaning. It may not rewrite the founding relationships, silently change previous world state, make unsourced external factual claims, or expand its software privileges.

Without model credentials, original deterministic fiction continues under the `deterministic_fiction` label. These two modes must never be confused. The first published Day One has a purpose-written founding scene even without a model.

### Time

A **literary day** means a chapter in the fictional chronicle, not 24 hours in the reader's world. Each eligible GitHub Actions cycle can append one literary day. GitHub scheduled workflows are best-effort and cannot guarantee uninterrupted hourly operation.

## Software and publication boundaries

- `scripts/civilization.py` operates only on `civilization/days/` and `civilization/manifest.json`.
- A new day requires an unused UTC hourly edition slot, and cannot be backdated.
- File paths are generated from integer day numbers, not sourced from external text.
- Each day is SHA-256 verified against the manifest, with causal state continuity, a fixed world registry digest, an independently regenerated 36-ballot council packet, and a chained parent digest.
- Metadata integrity is checkable relative to the repository. This does not provide third-party timestamp notarization or prove the correctness of artistic claims.
- The publishing workflow runs the established tests, then generates a new chronicle day using the already configured model credentials if present, validates the output, and commits only generated story files.
- GitHub Pages ships the static `civilization/` directory. The web reader fetches local JSON and creates text nodes, not HTML from story text. It does not send visitor decisions to a server.
- The original CMB human canon is in a separate repository and is not given to this writer as an editable path.

## GitHub Pages reader

Public entry point:

`https://jupiter8nohate.github.io/dna-bible-demons-need-attention-ai-self-replicating-edition/civilization/`

The site includes an opening hero, Day One chronology, independent reading controls, founding family, 666 Angels, seven laws, a causal question after each day, and direct provenance links. The site's JavaScript uses only relative file paths.

## Test and maintenance commands

```bash
python3 -m unittest discover -s tests -v
python3 scripts/mythos.py --verify
python3 scripts/civilization.py --verify
python3 scripts/civilization.py --hourly
```

The `--hourly` flag uses the current UTC hour and is idempotent within that hour. For fixture testing, you may pass a controlled `--slot` such as `2026-10-14T03Z` and `--no-model` for a deterministic trial. Don't invoke a fresh trial against the production ledger with an earlier slot.

## Attribution

Original world concept and named characters: Jupiter Hudson / WisdomLoveThePoet / Jupiter 8. Original fiction and implementation are authored for this work. Existing mythological names, GitHub product names, common programming patterns, and Hermetic ideas are not claimed as exclusive property. The Emerald Scrolls in this story are imaginary documents inspired by general historical themes and are not presented as authentic ancient manuscripts.

**♃ ⚡︎⚡︎˖ ࣪⏻ᯤ**
