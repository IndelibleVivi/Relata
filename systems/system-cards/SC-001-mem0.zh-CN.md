[English](SC-001-mem0.md) | **简体中文**
<!-- language: zh-CN; mirror: SC-001-mem0.md; translation-status: synchronized -->

# System Card：Mem0 Python OSS

**Card ID：** SC-001\
**Status：** source-reviewed\
**Basis：** public-source\
**Visibility：** public\
**Contribution ID：** not applicable（公开源码分析）\
**Contributor attribution：** 不适用；这是 Relata 独立源码分析，不代表维护方声明或背书\
**Source analyst / contributor authority：** Relata 源码分析者；仅对照既有固定版本 source study 与 atlas 做忠实性核对\
**Exact version or observation date：** `mem0ai/mem0` commit `a39a802bbc93e85b820078cd3c4dbaf53af25dbe`；source study 日期 2026-09-22；card fidelity review 日期 2026-10-23（对照既有 studies/atlas）

> 这不是产品评分卡。先按系统自己的术语描述，再翻译成 Relata 的拟议边界。

## 中文摘要

Mem0 的 Python OSS 是一个供应用调用的持久化与检索层：它由对话抽取带 scope 的事实条目，配合近期消息缓冲、变更历史与实体索引。当前主路径是 V3 ADD-only，记住什么、何时调用、怎样把结果变成可靠行动由模型、harness、应用与人共同承担。本 card 绑定固定公开 commit 的静态源码，不把 managed platform 的分数当作 OSS 实测，也不声称任何运行或语义效果。

## English summary

The Mem0 Python OSS is an application-facing persistence and retrieval layer. Conversation-derived fact entries (with scope), a recent-message buffer, a change history and an entity index form its native memory. The current default path is V3 ADD-only, so what to store, when to call it, and how to turn results into reliable action stay with the model, harness, application and people. This card binds a pinned public commit’s static source; it treats no managed-platform score as an OSS result and claims no runtime or semantic outcome.

## 1. 系统身份与范围

- 主要用途与关系/agent 角色：供 AI agent 与应用调用的 memory 层；本身不是 agent、agent loop 或聊天产品。
- local / hosted / mixed：本地 Python 库。本地 `Memory` 库组合可配置的 embedder、vector-store、LLM clients 与 SQLite history；模型不一定在本地运行；`MemoryClient` 是另一个默认连到 `api.mem0.ai` 且需要 API key 的 managed 边界，本 card 不覆盖它。
- 包含组件：`Memory` 的写入、scope、检索、更新、删除、history 与 procedural 路径；V3 抽取 prompt；SQLite schema 与近期消息保留；scoring；消息解析；spaCy loader。
- 明确排除：managed platform 内部、self-hosted server 认证、TypeScript、未读的 graph/history 路径、evaluation submodule 与全部 integrations。
- 当前成熟度：pinned commit 上的当前 OSS main，README 自身区分 OSS 与 managed 产品。
- 可用证据：公开源码（静态检查）。

## 2. System-native map

```text
add(messages, user_id/agent_id/run_id)
  -> 该 scope 的最近 10 条消息
  -> 对新文本 embedding，取最多 10 条相关 memory
  -> 一次 LLM 抽取（默认 infer=True，V3 ADD-only）
  -> 批量 embedding；在本批与已检索条目内按文本 hash 去重
  -> 记录 UUID、文本、创建时间、可选 attributed_to
  -> 写主向量索引 + 变更历史 + 实体索引

search(query, scope filters, top_k=20)
  -> semantic 候选池 max(4*top_k, 60)
  -> 叠加 BM25 与 entity boost
  -> 返回文本、ID、score、时间、metadata（不生成回答）

update(id) / delete(id) / delete_all(scope)  -> 改主索引、写 history、best-effort 清理实体
```

`infer=False` 会逐条保存非 system 消息及 role/name；procedural 分支先生成文本摘要再入库。它们是分开的入口，不是同一条默认流程。

## 3. 持续性材料

随时间保留的内容：抽取的事实条目（UUID、文本、创建时间、可选 `attributed_to`）、SQLite 中的近期消息缓冲、变更历史（ADD/UPDATE/DELETE），以及连接实体与 memory 的实体索引。

