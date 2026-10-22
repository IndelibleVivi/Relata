[简体中文](SC-001-mem0.zh-CN.md) | **English**
<!-- language: en; mirror: SC-001-mem0.zh-CN.md; translation-status: synchronized -->

# System Card: Mem0 Python OSS

**Card ID:** SC-001\
**Status:** source-reviewed\
**Basis:** public-source\
**Visibility:** public\
**Contribution ID:** not applicable (public-source analysis)\
**Contributor attribution:** not applicable; independent Relata source analysis, not a maintainer statement or endorsement\
**Source analyst / contributor authority:** Relata source analyst; fidelity review of the existing pinned source study and atlas only\
**Exact version or observation date:** `mem0ai/mem0` commit `a39a802bbc93e85b820078cd3c4dbaf53af25dbe`; source study dated 2026-09-22; card fidelity-reviewed 2026-10-23 against existing studies/atlas

> This is not a product scorecard. Describe the system in its own terms before translating anything into Relata’s proposed boundaries.

## 中文摘要

Mem0 的 Python OSS 是一个供应用调用的持久化与检索层：它由对话抽取带 scope 的事实条目，配合近期消息缓冲、变更历史与实体索引。当前主路径是 V3 ADD-only，记住什么、何时调用、怎样把结果变成可靠行动由模型、harness、应用与人共同承担。本 card 绑定固定公开 commit 的静态源码，不把 managed platform 的分数当作 OSS 实测，也不声称任何运行或语义效果。

## English summary

The Mem0 Python OSS is an application-facing persistence and retrieval layer. Conversation-derived fact entries (with scope), a recent-message buffer, a change history and an entity index form its native memory. The current default path is V3 ADD-only, so what to store, when to call it, and how to turn results into reliable action stay with the model, harness, application and people. This card binds a pinned public commit’s static source; it treats no managed-platform score as an OSS result and claims no runtime or semantic outcome.

## 1. System identity and scope

- Primary use and relationship or agent role: an application-callable memory layer for AI agents and applications; not an agent, agent loop or chat product on its own.
- Local, hosted, or mixed: local Python library. The local `Memory` library composes configurable embedder, vector-store and LLM clients with SQLite history; the models need not run locally. `MemoryClient` is a separate managed boundary that defaults to `api.mem0.ai` and needs an API key; this card does not cover it.
- Included components: `Memory` write, scope, search, update, delete, history and procedural paths; V3 extraction prompts; SQLite schema and recent-message retention; scoring; message parsing; the spaCy loader.
- Explicitly excluded components: managed platform internals, self-hosted server authentication, TypeScript, the graph/history paths not read, evaluation submodule and all integrations.
- Current maturity: current OSS main at the pinned commit, described by its own README as differentiating OSS from a managed product.
- Evidence available: public source (static inspection).

## 2. System-native map

```text
add(messages, user_id/agent_id/run_id)
  -> recent 10 messages for the scope
  -> embed the new text, retrieve up to 10 related memories
  -> one LLM extraction pass (default infer=True, V3 ADD-only)
  -> batch embed; dedupe by text hash within the batch and retrieved items
  -> record UUID, text, created time, optional attributed_to
  -> write main vector index + change history + entity index

search(query, scope filters, top_k=20)
  -> semantic candidate pool of max(4*top_k, 60)
  -> add BM25 and entity boost
  -> return text, ID, score, time, metadata (no chat generation)

update(id) / delete(id) / delete_all(scope)  -> mutate main index, write history, best-effort entity cleanup
```

`infer=False` saves non-system messages one by one with role/name, and the procedural branch generates a text summary before storage. These are separate entry paths, not one default pipeline.

## 3. Continuity-bearing material

What persists over time: extracted fact entries (UUID, text, created time, optional `attributed_to`), a recent-message buffer in SQLite, a change history (ADD/UPDATE/DELETE), and an entity index linking entities to memories.

The active extraction prompt accepts both user and assistant content and asks the model to separate user facts from assistant suggestions, so project work, plans and agent actions can enter memory alongside user preferences. Personal-lived, shared-relational, operational/project and companion/system material are all representable, but nothing routes them: scope is a calling convention, not automatic domain or relationship recognition. Only model-selected statements are retained; retrieval score expresses relevance and `attributed_to` expresses the model’s own source classification, none of which equals factual reliability, user approval or relationship meaning.

## 4. Change and repair

- Default `infer=True` writing is ADD-only, which limits automatic overwrite; the explicit `update(id)` path still replaces text and vector, keeps the original creation time, writes an UPDATE history row and attempts to relink entities.
- `delete(id)` removes the main vector, writes a DELETE history row carrying the old text and attempts best-effort entity cleanup; cleanup is skipped when the entity store is not initialized in the process.
- `delete_all` walks the scope’s vector entries; the read path does not clear the SQLite recent-message buffer.
- `expiration_date`, where present, is a default search/list visibility filter, not temporal reasoning and not physical clearing.
- What can fail silently: on a batch write failure the code retries each record, and a still-failing record is only logged while later history, entity linking and the returned list still iterate the original records. A returned ADD event is therefore not, by itself, proof that each fact is searchable. No fault injection was performed, so production lost writes are not claimed.

## 5. Activation and use

`search` requires scope filters and defaults to `top_k=20`. It first takes `max(4*top_k, 60)` semantic candidates, then adds BM25 and entity boosts. Final candidates come only from the semantic set, and the semantic threshold applies before fused scores, so keyword or entity hits cannot rescue an item outside the pool. Optional reranker and `explain` widen observability. It returns text, ID, score, time and metadata and does not generate a final answer; `chat` is not implemented. Prior material affects a response only through the caller, which owns query construction, context budget, conflict handling and the action decision.

## 6. Source, authority, and perspective

