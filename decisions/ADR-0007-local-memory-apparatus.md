# ADR-0007 — Build a Bounded Local Memory Apparatus

**Status:** accepted for the maintainer-authorized implementation continuation on 2026-09-26; no evaluation protocol or capability result accepted
**Scope:** independently authored local experiment in a separate repository, working name `relata-memory`

## 中文摘要

在自有架构设计与测试映射之后，maintainer 要求继续推进。此次承接设计中第一次 `git init` 的完整本地路径：明确输入与来源/scope、持久保存、检索/context、scripted consumption、局部修订、重启、检查与导出恢复，并保留原始历史和简单文件搜索对照。选择 Python 标准库与 SQLite，先验证显式操作下的状态机制。实现放在独立本地 repo；Relata 保留研究记录与评价的独立性。此决定不授权模型/provider、私人材料、跨系统 runner、服务、部署或新 repo 的公开发布。

## English summary

The maintainer's continuation advances the own-memory design into its first complete local engineering loop: explicit input/provenance/scope, persistence, retrieval/context, scripted consumption, scoped revision, restart, inspection, export/restore, and raw-history/simple-file controls. The implementation uses Python's standard library and SQLite in a separate local repository. This authorizes a bounded state-mechanism experiment, not a model study, private-data import, cross-system runner, service, deployment, public repository creation or capability claim.

## Decision and rationale

1. Implement the local path proposed in [the design study](../research/own-memory-architecture.md), using explicit operations and public synthetic examples. Candidate B becomes an engineering hypothesis with an implementation; it is not accepted as superior to simpler candidate A or as a universal memory schema.
2. Reuse SQLite transactions and Python's standard library for one local persistent state owner. Do not build a database, external queue or framework. The current environment provides Python 3.13 and SQLite; no new production dependency is necessary. Atomic checks/mutations use a single transaction boundary, following [SQLite's transaction semantics](https://www.sqlite.org/lang_transaction.html) and [Python's sqlite3 interface](https://docs.python.org/3.13/library/sqlite3.html).
3. Preserve current versus historical material, declared provenance and acceptance evidence, scope, expected revisions, and derived-view freshness into observable use. Local caller declarations are not authentication or proof that a claim is true. Logical erasure and withdrawal must have stated coverage; neither recalls previously exported material nor promises physical media erasure.
4. Keep raw-history and simple-file controls inspectable. Explicitly prepared operations can test state mechanisms, but cannot demonstrate extraction quality, semantic use, memory necessity, long-term utility or comparative superiority. Do not feed Case Lab evaluator keys into the apparatus or present a development demo as a completed case.
5. Keep implementation in a separate local Git repository. This split separates an experimental system from its research/evaluation programme; it does not implement the historical public/sealed/operations three-repository scheme. The new repository has no remote or public license by default. Research documentation remains here.

## Retained boundaries

ADR-0001's research discipline, ADR-0004's language policy, ADR-0005's specific rehearsal and ADR-0006's plural lab identity remain in force. This decision narrowly permits one first-party local experimental runtime; it does not promote a stable system-under-study API, SDK, benchmark runner, hosted infrastructure, canonical ontology, model/provider integration, live personal memory, or existing Case Cards. Cross-system evaluation retains its separate promotion gate.

## Alternatives and review

Continuing only design documents would leave the requested state mechanisms untested. Building a hosted or model-backed application now would add execution and data boundaries that this task has not chosen. A local explicit-input apparatus makes the mechanisms inspectable while keeping those choices separate.

Revisit candidate B when simple file/history controls meet the same need with less burden, or when observed failures require changing the state model. New claims must bind actual code, inputs, operations, outputs and limits. The [experiment record](../experiments/local-memory-apparatus.md) owns engineering observations; this decision records scope, not successful execution.
