[简体中文](SC-003-letta.zh-CN.md) | **English**
<!-- language: en; mirror: SC-003-letta.zh-CN.md; translation-status: synchronized -->

# System Card: Letta (current OSS local backend)

**Card ID:** SC-003\
**Status:** source-reviewed\
**Basis:** public-source\
**Visibility:** public\
**Contribution ID:** not applicable (public-source analysis)\
**Contributor attribution:** not applicable; independent Relata source analysis, not a maintainer statement or endorsement\
**Source analyst / contributor authority:** Relata source analyst; fidelity review of the existing pinned source study and atlas only\
**Exact version or observation date:** `letta-ai/letta-code` commit `f5c5bbce6e9394b30c626909315c2b3acc665672` (`package.json` 0.32.17); source study dated 2026-09-22; card fidelity-reviewed 2026-10-23 against existing studies/atlas

> This is not a product scorecard. Describe the system in its own terms before translating anything into Relata’s proposed boundaries.

## 中文摘要

当前 Letta 的 local backend 是一个 stateful agent harness：conversation 的原始消息记录与压缩事件、Git 管理的可修改 MemFS，以及供后续调用使用的编译后 system prompt。模型可通过 `memory` 工具改写文件并按路径 commit，每个 turn 检测 Git revision 变化并把新编译结果作为 system 消息追加。本地检索是 FTS-lite，没有向量索引；记忆内容的演化变成普通文件与 Git 操作，但 Git 可追溯不等于事实归属或遗忘保证。本 card 绑定固定公开 commit 的静态源码，不代表运行或语义效果。

## English summary

The current Letta local backend is a stateful agent harness built from three persistent objects: a conversation’s raw message record and compaction events, a Git-managed, editable MemFS, and a compiled system prompt used by later calls. The model can rewrite files through the `memory` tool and commit by path; each turn compares the compiled version with the current Git revision and appends the new memory update as a system message. Local search is FTS-lite, with no vector index. Memory content evolution becomes ordinary file and Git operations, but Git traceability is not fact attribution or a forgetting guarantee. This card binds a pinned public commit’s static source and claims no runtime or semantic outcome.

## 1. System identity and scope

- Primary use and relationship or agent role: a stateful agent harness that rewrites memory, skills, prompts and mods to persist identity and experience across calls; not a standalone memory service.
- Local, hosted, or mixed: current OSS with a local and a Cloud backend. This card covers the local backend; the Cloud backend is a separate boundary and its hosted database, retrieval, deletion guarantees and availability are not established here.
- Included components: conversation message persistence (`conversation.json`, `messages.jsonl`) with `parentId` and timestamps; the `memory` tool (`create`, `str_replace`, `insert`, `delete`, `rename`, `update_description`); Git commits with agent author and reason; the local system-prompt compiler; the FTS-lite transcript search; turn-end compaction.
- Explicitly excluded components: the retired `letta-ai/letta` archive and V1 API server, old MemGPT tools and database hierarchy, channels, multi-user authorization, shared memory, permission confinement, the Cloud backend and all migration/recovery paths.
- Current maturity: current OSS source snapshot at the pinned commit.
- Evidence available: public source (static inspection).

## 2. System-native map

```text
turn input -> message {id, role, timestamp, agent_id, conversation_id}
  -> persist conversation.json + messages.jsonl (parentId chain)
  -> model may call memory(create/str_replace/insert/delete/rename/update_description)
       -> check workspace, edit file, git commit with agent author and reason
  -> compile committed Markdown: persona -> <self>, system files -> <memory>, external dirs listed only
  -> per turn: compare compiled revision with current Git revision; on change, mint a memory update
  -> stream adapter appends the update as a system message (original system prompt kept)

long conversation -> compaction: model summary + retained tail; transcript appends a compaction event
local recall -> agent/conversation + date + hidden filters, FTS-lite matching (no local vector index)
```

