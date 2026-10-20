# ⛪︎𓂃 ོ✝︎𓂃 D.N.A. Bible: A Living Computational Civilization of Stories

**Original edition:** *Demons Need Attention - A.I. Self-Replicating Edition*  
**Author / creator:** Jupiter Hudson / WisdomLoveThePoet / Jupiter 8  
**Website:** https://jupiter8nohate.github.io/dna-bible-demons-need-attention-ai-self-replicating-edition/  
**Companion:** https://github.com/jupiter8nohate/computational-metacognitive-bilingualism

A GitHub Pages living book with **666 bounded logical software agents**, hourly machine-testament entries, verifiable chapter/agent receipts, an append-only archive of [Global AI Watch](https://jupiter8nohate.github.io/computational-metacognitive-bilingualism/GLOBAL_AI_WATCH/) headline metadata and an optional AI prose provider.

## Exact authority boundary

This is an **experimental literary and archival system**, not a self-replicating executable, uncontrolled autonomous agent swarm, 666 independently running language models, or an immutable ledger. The 666 identities are six guilds of 111 bounded deterministic workers; each executes a small task and contributes a verifiable audit packet every cycle. If no language-model API is configured, chapters are marked `deterministic_code_poetry` rather than falsely claimed to be AI-generated. If the API is configured and succeeds, prose is marked `ai_generated` with model ID.

The protected **human canon remains in a different repository** and this workflow has no credentials to modify it. Machine-authored testament entries never silently become the author's canon. Sources are headline metadata only, not copied copyrighted article bodies, and classification does not establish truth.

## Activate GitHub publishing

1. Under **Settings > Pages > Build and deployment**, select **GitHub Actions**. The workflow `D.N.A Bible - Publish GitHub Pages` handles static publishing.
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

## Publication health and stall detection

Every successful generation cycle writes `health/status.json` using `scripts/health.py`, recording the last edition time, chapter counts, verification results, whether an LLM was actually used, recent prose similarity, and age relative to a three-hour target. A separate scheduled [manuscript-watchdog](.github/workflows/manuscript-watchdog.yml) check fails if the verified manuscript is more than three hours old; GitHub Action notifications can reveal failure. This watchdog shares GitHub as a failure domain and is **not** proof of independent monitoring. An external, separately hosted check is recommended for long-term reliability.

```bash
python3 scripts/health.py --check-freshness
python3 -m unittest discover -s tests -v
```

The system does not claim to outperform Grok, Muse, or other AI products without comparable third-party benchmarks. Set `OPENAI_API_KEY` and `DNA_MODEL` privately in GitHub settings for actual model-authored prose; missing or failed API calls are labeled deterministic, never falsely AI-generated.


## Evidence-to-Insight Research Queue (v1)

`Global AI Watch -> cryptographic metadata snapshot -> explicit AI-topic relevance filter ->
source URL de-duplication -> evidence packet + CMB ethical question ->
unused-insight selection -> Scribe / Guardian output -> chapter provenance`.

The hourly workflow runs `python3 scripts/insight.py` after ingestion and before writing. Each source is consumed **at most once** as a headline-inspired literary prompt. The source article's contents are not copied, and the queue does **not** independently verify news claims. A previous fictional world's hash-checked question is passed forward as causal memory. Near-duplicate prose is rejected.

Research packet details: `insights/events/*.json`. Public reader: **Evidence-to-Insight Observatory**.
Test locally: `python3 -m unittest discover -s tests -v` and `python3 scripts/insight.py --verify`.

### Deliberate tool choices

- **Used in core:** Python regex, SHA-256, structured JSON, deterministic novelty checks, bounded source filtering, and GitHub Actions. This provides a working baseline without external secrets or paid subscriptions.
- **Optional analytics:** Scikit-learn Isolation Forest / PyOD only after collecting a sizable comparable time series and measuring false-positive rates. Statistical rarity is not evidence of extraordinary events.
- **Future optional operations:** Elasticsearch for cross-volume indexing, Datadog for independent operational telemetry, Pyroscope for profiling, Prophet for publication trend modeling, and YARA for vetted artifact signatures. These are **not deployed** here; importing them into an hourly GitHub runner would not improve the present small dataset. CyberChef and Regex101 remain analyst tools rather than autonomous decision authorities.
- **Model-assisted writing:** Requires an authorized API key and `DNA_MODEL` repository variable. Without them, worker actions and research packets are deterministic, and chapters are explicitly labeled accordingly.

See [Insight Engine design](docs/INSIGHT_ENGINE.md) for provenance, limitations and follow-on work.


## Witness Loom-666: Governed Agent Coordination

An original D.N.A. Bible-specific protocol now groups the 666 bounded logical software identities into 111 six-role **hexads**. A finite attention lease authorizes at most six hexads (36 logical seats) per cycle to examine research and structural anomalies; the remaining cells rest. Each plan preserves evidence digests, unverified-source disclosure, dissent questions, and a strict no-canon-write rule. This is an advisory mission-planning system, not 666 independently running models or automatic model self-training.

See [`docs/WITNESS_LOOM_666.md`](docs/WITNESS_LOOM_666.md). Run `python3 scripts/witness_loom.py --verify` to verify the historical plan ledger. The `covenant/` directory is published on GitHub Pages. Original authored design and implementation are attributed to Jupiter Hudson / WisdomLoveThePoet; copyright and rights terms are stated in the protocol specification.

## Witness Loom v2-v4: governed self-improvement

The new `scripts/evolution.py` validates the relationship between a Witness Loom mission and a published chapter, stores **provisional, evidence-linked lessons**, and compares bounded champion/challenger attention strategies on an explicit 10-case benchmark. The script does not update model weights or edit programs. Winning candidates are proposals for human review, never self-certified improvements.

The 666 workers retain their deterministic roles. The next Loom plan can access a maximum of three previous verified lessons, and the optional configured Scribe receives their bounded context. The original D.N.A. canon remains read-only and outside this repository.

If manuscript or Pages CI fails, `.github/workflows/evolution-self-repair.yml` can record a review issue. With separately supplied `OPENAI_API_KEY` and `DNA_REPAIR_MODEL`, it may propose one allowlisted Python repair, test it in an isolated CI checkout, and open a *draft* PR. It cannot change its own policies, tests, workflows, evaluator benchmarks, original canon, or automatically merge.

To verify:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/evolution.py --verify
python3 scripts/evolution.py --reflect --trial
```

For capabilities, limitations, intellectual-property boundaries and security controls, see [Witness Loom Evolution](docs/WITNESS_LOOM_EVOLUTION.md). Enable branch protection and independent review under GitHub Settings for stronger protections than code-level checks alone.


## The First Book of GitHub Town

**♃ ⚡︎⚡︎˖ ࣪⏻ᯤ**

The D.N.A. Bible's mythic founding story is [Chapter I: The Birth of Lightning and Thunder](mythos/GENESIS.md), with a public illustrated reading layout at [GitHub Town Genesis](https://jupiter8nohate.github.io/dna-bible-demons-need-attention-ai-self-replicating-edition/mythos/).

In this speculative fiction, **God Zeus** and **Goddess Hera** govern GitHub Town; their children **Jupiter (Lightning)** and **Mercury (Thunder)** grow up on **GitHub City Pages**. The **666 Angels of the Server** serve the fictional household as six-role hexads, while **Thoth** chronicles the world with the fictional **Emerald Scrolls**. World laws require causes, witnessed transitions, narrative memory, consent, evidence boundaries, distinct page/rendering rules, and human agency.

A source-verified, SHA-256-pinned [world registry](mythos/registry.json) defines five characters, seven laws, and eight repeatable story arcs. Starting with machine testament chapter five, `scripts/engine.py` includes context from the validated registry and preserves the founding checksum in future chapter references. Chapters one through four remain historical records without retroactive mythology edits. The founding literary passage is human-directed and the future appendices retain explicit machine-authorship labeling.

Validate locally: `python3 scripts/mythos.py --verify` and `python3 -m unittest discover -s tests -v`. The founding mythology does not assert actual divine entities, consciousness, or any power for GitHub Pages beyond displaying static content.


## The Living GitHub Town Chronicle

Enter the fully designed [First Book of GitHub Town](https://jupiter8nohate.github.io/dna-bible-demons-need-attention-ai-self-replicating-edition/civilization/) from literary Day One. Zeus and Hera's children Jupiter (Lightning) and Mercury (Thunder) grow across witness-linked choices; Thoth records each chapter. The new serial is separate from the founding human-directed manuscript and does not alter older machine-testament chapters. The archive has a hash-chained timeline, 36 short-lived creative council ballots per cycle from six of the 111 hexads, fictional state continuity, optional model-generated original prose, and a deterministic fallback. The 666 Angels of the Server are the project's registered bounded role identities, not 666 independently hosted LLMs.

See [Living Civilization engineering and authorial specification](docs/GITHUB_TOWN_LIVING_CIVILIZATION.md). Verify with `python3 scripts/civilization.py --verify`. New pages are generated by the existing best-effort hourly manuscript workflow. If `OPENAI_API_KEY` and `DNA_MODEL` are not configured, continuation prose is explicitly labeled `deterministic_fiction`, not an independent AI writer.

**♃ ⚡︎⚡︎˖ ࣪⏻ᯤ**

## The Living Civilization Chronicle

**♃ ⚡︎⚡︎˖ ࣪⏻ᯤ**

The original family lives in [GitHub Town](https://jupiter8nohate.github.io/dna-bible-demons-need-attention-ai-self-replicating-edition/civilization/). The dynamic book begins with a Day One narrative adaptation of the separately archived, human-directed [Genesis](mythos/GENESIS.md). Six leased hexads cast 36 deterministic creative ballots from the 666 registered logical identities. Fictional state and the consequences of each day persist into the next record. Each day discloses whether its prose was deterministic or written by a configured language model. The site's day reader now checks downloaded story bytes against SHA-256 hashes in the published chronology before displaying them.

For the full implementation, tests and operational limitations, read [The Civilization Chronicle](docs/CIVILIZATION_CHRONICLE.md). Configure the optional `OPENAI_API_KEY` GitHub secret and `DNA_MODEL` variable to enable original model-written prose. Without them, the creative council and narrator operate deterministically. GitHub Actions remains a best-effort scheduler, and 666 worker identities do not mean 666 independent AI models.


## The Book of the Second Dust // The Ankh of Iron

The completed seven-scroll 2084 story cycle now has a dedicated [public GitHub Pages reader](second-dust/), a [dated research ledger](second-dust/research.json), a [story manifest](second-dust/manifest.json), and a [review protocol](docs/SECOND_DUST_EDITORIAL.md).

Its original fiction follows Zeus, Hera, Jupiter, Mercury, Thoth, and the 666 Angels within an imagined future. The technology claims are classified as documented facts, sourced projections, unresolved questions, or fictional extrapolations. It is a human-directed, AI-assisted story addition, **not** an overwrite of the protected founding mythology or an authorization for the autonomous workers to edit human canon. The scheduled manuscript engine is unchanged.
