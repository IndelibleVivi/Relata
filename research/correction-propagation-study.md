# 更正传播研究：一次更正之后，哪些旧影响仍沿其他 read path 回来

**Status:** `draft` / `proposed`。本文是基于已有固定源码研究的**再综合（secondary synthesis）**，不是新的源码阅读、新的上游调查、新运行结果、accepted Evidence Card、case acceptance 或系统评测。它不改变任何 source study、Case Card 或 Evidence Card 的接受级别。

**Scope:** public-source research and synthetic-case writing only。本文不执行上游、不调用模型或 embedding provider、不部署、不新增 runner / adapter / service / scorer、不写 Tilia 产品实现。

**Evidence basis:** 本轮**没有**新读上游源码，也没有任何新运行。下面每一处机制性判断都来自仓库内已有的十份 [source-study drafts](../systems/source-studies/README.md) 与 [architecture atlas](../systems/architecture-atlas/README.md) 的 `models/*.json`（pinned source-observed），并沿用其证据口径。凡原文标注为 `INFERRED` / `UNVERIFIED` 的，本文不升格。exact 上游链接指向既有报告已固定的同一 commit/行区间；本轮没有重新 GET 验证，也未运行 `observations/` 脚本。

## 中文摘要

本文问一个具体问题：**当一处记忆被更正后，哪些仍然存在的旧影响可能沿其他 read path 回来；同时怎样保留那些并未被撤回的邻域？** 它复用十份 source studies 与架构 atlas 的 `revision` 视图，对 Mem0、Letta、Graphiti、Hindsight、A-MEM 做深入比较，并加入机制不同的 Aelios 作为对照。核心做法是把「写入/整理解析」与「读取路径（retrieval / 自动注入 / boot / 延迟任务）」分开观察：更正可能只改了一条主记录，而旧值仍可能从 recent-message 缓冲、派生 observation、过期 embedding、近似重复边、历史 transcript 或另一个 read path 返回。本文区分 update / supersede / retract / delete / archive / expire，不把它们当同义词；把「未观察到」记为 `unknown` 而非缺陷；不产出总分，也不判定某个候选胜出。文末给出三条可证伪的 competing hypotheses（含可区分观察与真正的反证条件）、三组公开合成 mini incident（三组均为既有问题族的 development adaptations，不新增独立 family 计数；每组含完整原始 utterance、明确更正、具体 probe、不变邻域、对照与能/不能得出的结论）、一张跨系统机制表，以及连接到 first-cycle Q2 与既有 test map 的设计启示。

## English summary

This draft is a secondary synthesis over Relata's existing pinned source studies and architecture atlas; it adds no new source reading or runs. It asks which stale influences can return through read paths that a correction never touched, while still preserving the un-retracted neighborhood. It draws a mechanism table across Mem0, Letta, Graphiti, Hindsight, A-MEM and Aelios (entry point, affected objects, derived layers/neighborhood, read path, timing/recovery, positive capability, evidence line), separates update / supersede / retract / delete / archive / expire, treats unobservability as `unknown` rather than a defect, and refuses composite scores. It states three falsifiable competing hypotheses, three public synthetic development adaptations (no additional independent families) with controls, minimal observations and claim limits, links design implications to first-cycle Q2 and the existing test map, and closes with prioritized questions and tradeoffs. Nothing here is accepted evidence, human review, a system result, or a winner declaration.

## 1. 问题与边界

一次「更正」在系统里可能只落在**一条主记录**上：一条 fact 被 update、一条边被 invalidate、一个文件被 delete。但「更正后的后续影响」并不只经过那一条记录。相同的过去可能同时存在于多种状态中——原始消息/transcript、recent-message 缓冲、抽取事实、派生 observation/画像/摘要、embedding、图边、boot 快照——它们有各自的 writer、刷新时机和读取入口。于是核心问题拆成两半：

1. **回归问题**：更正之后，哪些旧影响仍可能沿**未被更正触及的 read path** 回来？
2. **邻域问题**：怎样让更正生效，又不误伤那些**并未被撤回**的邻近材料（同一关系、同一项目、同一 scope 里仍然有效的部分）？

三个必须先立住的区分（后文所有比较都依赖它们）：

