[简体中文](ADR-0008-three-core-research-functions.zh-CN.md) | **English**
<!-- language: en; mirror: ADR-0008-three-core-research-functions.zh-CN.md; translation-status: synchronized -->

# ADR-0008 — Make Three Research Functions Core to Relata

**Status:** accepted
**Accepted:** 2026-09-26
**Scope:** project identity, research responsibilities and reading paths; no new execution or publication authority

## 中文摘要

Relata 将三项相互支持的职责纳入核心定位：自己的 benchmark 研究、可检查与比较的系统样本研究空间，以及面向未来记忆装置的 incubator。第二项可以称为 museum、样本间或研究室，正式名称仍开放。现有案例、源码研究、架构图与候选设计分别是这些职责的积累，不因此成为已验证 benchmark 或已接受架构。AMS 与 Relata 各自保持独立研究价值，也都可以为长篇综合写作提供依据。未来 Tilia 的产品源码位于独立项目。

## English summary

Relata makes three mutually supporting functions core to its identity: its own benchmark research, an inspectable collection of system studies, and an incubator for future memory systems. The collection's name remains open: museum, sample room and research lab are working possibilities. Existing cases, source studies, architecture views and candidate designs support these functions without becoming a validated benchmark or accepted architecture. AMS and Relata retain independent research value and can both inform long-form synthesis. Future Tilia product source belongs in a separate project.

## Context and authority

The maintainer explicitly endorsed these three functions as Relata's core meaning on 2026-09-26. [ADR-0006](ADR-0006-frontier-memory-research-lab.md) established the broader research lab; corrected [ADR-0007](ADR-0007-local-memory-apparatus.md) separated the independent Tilia goal from implementation within Relata. This decision makes the lab's responsibilities clearer while retaining both decisions' boundaries.

## Decision

1. **Own benchmark research.** Relata develops its own questions, cases, controls, evaluation methods, experiments and evidence-backed comparisons. The [Case Lab](../case-lab/README.md) and existing methodology studies are foundations for that work. Relata advances this programme itself; collecting third-party scores does not define its role. Current R0 evidence and execution limits remain explicit in [STATUS](../STATUS.md).
2. **System collection.** Relata makes memory systems inspectable through source studies, System Cards, architecture views and conditional comparisons. The [System Census](../systems/README.md), [source studies](../systems/source-studies/README.md) and [architecture atlas](../systems/architecture-atlas/README.md) are existing entrypoints. Each study retains its version, system boundary, coverage and evidence limits. The museum / sample-room / lab name remains open; this decision requires no new directory, interface or permanent classification.
3. **Incubator for future systems.** Relata develops design hypotheses, alternatives, counterexamples and lessons from its studies and cases. The [candidate design](../research/own-memory-architecture.md) and [test map](../research/memory-design-test-map.md) are current research artifacts. Future Tilia product source belongs in its own project. Incubation does not make a preferred design the evaluator's ontology or answer format.
4. **Mutual support without a mandatory sequence.** System studies can expose questions for cases; benchmark research can challenge architectural claims; both can inform future designs, whose unresolved choices can return as research questions. Each function can produce useful work independently. These are research responsibilities, not benchmark tracks or a universal memory taxonomy.
5. **AMS and writing.** [Agent Memory Study](https://github.com/IndelibleVivi/agent-memory-study) and Relata may both read papers, inspect source and run appropriately authorized experiments. Relata draws on existing AMS work for its own benchmark, system studies and design questions, carrying over provenance, conditions, counterexamples and uncertainty. Gaps can inform further AMS research. Both projects can support long-form writing while retaining their own questions, artifacts and value; this decision neither merges them nor authorizes cross-repository edits.

## Alternatives and consequences

- A benchmark-only identity would hide the independent value of system studies and design research.
- A source-reading collection alone would leave Relata's own evaluation responsibility unclear.
- A product incubator that also hosts Tilia implementation would repeat the scope error corrected by ADR-0007.

README, Charter, Status, agent guidance and research entrypoints must expose the three functions and their existing artifacts. Source observations, proposed transfers, executed experiments and accepted results keep their original status. Definitions and synthesis can develop without a predetermined article thesis.

## Retained boundaries and review

This decision supplements ADR-0006 and ADR-0007. It accepts no benchmark release, scoring contract, system ontology, Tilia architecture, runner, provider adapter, hosted service or new model execution. Existing offline exceptions, case acceptance, privacy and implementation promotion requirements continue to govern their own scope. No code, repository or live memory state is moved or renamed.

Terminology and research emphasis can evolve with the work. Any later change to implementation authority, project boundaries or public evidence claims needs its corresponding decision and evidence; selecting the collection's eventual name does not itself authorize those changes.
