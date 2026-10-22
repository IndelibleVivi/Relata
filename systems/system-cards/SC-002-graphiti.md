[简体中文](SC-002-graphiti.zh-CN.md) | **English**
<!-- language: en; mirror: SC-002-graphiti.zh-CN.md; translation-status: synchronized -->

# System Card: Graphiti

**Card ID:** SC-002\
**Status:** source-reviewed\
**Basis:** public-source\
**Visibility:** public\
**Contribution ID:** not applicable (public-source analysis)\
**Contributor attribution:** not applicable; independent Relata source analysis, not a maintainer statement or endorsement\
**Source analyst / contributor authority:** Relata source analyst; fidelity review of the existing pinned source study/atlas and its recorded isolated offline check\
**Exact version or observation date:** `getzep/graphiti` commit `16cdf7045378c8d53ae01f94e2fa60d238cb0f68`; source study dated 2026-09-22; card fidelity-reviewed 2026-10-23 against existing studies/atlas

> This is not a product scorecard. Describe the system in its own terms before translating anything into Relata’s proposed boundaries.

## 中文摘要

Graphiti 把 episode、实体、事实边与时间有效性连接成可查询的 temporal knowledge graph。写入时以 LLM 抽取并解析重复/矛盾，把较早事实的 `invalid_at` 设为新事实开始时间；检索返回边或节点，调用者决定查询语义与上下文消费。来源连接存在但不是真实性担保，删除入口不重算所有派生状态。本 card 绑定固定公开 commit 的静态源码，并含一段隔离的源码分支离线观察，不代表端到端运行或语义效果。

## English summary

Graphiti connects episodes, entities, fact edges and temporal validity into a queryable temporal knowledge graph. Writes extract and resolve duplicates/contradictions with an LLM, setting an earlier fact’s `invalid_at` to a new fact’s start; search returns edges or nodes, and the caller chooses query semantics and context consumption. Provenance links exist but are not a truth guarantee, and the removal entry does not recompute every derived state. This card binds a pinned public commit’s static source plus one isolated source-branch observation; it is not an end-to-end run or a semantic result.

## 1. System identity and scope

- Primary use and relationship or agent role: a temporal knowledge graph framework and memory backend for agents and applications; not a complete agent or chat product.
- Local, hosted, or mixed: local OSS framework, usually run against a graph database. The README separates the self-hosted OSS from Zep managed context infrastructure, whose governance, scale and latency claims do not transfer.
- Included components: `graphiti.py` single-episode write, extraction wrapper, save, search and delete entries; entity/edge models; node/edge maintenance (extraction, dedupe, summary, invalidation); extraction and dedupe prompts; search recipes, filters and Cypher; a LangGraph example agent.
- Explicitly excluded components: bulk/dense ingestion, saga/community updates, all database drivers, MCP/server, security and deployment, historical versions, papers and evaluation data.
- Current maturity: one pinned public OSS commit.
- Evidence available: public source (static) plus one offline source-branch check with in-memory doubles.

## 2. System-native map

```text
add_episode(content, source_description, type, reference_time, group_id)
  -> fetch prior episodes of the same group as context
  -> created_at := system now; valid_at := episode reference_time
  -> extract entities; resolve/dedupe against candidates
  -> extract fact edges; resolve duplicate / contradicted candidates with an LLM
  -> update entity attributes and summaries; save the graph

search(query, ...)
  -> keyword + vector candidates, merged and ranked (BM25 + cosine + RRF)
  -> returns EntityEdge by default; advanced paths add nodes/episodes/communities with optional BFS/MMR/cross-encoder
  -> caller turns edges into context (the example concatenates edge.fact)
```

Fact edges store both endpoint UUIDs, the `fact` text, an embedding, a source-episode UUID list and time fields. MENTIONS edges and each episode’s `entity_edges` list give a walkable connection back to sources. Entity summaries append first and then switch to a length-thresholded LLM summary with no per-sentence validity.

