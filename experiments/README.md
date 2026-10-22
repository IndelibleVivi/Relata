# Relata Experiments

R0 experiments are local, small, and evidence-producing. They investigate cases, observation boundaries and authorized state mechanisms; they do not create benchmark releases or rankings.

## Available offline tools

The [future-question input diagnostic](../research/future-question-memory/README.md) computes task-relative collisions and global answer-region intersections for seven fixed authored families. Run `python3 -B tools/future_question_inputs.py audit` and `check`; `show` exposes source-only views without loading the separate answer contract. Source lookup returns actual current, missing, denied or known-stale material. No subject or semantic scorer is executed, and no benchmark case is promoted.

- [RC-002 execution rehearsal](offline-rehearsal.md) — bundled scripted subject, transport/evidence checks; no model evaluation.
- [RC-005 input preparation and audit](continuity-input-audit.md) — 18 unanswered speaker-preserving checkpoint inputs, source-bound verification, and literal projection collisions; no subject execution.

Both use public adult synthetic material and local derived artifacts. They retain separate responsibilities; the RC-002 text-only tape is not the RC-005 input boundary.

## Authorized fixed-study research

[ADR-0009](../decisions/ADR-0009-exploratory-research-boundary.md) is accepted on 2026-10-23, activating only the [RC-005 → pinned Mem0 execution packet](rc005-native-execution-packet.md). Its fixed-study CLI covers 54 reader preflight, 36 raw-source control and 54 native answer positions; source implementation and offline plumbing checks do not prove live runnability or semantic success. Existing generation entitlement and local Qwen3-Embedding-0.6B-Q8_0/1024 are the selected resources, with 300 chat / 500 embedding client dispatches including failures and diagnostics, no recharge or paid fallback. Native states, attempts, responses and unreviewed blind packets remain ignored local artifacts. Formal benchmark promotion, other study envelopes, Tilia product implementation, publication, hosting, outreach and licensing retain their separate boundaries. [ADR-0010](../decisions/ADR-0010-bounded-provider-compatibility-checks.md) remains the independent compatibility-only exception; matching protocol evidence may be reused.

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

## Fixed-study offline review

The [future-question study workflow](../research/future-question-memory/README.md#离线-responsereview-闭环) prepares and verifies the fixed authored inputs, imports already supplied response states, exports blind review items, appends reviewer judgments and recomputes per-family counts. It has no subject/model/provider execution seam. `show` is author inspection; input bodies come from the allowlisted export. Keep the hidden mapping out of model input, send reviewers only their blind `items` plus governing evidence, and retain imported records locally in ignored artifacts.

该工具只核验当前固定bundle与本地导入，不能证明外部回答实际来自所声称的系统，也不替代run payload/attempt/state证据。导入provenance如实描述人工测试或外部来源；未执行、失败和未评审分开，不把示例回答发布为系统结果。
