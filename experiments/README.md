# Relata Experiments

R0 experiments are local, small, and evidence-producing. They investigate cases, observation boundaries and authorized state mechanisms; they do not create benchmark releases or rankings.

## Available offline tools

- [RC-002 execution rehearsal](offline-rehearsal.md) — bundled scripted subject, transport/evidence checks; no model evaluation.
- [RC-005 input preparation and audit](continuity-input-audit.md) — 18 unanswered speaker-preserving checkpoint inputs, source-bound verification, and literal projection collisions; no subject execution.

Both use public adult synthetic material and local derived artifacts. They retain separate responsibilities; the RC-002 text-only tape is not the RC-005 input boundary.

## Retained early apparatus experiment

[Local memory apparatus](local-memory-apparatus.md) records the already-written `relata-memory` experiment retained after the scope correction in ADR-0007. Explicit operations, raw-history/simple-file controls and a scripted consumer test state behavior. The code lives in a separate local repository; it is very early, lacks vector retrieval, and is neither formal Tilia nor a completed Case Lab study. Retention does not supply a new implementation mandate.

## Response-level controls

Every response-level case should consider:

- current-turn-only;
- no-memory;
- full minimal history;
- reference-context;
- system-native.

Not every system exposes the same internal artifacts. Missing observability limits attribution; it does not automatically become failure.

## Local artifact packet

Keep working outputs under an ignored local path:

```text
experiments/artifacts/<pilot-id>/<run-id>/
├── pilot-record.md
├── inputs/
├── outputs/
└── review/
```

Start `pilot-record.md` from [`pilot-record-template.md`](pilot-record-template.md). Record the exact case revision, system or model version, prompt/configuration, run date, manual intervention, output paths, review assignment, disagreement, and decision.

Only a separately reviewed, public-safe packet may later move to a tracked publication path. The current repository has no released pilot artifacts.

## Interpretation rule

A good final response does not prove the memory system succeeded. A bad final response does not identify a failed layer unless observable evidence supports that attribution. Preserve `unknown`, `opaque at this boundary`, case ambiguity, and evaluator failure as separate outcomes.