活跃抽取 prompt 同时接纳 user 与 assistant 内容，并要求区分用户事实与助手建议，因此项目工作、计划与 agent 行动可以随用户偏好一起进入 memory。personal-lived、shared-relational、operational/project 与 companion/system 材料都可表示，但没有任何路由：scope 是调用约定，不是自动的内容域或关系识别。被保留的只是模型选出的表述；检索分数表达相关性，`attributed_to` 表达模型自己的来源分类，都不等于事实可信度、用户认可或关系意义。

## 4. 变更与修复

- 默认 `infer=True` 写入是 ADD-only，限制自动覆写；显式 `update(id)` 仍替换文本与向量、保留创建时间、写 UPDATE history 并尝试重新链接实体。
- `delete(id)` 删除主向量、写含旧文本的 DELETE history，并尝试 best-effort 清理实体；当进程未初始化 entity store 时直接跳过。
- `delete_all` 遍历该 scope 的向量条目；所读路径不清空 SQLite 近期消息缓冲。
- `expiration_date` 是默认检索/列表的可见性过滤，不是时间推理，也不是物理清除。
- 可静默失败之处：批量写入失败时逐条重试，仍失败的条目只记日志，而后续 history、实体链接与返回列表仍遍历原始 records。因此返回 ADD 事件本身不能证明每条事实已可检索。本文未做故障注入，不声称生产丢写。

## 5. 唤起与使用

`search` 要求 scope filters，默认 `top_k=20`；先取 `max(4*top_k, 60)` 个 semantic 候选，再叠加 BM25 与 entity boost。最终候选只来自 semantic 集合，且 semantic threshold 先于融合分数生效，keyword/entity 命中不能救回池外条目。可选 reranker 与 `explain` 扩大可观察空间。它返回文本、ID、score、时间与 metadata，不生成最终回答，`chat` 未实现。过去材料只能经调用方影响回答，而 query 构造、上下文预算、冲突处理与行动判断由调用方负责。

## 6. 来源、权威与视角

抽取 prompt 要求区分用户事实与助手建议并避免回声重复。`attributed_to` 来自 LLM 输出，不能充当来源认证、原文定位或行动已完成的凭据。默认 `parse_messages` 仅保留 system/user/assistant 的 role 与 content，忽略结构化 name 与 tool role。prompt 中的 `linked_memory_ids` 不被默认写路径持久化，实体与 memory 的关联另由 NLP 阶段建立，因此不能据 prompt 假定修订谱系或依赖撤回。

## 7. 时间

OSS 拒绝 `add(timestamp=...)` 与 `search(reference_date=...)`。默认 prompt builder 把 observation date 设为当天，而 `add` 未传历史时间，因此回灌旧对话必须显式处理事件时间。可保存 `created_at` metadata 与文本日期，也支持 `expiration_date`，但后者只过滤默认可见性。

## 8. Surfaces、模型与身份

scope 身份是显式 `user_id`/`agent_id`/`run_id` 组合（至少一个），metadata 不能覆盖它。按 ID 的 `get`/`update`/`delete` 在该 library 边界不接收调用者身份，应用必须自行实施权限与 scope 映射。默认 NLP 使用英文 `en_core_web_sm`；不能由英文功能推出中文效果。

## 9. 前瞻行为

没有调度、触发器或未来唤醒行为。`expiration_date` 是可见性过滤，procedural 分支只生成待入库的文本摘要。未来计划文本仍可保留，但所检查路径不提供未来意向的触发执行。

## 10. Contributor control 与用户主权

存在显式 update、delete 与按 scope 的 delete_all API，以及可检查的变更历史。单条删除不等于来源消除、完全遗忘或下游撤回：history 保留旧文本，实体清理是 best-effort，残留的近期消息缓冲还可能继续进入之后的抽取。残留文本是否再生具体事实需要 probe 验证。

## 11. 已知成功与失败

