# ADR-0006 — Expand Relata into a Frontier Memory Research Lab

**Status:** accepted
**Accepted:** 2026-09-22
**Scope:** research identity, questions, outputs and bounded source-study diagnostics; no model or cross-system execution interface

## 中文摘要

Relata 扩展为「前沿记忆研究室」：定义、综合与批评 agent memory 的概念、开源实现、架构取舍与评价证据。通用 agent 场景和人机亲密关系内的研究都有独立地位；成人长期人机亲密与浪漫关系继续是 founding focus，现有 mixed-domain Case Lab 保持自己的对象与证据要求。文章、跨源综合与有条件的架构判断本身就是研究产出，不必等待 benchmark 平台。本决定不接受任何系统优劣结论、固定 ontology、评测协议或新的模型执行权限。

## English summary

Relata becomes a frontier memory research lab studying definitions, open-source implementations, architectural tradeoffs and evidence about agent memory. General agent uses and human–AI intimacy are both legitimate research contexts. Adult long-term intimacy remains a founding focus, and the existing mixed-domain Case Lab retains its evidence requirements. Synthesis and critical writing are research outputs in their own right. This decision accepts no system ranking, canonical ontology, evaluation protocol or additional model execution authority.

## Context and authority

The maintainer explicitly endorsed this semantic expansion on 2026-09-22, emphasizing the definition, synthesis and assessment of open-source memory projects on GitHub, their architectural strengths and limitations, a standalone article, and connections with Agent Memory Study (AMS).

ADR-0003 broadened memory content within a primary relationship deployment domain. That distinction remains useful, but it does not cover research whose question is about a general agent architecture without a relationship-specific application. The original evaluation-platform ambition also does not exhaust the lab's useful outputs.

## Decision

1. **Identity:** Relata is an open, community-grounded frontier memory research lab. It studies what agent memory means, how implementations turn past material or experience into present behavior, how that influence changes, and what evidence supports claims about it.
2. **Research scope:** concepts, public-source architecture studies, comparative synthesis, criticism, methods and bounded cases are first-class work. A study need not justify itself through romance or immediately produce a benchmark case.
3. **Application contexts:** general agent use and adult long-term human–AI intimacy may be studied separately or comparatively. Intimacy remains a founding focus with community expertise and relationship-local norms; it is not a universal eligibility filter. Neither context's requirements automatically become the other's quality standard.
4. **Existing Case Lab:** its longitudinal mixed-domain memory ecology, adult synthetic cases, controls, privacy commitments and acceptance requirements remain in force. Its coverage strata do not classify all agent memory research.
5. **Architectural judgment:** describe the actual system boundary and lifecycle before evaluating a design. State what a choice enables, what it costs or constrains, the conditions under which that matters, and the evidence. Separate source claims, inspected implementation, observed behavior and editorial interpretation. An absent, opaque or unexamined capability is not automatically a defect.
6. **Outputs:** source studies, System Cards, comparative essays and research articles may progress alongside case work. Source review does not require a live benchmark; runtime or comparative performance claims still need corresponding evidence and authorization. The existing implementation promotion gate does not gate ordinary source research or writing.
7. **AMS connection:** link selected public papers, readings and experiments with their original provenance and limits. AMS and Relata may overlap in methods. A link imports neither acceptance nor authority, and this decision does not merge projects or authorize changes to AMS.

## Supersession and retained boundaries

This decision supersedes ADR-0003's restriction of the overall research scope to a primary relationship deployment domain, including decision item 1 and any reading of its preserved alternatives that excludes independent general-memory research. It retains ADR-0003's mixed-domain continuity constructs and the existing relational case programme. Assumption 2 is revised accordingly.

ADR-0001's research-first approach, ADR-0004's bilingual policy, ADR-0005's narrow offline exception and the RC-005 input-only scope remain applicable. No runner, provider adapter, stable system interface, hosted service, Leaderboard, Arena, sealed corpus or canonical system ontology follows from the new identity. Existing consent, privacy, public-result and release boundaries remain applicable.

The maintainer also requested separate investigations of five public upstreams in this task. The resulting [source studies](../systems/source-studies/README.md) may retain two small, dependency-free offline diagnostic scripts for exact lmc-5 and Graphiti source revisions, with synthetic inputs and explicit observation limits. They import inspected local code or extract specified functions; they do not execute a model, use private state or define a reusable cross-system runner. This bounded research artifact does not widen the provider or service boundary.

## Alternatives and consequences

- Keeping all work subordinate to intimacy would exclude the newly accepted general architecture questions.
- Dropping the relational focus would lose an established research context and community contribution path without a maintainer request to do so.
- Treating the lab as a benchmark platform would confuse a research programme with an unvalidated implementation and scoring contract.

Current identity, authority, reading paths and census guidance must reflect the expansion. Historical observations and case evidence are not retroactively promoted. The initial [agent-memory inquiry](../research/agent-memory-inquiry.md) records open questions and source leads, not a completed survey or a settled article thesis.

## Review or reversal

Revise the scope through a later accepted decision if actual studies show an unhelpful overlap, an unmanageable research object or a better division of work. Individual article questions and sampling choices remain revisable research choices; they do not each require an identity decision.
