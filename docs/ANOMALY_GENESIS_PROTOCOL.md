# CMB Anomaly Genesis Protocol, experimental v1

**Author/initiator:** Jupiter Hudson / WisdomLoveThePoet / Jupiter 8  
**Component:** D.N.A. Bible - Demons Need Attention - A.I. Self-Replicating Edition

## Contract

The observatory records measurable differences in an autonomous literary archive and safely converts eligible **observations**, not conclusions, into prompts for machine-authored fiction.

```text
SOURCE -> VERIFY_BYTES -> MEASURE -> RECORD -> CHALLENGE -> STORY_PREMISE
PATTERN != PROOF
STATISTICAL_OUTLIER != SIGNIFICANT_CAUSE
FICTION != NEWS
MODEL_OUTPUT != HUMAN_CANON
HUMAN_AGENCY > MACHINE_AUTHORITY
```

This prototype runs on the Python standard library; it does not claim to run Elasticsearch, PyOD, Datadog, Prophet, YARA or external AI anomaly models. Such providers can be evaluated as **optional future adapters**, with false-positive benchmarks and bounded licensing/cost controls.

## Signal definitions

| Detector | Measurement | Limits |
| --- | --- | --- |
| `REPEATED_PROSE` | Sequence-similarity >= 0.76 between the last two machine-authored chapter bodies | Similar prose is not plagiarism or proof of shared authorship; the score is not confidence |
| `REPEATED_PATHS` | Exactly matching interactive scene IDs and target edges across two consecutive fictional worlds | Matching topology may be intentional; changing labels alone does not imply a novel choice structure |
| `REUSED_NEWS_SOURCE` | Two consecutive chapters refer to an identical URL from the existing metadata feed | Headlines are not validated news facts; same URL alone is not evidence of deception |
| `STALE_RESEARCH_FEED` | Last archived metadata snapshot is more than 72 hours old | Unchanged snapshots may indicate stable upstream content, not collector failure |

Archive byte integrity is checked separately and any corruption fails the pipeline. A violation must not be turned into a creative discovery to justify ignoring it.

## Data and trust boundaries

- Sources: existing `book/`, `realities/`, `interactive/` and `archive/` files only. No unrestricted crawler or general shell access.
- Each `anomaly/events/anomaly-NNNNNN.json` contains a deterministic fingerprint, detector name, evidence file SHA-256 values, timestamp, observable explanation, story premise, and the exact state `detected_unverified`.
- `anomaly/manifest.json` records each event SHA-256 and its predecessor. The engine never changes an earlier event by design. Checksums detect changes relative to the manifest; they are **not** external signatures or proof of provenance ownership.
- Detector fingerprints are stable for known recurring pattern families, to avoid emitting essentially the same warning every hour. A changed evidence reference may therefore remain represented by an earlier warning rather than creating an endlessly growing list. Detector-version upgrades should introduce a versioned fingerprint policy.
- All generated writing is labeled machine-authored; archived article metadata is not copied as copyrighted full-text journalism.
- The distinct human-authored CMB canon repository is not an output of this workflow. No runtime tool can change its permissions.

## Recurring production cycle

1. Verify all existing receipts and anomaly evidence.
2. Fetch bounded metadata from CMB Global AI Watch, falling back only to already verified local snapshots when the collector cannot reach the source.
3. Observe novelty patterns before writing; append at most three previously unrecorded events.
4. The chapter generator may select one **unconsumed** anomaly record and incorporate its controlled fictional premise. No record is automatically promoted to a verified news event, doctrinal statement, or original human canon.
5. Append chapter, causal lens and interactive story to their separately chained archives.
6. Re-examine new output, append any eligible detector observations, verify all records, and commit generated paths only.

## Compact 666-worker receipt

Version `deterministic_seed_v1` records `cycle`, `source_count`, deterministic guild counts, hash of regenerated ballots, and hash of the canonical roster. A verifier independently regenerates all 666 bounded workers using `scripts.engine.run_agents(cycle, source_count)` and compares digests. Existing full `ballots` receipts are supported and remain unchanged. This is integrity evidence for deterministic task simulation, **not** proof that hundreds of independent AI models ran.

## Failure and recovery

If a historic chapter, archive snapshot, reality world, interactive graph, or referenced anomaly event has an integrity mismatch, the job fails **before** publishing new material. Restore from a trustworthy independent snapshot and audit the discrepancy; never automatically overwrite the old record to make checks pass. GitHub may delay scheduled jobs, so track missed schedules independently before claiming continuous operation.

## Responsible research expansion

Before introducing Isolation Forest or PyOD, accumulate a labeled dataset of legitimate rare events, normal repetition, and known faults. Evaluate detector precision, recall, false-alarm rate, and drift; compare against the deterministic baseline. Do not let a statistical detector autonomously certify a person's identity, medical status, criminal intent, or supernatural claim. Use local and access-controlled processing for reader-specific data.