SOURCE-OBSERVED（静态、固定版本）：清晰的应用侧检索服务边界；ADD-only 默认与显式修订 API 分开；semantic 候选门槛先于融合（是精度、成本与接口一致性的取舍，不是单纯缺陷）；操作级 history 可审计；批量部分失败可保留部分有用材料但要求应用自行核验落库。SOURCE-CLAIMED：README 的 headline 数字（如 LoCoMo 92.5、LongMemEval 94.4）属于 managed platform，不是 OSS 结果。UNVERIFIED：性能、中文召回、事实忠实性、长期稳定性与端到端纠错。

## 12. 候选 Relata 边界上的可观察性

图例：`N` native · `E` adapter-emulated · `O` opaque · `U` unsupported · `?` unknown · `—` not applicable（定义见 [`systems/README.zh-CN.md`](../README.zh-CN.md)）。

| 候选观察 | 类别 | 证据 | 失真说明 |
|---|---:|---|---|
| ordered history exposure | N | source study，“生命周期”（add 接收 messages 列表） | 排序按单次调用；无全局事件时钟 |
| distinct ingest/write output | N | source study，“生命周期”（`add`） | 返回 ADD 不是逐条持久化证明 |
| retrieval/activation material | N | source study，“检索与交接” | 仅有候选；无重排后的最终 context |
| rendered model context | E | source study，“检索与交接”（无 `chat`） | 调用方负责 context、预算与冲突策略 |
| final response or action | U | source study，“检索与交接” | 生成与行动在边界之外 |
| correction/revocation route | N | source study，“更新与删除” | 仅操作级；不是来源消除 |
| inspection/explanation route | N | source study，“检索与交接”“更新与删除” | `explain` 与 history，不是事实级权威 |
| time advance or future wake | U | source study，“来源、角色、时间与派生影响” | `expiration_date` 是过滤，不是唤醒 |
| full-history or full-search exposure | O | source study，“更新与删除”（近期消息保留） | 有 history 与缓冲，无原生 full-search 合约 |
| multi-project isolation | O | source study，“对象边界与证据口径”（scope 参数） | scope 是调用约定，不是强制路由 |
| artifact/source authority | O | source study，“来源、角色、时间与派生影响” | `attributed_to` 是模型输出，不是权威 |
| role/surface routing | O | source study，“对象边界与证据口径” | 无自动 surface 或 role 路由 |
| cross-domain context contamination | O | source study，“来源、角色、时间与派生影响” | 无内容域路由；需应用阻止混用 |

## 13. 候选 Relata probes

本 card 可对 distinction D-002（authority without narrative theft）施加压力，并使用 source study 提议的归属/修订 probe：两名虚构成年人的跨日对话，用户提出 deadline、助手仅建议、用户随后更改，在稳定的 user/agent scope 与另一个 project scope 下查询。也可通过 source study 的删除/派生 probe（事实 A、依赖 A 的计划 B，随后改 A、删 A）服务 D-004 与更正传播。保留系统的 lane 是应用侧服务边界：观察返回候选、history 行与（另行标注的）应用 context 组装，而不是重建的流水线。

## 14. 保密与发布限制

本 card 不得发布私人对话、凭据、私有配置或暗示内幕，也不得把 managed platform 的分数当作 OSS 结果或暗示维护方背书。它仅基于公开源码。

## 15. 来源 / contributor review

- 系统描述对既定用途足够准确：yes
- review 依据与检查的源码路径：对照核查 [`systems/source-studies/mem0.md`](../source-studies/mem0.md) 及其固定 commit 链接；图模型 [`mem0.json`](../architecture-atlas/models/mem0.json)
- Public-safe contributor-derived fields approved：not applicable（仅公开源码）
- 保留的分歧或未知：managed 与 OSS 的边界；实体清理跳过；批量部分失败语义；全部运行与语义效果 UNVERIFIED
- Review date：2026-10-23
- Reviewer / contributor confirmation route：Relata source-fidelity review；无 contributor 确认适用
- Review 限制：本轮 2026-10-23 仅核对既有 source studies 与 atlas models 的一致性；未重读全部 upstream 链接、重跑离线核对或执行系统。此前 2026-10-14 review 来源未能建立，不予追认。