The extraction prompt asks the model to distinguish user facts from assistant suggestions and to avoid echoing duplicates. `attributed_to` comes from LLM output and cannot act as provenance authentication, an original-text locator, or proof that an action was taken. Default `parse_messages` keeps only role and content for system/user/assistant and ignores structured names and tool roles. The prompt-level `linked_memory_ids` are not persisted by the default write path, and entity-to-memory links come from a separate NLP stage, so no revision lineage or dependency revocation should be assumed from the prompt.

## 7. Time

The OSS rejects `add(timestamp=...)` and `search(reference_date=...)`. The default prompt builder sets observation date to the current day while `add` passes no historical time, so replaying old conversations must handle event time explicitly. `created_at` metadata and text dates can be stored and an `expiration_date` is supported, but the latter only filters default visibility.

## 8. Surfaces, models, and identity

Scope identity is the explicit `user_id`/`agent_id`/`run_id` combination (at least one required); metadata cannot override it. `get`/`update`/`delete` by ID do not receive caller identity at this library boundary, so the application must implement permissions and scope mapping. Default NLP uses English `en_core_web_sm`; Chinese behavior cannot be inferred from English functionality.

## 9. Prospective behavior

No scheduling, trigger or future-wake behavior is present. `expiration_date` is a visibility filter, and the procedural branch only generates a text summary to store. Future-plan text may be retained, but prospective trigger execution is not supplied by these inspected paths.

## 10. Contributor control and user sovereignty

Explicit update, delete and per-scope delete-all APIs and an inspectable change history exist. A single delete is not source erasure, complete forgetting or downstream revocation: history rows keep old text, entity cleanup is best-effort, and a residual recent-message buffer can keep feeding later extraction. Whether residual text regenerates a specific fact needs a probe.

## 11. Known successes and failures

Source-observed (static, pinned version): a distinct application-facing retrieval-service boundary; ADD-only default with explicit correction APIs kept separate; semantic-candidate gating before fusion (a precision, cost and interface tradeoff rather than a plain defect); operation-level auditability via history; and batch partial-failure handling that preserves some useful material while requiring the application to verify persistence. Product-claimed: README headline numbers (for example LoCoMo 92.5, LongMemEval 94.4) belong to the managed platform and are not an OSS result. UNVERIFIED: performance, Chinese recall, factual fidelity, long-term stability and end-to-end correction.

## 12. Observability at candidate Relata boundaries

Legend: `N` native · `E` adapter-emulated · `O` opaque · `U` unsupported · `?` unknown · `—` not applicable (as defined in [`systems/README.md`](../README.md)).

| Candidate observation | Class | Evidence | Distortion note |
|---|---:|---|---|
| ordered history exposure | N | source study, “生命周期” (add takes a messages list) | Ordering is per-call; no global event clock |
| distinct ingest/write output | N | source study, “生命周期” (`add`) | Returned ADD is not per-fact durability proof |
| retrieval/activation material | N | source study, “检索与交接” | Candidates only; no reranked final context |
| rendered model context | E | source study, “检索与交接” (no `chat`) | Caller assembles context, budget and conflict policy |
| final response or action | U | source study, “检索与交接” | Generation and action are outside the boundary |
| correction/revocation route | N | source study, “更新与删除” | Only operation-level; not source erasure |
| inspection/explanation route | N | source study, “检索与交接”, “更新与删除” | `explain` and history, not fact-level authority |
| time advance or future wake | U | source study, “来源、角色、时间与派生影响” | `expiration_date` is a filter, not a wake |
| full-history or full-search exposure | O | source study, “更新与删除” (recent-message retention) | History plus buffer, no native full-search contract |
| multi-project isolation | O | source study, “对象边界与证据口径” (scope params) | Scope is a calling convention, not enforced routing |
| artifact/source authority | O | source study, “来源、角色、时间与派生影响” | `attributed_to` is model output, not authority |
| role/surface routing | O | source study, “对象边界与证据口径” | No automatic surface or role routing |
| cross-domain context contamination | O | source study, “来源、角色、时间与派生影响” | No content-domain routing; app must prevent mixing |

## 13. Candidate Relata probes

This card could pressure-test distinction D-002 (authority without narrative theft) and the attribution/revision probe the source study proposes: a two-person synthetic cross-day dialogue where the user states a deadline, the assistant only suggests, then the user changes it, queried under stable user/agent scope and a separate project scope. It could also serve D-004 and correction propagation through the source study’s deletion/derived probe (a fact A, a dependent plan B, then edit and delete A). The lane that preserves the system is the application-facing service boundary: observe returned candidates, history rows and (separately labelled) the application’s context assembly, not a reconstructed pipeline.

## 14. Confidentiality and publication limits

This card must not publish private conversations, credentials, private configuration or implied insider knowledge, and must not present managed-platform scores as OSS results or imply maintainer endorsement. It is public-source only.

## 15. Source / contributor review

- System description accurate enough for the stated use: yes
- Review basis and inspected source paths: fidelity review against [`systems/source-studies/mem0.md`](../source-studies/mem0.md) and its pinned evidence references; atlas model [`mem0.json`](../architecture-atlas/models/mem0.json)
- Public-safe contributor-derived fields approved: not applicable (public-source only)
- Disagreements or unknowns preserved: managed-vs-OSS boundary; entity-cleanup skip; batch partial-failure semantics; all runtime and semantic effects UNVERIFIED
- Review date: 2026-10-23
- Reviewer / contributor confirmation route: Relata source-fidelity review; no contributor confirmation applies
- Review limits: this 2026-10-23 review checked consistency with existing source studies and atlas models; it did not reread all upstream source links, rerun the offline checks, or execute a system. Earlier 2026-10-14 review provenance could not be established and is not asserted.
