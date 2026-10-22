[English](SC-002-graphiti.md) | **简体中文**
<!-- language: zh-CN; mirror: SC-002-graphiti.md; translation-status: synchronized -->

# System Card：Graphiti

**Card ID：** SC-002\
**Status：** source-reviewed\
**Basis：** public-source\
**Visibility：** public\
**Contribution ID：** not applicable（公开源码分析）\
**Contributor attribution：** 不适用；这是 Relata 独立源码分析，不代表维护方声明或背书\
**Source analyst / contributor authority：** Relata 源码分析者；对照既有固定版本 source study/atlas 及其已记录的隔离离线核对\
**Exact version or observation date：** `getzep/graphiti` commit `16cdf7045378c8d53ae01f94e2fa60d238cb0f68`；source study 日期 2026-09-22；card fidelity review 日期 2026-10-23（对照既有 studies/atlas）

> 这不是产品评分卡。先按系统自己的术语描述，再翻译成 Relata 的拟议边界。

## 中文摘要

Graphiti 把 episode、实体、事实边与时间有效性连接成可查询的 temporal knowledge graph。写入时以 LLM 抽取并解析重复/矛盾，把较早事实的 `invalid_at` 设为新事实开始时间；检索返回边或节点，调用者决定查询语义与上下文消费。来源连接存在但不是真实性担保，删除入口不重算所有派生状态。本 card 绑定固定公开 commit 的静态源码，并含一段隔离的源码分支离线观察，不代表端到端运行或语义效果。

## English summary

Graphiti connects episodes, entities, fact edges and temporal validity into a queryable temporal knowledge graph. Writes extract and resolve duplicates/contradictions with an LLM, setting an earlier fact’s `invalid_at` to a new fact’s start; search returns edges or nodes, and the caller chooses query semantics and context consumption. Provenance links exist but are not a truth guarantee, and the removal entry does not recompute every derived state. This card binds a pinned public commit’s static source plus one isolated source-branch observation; it is not an end-to-end run or a semantic result.

## 1. 系统身份与范围

- 主要用途与关系/agent 角色：面向 agent 与应用的 temporal knowledge graph framework 与 memory backend；不是完整 agent 或聊天产品。
- local / hosted / mixed：本地 OSS framework，通常配 graph 数据库运行。README 分开 self-hosted OSS 与 Zep managed context infrastructure，后者的治理、规模或延迟主张不能移植。
- 包含组件：`graphiti.py` 的单 episode 写入、抽取封装、保存、检索与删除入口；实体/边模型；node/edge maintenance（抽取、去重、摘要、失效）；抽取与去重 prompt；search recipes、filters 与 Cypher；一个 LangGraph 示例 agent。
- 明确排除：bulk/dense ingestion、saga/community 更新、全部数据库 driver、MCP/server、安全与部署、历史版本、论文与评测数据。
- 当前成熟度：一个固定公开 OSS commit。
- 可用证据：公开源码（静态）与一次使用内存替身的隔离源码分支核对。

## 2. System-native map

```text
add_episode(content, source_description, type, reference_time, group_id)
  -> 取同组先前 episodes 作上下文
  -> created_at := 系统当前时间；valid_at := episode reference_time
  -> 抽取实体；对候选做解析/去重
  -> 抽取事实边；用 LLM 解析 duplicate / contradicted 候选
  -> 更新实体属性与摘要；保存图

search(query, ...)
  -> 关键词 + 向量候选，合并排序（BM25 + cosine + RRF）
  -> 默认返回 EntityEdge；高级入口加 nodes/episodes/communities 与可选 BFS/MMR/cross-encoder
  -> 调用者把边转为 context（示例只拼接 edge.fact）
```

事实边保存两端 UUID、`fact` 文本、embedding、来源 episode UUID 列表与时间字段。MENTIONS 边与 episode 的 `entity_edges` 列表构成回查连接。实体摘要先追加，再在长度阈值后走 LLM 摘要，且无逐句有效期。