## 3. Continuity-bearing material

What is retained: episodes and their content, entity nodes, fact edges with `valid_at`/`invalid_at` plus `created_at`/`expired_at`, entity summaries, and source links. `store_raw_episode_content=False` blanks the in-process `episode.content` before saving, so retaining a UUID is not the same as retaining full auditable original text. Ordinary personal history, shared-relational material and operational/project history can all be encoded as episodes and edges, but the framework does not separate these domains; it keeps episodes, entities and time-bounded facts.

## 4. Change and repair

- Contradiction resolution is semantic and LLM-mediated, not date arithmetic: once chosen as a candidate, the code skips non-overlapping intervals and sets an earlier fact’s `invalid_at` to the new fact’s start time, writing `expired_at`. A late old fact can also be truncated by a later candidate. Strict `<`/`>` and non-null time conditions mean same-time or missing-time facts do not share one automatic resolution.
- `remove_episode()` deletes edges whose `edge.episodes[0]` equals the episode UUID, deletes entities mentioned only by that episode, then deletes the episode. It does not recompute surviving entity summaries, clear surviving edges’ source arrays, rebuild communities or restore previously invalidated edges.
- What can fail silently: derived summaries and source arrays can drift from the graph state after a removal. The offline check showed that when two sources support one edge, removing the first source still requests deleting the whole edge, while removing the second keeps the edge with its source array unchanged.

## 5. Activation and use

Search merges keyword and vector results; the basic entry returns `EntityEdge`, and advanced entries may return nodes, episodes and communities with BFS, MMR or cross-encoder options. The basic recipe is BM25 + cosine + RRF and does not traverse the graph every time. The caller decides how edges become context: the official agent example concatenates only `edge.fact` into a system message and writes the conversation back as a new episode, so storage time and provenance do not automatically all reach generation.

## 6. Source, authority, and perspective

Source connections exist but are not a truth guarantee for the referenced content. Entity resolution mixes deterministic similarity rules and an LLM; edge resolution retrieves same-endpoint duplicate candidates and wider contradiction candidates, then has the LLM return duplicate/contradicted indices. Facts outside the candidate recall step are not compared by time rules. The application should distinguish author, speaker, information source and their authority, and must not let an agent’s own write-back be silently upgraded to human approval.

## 7. Time

Graphiti is deliberately bi-temporal: `valid_at`/`invalid_at` mark when a fact held, while inherited `created_at`/`expired_at` mark graph processing time. However, the default `search()` builds an empty `SearchFilters()`, and all four time filters default to None, so the “current time relevance” in the docstring is not an automatic exclusion of historical invalid facts. Historical versus current views are configurable; the caller must choose the query semantics.

## 8. Surfaces, models, and identity

`group_id` partitions the graph, and a write can create a request-scoped driver to avoid concurrent redirection of a shared driver. Group conditions in retrieval are optional and a null value normalizes to no filter. This partition facility does not by itself prove per-person authorization, consent management or cross-relationship isolation; the caller binds the authenticated subject to allowed groups, sources and serial write order. The framework does not separate personal, relational and operational material in its own vocabulary.

## 9. Prospective behavior

No future-trigger or wake behavior is present. `valid_at`/`invalid_at` describe when a fact holds, not a scheduled action. Future-plan text may be stored as episodes or facts; this does not supply prospective trigger execution.

## 10. Contributor control and user sovereignty

`remove_episode()` is the visible removal entry, but it does not close revision propagation across derived state, as noted above. Whether a user-level promise to revoke one source holds is a caller-contract question, not something the code guarantees.

## 11. Known successes and failures

