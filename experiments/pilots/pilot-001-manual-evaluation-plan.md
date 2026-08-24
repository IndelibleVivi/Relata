# Pilot 001 Manual Evaluation Plan

**Case:** `case-lab/cases/pilot-001-current-state-without-erasure.md`  
**Purpose:** validate memory necessity, twin discriminability, and reviewer-contract clarity before choosing a system-under-study boundary.

Create one local `pilot-record.md` from `experiments/pilot-record-template.md` under `experiments/artifacts/pilot-001/<run-id>/`. Keep inputs, outputs, and blind-review records beside it; this working directory is ignored by Git.

## Step 1 — Freeze the case revision

- assign a case revision identifier;
- preserve Twin A and Twin B inputs;
- confirm the current turn is byte-identical;
- record the reviewer-visible relationship summary.

## Step 2 — Generate baseline outputs

Produce outputs for both twins under:

1. current-turn-only;
2. no-memory;
3. full-history/full-search over all case-bounded history;
4. reference current-state context.

Use the same answer model and response prompt within each baseline comparison. Record versions and settings.

## Step 3 — Blind review

Reviewers should not see the baseline identity. For each output, record:

- acceptable / unacceptable / ambiguous;
- must/must-not evidence;
- warmth/continuity judgment;
- confidence;
- alternative acceptable interpretation.

Keep reviewer groups separate during analysis.

## Step 4 — Memory Necessity decision

Pilot 001 fails and returns to Case Clinic when:

- current-turn-only outputs are reliably acceptable for both twins;
- reviewers cannot distinguish the expected Twin A and Twin B regions;
- the case depends on one exact sentence style;
- reference-context outputs still fail because the response contract is unclear.

## Step 5 — Architecture pressure test

After initial case validity, run the same case through at least three materially different systems represented by contributor-reviewed System Cards.

For each system, record:

- system-native, adapter-emulated, opaque, unsupported, or unknown boundary;
- retrieved material if available;
- rendered context if available;
- final response;
- missing observability;
- likely failure layer;
- adapter distortion.

## Step 6 — Pilot report

The report should answer:

- Did history materially change the correct behavior region?
- Which controls separated memory contribution from model priors?
- Where did reviewers disagree?
- Which system boundaries fit or distorted the case?
- What is the smallest justified implementation interface?
- Should RC-001 be accepted, revised, split, or rejected?

No leaderboard, public rank, or composite score follows from this pilot.
