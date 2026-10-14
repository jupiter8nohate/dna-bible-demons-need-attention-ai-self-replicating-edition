# ⛪︎𓂃 ོ✝︎𓂃 D.N.A Bible: Demons Need Attention - A.I. Self-Replicating Edition

**Author / creator:** Jupiter Hudson / WisdomLoveThePoet / Jupiter 8  
**Website:** https://jupiter8nohate.github.io/dna-bible-demons-need-attention-ai-self-replicating-edition/  
**Companion:** https://github.com/jupiter8nohate/computational-metacognitive-bilingualism

A GitHub Pages living book with **666 bounded logical software agents**, hourly machine-testament entries, verifiable chapter/agent receipts, an append-only archive of [Global AI Watch](https://jupiter8nohate.github.io/computational-metacognitive-bilingualism/GLOBAL_AI_WATCH/) headline metadata and an optional AI prose provider.

## Exact authority boundary

This is an **experimental literary and archival system**, not a self-replicating executable, uncontrolled autonomous agent swarm, 666 independently running language models, or an immutable ledger. The 666 identities are six guilds of 111 bounded deterministic workers; each executes a small task and contributes a verifiable audit packet every cycle. If no language-model API is configured, chapters are marked `deterministic_code_poetry` rather than falsely claimed to be AI-generated. If the API is configured and succeeds, prose is marked `ai_generated` with model ID.

The protected **human canon remains in a different repository** and this workflow has no credentials to modify it. Machine-authored testament entries never silently become the author's canon. Sources are headline metadata only, not copied copyrighted article bodies, and classification does not establish truth.

## Activate GitHub publishing

1. Under **Settings > Pages > Build and deployment**, select **GitHub Actions** as the publishing source. The `D.N.A Bible - Publish GitHub Pages` workflow deploys the latest validated records after each successful manuscript run. Do **not** rely on branch pushes from `GITHUB_TOKEN`, because they do not trigger separate Pages builds.
2. Under **Settings > Actions > General > Workflow permissions**, grant **Read and write permissions** for the dedicated living-book repository, if the available account settings permit it. This workflow commits only to `archive/`, `book/`, `realities/`, and `interactive/`.
3. Run **Actions > D.N.A Bible - 666 Agent Living Manuscript > Run workflow**. It also runs every UTC hour at minute 23 on a best-effort schedule.
4. Optional real AI prose: set the repository secret `OPENAI_API_KEY` and repository variable `DNA_MODEL` to a supported model name; this uses the configured OpenAI Responses API and may incur charges. Never commit keys. Without them the complete free deterministic pipeline still runs.
5. Read the website and check Actions logs for success. Configure independent backups and operational succession before claiming lasting continuity.

## How it works

`Global AI Watch metadata -> hash-chained snapshots -> 666 worker tasks -> optional AI prose -> machine-testament chapter + receipt -> twelve-lens reality world -> timed branching interactive scenes -> GitHub Pages`

Six worker guilds: **SEEKER**, **WITNESS**, **SCRIBE**, **SKEPTIC**, **GUARDIAN**, **ARCHIVIST**. Each has exactly 111 unique IDs. Every published chapter has a full machine-readable receipt listing all 666 completed software tasks. This is an audit of software workers, not evidence of collective AI consciousness or independent scientific verification.

## Run and verify locally

```bash
python3 -m unittest discover -s tests -v
python3 scripts/collect.py --verify
python3 scripts/engine.py --verify
python3 scripts/collect.py  # Requires network, but failures need not block a chapter
python3 scripts/engine.py --no-model
python3 scripts/engine.py --verify
python3 -m http.server 8000
```

## Longevity limitations

GitHub Actions, GitHub Pages, source publishers, and optional AI APIs can fail or change; GitHub schedules may be delayed or disabled. Git object hashes and our SHA-256 manifests only validate bytes against the published manifests; they are not independently anchored, tamperproof timestamps or proof of authorship. For preservation, periodically export and independently verify `book/`, `archive/`, and the Git history to a separate operator/storage provider. Human succession, payment for external models, and storage availability require actual ongoing arrangements.

**CMB axioms:** `PATTERN != PROOF` | `PROFILE != PERSON` | `MODEL != MIND` | `HUMAN_AGENCY > MACHINE_AUTHORITY`


## The Eternal Reality Engine - 12 original philosophical lenses

The creative companion engine `scripts/reality.py` constructs one original fictional
world for every machine-testament chapter. Each world contains a scene, a
philosophical question, a scriptural study reference, an echo of the previous
world, and three reader choices. Every world references its source chapter's
SHA-256 and is itself linked into a hash chain. Verify it with:

```bash
python3 scripts/reality.py
python3 scripts/reality.py --verify
python3 -m unittest discover -s tests -v
```

The GitHub workflow now automatically creates and publishes these files under
`realities/` after generating a chapter. On GitHub Pages, readers can browse
worlds and choose local fictional consequences; those choices do not modify
published records or the human-authored canon. New worlds are appended, not
retroactively rewritten.

### Creative influences, not adaptations

The twelve lenses draw on general philosophical topics associated with:
*Dark City* (time/memory), *The Matrix* (constructed consensus), *eXistenZ*
(nested worlds), *World on a Wire* (simulation recursion), *Inception*
(suggestion), *Source Code* (replay), *Vanilla Sky* (memory uncertainty),
*Cypher* (identity masks), *The Game* (consent and rules), *The Thirteenth Floor*
(observer levels), *Strange Days* (recorded senses), and *Gattaca*
(prediction versus destiny). No film characters, plots, dialogue, fictional
settings, or promotional assets are copied or endorsed.

`GotQuestions.org` is linked only as an independent theological study reference,
not a source of automatically copied content or proof that the project endorses
or represents that ministry. Scripture references are study prompts, not
purported divine revelations from a software system.

This new feature is independent of the optional OpenAI text-generation API.
Current branches are browser-local interpretations, not independently hosted
AI agents, multiplayer sessions, or irreversible changes to canon.


## Interactive Bandersnatch-style mechanics (original work)

The public site is a text-based interactive story engine, **not a copy of the film** or its copyrighted characters or scenes. Each verified chapter receives an original graph of ten nodes: seven decision scenes, three endings, two-choice 10-second selection points, default choices when the clock expires, revisitable pivots, local memory echoes, and repeatable loops. Untimed mode supports accessibility and reduced-motion preferences. Readers can explore alternate endings and resume their own path using local browser storage; this does not send their choices to GitHub.

The engine currently schedules a new chapter **once per UTC hour at minute 23** (best effort, not uninterrupted execution). GitHub may skip, delay, or disable scheduled jobs; an independent external monitor and backups will be required for serious long-term continuity. Hourly receipts are around 100 KB each, potentially ~0.9 GB/year before Git overhead. Long-term archiving must eventually rotate/shard older records.

Every new cycle runs `engine.py --hourly`, `reality.py`, and `branching.py`, verifies the corresponding append-only manifests and outputs, and publishes static JSON consumed by `static/player.js`. The workflow's GitHub token is scoped to the manuscript repository and cannot edit the protected CMB original canon.

This project is not affiliated with Netflix, *Black Mirror: Bandersnatch*, or the directors/producers of other inspiration films. The source of any new licensed multimedia must be authorized separately.


## Reader-directed branching world engine

`scripts/branching.py` derives original interactive scene graphs from each verified chapter and reality world. A graph has ten reachable scenes, two choices per decision, a memory-bearing loop, and three distinct endings. Each serialized story is hash-linked to the prior story and source chapter. All decisions run exclusively in the browser; they do not alter shared published data or the protected human canon.

```bash
python3 scripts/branching.py
python3 scripts/branching.py --verify
```

The published website offers an **interactive story reader**. Readers can revisit a node, select branches, and optionally turn on a 10-second decision clock; timed play is off by default for accessibility. The underlying published storyline is deterministic unless an explicitly configured LLM is authorized to generate the source chapter. This is not a multiplayer engine, sentient AI, or literal reality manipulation.

## Anomaly Genesis Protocol v1 (experimental)

`python3 scripts/anomaly.py` checks source-linked observations against the existing verified manuscript, world graphs, and public metadata archive. It emits bounded, immutable-by-policy, SHA-256-linked event records to `anomaly/`; a visible Observatory panel renders the records without copying news articles. Built-in detectors flag repeated narrative prose, repeated choice graphs, a duplicated headline source and research-feed staleness. These measurements **do not validate supernatural, historical, scientific, or theological claims**.

Every event stores a detector ID, observed evidence hashes, a deterministic fingerprint, a plain-language explanation, and a *fictional writing premise*. The next chapter can consume one unprocessed observation, clearly marked `detected_unverified`. New published events are append-only; duplicates sharing a stable detector signature are suppressed.

The publication workflow checks anomalies before writing, attaches a permissible prompt to the new machine-testament entry, then inspects that entry after publication. `python3 scripts/anomaly.py --verify` rejects modified event and referenced evidence bytes. It cannot substitute for externally anchored receipts or independent review.

From this release onward, the 666 bounded workers produce **compact reproducible receipts** (`deterministic_seed_v1`) by recording deterministic inputs and a SHA-256 digest of the fully reconstructed ballots. Historical full-ballot receipts remain valid; every future result can be reconstructed via `scripts.engine.run_agents(cycle, source_count)` and compared to the recorded digest. This reduces disk growth without pretending independent model reasoning occurred.

No Elasticsearch, PyOD, Datadog, or machine learning model is installed. Rule-based detectors come first so their false positives, novelty, and archival impact can be measured. All public observations remain separate from the protected, human-authored D.N.A. canon.


## Publication health and recovery
The hourly workflow now emits `health/status.json` after verifying the archives. A separate watchdog checks freshness hourly and reports a failed GitHub Actions run if the last chapter is more than three hours old. The status panel distinguishes deterministic code-poetry from actual AI-generated prose. These two workflows share GitHub infrastructure: independent uptime monitoring and off-platform backups are still recommended. Original canon is never a bot output.


## Narrative novelty safeguards
When no paid model is available, the deterministic author uses twelve original fictional mechanisms rather than a single repeated passage. `tests/test_novelty.py` evaluates consecutive text similarity and fails if fallback output clones adjacent chapters. This is a baseline quality check, not a substitute for creative editorial judgment, independent AI reasoning, or a competitive Grok/Muse benchmark.


**Verified publishing blocker (2026-10-14):** The first explicit Pages deployment successfully verified and packaged the book, but `actions/configure-pages` returned HTTP 404 because GitHub Pages was not enabled for this repository. The repository owner must select GitHub Actions under Settings > Pages. See [the deployment attempt](https://github.com/jupiter8nohate/dna-bible-demons-need-attention-ai-self-replicating-edition/actions/runs/38500060964). The writing workflow itself remains operational. A model API credential and independent benchmarking are additional optional setup requirements, not claims of existing AI-model superiority.
