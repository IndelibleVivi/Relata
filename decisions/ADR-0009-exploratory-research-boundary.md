[简体中文](ADR-0009-exploratory-research-boundary.zh-CN.md) | **English**
<!-- language: en; mirror: ADR-0009-exploratory-research-boundary.zh-CN.md; translation-status: synchronized -->

# ADR-0009 — Separate Bounded Exploratory Execution from Benchmark Promotion

**Status:** proposed; not accepted or activated
**Prepared:** 2026-09-27
**Scope:** a candidate execution boundary for the [first research cycle](../research/first-research-cycle.md); no execution, spending, hosting or result-publication authority is granted by this draft

## 中文摘要

建议为有明确对象、公开成人合成材料、配置、预算与停止条件的探索性实测建立独立边界，使其能够先于正式 benchmark promotion 产生有界观察。一个获准研究包内的重复运行、诊断与条件变化无需逐项重新审批；越出对象、数据、费用或外部操作范围才需要新决定。本文仍为 proposed；既有 STATUS、CHARTER 与 AGENTS 的执行限制保持有效。计划、代码、运行证据、案例接受、比较主张和公开发布是不同状态。

## English summary

This proposal would permit bounded exploratory studies before formal benchmark promotion, through a named study envelope covering exact subjects, public adult synthetic material, configurations, resource limits and stopping conditions. Authorized repetitions, diagnostics and condition changes would not need individual approvals. The draft changes no current authority: execution, case acceptance, comparative claims and publication remain distinct decisions with their own evidence.

## Context and evidence

[ADR-0008](ADR-0008-three-core-research-functions.md) accepts benchmark research, system collection and incubation as independent, mutually supporting functions. [STATUS](../STATUS.md) records ten source-study drafts, an offline atlas, scripted RC-002 rehearsal and eighteen unanswered RC-005 inputs, but no model-backed comparative results. The [test map](../research/memory-design-test-map.md) already identifies controls and unexecuted mechanism questions.

[ADR-0005](ADR-0005-offline-pilot-tooling.md) permits a narrow scripted rehearsal; it supplies neither a provider adapter nor permission to run real systems. The present cross-system implementation gate protects a broader evaluation programme. A separate bounded exploration route could produce the observations needed to revise cases, expose adapter contributions and challenge candidate designs, while leaving formal comparison requirements intact. This is a governance proposal, not evidence that any selected system or evaluator is ready.

## Proposed decision

### 1. Accept a narrow exception, not a general platform

If accepted and reflected in the current authority surfaces, this ADR would allow study-specific connectors, isolated subject environments, model calls and evidence recording **only within a maintainer-authorized study envelope**. A local database or process required by a named subject may be part of that envelope. It would not authorize a stable cross-system API, general benchmark runner, SDK, hosted orchestration, public service, Leaderboard, Arena or canonical ontology.

The envelope belongs in the relevant study's record, using the existing [pilot record](../experiments/pilot-record-template.md) where suitable. It is a human-readable agreement, not a new mandatory runtime schema. One envelope may cover several named subjects, cases and configuration ranges; it need not be renewed for every run or condition already inside those ranges.

### 2. Make the actual permission concrete

Before subject execution, the envelope must resolve the following facts and choices:

| Item | What the accepted envelope must identify |
|---|---|
| Research target and subjects | Question, exact public source revision or product version, complete-agent / memory-support / combined boundary, and included cases or bounded family-generation scope |
| Inputs and exposure | Public adult synthetic sources and revisions, locale, allowed history, evaluator separation, fixed replay or co-evolving interaction, and isolated test state |
| Effective configuration | Model/provider and endpoint category, reader/harness, prompts, tools/hooks, context policy, relevant dependencies, permitted variation and adapter contribution; no credentials in the record |
| Resources and external effects | Approved provider/account use, cost cap and currency, included ingestion/embedding/maintenance/review calls, usage accounting, retry reserve, and allowed local processes; hosting and external actions are separately named or excluded |
| Evidence and stopping | Local artifact destination, observable stages, raw outcomes and failures, review needs, claim limits, operator, and conditions for stopping or resuming |

Names on a candidate list are not installation or readiness evidence. A subscription, credential, public endpoint or working connector is not permission to use it. Manual browser calls to a model are still subject execution; changing transport does not avoid this boundary. Research inputs must not inherit personal memory, unrelated account context or the evaluator key from the engineering environment.

Acceptance of this ADR and a completed envelope may occur together. An envelope with an unresolved provider, account authorization or spending cap cannot start dependent calls; preparing public inputs and studying source can continue within existing authority.

### 3. Allow useful iteration within that envelope