## 3. 持续性材料

保留内容：episode 及其内容、实体节点、带 `valid_at`/`invalid_at` 与 `created_at`/`expired_at` 的事实边、实体摘要与来源连接。`store_raw_episode_content=False` 会在保存前把进程内 `episode.content` 置空，因此保留 UUID 不等于保留完整可审计原文。普通个人历史、共同关系材料与项目历史都可编码为 episode 与边，但 framework 不区分这些域；它保留的是 episode、实体与时间化事实。

## 4. 变更与修复

- 矛盾解析是语义且 LLM 介导的，而不是日期运算：一旦被选为候选，代码跳过不重叠区间，把较早事实的 `invalid_at` 设为新事实开始时间并写 `expired_at`。迟到旧事实也可被更晚候选截断。严格 `<`/`>` 与非空时间条件意味着同时间或缺时间事实不走同一套自动消解。
- `remove_episode()` 按 `edge.episodes[0]` 等于该 episode UUID 删除边，只删除仅被该 episode 提及的实体，再删 episode。它不重算保留实体摘要、不清空存活边的来源数组、不重建 community、也不恢复此前失效的边。
- 可静默失败之处：删除后派生摘要与来源数组可能偏离图状态。离线核对显示：两个来源共同支持一条边时，删首来源仍请求删整边；删次来源则保留边且来源数组不变。

## 5. 唤起与使用

检索合并关键词与向量结果；基本入口返回 `EntityEdge`，高级入口可返回 nodes、episodes、communities 并选 BFS、MMR 或 cross-encoder。基本 recipe 是 BM25 + cosine + RRF，并非每次遍历图。调用者决定边如何变成 context：官方 agent 示例只把 `edge.fact` 拼进 system message，并把对话作为新 episode 回写，因此存储时间与来源不会自动全部进入生成。

## 6. 来源、权威与视角

来源连接存在，但不是对所引内容的真实性担保。实体解析混用确定性相似规则与 LLM；边解析检索同端点重复候选与更广矛盾候选，再让 LLM 返回 duplicate/contradicted 索引。候选召回之外的事实不会凭时间规则被比较。应用应区分作者、说话人、信息来源及其权威，不能让 agent 自己的回写被悄然升级成人的认可。

## 7. 时间

Graphiti 有意采用双时间：`valid_at`/`invalid_at` 表示事实何时成立，继承的 `created_at`/`expired_at` 记录图处理时间。然而默认 `search()` 构造空 `SearchFilters()`，四种时间过滤默认 None，因此 docstring 的“当前时间相关性”不是自动排除历史失效事实。历史/当前视图是可配置能力，调用者必须选择查询语义。

## 8. Surfaces、模型与身份

`group_id` 是图分区，写入可创建 request-scoped driver 以避免并发重定向共享 driver。检索的 group 条件可选，空值规范化为无过滤。该分区设施本身不能证明人级授权、同意管理或跨关系隔离；调用者把认证主体绑定到允许的 group、来源与串行写入顺序。framework 不在自身词汇中区分个人、关系与项目材料。

## 9. 前瞻行为

没有未来触发或唤醒行为。`valid_at`/`invalid_at` 描述事实何时成立，不是排定行动。未来计划文本可以存为 episode 或事实，这不提供未来意向触发执行。

## 10. Contributor control 与用户主权

`remove_episode()` 是可见的删除入口，但它不闭合派生状态上的撤回传播，如上所述。用户层面的“只撤回这一个来源”是否成立属于调用契约问题，不是代码保证。

## 11. 已知成功与失败

SOURCE-OBSERVED（静态、固定版本）：支持“何时发生”与“何时系统获知”两类查询的双时间边；可承载来源的图；增量重组。离线源码分支观察：两个来源共同支持一条边时，删首来源仍请求删整边、删次来源保留边不变；exact-duplicate shortcut 复用旧边、追加来源、保留旧有效期且不调用 LLM。UNVERIFIED：真实自然语言抽取、候选召回与真实数据库是否走到这些分支；冲突准确率；中文细节保留；隐私删除完整性；规模与延迟；任何优于 RAG 的效果。

