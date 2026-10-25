# Case Reviews

Store one review file per case and review round:

```text
RC-001-review-01.md
```

A review records:

- reviewers and disclosed perspective pool;
- baseline outputs examined;
- checklist result;
- disagreements;
- requested changes;
- accept/revise/split/reject decision;
- links to preserved pilot artifacts.

## Fixed RC-005 response review

The [offline review desk and operator procedure](workbench/README.md) implements first-blind-pass response review for the existing native RC-005 anonymous export. The [standalone interface](workbench/index.html) includes a clearly labelled public authored practice packet, resumable drafts and preserved amendments. `tools/rc005_review.py` verifies original-run binding, imports cumulative judgments and produces descriptive disagreement reports. Mutable packets, drafts, judgments, snapshots and reports stay in ignored local/private workspaces; they are not case acceptance records or public results. This does not exercise external reviewer recruitment or validate the development worksheet.

## Candidate calibration material

- [`RC-001 E0 evaluator calibration pack`](RC-001-e0-calibration-pack.zh-CN.md) — authored zh-CN anchors, normalization candidate, reviewer questions, and disagreement categories; not yet dry-reviewed and not a case-review disposition.

Calibration fixtures are not evaluated system outputs. Their presence does not validate the evaluator or change RC-001's `clinic-ready` state.