The operator may repeat runs, inspect failures, repair connector defects and vary declared conditions without returning for approval each time. Record the actual configuration and every attempt. If a repair changes what the system received or which component solved the task, mark the affected runs and repeat only the comparisons needed to restore a valid interpretation; preserve earlier failures.

Pause dependent execution when the resource cap cannot cover the next bounded operation, actual input exposure violates the study, the subject/configuration identity is unresolved, or state isolation fails. Resume after an in-scope repair and verification; obtain new authority only for an expanded subject/data/resource/external-action envelope. Existing local analysis need not stop. Do not launch unbounded automatic retries; count unsuccessful and repair calls against the cap. Where provider billing is delayed, reserve a conservative allowance before dispatch.

### 4. Keep evidence levels separate

An exploratory record may say that a named configuration produced a preserved response or action under stated conditions. It does not thereby accept the case, establish memory necessity, identify the responsible mechanism, validate a semantic evaluator or rank a product.

Current-only and ingest-then-disable are different controls. Full history, searchable raw source, author-selected reference context and supported native conditions answer different questions. Complete native systems and fixed-reader memory components are not automatically comparable. Adapter-created extraction, provenance, temporal filtering, routing or state belongs to the combined pipeline. Missing visibility remains unknown, not automatic failure. [Claim-boundary labels](../research/claim-boundary-study.md) remain candidate terminology; this ADR would not accept their ladder or schema wholesale.

Exploratory outputs can precede independent semantic review if labeled unreviewed. Case acceptance and contested semantic conclusions still need the relevant review evidence and recorded disagreement. Exact artifact checks need no ceremonial human approval; model cross-review does not become independent human calibration. No automatic hard semantic scorer follows.

### 5. Separate recording, publication and deployment

Keep raw working outputs in the existing ignored local artifact area; see [experiments](../experiments/README.md). Public source material and synthetic inputs do not make all runtime logs public-safe: credentials, personal context, private service details and identifying review data stay out of Git.

A public exploratory exhibit requires an explicitly selected, reviewed packet and the applicable publication and rights decision. It must retain its exact object, conditions, missing evidence and unreviewed judgments. Permission to execute does not publish a result, grant licenses, send invitations or deploy a website. Existing source research and local reader development retain their independent scope; public hosting needs its own authority.

## Relationship to existing authority

**While proposed:** no existing gate changes. [STATUS](../STATUS.md), [CHARTER](../CHARTER.md), [ASSUMPTION_REGISTER](../ASSUMPTION_REGISTER.md) and [AGENTS](../AGENTS.md) remain current authority. The first research cycle is planning material. Neither its existence nor this ADR's presence permits implementation or model execution.

**On acceptance:** update STATUS, CHARTER, ASSUMPTION_REGISTER, AGENTS and affected bilingual reading paths in the same change. State explicitly that this named exploration exception does not require prior completion of the formal cross-system implementation promotion gate. Retain that gate for promotion of a reusable evaluation boundary and formal coverage/comparison claims; do not silently delete its distinctions, System Cards, memory necessity, reviewer-disagreement, contribution-path or adapter-pressure requirements. If those requirements themselves need revision, record the specific change and rationale rather than treating this exception as their removal.

ADR-0007's correction remains in force. This proposal does not accept candidate B as Tilia's architecture, authorize continued product development in the retained `relata-memory` experiment, import private memory, or make a system's internal schema the evaluator's answer format. A separately authorized research prototype is a system under study, not an accepted product design.

## Alternatives and consequences

| Alternative | Consequence |
|---|---|
| Retain only current offline exceptions | Source research and input preparation continue; model-backed studies remain outside the accepted execution boundary |
| **Recommended: named exploratory envelopes** | Enables targeted observations and iteration while preserving cost/data ownership, architectural differences and evidence status |
| Authorize a general evaluation platform now | Commits to shared interfaces and operations before their distortions and maintenance needs are demonstrated; not recommended by this proposal |

The proposed exception reduces repeated permission questions inside a settled experiment, while requiring the initial packet to be concrete. Public-source studies do not need maintainer endorsement from the studied project. Community participation remains optional; restricted contributions retain consent and stewardship requirements, and this ADR authorizes no outreach or human-participant study.

## Review, acceptance and reversal

The maintainer can accept, revise or reject the proposed boundary after reviewing the research plan and a concrete execution envelope. Acceptance must name scope and update the authority surfaces above; a source commit or passing test is insufficient. Study execution then stops at its own resource/evidence limits, rather than remaining perpetually enabled.

At the cycle review, decide whether the exception should expire, continue within a new envelope, or inform a later implementation decision. Retain observations that contradict the plan and document material exclusions. Acceptance of a later platform, ranking policy, release, website deployment or Tilia implementation remains separately identifiable.
