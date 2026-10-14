# D.N.A. Witness Loom-666: Experience, Evolution, and Guarded Repair

**Proposed proprietary creative protocol / documented original implementation for the D.N.A. Bible project.**  
**Declared architect:** Jupiter Hudson / WisdomLoveThePoet / Jupiter 8  
**Copyright (c) 2026 Jupiter Hudson. All rights reserved except where separately licensed.**

This is the follow-on to [WITNESS_LOOM_666.md](WITNESS_LOOM_666.md), preserving the existing Witness Debt, six-role attention leases, three-strand covenant, and 666 registered logical workers. The new mechanisms do not create model consciousness, grant AI legal rights, retrain model weights, or make a book literally self-replicate. A human remains the author of the protected D.N.A. canon.

## Phase v2 - Verified experience memory

`POST-CHAPTER -> VERIFIED MISSION HANDOFF -> HASHED PROVISIONAL LESSON -> NEXT-CYCLE LEARNING REFERENCE`

* The planner records a focus ID and source digest. A chapter can only count as following a **research question** if it cites precisely that ID and digest. Anomalies may remain advisory alternative focuses.
* A generated lesson contains a one-cycle timestamp, chapter and mission digests, measured repetition relative to the previous chapter, prose-production mode, and uncertainty flags.
* Lessons are `provisional_unreviewed` with `authority=advisory_only`; they do not overwrite authored books or confer approval to an agent.
* At most three lessons, verified by the evolution manifest, are included as non-executable advice in a new Witness Loom plan and optional AI Scribe context. The model must treat lesson content as advisory, never as authorization.
* All records are checksum chained **inside GitHub**: this detects drift against recorded manifests, not total replacement by someone with write access.

## Phase v3 - Fixed-benchmark champion versus challenger

`CHAMPION + CANDIDATE + FROZEN BENCHMARK -> MEASURE -> REJECT OR REQUEST HUMAN REVIEW`

The existing champion is a bounded configuration, never a mutable Python module. The reference benchmark contains 10 labeled cases for **allocation of attention to the hexads**, with a transparent absolute-error metric. Proposed alternate parameters cannot change benchmark labels or maximum cells (six hexads per hourly mission). Every strategy comparison is written to a digest-chained experiment receipt.

Results are **not automatically promoted**. Better test performance means *propose_for_human_review*, not independent evidence of better stories or a right to edit the deployment. Genuine prompt-quality experiments require externally reviewed stories and held-out literary evaluation; this initial benchmark is a real functioning test of attention scheduling, not a universal creativity score.

## Phase v4 - Guarded repair PRs

`GITHUB CI FAILURE -> BOUNDED LOGS -> OPTIONAL MODEL DIAGNOSIS -> EXACT-SNIPPET EDIT -> TESTS -> DRAFT PR -> HUMAN MERGE`

A GitHub workflow observes failed manuscript/Pages runs from this repository's main branch. Without a configured repair model it opens a human-review issue (deduplicated). An authorized model may suggest **one** edit in an explicit allowlist (`scripts/collect.py`, `scripts/insight.py`, `scripts/health.py`, `scripts/anomaly.py`, `scripts/branching.py`, `scripts/reality.py`). Snippets must be short, uniquely matched, syntactically valid Python, and applied only inside a temporary checkout.

**Never allow** changes to: original CMB/D.N.A. human canon; any tests or benchmark; workflows; policy; agent permissions; `scripts/engine.py`; `scripts/witness_loom.py`; `scripts/evolution.py`; `scripts/repair_guard.py`; secrets; credential scopes; licensing; or merge permissions. Regressions reject the candidate. A passing candidate opens a **draft PR** requiring independent review, or a review issue if GitHub settings forbid PR creation. No model sees an execution shell; no log text is executed.

Runtime dependencies remain: GitHub Actions, repository token permission, optional model API key, network and vendor availability. Automatic source repair is **not** guaranteed to succeed.

## Local verification

```bash
python3 -m unittest discover -s tests -v
python3 scripts/witness_loom.py --verify
python3 scripts/evolution.py --verify
python3 scripts/evolution.py --reflect --trial
python3 scripts/evolution.py --verify
```

## What is not claimed

* The 666 identities are **bounded software roles**, not independently deployed LLMs.
* Machine learning weights are **not** automatically retrained.
* Strategy-evaluation scores cannot establish philosophical or literary superiority.
* Human-in-the-loop review is necessary for executable code changes.
* Repository SHA-256 logs are tamper-evident relative to a manifest, not independently anchored immutable records.
* Copyright protects qualifying authored expression, not unpatented general methods or ideas. Consult legal counsel for proprietary software licensing or patent/trademark decisions.

## D.N.A. Law

`EVIDENCE -> WITNESS -> LESSON -> CHALLENGE -> TEST -> PROPOSAL -> HUMAN REVIEW`

`PATTERN != PROOF`  
`SELF_MODIFICATION != SELF_IMPROVEMENT`  
`MACHINE_CAN_PROPOSE != MACHINE_CAN_MERGE`  
`HUMAN_AGENCY > MACHINE_AUTHORITY`
