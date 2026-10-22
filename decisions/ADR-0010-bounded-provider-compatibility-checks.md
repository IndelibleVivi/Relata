[简体中文](ADR-0010-bounded-provider-compatibility-checks.zh-CN.md) | **English**
<!-- language: en; mirror: ADR-0010-bounded-provider-compatibility-checks.zh-CN.md; translation-status: synchronized -->

# ADR-0010: Bounded Provider Compatibility Checks

**Status:** accepted
**Accepted:** 2026-10-23
**Scope:** one operator-owned compatibility check at the public interface boundary; no memory-system evaluation or general execution authority

## 中文摘要

Maintainer 另行接受一项很窄的 provider 兼容性检查，用于确认已授权接口能否解析普通请求与返回、呈现 usage 与模型或服务身份，并返回具有稳定批量顺序的有限 embedding 结果。它只使用公开原创合成文本，不做记忆能力、案例、排名或语义正确性评估。本兼容性决定本身不授予 native 权限；另行接受的 [ADR-0009](ADR-0009-exploratory-research-boundary.md) 仅激活 [RC-005 → Mem0 执行包](../experiments/rc005-native-execution-packet.md) 的 144 个回答位置与该包现行资源限制，旧 USD 10 方案已被替代。精确运行观察留在私有 operator 记录；本公共决定不发布运行结果。

## English summary

The maintainer separately accepted a narrow provider compatibility check. It verifies that authorized interfaces can parse ordinary requests and returns, expose usage and model or service identity when available, and return bounded embeddings with stable batch order. It uses only public original synthetic text and evaluates no memory capability, case, ranking or semantic correctness. This compatibility decision itself grants no native authority; separately accepted [ADR-0009](ADR-0009-exploratory-research-boundary.md) activates only the 144-position [RC-005 → Mem0 packet](../experiments/rc005-native-execution-packet.md) under that packet’s current resource limits, superseding its historical USD 10 plan. Exact runtime observations stay in private operator records; this public decision publishes no runtime result.

## Context and authority

The maintainer allowed limited test model calls on 2026-10-23. Generation should use an already available generation entitlement without replenishment or a paid fallback. Embeddings should use an already available local Qwen model or Workers AI, with no recharge or alternative paid provider. Actual account identity, credentials, endpoint details, balances and private configuration stay outside this public record.

ADR-0010 remains a self-contained compatibility exception. ADR-0009 was separately accepted on 2026-10-23 solely for the RC-005 → pinned Mem0 packet; its 144 positions, native execution and resource limits derive from that packet, not this smoke. Matching protocol observations may be reused. No general runner, paid fallback, result publication or capability claim follows.

## Decision

### 1. Fixed request envelope

The coordinator selected the following cumulative dispatch budget for this first check; these numbers are an execution choice, not a maintainer-imposed limit on all future in-scope tests:

- at most 6 generation requests in total, each with an output limit of at most 2,048 tokens;
- at most 4 embedding requests in total, each containing at most 8 texts; every text is public original synthetic material of at most 2,000 characters; and
- failed, timed-out and malformed client dispatches count against the respective total. The client performs no automatic retries. Downstream provider retries or pool fallbacks may be opaque: record that limit rather than claiming the dispatch count bounds all upstream attempts.

All inputs must be public original synthetic text. The check may use the existing generation entitlement and an existing local Qwen or Workers AI embedding path. It may not replenish an account, select a paid fallback, or add another provider. Missing authorization for any intended path stops that path rather than widening the scope.

### 2. Observable compatibility only

The check may inspect only whether:

- requests are accepted and responses can be parsed;
- ordinary text and JSON-object response forms are handled as declared by the interface;
- usage and effective model or service identity are visible, absent or insufficiently attributed;
- embedding responses expose vector dimension and finite numeric values; and
- an embedding batch preserves input order and length for the submitted synthetic texts.

An absent usage or identity field is recorded as unavailable; it is not reconstructed from assumptions. A valid response demonstrates transport and shape compatibility only. It does not validate answer quality, memory, retrieval, retention, correction, routing, relationship behavior or any system under study.

### 3. Evidence and publication boundary

This check is operator-owned. No public replay command is supplied by this decision, and the repository contains no executable entrypoint for it. If a later operator report is incorporated, it must state the provider category, request counts, synthetic-only input boundary, parse and visibility observations, embedding dimension, finite-value result, batch-order result and recorded failures without exposing private account, endpoint, credential, balance, route, worker or artifact details.

This is an authorization record, not a runtime report. Exact execution state and observations stay in private operator records; no public result packet is adopted here. Authorization alone is not evidence of success.

### 4. Explicit exclusions

This decision does not authorize:

- a memory-system, case, benchmark, semantic-judgment or scoring run;
- the RC-005 144-answer plan, Mem0 installation or ingestion, indexing migration, or a native system comparison;
- a general adapter, runner, SDK, API, service, hosted operation or deployment;
- real private conversation, personal continuity, production memory or a non-synthetic corpus;
- public result packets, external outreach or publication of operator artifacts;
- model/provider selection beyond the categories named above; or
- any change to release, licensing, case acceptance or the cross-system promotion gate.

## Relationship to ADR-0009 and the RC-005 packet

ADR-0010 remains a self-contained compatibility exception. ADR-0009 was separately accepted on 2026-10-23 solely for the RC-005 → pinned Mem0 packet; its 144 positions, native execution and resource limits derive from that packet, not this smoke. Matching protocol observations may be reused. No general runner, paid fallback, result publication or capability claim follows.

[ADR-0005](ADR-0005-offline-pilot-tooling.md)'s scripted rehearsal remains offline. The input-only RC-005 audit also remains input-only. This compatibility exception extends neither into a subject execution facility.

## Consequences and stopping rule

The check may establish limited interface compatibility and preserve explicit unavailable evidence. It cannot establish system quality or research results. Stop this batch at its selected dispatch limit or an actual data, provider or spending boundary, preserving failed attempts. Further finite compatibility batches within the maintainer's existing synthetic-data and resource authorization can be selected and recorded by the operator without renewed permission. New spending, private-data exposure, production changes or a memory-system study still require their applicable authority.

## Review and reversal

The maintainer may suspend, narrow or supersede this exception. Actual compatibility observations do not promote ADR-0009, the RC-005 packet, any case or any system capability claim. Any later decision to record a public compatibility summary must retain the distinction between observation, inference and pending evidence and must pass the repository's public-document checks.