## 12. 候选 Relata 边界上的可观察性

图例：`N` native · `E` adapter-emulated · `O` opaque · `U` unsupported · `?` unknown · `—` not applicable（定义见 [`systems/README.zh-CN.md`](../README.zh-CN.md)）。

| 候选观察 | 类别 | 证据 | 失真说明 |
|---|---:|---|---|
| ordered history exposure | N | source study，“一条原生生命周期”（add_episode） | episode 按组组织，非全局有序日志 |
| distinct ingest/write output | N | source study，“一条原生生命周期”（`add_episode`） | 内联抽取；写入被 await |
| retrieval/activation material | N | source study，“一条原生生命周期”（search） | 基本入口返回边，不是 context |
| rendered model context | E | source study，“时间、冲突与来源”（示例拼接 `fact`） | 组装属示例/应用代码 |
| final response or action | E | source study，“时间、冲突与来源”（示例 agent） | framework 不生成回答 |
| correction/revocation route | N | source study，“Scope、更新与撤回”（`remove_episode`） | 不重算派生状态 |
| inspection/explanation route | N | source study，“时间、冲突与来源” | 边/episode 可查；摘要不透明 |
| time advance or future wake | U | source study，“一条原生生命周期” | 时间字段是有效性，不是触发器 |
| full-history or full-search exposure | N | source study，“Scope、更新与撤回”（保留 episodes） | 原文可选（`store_raw_episode_content`） |
| multi-project isolation | O | source study，“Scope、更新与撤回”（`group_id`） | 仅分区；调用者绑定 auth |
| artifact/source authority | O | source study，“时间、冲突与来源” | 来源连接不是真实性担保 |
| role/surface routing | O | source study，“Scope、更新与撤回” | 无 role/surface 路由 |
| cross-domain context contamination | O | source study，“Scope、更新与撤回” | 需调用者强制 group 边界 |

## 13. 候选 Relata probes

本 card 可对 D-004（repair without overcorrection）与来源/权威忠实施加压力：source study 提议同句复现的有效区间 probe（1 月陈述、2 月离开、3 月重新入职，外加平行的关系约定），以及双来源支持 probe，先后删除共享事实的首、次来源，检查存活事实、episode UUID、共享摘要与此前失效边。保留系统的 lane 是原生写/检索边界加固定离线分支核对；不要把示例 agent 的 only-fact 组装当作系统结果。

## 14. 保密与发布限制

仅公开源码。不得发布私人数据或暗示 Zep managed 保证，也不得把离线分支核对当作端到端结果或维护方背书。

## 15. 来源 / contributor review

- 系统描述对既定用途足够准确：yes
- review 依据与检查的源码路径：对照核查 [`systems/source-studies/graphiti.md`](../source-studies/graphiti.md) 及其固定 commit 链接；离线核对 [`observations/graphiti-observe.py`](../source-studies/observations/graphiti-observe.py) 与 [`graphiti-observed.json`](../source-studies/observations/graphiti-observed.json)；图模型 [`graphiti.json`](../architecture-atlas/models/graphiti.json)
- Public-safe contributor-derived fields approved：not applicable（仅公开源码）
- 保留的分歧或未知：真实抽取是否走到所观察分支；删除传播；全部运行与语义效果 UNVERIFIED
- Review date：2026-10-23
- Reviewer / contributor confirmation route：Relata source-fidelity review；无 contributor 确认适用
- Review 限制：本轮 2026-10-23 仅核对既有 source studies 与 atlas models 的一致性；未重读全部 upstream 链接、重跑离线核对或执行系统。此前 2026-10-14 review 来源未能建立，不予追认。