Local MemFS is forced to v1 (`system/*.md` is core); non-local MemFS with a root `MEMORY.md` is v2. v1/v2 is a current MemFS format difference, not the retired V1 API era.

## 3. Continuity-bearing material

What persists: raw messages (role, timestamp, provider/model metadata, `parentId`), compaction events, editable Markdown memory files grouped as core/deferred/skills, and derived Git commits. Identity is bound to MemFS; a conversation binds one active context, and a new conversation on the same agent can reuse the same memory. The system keeps a transcript and editable files rather than one vector store. A persona file and any number of memory files can express content boundaries, so personal-lived, shared-relational, operational/project and companion/system material can be written, but the structure does not enforce which domain a file belongs to.

## 4. Change and repair

- The `memory` tool edits files and commits by path with a required non-empty reason and the agent author. `memory delete` removes a target file or directory and commits; `rename` moves a path. That tool path has no cascade to the transcript, existing summaries, recollections in other memory files or Git history.
- A new compile stops injecting a deleted file, but disappearing from active memory is not the same as being unrecoverable or forgotten everywhere.
- Cloud sync can return dirty, conflict or push_failed; a non-fast-forward attempts rebase then push, and a failure state is returned.
- What can fail silently: if the model condenses “a colleague likes coffee” into “the user likes coffee”, Git faithfully records the wrong condensation; the structure does not correct attribution unless the file text keeps its own reference.

## 5. Activation and use

The local compiler reads committed Markdown with `git ls-tree HEAD` and `git show HEAD:path`; each turn compares the compiled version with the current Git revision, and a changed revision produces a new memory update that the stream adapter appends as a system message. This is not an immediate rewrite of the in-flight turn, and the code alone cannot show that the model followed the new rule. Long-conversation compaction keeps a model summary plus a retained tail and appends a compaction event instead of deleting early records. Local recall matching cannot distinguish “the system has no memory” from “wrong vocabulary”, “wrong scope”, “the model did not search” or “it was never written”.

## 6. Source, authority, and perspective

Git revision, diff, commit reason, file body, conversation/message IDs and timestamps give strong operation-level inspectability; roles distinguish user, assistant and toolResult with provider/model metadata; search results can return to a conversation and message. These are message and operation provenance, not per-fact source. MemFS frontmatter allows mainly `description`/`read_only`/`limit` or `name`/`description`, with no forced fact-level source, speaker, valid-time or supporting-evidence ID. So Git faithfully records the model’s condensation, including wrong attribution, unless the text itself cites its source.

## 7. Time

Messages carry `timestamp`, and compaction events are appended in time order. There is no explicit event-time versus record-time distinction at the memory layer; time enters mainly as message order and commit history. Historical material survives in the transcript and Git history, but the system does not treat older material as clearly non-current guidance by structure alone.

## 8. Surfaces, models, and identity

`agent` and `conversation` are technical scopes that do not by themselves equal a household, client, project or intimate-relationship scope. Messages carry provider/model metadata, and Cloud sync crosses machines with its own timing. File structure and prompts can express content boundaries, but this study does not prove they deterministically prevent cross-domain generalization. Multiple projects, roles, people and surfaces are isolated only as far as the harness maps them to agents/conversations.

## 9. Prospective behavior

No local future-trigger, reminder or wake behavior is established by the inspected paths. Schedulers and reminders are not part of this card’s reviewed boundary, so prospective behavior is marked unknown rather than asserted.

## 10. Contributor control and user sovereignty

Memory evolution is ordinary file and Git operations, which is inspectable, amendable and migratable by both human and agent. Raw experience and compressed working context are separated, so a summary omission can be revisited through search. But a delete should be split into correction, withdraw-from-use and data erasure; there is no evidence of a system-wide semantic revocation closure. Cloud state remains technically and institutionally opaque.

## 11. Known successes and failures

