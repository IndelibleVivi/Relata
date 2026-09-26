# ADR-0007 — Correct the Local Apparatus Scope

**Status:** corrected on 2026-09-26 following maintainer clarification; the earlier claim of implementation authorization is withdrawn because the original “accepted” status misread a long-term goal as an implementation request
**Scope:** distinguish Relata research, the future independent Tilia goal, and an already-written early experiment retained for inspection

## 中文摘要

Maintainer 澄清：从零编写自有记忆装置是长期 **goal**，不是要求在 Relata 中启动实现；未来独立装置以 **Tilia** 的名字承接。协调者把“继续推进研究”误读成了立即实现，并据此写下原 ADR。即使代码位于独立 repo，也不能使这项误读成为授权。现保留已经写出的 `relata-memory` 作为非常早期的工程实验，不将其认定为正式 Tilia、已接受架构或后续实现任务。

Tilia 的预期设计必须包含向量语义检索；编码小模型可作为研究候选，具体模型与集成方式尚未选择。现有实验只有字面检索，未达到这项要求。Relata 继续推进定义、源码研究、架构图、比较文章与 cases；其研究可以为独立 Tilia 提供依据，不承担 Tilia 产品身份。

## English summary

The maintainer clarified that an independently authored memory apparatus is a long-term goal, to be pursued under the name **Tilia**, not an instruction to start implementation within Relata. The coordinator incorrectly promoted research continuation into implementation authority. The already-written local `relata-memory` code is retained as a very early engineering experiment; it is neither the accepted Tilia architecture nor an ongoing implementation mandate. Vector-based semantic retrieval is required for the intended Tilia system, with encoder models still open for research. The experiment's literal search does not meet that requirement. Relata remains an independent research lab.

## Historical implementation rationale — not current authority

The following choices explain the retained experiment. They record what the coordinator implemented under the mistaken scope interpretation; they do not represent maintainer acceptance of an architecture or permission to extend it.

1. Implement the local path proposed in [the design study](../research/own-memory-architecture.md), using explicit operations and public synthetic examples. Candidate B becomes an engineering hypothesis with an implementation; it is not accepted as superior to simpler candidate A or as a universal memory schema.
2. Reuse SQLite transactions and Python's standard library for one local persistent state owner. Do not build a database, external queue or framework. The current environment provides Python 3.13 and SQLite; no new production dependency is necessary. Atomic checks/mutations use a single transaction boundary, following [SQLite's transaction semantics](https://www.sqlite.org/lang_transaction.html) and [Python's sqlite3 interface](https://docs.python.org/3.13/library/sqlite3.html).
3. Preserve current versus historical material, declared provenance and acceptance evidence, scope, expected revisions, and derived-view freshness into observable use. Local caller declarations are not authentication or proof that a claim is true. Logical erasure and withdrawal must have stated coverage; neither recalls previously exported material nor promises physical media erasure.
4. Keep raw-history and simple-file controls inspectable. Explicitly prepared operations can test state mechanisms, but cannot demonstrate extraction quality, semantic use, memory necessity, long-term utility or comparative superiority. Do not feed Case Lab evaluator keys into the apparatus or present a development demo as a completed case.
5. Keep implementation in a separate local Git repository. This split separates an experimental system from its research/evaluation programme; it does not implement the historical public/sealed/operations three-repository scheme. The new repository has no remote or public license by default. Research documentation remains here.

## Current disposition and boundaries

ADR-0001's research discipline, ADR-0004's language policy, ADR-0005's specific rehearsal and ADR-0006's plural lab identity remain in force. Retain the existing code, diagrams and bounded engineering evidence. The directory/package name `relata-memory` / `relata_memory` is historical; this correction does not rename or migrate it, establish a formal Tilia implementation, or authorize feature expansion. No stable system-under-study API, SDK, benchmark runner, hosted infrastructure, canonical ontology, model/provider integration, private-data import, release or deployment follows. Cross-system evaluation retains its separate promotion gate.

## Evidence and future design

The experiment makes selected state mechanisms inspectable, but its existence and passing tests do not settle the intended system's design. Candidate B remains a proposal that may change or be replaced; its schema must not become Relata's evaluator contract. Vector retrieval is a Tilia requirement, not a claim that all memory research must use vectors.

The [experiment record](../experiments/local-memory-apparatus.md) preserves actual code, inputs, operations, outputs and limits. The [design study](../research/own-memory-architecture.md) and test map remain research inputs to future discussion, not a completed product SPEC. The earlier wording remains recoverable in Git history.