Source-observed (static, pinned version): bi-temporal edges that support both when-it-happened and when-the-system-learned-it queries; a provenance-capable graph; and incremental reorganisation. Offline source-branch observation: with two sources supporting one edge, removing the first still requests deleting the whole edge and removing the second keeps the edge unchanged; and an exact-duplicate shortcut reuses an old edge, appends the source, keeps the old validity and calls no LLM. UNVERIFIED: whether natural-language extraction, candidate recall and the real database actually reach those branches; conflict accuracy; Chinese detail retention; privacy-deletion completeness; scale and latency; and any better-than-RAG effect.

## 12. Observability at candidate Relata boundaries

Legend: `N` native · `E` adapter-emulated · `O` opaque · `U` unsupported · `?` unknown · `—` not applicable (as defined in [`systems/README.md`](../README.md)).

| Candidate observation | Class | Evidence | Distortion note |
|---|---:|---|---|
| ordered history exposure | N | source study, “一条原生生命周期” (add_episode) | Episodes are grouped, not a global ordered log |
| distinct ingest/write output | N | source study, “一条原生生命周期” (`add_episode`) | Inline extraction; write is awaited |
| retrieval/activation material | N | source study, “一条原生生命周期” (search) | Basic entry returns edges, not context |
| rendered model context | E | source study, “时间、冲突与来源” (example concatenates `fact`) | Assembly is example/application code |
| final response or action | E | source study, “时间、冲突与来源” (example agent) | Framework does not generate the answer |
| correction/revocation route | N | source study, “Scope、更新与撤回” (`remove_episode`) | No recomputation of derived state |
| inspection/explanation route | N | source study, “时间、冲突与来源” | Edges/episodes inspectable; summaries opaque |
| time advance or future wake | U | source study, “一条原生生命周期” | Time fields are validity, not triggers |
| full-history or full-search exposure | N | source study, “Scope、更新与撤回” (episodes retained) | Raw content optional (`store_raw_episode_content`) |
| multi-project isolation | O | source study, “Scope、更新与撤回” (`group_id`) | Partition only; caller binds auth |
| artifact/source authority | O | source study, “时间、冲突与来源” | Source links are not a truth guarantee |
| role/surface routing | O | source study, “Scope、更新与撤回” | No role/surface routing |
| cross-domain context contamination | O | source study, “Scope、更新与撤回” | Caller must enforce group boundaries |

## 13. Candidate Relata probes

This card could pressure-test D-004 (repair without overcorrection) and source/authority fidelity: the source study proposes a same-sentence-reproduction probe over validity intervals (a statement in January, a departure in February, a rehire in March, plus a parallel relational appointment) and a dual-source-support probe that removes the first and then the second source of a shared fact while checking surviving facts, episode UUIDs, shared summaries and previously invalidated edges. The lane that preserves the system is the native write/search boundary plus the pinned offline branch check; do not treat the example agent’s fact-only assembly as a system result.

## 14. Confidentiality and publication limits

Public-source only. Do not publish private data or imply Zep managed guarantees, and do not present the offline branch check as an end-to-end result or as maintainer endorsement.

## 15. Source / contributor review

- System description accurate enough for the stated use: yes
- Review basis and inspected source paths: fidelity review against [`systems/source-studies/graphiti.md`](../source-studies/graphiti.md) and its pinned evidence references; offline check [`observations/graphiti-observe.py`](../source-studies/observations/graphiti-observe.py) and [`graphiti-observed.json`](../source-studies/observations/graphiti-observed.json); atlas model [`graphiti.json`](../architecture-atlas/models/graphiti.json)
- Public-safe contributor-derived fields approved: not applicable (public-source only)
- Disagreements or unknowns preserved: whether real extraction reaches the observed branches; removal propagation; all runtime and semantic effects UNVERIFIED
- Review date: 2026-10-23
- Reviewer / contributor confirmation route: Relata source-fidelity review; no contributor confirmation applies
- Review limits: this 2026-10-23 review checked consistency with existing source studies and atlas models; it did not reread all upstream source links, rerun the offline checks, or execute a system. Earlier 2026-10-14 review provenance could not be established and is not asserted.