Source-observed (static, pinned version): three persistent objects with a clear compile step; model-and-human editable memory with committed reasons; revision-triggered recompilation; raw transcript separated from compressed context; FTS-lite local search (explicitly not vector/hybrid). A competing reading is that this is programmable context management, and “learning” may mean future prompt change; that does not diminish the engineering value but cannot replace evidence of behaviour improvement. UNVERIFIED: online performance, recall rate, cross-process consistency, long-term relational effect, managed deletion guarantees and global permission safety.

## 12. Observability at candidate Relata boundaries

Legend: `N` native · `E` adapter-emulated · `O` opaque · `U` unsupported · `?` unknown · `—` not applicable (as defined in [`systems/README.md`](../README.md)).

| Candidate observation | Class | Evidence | Distortion note |
|---|---:|---|---|
| ordered history exposure | N | source study, “一条写入、保留、使用与修订路径” (messages.jsonl) | Per-conversation order plus `parentId` |
| distinct ingest/write output | N | source study, “一条写入、保留、使用与修订路径” (memory tool) | File edit plus Git commit |
| retrieval/activation material | N | source study, “可检查性、来源与控制” (FTS-lite recall) | Keyword/phrase match, no local vector |
| rendered model context | N | source study, “一条写入、保留、使用与修订路径” (compiled prompt) | Original system prompt kept alongside |
| final response or action | N | source study, “结论与对象边界” (stateful harness) | Model/provider is external but the harness runs it |
| correction/revocation route | N | source study, “修改、删除及派生影响” (`memory delete`) | No cascade to transcript or Git history |
| inspection/explanation route | N | source study, “可检查性、来源与控制” | Git diff/reason and message IDs |
| time advance or future wake | ? | source study, “覆盖与未验证” | Schedulers not reviewed; not asserted |
| full-history or full-search exposure | N | source study, “一条写入、保留、使用与修订路径” (transcript) | Transcript searchable; compaction boundary |
| multi-project isolation | O | source study, “可检查性、来源与控制” | agent/conversation scope, not project scope |
| artifact/source authority | O | source study, “可检查性、来源与控制” | Message provenance is not fact authority |
| role/surface routing | O | source study, “可检查性、来源与控制” | No automatic role/surface routing |
| cross-domain context contamination | O | source study, “可检查性、来源与控制” | Structure does not prevent generalization |

## 13. Candidate Relata probes

This card could pressure-test D-005 (identity continuity across migration) and D-002 (authority without narrative theft): the source study proposes an attribution-and-timing double-revision probe (A says B likes coffee, A used to drink coffee and now does not; later project chat only says to bring B coffee) and a deletion-residual probe (a synthetic preference written to core, an external reference and a summary, then withdraw future use under three conditions). The lane that preserves the system is the local compile-plus-Git boundary: observe original roles/times, the memory diff, the compiled context, search calls and the answer, and keep Cloud behaviour separate.

## 14. Confidentiality and publication limits

Public-source only. Do not read or publish private memory, Cloud internals or credentials, do not imply Letta endorsement, and do not extend local findings to Cloud or to the retired archive.

## 15. Source / contributor review

- System description accurate enough for the stated use: yes
- Review basis and inspected source paths: fidelity review against [`systems/source-studies/letta.md`](../source-studies/letta.md) and its fixed-commit evidence index; atlas model [`letta.json`](../architecture-atlas/models/letta.json)
- Public-safe contributor-derived fields approved: not applicable (public-source only)
- Disagreements or unknowns preserved: local-vs-Cloud boundary; reflection lifecycle not fully read; prospective behaviour not asserted; all runtime and semantic effects UNVERIFIED
- Review date: 2026-10-23
- Reviewer / contributor confirmation route: Relata source-fidelity review; no contributor confirmation applies
- Review limits: this 2026-10-23 review checked consistency with existing source studies and atlas models; it did not reread all upstream source links, rerun the offline checks, or execute a system. Earlier 2026-10-14 review provenance could not be established and is not asserted.
