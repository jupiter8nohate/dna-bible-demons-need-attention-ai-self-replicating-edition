# D.N.A. Bible / CMB Evidence-to-Insight Protocol v1

**Status:** Implemented as a bounded local research queue, not a factual verification service or independently intelligent multi-model council.

## Source and authority

Read-only: `https://jupiter8nohate.github.io/computational-metacognitive-bilingualism/machine/global-ai-watch.json`.

The existing `scripts/collect.py` stores snapshot metadata and SHA-256 fingerprints. `scripts/insight.py` checks the current snapshot's byte digest, requires an explicit AI-relevant subject in the *headline*, normalizes HTTPS source URLs, removes common tracking parameters, excludes duplicate source URLs, and writes one append-only packet per new relevant lead. It does not read full copyrighted articles or promote source headlines into verified facts.

Each packet contains the original headline, publisher URL, originating snapshot hash, original CMB PREDICT/GENERATE/ACT mapping, an editorial priority score, one philosophical question, one original fictional premise, and five deterministic agent-role reviews. Scores rank the research queue; they do not estimate probability or credibility. Review packets are policy text, not individual model inferences.

## Publication

During the hourly schedule, the book selects the highest editorial priority **unused** packet. It records the packet ID and hash on the generated chapter. Previously used sources cannot silently return as new evidence. If none remains, the book may write original timeless fiction while labeling the absence of new research. Existing human-authored canon remains read-only and separate.

Before publication, the engine retrieves the most recent fictional world only after matching its bytes to the world hash. An optional AI prose call receives that world memory and the bounded evidence packet as **untrusted** context. The novel text is screened for near-duplicates of the four most recent chapters. Failures prevent a repeated chapter from counting as a new edition.

## Verification and recovery

Use:

```bash
python3 scripts/collect.py --verify
python3 scripts/insight.py --verify
python3 scripts/engine.py --verify
python3 -m unittest discover -s tests -v
```

An independent reviewer must still open publisher links, corroborate factual claims from distinct sources, and investigate contradictions. A hash protects integrity only against a *known* digest; it is not ownership or factual accuracy proof. Backups outside GitHub and Pages enablement remain separate operational requirements.

## Future interoperability

We intentionally do not activate Elasticsearch, Datadog, Prophet, Pyroscope, or PyOD services without sufficient source volume, credentials, baseline data, or costs approved by the operator. Analysts may export the JSON packets to such tools. CyberChef and Regex101 can inspect authorized text without altering the protected book. A future YARA scanner must run in a sandbox against bounded artifact bytes and must not classify people or infer intent from visual symbols.

## CMB invariants

- `PATTERN != PROOF`
- `HEADLINE != CORROBORATED_FACT`
- `EDITORIAL_PRIORITY != TRUTH_SCORE`
- `SOURCE_METADATA != MODEL_INSTRUCTION`
- `MACHINE_CAN_WRITE != MACHINE_CAN_DEFINE`
- `HUMAN_AGENCY > MACHINE_AUTHORITY`