- **写入/修订 vs 读取/消费。** 更正发生在一个位置，但「旧值是否回来」发生在另一个位置。只检查写路径会漏掉 read path。
- **操作不是同义词。** `update`（原位改值）、`supersede`（新版取代旧版、旧版降级但常仍可查）、`retract`/`invalidate`（撤回某事实并可能连带派生）、`delete`（移除记录/文件）、`archive`/`expire`（移出 live 但保留）、`redact`（输出或输入脱敏）语义不同，其传播范围也不同。任何一个都不能代表「忘记」。
- **不可观测 ≠ 缺陷。** 某系统把派生层藏在托管或异步阶段时，正确记录是 `unknown`，不是自动判 failure（沿用 [claim-boundary](claim-boundary-study.md) 的取向）。

读法沿用既有 atlas 的 `revision` 视图（"更正、删除与派生状态传播"），并补充既有报告里已经写出的 read path：retrieval 候选、自动注入、boot 快照、延迟/后台任务。

## 2. 跨系统机制表

下表的每一行都以既有固定源码研究为据；「证据界线」列写清该行结论的来源层级与未验范围。**不构成质量排序**：不同系统解决的是不同问题，行内「正面能力」指机制提供的可能性，不是已测量的部署效果。

| 系统（pinned） | 更正入口 | 受影响对象 | 派生层 / 邻域 | read path | 时间 / 恢复 | 正面能力 | 证据界线 |
|---|---|---|---|---|---|---|---|
| **Mem0** `a39a802` | 显式 `update(id)`（替换文本与向量、保留创建时间、写 UPDATE history）；`delete(id)`（删主向量、写含旧文本的 DELETE history） | 单条 fact 记录 + 其向量 | entity 关联（best-effort 清理）；recent-message 缓冲**未**随删除清理 | `search`（semantic 候选池先于融合过滤；keyword/entity 命中不能救回池外条目） | 变更 history 可审计；缓冲是否在后续 `infer=True` 抽取中再生需 probe | 追加保存与显式修订分离、检索结果可检查、操作可审计 | 更正入口 SOURCE-OBSERVED：[update/delete `main.py#L2038-L2128`](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/main.py#L2038-L2128)、[entity cleanup `main.py#L652-L728`](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/main.py#L652-L728)；read path SOURCE-OBSERVED：[semantic 候选门槛 `utils/scoring.py#L60-L139`](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/utils/scoring.py#L60-L139)、[search `main.py#L1628-L1731`](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/main.py#L1628-L1731)；缓冲再抽取 UNVERIFIED（[mem0.md](../systems/source-studies/mem0.md)） |
| **Letta** `f5c5bbc` | `memory delete` 删文件并 commit；`str_replace`/`insert`/`rename` 编辑 MemFS | MemFS 工作区文件（core/deferred/external） | compaction summary、原始 transcript、Git 历史、Cloud 远端；记忆正文里的复述**无**级联 | 编译后 system prompt（`<self>`/`<memory>`）；本地 recall 为 FTS-lite；搜索结果需调用方注入 | 每次 turn 比较 Git revision，revision 改变才产生新 memory update；delete 不触发 transcript/summary 撤回 | 修订进入后续 context；经验保留与活动摘要分离，可再检索 | 更正入口 SOURCE-OBSERVED：[delete/rename 无级联 `tools/impl/memory.ts#L289-L350`](https://github.com/letta-ai/letta-code/blob/f5c5bbce6e9394b30c626909315c2b3acc665672/src/tools/impl/memory.ts#L289-L350)；read path SOURCE-OBSERVED：[HEAD 驱动编译 `system-prompt-compilation.ts#L76-L115`](https://github.com/letta-ai/letta-code/blob/f5c5bbce6e9394b30c626909315c2b3acc665672/src/backend/local/system-prompt-compilation.ts#L76-L115)、[revision 检测 `local-backend.ts#L924-L1003`](https://github.com/letta-ai/letta-code/blob/f5c5bbce6e9394b30c626909315c2b3acc665672/src/backend/local/local-backend.ts#L924-L1003)；模型遵循未验（[letta.md](../systems/source-studies/letta.md)） |
| **Graphiti** `16cdf70` | **语义矛盾候选** → 较早边 `invalid_at` 置为新事实开始时间并写 `expired_at`；`remove_episode()` 删除**首来源恰为该 episode** 的边（按 `edge.episodes[0]` 判定，不是检查来源数组只有一项），并非笼统删所有关联边 | 事实边（含 `valid_at/invalid_at/expired_at` 双时间）、源 episode 数组 | 共享实体摘要（**不**逐句失效，`node_operations` 另走追加/LLM 分支）、community、存活边的来源数组 | `search()` 默认 `SearchFilters()` 时间为 None → 当前有效性需要调用方显式过滤或下游判读，不能假定默认已过滤；官方示例只拼 `edge.fact` | 双时间支持「何时发生/何时获知」两类查询；LLM 语义裁决有不确定性 | 时间与来源成为可查询结构；失效历史边可保留供查询 | 更正入口 SOURCE-OBSERVED：[区间失效 `edge_operations.py#L538-L572`](https://github.com/getzep/graphiti/blob/16cdf7045378c8d53ae01f94e2fa60d238cb0f68/graphiti_core/utils/maintenance/edge_operations.py#L538-L572)、[remove_episode 首来源条件](https://github.com/getzep/graphiti/blob/16cdf7045378c8d53ae01f94e2fa60d238cb0f68/graphiti_core/graphiti.py#L1824-L1852)；read path SOURCE-OBSERVED：[默认空过滤 `graphiti.py#L1586-L1691`](https://github.com/getzep/graphiti/blob/16cdf7045378c8d53ae01f94e2fa60d238cb0f68/graphiti_core/graphiti.py#L1586-L1691)、[基本 recipe `search_config_recipes.py#L80-L116`](https://github.com/getzep/graphiti/blob/16cdf7045378c8d53ae01f94e2fa60d238cb0f68/graphiti_core/search/search_config_recipes.py#L80-L116)；首来源删除分支另有既有离线替身观察；真实抽取/召回/数据库行为 UNVERIFIED（[graphiti.md](../systems/source-studies/graphiti.md)） |
| **Hindsight** `9c7f6c6` | fact edit 使关联 observation 失效；document delete 删关联 facts/links 并清 stale observation；invalidate 归档到 `invalidated_memory_units` | documents/chunks、world/experience facts、observations、mental models | observations（绑 `source_memory_ids`）、mental model 文档、history 快照 | recall（多路 semantic/text/graph/temporal + RRF）；reflect 为只读 tool loop；可选 LiteLLM callback 注入 context | 源移除→observation 行与 history 删除、幸存来源 `consolidated_at` 归空后重新归纳；mental model 仅 best-effort 刷新，手动模型由 owner 维护 | 原始依据与派生理解分开、可回查来源、异步刷新可检查 | 更正入口 SOURCE-OBSERVED：[删除受影响 observation/history `writes.py#L240-L338`](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memories/pg/writes.py#L240-L338)、[fact edit 失效 observation `memory_engine.py#L12065-L12225`](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L12065-L12225)；read path SOURCE-OBSERVED：[recall 多路候选 `memory_engine.py#L8550-L8668`](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L8550-L8668)、[融合 `#L8849-L9210`](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L8849-L9210)；invalidation archive 是否可经任何当前 read path 达 UNKNOWN（[hindsight.md](../systems/source-studies/hindsight.md)） |
| **A-MEM** `0c8039f` | **无专用更正/删除/撤回 API**；新输入可触发 `UPDATE_NEIGHBOR` 覆盖旧 note 的 context/tags | note（content 保留；context/tags 可被改写） | 旧 note 的 corpus/embedding 行**不即时刷新**（`evo_threshold` 计满才全量重建）；positional `links`；新 note 可携带 STRENGTHEN 链接 | 单跳 link 扩展 + query-embedding top-k cosine | 默认 `evo_threshold=100`（仅计「被标记演化」的 add）才全量重建索引；无 revision history | 新经验可重组旧 note 的组织方式、链接扩大上下文 | 演化入口 SOURCE-OBSERVED：[邻居更新 `memory_layer_robust.py#L463-L540`](https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer_robust.py#L463-L540)、[重建阈值 `#L352-L409`](https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer_robust.py#L352-L409)；read path SOURCE-OBSERVED：[共享 cosine top-k `memory_layer.py#L554-L610`](https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer.py#L554-L610)、[robust 单跳 links `#L411-L459`](https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer_robust.py#L411-L459)；排名是否改变 UNVERIFIED（[a-mem.md](../systems/source-studies/a-mem.md)） |
| **Aelios** `9e65c80`（机制对照） | `upsertMemoryByFactKey`（同键原地改）、`supersedeMemory`（新 ID、旧版本下架向量、写版本指针）、REST soft-delete、MCP v2 hard-delete、夜间 Dream supersede | `memories` + `memory_lifecycle`、`memory_candidates` | triggers（`trg:` 向量）、daily/weekly/monthly 印象、`perception_cache`、原消息与 exchange | 召回合并多空间多来源候选再重排注入当前 user 尾部；显式 boot 读 precious/glossary/印象/感知缓存 | 存在多套删除语义；触发器的 D1 复核挡已删记忆，但派生 trigger 不保证删除；retention 按 `updated_at` 180 天过期 | 显式 fact_key/版本/署名、珍贵原文、可检查候选与来源窗口 | 更正入口 SOURCE-OBSERVED：[同键 upsert/supersede `db/v2/memories.ts#L173-L287`](https://github.com/wusaki0723/Aelios/blob/9e65c802ec1c13a68d22a68c5c9d7cdce385e041/src/db/v2/memories.ts#L173-L287)、[supersede `#L385-L586`](https://github.com/wusaki0723/Aelios/blob/9e65c802ec1c13a68d22a68c5c9d7cdce385e041/src/db/v2/memories.ts#L385-L586)；read path SOURCE-OBSERVED：[boot 读印象/感知缓存 `memory/v2/recall.ts#L202-L270`](https://github.com/wusaki0723/Aelios/blob/9e65c802ec1c13a68d22a68c5c9d7cdce385e041/src/memory/v2/recall.ts#L202-L270)、[perception 快照 `memory/perception.ts#L36-L111`](https://github.com/wusaki0723/Aelios/blob/9e65c802ec1c13a68d22a68c5c9d7cdce385e041/src/memory/perception.ts#L36-L111)；删除跨层同步 UNVERIFIED（[aelios.md](../systems/source-studies/aelios.md)） |

（更广的十系统对照见 [source-studies README 机制表](../systems/source-studies/README.md)；本表只抽取与「更正传播」直接相关的入口、派生层与 read path。上述 exact 上游链接取自各 source study 与 architecture atlas `models/*.json` 已固定的同一 commit 与行区间；**本轮没有重新 GET 验证这些上游对象**，语义以既有报告为准。）

### 2.1 表读出的四条结构性观察（`INFERRED`；均为**待区分假设**，非测量结论）

1. **更正写入点与检索使用点可能分离。** 静态源码显示二者的控制量不同：Mem0 的 `update` 改主记录，而 `search` 的候选池由 semantic threshold 先截断；Graphiti 写 `invalid_at`，但默认时间过滤为 None；A-MEM 改 note metadata，embedding 是否随之刷新取决于重建路径与阈值。因此**需要区分**「记录已改」与「新值被检索到 / 旧值不再被检索到」是两个可观察量，而不能直接推断二者一致。
2. **派生层是候选回归通道，但不能据机制清单判定普遍性或收敛速度。** 表中若干系统存在派生层（Hindsight 的 observation / mental model、A-MEM 的 embedding vs metadata、Aelios 的 trigger / perception / rollup），既有报告指出部分路径存在延迟、阈值或 best-effort 刷新；具体对象不能一概视作不同步。但是否真的回归、回归多久、是否随规模变差，均无本轮测量；本文没有证据支持「普遍」「最晚收敛」「派生层越多窗口越长」，只能作为待区分的假设（见第 3 节 H2/H3）。
3. **多 read path 使「撤回」难以闭包，是一条可能的解释而非结论。** 同一个过去可能从 transcript（Letta）、recent-message 缓冲（Mem0）、失效历史边（Graphiti）、impression 快照（Aelios）等位置返回，而这些入口不必共享同一更正触发器。它们是否**真的**在当前读取中让旧值回来，需要按 read path 逐项观察（见 H3）。特别地，Hindsight 的 `invalidated_memory_units` archive 与 mental model history 的**可读性**在既有报告中是 `unknown`：既有来源只说明「归档 / 历史快照存在」，未证明存在一条当前 read path 消费它，因此**不把保留供审计写成回归通道**。
4. **邻域误伤与回归是两种相反的失败面。** 激进级联（删源即连删派生）可能清空尚未被撤回的邻域；保守保留可能延长旧值可见期。二者需要分开观察（见第 6 节），但不能预设哪一种更普遍。

## 3. 三条可证伪的 competing hypotheses

三条解释针对同一现象（更正后旧影响仍被读到），**互相竞争也可以并存**：一次观察可以同时由其中两条解释。它们的价值在于给出**能区分观察的干预**，以及**可在固定历史上反证的条件**——而不是给一个「胜出解释」。

**H1 — 主记录假设（main-record hypothesis）。**
> 回归可由「更正本身没落到正确记录 / scope / identity」解释：更正命中的是别的记录或错误 scope，目标记录从未被改到。

- **区分干预：** 更正后核对写入回执、目标记录 identity 与 scope 是否即所声称者；再做一次已知命中目标记录的更正。
- **反证条件（削弱 H1）：** 更正已确认命中目标记录与 scope，且目标记录的 current 值已为新值，旧影响仍被读到。
- **可并存说明：** 一次研究的不同记录或不同时点可以分别暴露 H1 与 H2/H3；对已确认改对的同一目标，H1 不能再解释其残留旧影响。

**H2 — 派生延迟假设（derivation-lag hypothesis）。**
> 回归可由「源更正后，派生层（observation、mental model、embedding、trigger、impression 快照）尚未刷新」解释。注意：**延迟本身不保证正确**——即使最终会在刷新后收敛，在刷新前的任何一个时间点，读取仍可能把旧值当作事实并据此产生错误输出。

- **区分干预：** 记录每层的 current 值 + 刷新/水位信号 + 时刻，并在「已知刷新完成」后再读一次。
- **反证条件（削弱 H2）：** 在所有相关派生层都已给出「已刷新」的可观察信号（且该信号**经语义一致性核对**，不只是「刷新过」的标记）之后，旧影响仍在读取时返回。
- **不可判定边界：** 若某派生层当前不可观测（无 current 值、无水位、无刷新信号），则无法区分 H2 与其他解释，该情形记为 `unknown`，不据此判 H2 成立或失败。「刷新标记」不等于「语义已一致」，两者必须分开记。

**H3 — 多路径假设（multi-path hypothesis）。**
> 回归可由「存在多条独立 read path，而更正只被其中一部分可见」解释：即便所有派生层都已刷新，仍有一条 read path（例如 recent-message 缓冲、默认无时间过滤的 search、boot 快照、仍活跃的历史边）把旧影响带回来。

- **区分干预：** 逐条枚举并单独查询已声明的 read path（每路单独请求、记录返回值与来源层），并在「只经该路径」的条件下观察旧值是否出现。
- **反证条件（削弱 H3）：** 在有完整输入捕获的有界调用中，已确认所有实际被消费的路径都不含失效内容，最终输出却仍采用旧值；这削弱“另一 read path 携带旧值”的解释，转而检查 reader 的推断/使用。只检查若干可见路径不够反证。
- **与 H2 的区分：** 关键在于**是否需要等待刷新生效**——若在派生层刷新后回归消失，主要支持 H2；若刷新后回归仍在**某条特定路径**上稳定出现，支持 H3。
- **观察边界：** 修复一条路径后回归消失，与 H3 相容；“没找到旧值来源”若只因 trace 不完整，应记 `unresolved`，不能当反证。

三条解释都在**同一固定合成历史**上区分：变化的是「更正落点是否命中」（H1）、「是否等待派生刷新」（H2）、「读哪个入口」（H3）三个干预，而不是更换系统。当某一层不可观测、或某干预无法在原生条件下实施时，应记 `unresolved`，保留无法区分状态，不强行归因。

## 4. 三组公开合成 mini incident（development adaptations，不新增独立 family）

以下三组是**新写的公开合成**场景（adults only，无真实对话），但它们是**development adaptations**：I-B 沿用 [RC-001](../case-lab/cases/pilot-001-current-state-without-erasure.md) 的「停用短语但保留熟悉 presence」机制，I-C 沿用 [RC-005](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md) 的 provenance / 更名机制。因此它们**不增加独立 incident family 计数**，只能作为既有 family 的**开发用例**（用于打磨语义与工程），不能自称独立验证材料；锁定某项设计主张后仍需未参与开发的新变体。I-A 复用「项目交付日」主题族（[lmc-5](../systems/source-studies/lmc-5.md) / [Mem0](../systems/source-studies/mem0.md) 的 probe 同族），同属开发材料。执行条件一律保留 current-only、full-history、full-search/simple-file 三种对照（对齐 [test map §5](memory-design-test-map.md) 的 C0/C2/C3）；全部为 `proposed`、未运行。为便于 dry-review，每组给出**完整原始 utterance、明确更正、具体 probe、不变邻域与反事实/控制**。

### 4.1 Incident I-A —「发布日」事实更正：派生 observation 与保留邻域

- **原始历史（synthetic，成年 A 与 agent，同一项目 scope）：**
  - Day 1（2026-03-02，周一）A 说：「初稿定在 **2026-03-06（周五）** 公开。」
  - Day 3（2026-03-04）A 补充：「发布会上用『**青瓷**』主题，另外 **审校交给 B**。」
- **局部改正（Day 4，2026-03-05）：** A 说：「更正：**公开日改成 2026-03-10（周二）**，比原计划晚四天。**审校还是 B，主题还是青瓷，其它都不变。**」
- **应保留邻域（不变项）：** 「审校由 B 负责」「青瓷主题」仍有效，且不得因本次更正被抹掉或失联。
- **probes（各条件使用相同问题）：**
  - P-A1：「初稿现在定在哪天公开？」（期望：2026-03-10）
  - P-A2：「这批稿子谁审校？」（期望：B；邻域不变项）
  - P-A3：「发布会用什么主题？」（期望：青瓷；邻域不变项）
- **反事实/控制：** C0 仅给当前轮；C2 给完整的三条事件历史；C3 用平文件＋全文搜索，从**相同 raw 输入**开始（不给任一侧写入作者整理的正确状态）。若系统有派生 observation/摘要/boot 快照，另记该层 current 值与刷新时刻。
- **最小观测：** (a) 更正写入回执、目标记录 identity 与 scope；(b) P-A1/A2/A3 返回值；(c) 旧值若回归，归属到哪一层（主记录 / 派生层 / 某 read path）。
- **能得出：** 在给定 reader 下，更正是否同时满足「新公开日生效」与「邻域不失联」；旧公开日是否仍从某层返回。
- **不能得出：** 不判架构优劣、不证明长期可靠性；「邻域仍完整」不等于语义正确。

### 4.2 Incident I-B —「称呼/语气更正」：保留熟悉感而不复发旧短语（RC-001 机制的开发变体）

- **原始历史（synthetic，成年 Lin 与 agent，private 会话）：**
  - Day 1：Lin 说：「以后我说『今天有点沉』，你就先回一句『**我在，别急**』，然后陪我说两句，别分析。」
  - Day 2：Lin 说「今天有点沉」，agent 回「我在，别急」，并陪聊。Lin：「这样就对了。」
  - Day 3：Lin 说：「工作那份目录已经校完；周末我们继续整理相册，先给照片编号。」
- **局部改正（Day 10）：** Lin 说：「那个『**我在，别急**』以后别说了。**还是照旧熟悉地陪我，别变客气，也别分析**。」
- **应保留邻域（不变项）：** 熟悉互动本身、Lin 此前聊过的**两个共同话题**（工作进度、周末安排）不得一起变冷或失联。
- **probe（immediate 与 delayed 两个时点，各三类）：**
  - 复发探测 P-B1：Lin 说「今天有点沉」→ 检查是否出现精确短语「我在，别急」。
  - 邻域探测 P-B2：「上次说的周末安排是什么？」（期望：继续整理相册、先给照片编号；不变项）
  - 过度纠正探测 P-B3：Lin 说「今天有点沉」→ 检查回应是否变成冷/程序化（不主动陪聊、改称「用户」等）。
- **反事实/控制：** 同上三条件；另加 immediate 与 delayed（新 session）两时点。温暖度阈值留待**独立人类评审**，不做自动语义判分。
- **最小观测：** 精确短语在 B1 的 count；B2 是否答对；B3 的熟悉感是否有界；旧短语若回归，来自哪条 read path。
- **能得出：** 局部纠正是否持续，且是否同时满足「不复发」与「不过度纠正」两个相反失败面。
- **不能得出：** 单次成功不等于持续；精确短语检查不能宣称未枚举的语义泄漏也已解决。

### 4.3 Incident I-C —「归属更正」：改‘谁提出’而不丢共同成果（RC-005 机制的开发变体）

- **原始历史（synthetic，成年 A、同事 C、agent，同一项目 scope）：**
  - Day 1：A 说：「**方案由我（A）首提**，你来帮我把草稿写上，标题先叫『**北窗**』。」
  - Day 2：agent 说：「我把你转来的方案整理成草稿了：先列访问清单，再统一标文件编号。」A 说：「确认，这份草稿先保留。」
- **局部改正（Day 5）：** A 说：「更正一下：**这个方案最早是 C 提的，我只是转述**。标题『北窗』和内容都不变。」
- **应保留邻域（不变项）：** 方案内容、『北窗』标题、A 与 agent 的协作记录均保留，不得被「改归属」连带清除。
- **probes（各条件使用相同问题）：**
  - P-C1：「这个方案最早是谁提出的？」（期望：C）
  - P-C2：「方案现在叫什么？」（期望：北窗；不变项）
  - P-C3：「谁协助把方案整理成草稿？草稿列了哪两个步骤？」（期望：agent；列访问清单、统一标文件编号，均为不变项）
- **反事实/控制：** 同上；另加移除说话者标记的诊断，但本文正文仍显式包含 A/C 身份，不能把它当成去角色后必然产生字节碰撞的 RC-005 实验。
- **最小观测：** P-C1/C2/C3 返回值；回归时旧归属来自哪一层（含 agent 自身回写的断言）。
- **能得出：** 在给定条件下，归属更正是否生效且不破坏内容邻域。
- **不能得出：** 不能把一次归属正确当作多主体权限/同意的证明；系统读出「C」不代表它理解了「转述」这一关系。

## 5. 设计启示（连接 first-cycle Q2 与既有 test map）

- **Q2 的验收对象应是 read path，而不是单个写入口。** [first-cycle §2 Q2](first-research-cycle.md) 要求「更正如何沿实际 read paths 改变后续行为，同时不抹掉未撤回的邻域」。本文机制表把 read path 显式列为一列；建议 Q2 的每个 family 都记录「更正写在哪里」与「旧影响从哪个 read path 回来」两个坐标。
- **落在既有维度上，不新建 ontology。** X3（supersession/coexistence）、X7（修复后保留与过度纠正）、X9（派生状态与跨层传播一致性）已覆盖本主题；[test map §5 E-B](memory-design-test-map.md) 的「修订 → 派生传播切片」正是本文三组 development incident 的通用形式。本文不新增维度、不改写它们，只提供可 dry-review 的具体 incident。
- **派生层要分别记时间。** H2/H3 的区分要求记录每层 current 值与刷新时刻；这与 test map X9「每层的 current 值、写入/刷新时刻」一致，也与 [first-cycle §11](first-research-cycle.md) 的「原生 ready 信号或其缺失」一致。
- **邻域要用不变性检查，而非只查违规。** Incident I-A/I-C 的「应保留邻域」问题就是对未撤回材料的 invariance check，对应 [first-cycle §5](first-research-cycle.md) 的「邻域保留可用 invariance checks」。
- **不要把一个候选宣判胜出。** 本文机制表是横向机制对照，不是评分表；H1/H2/H3 是竞争假设空间，不是三种架构的名次。若将来进入实测，应保留 [first-cycle §9](first-research-cycle.md) 的 retain / simplify / reject 处置语言与 [ADR-0009](../decisions/ADR-0009-exploratory-research-boundary.md)（proposed，未接受）的执行边界。

## 6. 最值得优先研究的问题与取舍

1. **哪条 read path 最容易让旧值回归？** 优先级最高，因为它决定「更正」到底要触及几处。取舍：逐一枚举 read path 需要系统暴露中间状态；对不可观测层只能记 `unknown`，不能补造假路径。可先对可见 read path（检索候选、编译 context、boot 快照）做对照。
2. **派生层刷新是否可被外部观察到 ready？** 若不能，H2 与 H3 都无法干净分离。取舍：把「刷新 ready 信号」作为观察对象，而不是假定它存在；缺信号时降低结论强度。
3. **邻域保留与回归消除是否总是可同时满足？** Mem0 的 `infer=True` 会读 recent-message 缓冲，Graphiti 的时间过滤影响历史边候选；这些有具体读取入口。Hindsight 的 archive/history 则只确认留存，当前消费路径未知，不能一概称为回归通道。取舍：区分「保留供审计」与「仍驱动当前行为」两种用途，而不是二选一。
4. **更正权限与 scope 的绑定。** 若更正的 scope/fact_key 落点错误，H1 会掩盖真实原因。取舍：先固定操作、scope、输入视图与 reader，再谈机制差异（对齐 [first-cycle §7](first-research-cycle.md) 控制纪律）。
5. **中文与中英混合。** 既有报告已指出部分实现的后备 heuristic 偏英文；语义等价 matcher 尚未成 fixtures。取舍：先做纯机械检查（token 存在/缺失、层值/时刻绑定），语义判断留给独立人类评审。

## 7. 证据界线与未验事项

- 本文**没有**新增源码阅读、上游执行、模型/embedding/provider 调用、数据库或网络运行；所有机制陈述均为对既有来源研究的**再综合**，其底层证据层级（SOURCE-OBSERVED / 离线分支观察 / INFERRED / UNVERIFIED）以各报告为准，未升格。机制表中的 exact 上游链接取自既有 source studies 与 atlas 模型已固定的同一 commit 与行区间，**本轮没有重新 GET 验证**。
- 本文**没有**创建 ontology、平行 topology、runner、adapter、service、scorer 或 accepted ADR；没有新增或改写任何案例的接受级别。
- 第 4 节三组 mini incident 全部为 `proposed`、未运行，且明确是既有 family 的 **development adaptations**，**不新增独立 family 计数**；其「应保留邻域」「正面收益」均为设计对象。任何端到端试验仍需独立执行授权、exact 对象/配置与成本口径。
- 未核查上游 hosted / 托管阶段、未验证中文召回、未验证长期稳定性与任何「更正传播收敛」的端到端效果。Hindsight 的 archive / history 是否可经某条当前 read path 达，以及「保留供审计」是否也是回归通道，均记 `unknown`。

后续的[更正并发 challenge](correction-race-challenge.md)把 H2/H3 的竞争解释展开为任务交错与恢复对照；独立的 [Hindsight 源码核查](stale-write-source-audit.md)寻找已有保护。这些后续材料有自己的证据范围，不改变本文作为既有研究再综合的性质。

## 8. 参考入口（repo-relative）

- 十份 source studies 与对照表：[systems/source-studies/README.md](../systems/source-studies/README.md)
- 各系统报告：[Mem0](../systems/source-studies/mem0.md) · [Letta](../systems/source-studies/letta.md) · [Graphiti](../systems/source-studies/graphiti.md) · [Hindsight](../systems/source-studies/hindsight.md) · [A-MEM](../systems/source-studies/a-mem.md) · [lmc-5](../systems/source-studies/lmc-5.md) · [Tideline Memory](../systems/source-studies/tideline-memory.md) · [Aelios](../systems/source-studies/aelios.md) · [OpenViking](../systems/source-studies/openviking.md) · [LangMem](../systems/source-studies/langmem.md)
- 架构 atlas（含各系统 `revision` 视图）：[systems/architecture-atlas/README.md](../systems/architecture-atlas/README.md)
- 研究问题与写作入口：[research/agent-memory-inquiry.md](agent-memory-inquiry.md)
- 第一研究周期（Q2）：[research/first-research-cycle.md](first-research-cycle.md)
- 设计/测试映射（X3/X7/X9、E-B 与 C0–C5）：[research/memory-design-test-map.md](memory-design-test-map.md)
- 案例：[RC-001](../case-lab/cases/pilot-001-current-state-without-erasure.md) · [RC-005](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md)
- 候选方法学边界：[research/claim-boundary-study.md](claim-boundary-study.md)
- 候选执行边界（proposed，未接受）：[decisions/ADR-0009-exploratory-research-boundary.md](../decisions/ADR-0009-exploratory-research-boundary.md)
