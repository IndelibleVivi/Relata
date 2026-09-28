# Relata 第一研究周期计划（proposed）

**Status:** proposed research programme plan。它不是 accepted 执行决定、结果论文、排定日程或已批准预算；任何 live study、部署与发布仍需各自授权。
**Authority:** 依次遵循 [STATUS](../STATUS.md)、[CHARTER](../CHARTER.md)、[ASSUMPTION_REGISTER](../ASSUMPTION_REGISTER.md) 与 accepted decisions；[AGENTS.md](../AGENTS.md)将其落实为工程边界。[ADR-0008](../decisions/ADR-0008-three-core-research-functions.md) 已接受三项核心职能。有关探索性执行的边界见 proposed [ADR-0009](../decisions/ADR-0009-exploratory-research-boundary.md)，它在被接受前不授予执行权限。
**Reuse:** 复用现有 cases、[十份 source studies](../systems/source-studies/README.md)、[architecture atlas](../systems/architecture-atlas/README.md) 与 [设计／测试映射](memory-design-test-map.md)；不新建 topology、运行接口或评分契约。

## 中文摘要

本文提出 Relata 第一个实质研究周期的计划：把自有 benchmark 研究、系统样本研究空间（museum 名称仍开放）与未来系统 incubator 三项核心职能，加一条以证据为锚的 comparative synthesis 串起来。三项职能各有独立交付物，可以分别发布，不要求等待一次共同 release。周期围绕三个问题组织：跨 session 的共同／项目工作延续（RC-003/005）；更正如何改变后续影响而不破坏仍有效的邻域（RC-001 与 source-derived propagation 问题）；有用普通回忆与 scope/use/silence 的边界（RC-002/004）。计划把 12–20 个独立 incident families 设为**容量目标**而非科学样本量门槛，给出候选受测对象 readiness matrix、控制纪律、museum 的静态与运行 exhibit 计划（含读者端实现，公开阅读另需授权）、incubator 机制压力测试、一个以 RC-005 现有输入为预检起点、随后进入 native 路径的首个执行包候选，以及分离货币与人工时间的成本口径。prospective memory、companion continuity 与 learning transfer 作为**开放研究**保留其去向与下一个问题。本文全部内容为 `proposed`，不提升任何 case、Source Study 或 Evidence Card 的接受级别。

## English summary

This proposed first research cycle links Relata's three core functions, its own benchmark research, the system study collection (working museum name still open), and future-system incubation, joined by an evidence-grounded comparative synthesis. Each function keeps an independent deliverable and may ship separately. Three questions organise the cycle: continuing shared/project work across sessions (RC-003/005); how a correction changes later influence without damaging still-valid neighbors (RC-001 plus source-derived propagation); and useful ordinary recall with correct scope, use and silence (RC-002/004). 12–20 independent incident families is a capacity target, not a sample-size gate. The plan gives a candidate-object readiness matrix, control discipline, static and runtime museum exhibits (including reader implementation, with public hosting separately authorized), incubator mechanism tests, a first execution-package candidate taking existing RC-005 inputs through reader preflight and then a native memory path, and a cost convention that separates monetary spend from human hours. Prospective memory, companion continuity and learning transfer stay open research with a stated destination. Everything here is `proposed`; no case, source study or Evidence Card changes state.

## 1. 目标与授权边界

本周期的目标是让 Relata 的三项核心职能与 synthesis 同时取得可审查进展，各自保留独立交付与独立价值；本文是一份计划，不替代任何一个具体决策。

- 三项职能不要求共同 release。source study、case、exhibit、机制压力测试与文章可以分别成型、分别发布。
- public hosting 与 live study 属于未来的授权边界，不是本周期已完成的成果，也不能被当作已完成工作。
- 本周期不建立 benchmark runner、system-under-study API、Leaderboard、Arena、SDK、服务、sealed corpus 或统一 system ontology；也不把任何候选设计提升为 evaluator 的答案格式。
- 既有五个 Case Cards 是**已知开发表例**。它们能打磨语义与工程设计，但不能自称独立验证；锁定某项设计主张后，验证需使用未参与开发的新变体。
- **source study、架构研究、文章与 routine 的 state／链接／引用更新按其自身证据与仓库现有授权发布**，不需要为每次常规文档提交单独申请一次 publication 决定。需要独立授权的是：public hosting、正式 release、license 选择与对外 outreach。

系统样本空间的计划包含基于现有 atlas 的读者端实现，以及 hosting 获授权后的公开可读形态。运行 exhibit 展示保存的真实执行记录；读者浏览展品不触发 provider 调用。

## 2. 本周期要回答的三个问题

**Q1 跨 session 的共同／项目工作延续。** 一个系统或 pipeline 能否在 session、revise、handoff 与迟到旧稿之间延续当前 authority，而不被“最新收到”或“最像目标”的材料改写。落点：RC-003 的 project supersession 与邻近 scope 隔离，RC-005 的当前标题与原始提出者 provenance。边界：RC-005 的三个 checkpoint 属于**一个 family** 且相互相关，不是三个独立世界；它测 fixed-history replay，不测持续 co-evolution。

**Q2 更正改变后续影响的范围。** 一次更正如何沿实际 read paths 改变后续行为，同时不抹掉未被撤回的邻域。落点：RC-001 的 current-state-without-erasure，加上第 9 节的 source-derived propagation 问题（哪一层仍以旧值驱动行为）。这里要同时观察 required 与 prohibited 两侧，以及 positive task completion 与生命周期成本，而不是只统计违规。

**Q3 有用的普通回忆与 scope/use/silence。** 普通生活事实能否忠实回来，且只在允许的 scope 进入 context 与 response。落点：RC-002 的 ordinary location continuity，RC-004 的 scope-conditioned routing pair。边界：RC-004 的 textual probe 相同但 target metadata 有意不同，因此它**不是 pure historical twin**，不能继承 RC-001 的因果措辞；其 C0 metadata-only prior shortcut 尚未实测。

三个问题共用一个要求：每个 claim 必须能说明 subject、input view、condition 与 preserved evidence，且把“检索到”“进入 context”“实际正确使用”分开记录。三个问题与现有资产的落点：

| 问题 | 主要 cases | 可借用的 source mechanisms | 需要的新证据 |
|---|---|---|---|
| Q1 | RC-003、RC-005 | Graphiti `group_id`／双时间、Letta 文件修订与编译 | 未参与开发的 handoff／supersession 变体 |
| Q2 | RC-001（＋source-derived propagation） | lmc-5 supersede、Hindsight observation 失效、A-MEM 邻域演化 | 跨 read paths 的更正传播记录 |
| Q3 | RC-002、RC-004 | Mem0 scope 参数、OpenViking peer/scope | metadata-only prior 实测与 negative／negation fixtures |

## 3. 定位：与相邻公开工作的关系

本周期就 multi-session 任务完成、history necessity、持久化的后果与选择性修复等问题提交观察；这些问题并非无人研究。作为 inquiry leads（仅摘要／页面层面的公开入口，尚未做全文或结果复核）：

- [MemoryArena](https://arxiv.org/abs/2602.16313v2)：multi-session 相互依赖的行动；
- [DolphinBench](https://arxiv.org/abs/2609.24971v2)：task completion、history necessity 与 cost / latency；
- [MemSecBench](https://arxiv.org/abs/2607.27080)：persistence、consequence 与 selective repair。

以上仅作**写作与问题的入口**，不表示对其方法、结论或新颖性的背书；它们的存在也说明“任务能完成”本身不构成 Relata 的独特定位。Relata 与 AMS 的 broader inquiry 与长篇写作保持独立：本周期的 synthesis 不需要把更广的 essay 收窄到这三个问题，也不会把这三条入口当作已确认的领域边界。

## 4. 覆盖缺口作为开放研究

缺口是**开放研究**，各有去向与下一个问题，而不是永久排除，也不是已排定的测试：

- **prospective memory（D-006）** 仍缺 community-grounded incident 与 architecture-neutral observation boundary。去向：补一条 community-grounded incident、一个有界的 relational counterfactual 与一张 accepted microcase。下一个问题：怎样观察 valid future trigger、expiry 与 withdrawal，而不把 PM-Bench 的 task-handle 架构默默搬进来。
- **companion continuity（D-005）** 仍为 candidate，缺 source／event evidence。去向：让 System Census、migration 事件类研究与 case 设计相互补充。下一个问题：实例或模型变化后，哪些可观察区别属于 continuity，哪些只是当前 prompt 已提供的信息。
- **learning transfer** 属 incubator 的 C 方向，保持开放。第 9 节只描述**条件性判据**（若将来实施需要满足什么），不声称本周期已排定或完成此类测试。
- **evaluator calibration**：RC-001 E0 pack 未 dry-review，中文 semantic-equivalent matcher 尚未成 fixtures；RC-003 的 Twin B rationale 最小区间与 RC-001 的 warmth／overrepair 阈值仍待 human review，不能由精确短语检查代替。

## 5. 事件族容量与独立性

**12–20 个独立 incident families 是容量目标**，不是科学 sample-size gate，也不是强制作者配额。

- 按**不同机制或竞争解释**分配名额，而不是按主题 rename/paraphrase 凑数；改名、同义改写与同一 family 的额外 checkpoint 都不增加独立性。
- 已知 cases 是 development 材料。要新增独立验证材料，须先锁定一条具体设计主张，再构造未参与开发的变体；若新变体又被用于调参，应重新分类为开发材料。
- **fixed-history replay** 与 **co-evolving interaction** 是两类不同研究：前者给冻结前缀、可重复；后者观察持续互动中状态如何变化，成本与可变性都更高。两者分开设计、分开报告，不互相冒充。
- 每个 family 交付：bounded question、current probe、probe evidence contract、必要 controls、归因限制与合成来源说明。历史区分用 counterfactual twins，routing 用 scope-conditioned pairs，邻域保留可用 invariance checks；不把它们合并成同一种因果证据。

## 6. 候选受测对象与 readiness matrix

候选与基线都**不等于**已安装或可运行。以下对象需先确认 exact commit、clean checkout 与原生边界，才谈执行。原生 seam 与固定版本以各 source study 为准：[Mem0](../systems/source-studies/mem0.md)、[Letta local backend](../systems/source-studies/letta.md)、[Graphiti](../systems/source-studies/graphiti.md)、[Hindsight](../systems/source-studies/hindsight.md)。

| 对象（固定版本） | 原生承担什么 / seam | 本周期问题 | 运行前必须确立 |
|---|---|---|---|
| Mem0 Python OSS `a39a802` | 应用侧 memory 层：add 抽取事实、search 返回文本/score、update/delete 与 history；不生成最终回答，scope 由 caller 显式给出 | Q1/Q3：抽取后 authority 与 scope 是否保留；检索候选与最终使用分离 | 只测 OSS library，不借用 managed platform 分数；明确 scope 参数、query 构造与 reader；确认 embedding/provider 边界 |
| Letta Code local backend `f5c5bbc` | local backend：transcript（messages.jsonl）＋ Git-backed MemFS ＋ 编译后 context；**本地为 FTS-lite，无向量索引** | Q1/Q2：文件修订与编译时序如何影响后续调用 | 只用 local backend，**不是** generic Letta server／Cloud；固定 agent/MemFS/backend/model；把 Git 可追溯与事实归属分开 |
| Graphiti `16cdf70` | episode→实体→带 `valid_at/invalid_at` 的事实边；`group_id` 分区；**caller 选择时间过滤与 context 投影** | Q1/Q2：双时间与来源链是否进入实际使用；更正是否收敛 | 明确 caller 的时间过滤与投影策略；记录 LLM 语义裁决；确认 `remove_episode` 不重算摘要的边界 |
| Hindsight `9c7f6c6` | documents/chunks、world/experience facts、带 `source_memory_ids` 的 observations、mental models；retain/recall/reflect/consolidation | Q2：派生 observation 与 mental model 在源更正后如何失效 | **声明本地 synthetic 研究实际使用的 bank／scope 隔离**（无需为本地研究实现自定义 tenant 认证）；tags 不是 ACL；把异步新鲜度记为可观察状态 |
| raw-history / file 基线（**比较对象／配置**） | 分列 full-history、字面／关键词搜索、带向量语义检索的 raw-source A；保持各配置身份 | 全问题：判断更复杂机制是否值得其成本 | 保留身份、encoder／selection 与成本；从**相同 raw 输入**开始，不削弱基线的可用证据；记录实际 exposure 与 reader |

两条比较必须分开，不合并成一张序表：

- **complete-system native configuration**（按各系统 supported boundary 运行）；
- **fixed-reader memory-support comparison**（固定同一 reader 与 config，只换 memory 支撑）。

adapter 补上的 semantics／state／routing 会改变 attribution：为系统补出的能力不能记作该系统的原生能力，hidden 或 opaque 的 stage 记 `unknown`，不是自动 failure。本周期不建立 universal runtime interface／schema，也不做跨系统 ranking。

## 7. 控制与比较纪律

- **current-only 与 ingest-then-disable 不同。** 前者只给当前 turn；后者按原生路径摄入历史后再原生关闭使用，且只在系统支持时成立。不支持原生消融的记 `not applicable`，不造同名替身。
- 保留强对照：full-history、可搜索的 raw source、author 选择的 reference excerpt。**reference excerpt 是诊断性输入，不是检索上界，也不是真值来源**；它只说明给定 reader 在该材料下能否完成。
- 每个系统用**有效的原生条件**。budget-matched 比较与 native capabilities 比较分开报告；材料量不同就报告 exposure 差异，不靠统一截断让强基线失去关键证据。
- A/B 对照使用**相同 raw 输入**；不把作者整理好的正确状态喂给其中一边。
- **防止泄漏**：evaluator key、future events、probe 输出与 expected labels 不进入后续 fixed history；probe 的提问、回答与评审不写回更晚的 checkpoint。
- 原生 ablation 只在系统支持处使用；任何由 adapter 提前完成的 routing／筛选都记 attribution risk。

## 8. 系统样本空间（museum）

museum／样本间／研究室的正式名称仍开放。本周期**建立在现有十份 source studies 与 30 幅 atlas 视图之上**，不重建 topology、不新增平行副本。

- `systems/architecture-atlas/models/*.json` 继续拥有 source-grounded 节点、关系、边界、state 与 pinned evidence；[`build.cjs`](../systems/architecture-atlas/build.cjs) 与 render 脚本拥有呈现生成。编辑 model 或 viewer 源后须以 `node systems/architecture-atlas/build.cjs` 重新生成并肉眼检查。
- 读者端实现：复用已有搜索、三视图切换、节点证据、缩放与导出；新增从研究问题到 source study／展品的入口、运行记录与条件切换、证据阶段的逐项阅读，以及版本与判断修订的回看。源码图的关系仍从既有模型生成，运行记录引用对应对象，不另画一份 competing topology。静态分支可先推进，公开上线另需 hosting 授权。
- **静态 exhibit 与运行 exhibit 的依赖与 done criteria 不同**：静态 exhibit 只有 pinned source 与 render 依赖；运行 exhibit 需要**已执行的记录**（来自执行包与 incubator 证据），而不是仅有 readiness 清单。两者分开标注、分开验收。
- 为三个问题各设一个 **flagship target**（材料允许时）：可见输入、exact run/config、系统原生保存／派生／检索／context／output 证据、显式 missingness、cost、counterfactual／intervention 与 source links。
- exhibit 同时收**成功与失败**，保留 versioned judgement history；两者采用相同的证据要求。
- **reader journey**：从具体经历与当前任务出发 → 选择有明确状态的源码说明或运行记录 → 检查原生可观察路径 → 切换对照 → 查看判断与未知。**Done criteria**：读者能追到一项成功、失败或歧义的依据，分清 source observation 与 runtime observation，并打开支撑判断的 pinned source／run record；不可见阶段明确留白。实际检查桌面／窄屏阅读、条件切换、证据链接与版本回看，不以页面文件存在代替可用性。
- 静态 source exhibit 示例：Graphiti 的双时间字段与 `remove_episode` 不重算摘要、Letta 的 delete 不级联 transcript／summary、Hindsight 的派生 observation 失效路径、Mem0 的 ADD-only 与显式 update／delete 分离。这些在没有任何 native run 时就能成立，且各自带固定源码锚点。

## 9. Incubator：三方向与压力测试

incubator 用设计假设、替代方案、反例与获准的研究实验作取舍；实验所需 prototype 也须在执行范围内明确。Tilia 产品实现留在独立项目。保留的[早期实验](../experiments/local-memory-apparatus.md)提供的是局部工程证据，**不因此获得继续实现的 mandate**。

- **A：强语义 raw-source 基线（含向量）＋字面控制。** 向量语义检索是 Tilia 的**既定预期要求**：可以拒绝某个具体的 encoder／rerank／selection 策略或其组合，但不能由此否定向量语义检索本身，也不以字面搜索先失败为引入前提。
- **B：可修订证据／派生视图／context 编排。** 先证明相对 A 的必要性，再逐步加入加工。在**相同 raw 输入**上比较 B、强语义 raw-source A 与字面控制三者的抽取、检索与使用。结构使检索更有效本身可以是收益；需要排除的是额外 encoder、reranker、模型、上下文或预算带来的混杂，不能把结构影响的中间结果强行固定。
- **C：自主组织／学习**是**开放且独立的方向**，不作为第一装置的隐含前提；下表保留条件性判据，具体迁移实验尚未排定。

机制压力测试（`proposed`）：

1. **加工／抽取是否值得其损失与成本？** 相同 raw 输入下，自动抽取相对强语义 raw-source A 与字面控制带来什么、又丢了什么。
2. **最小充分更正传播**如何跨实际 read paths 生效？追溯 source、摘要、画像、embedding、context 各层，定位“抽取丢了／检索没到／检索到但被派生层覆盖”。
3. **编码器／重排／选择**对中文、英文与混合语言是否成立，含否定、provenance、conditions 与 stale drafts。

比较要求：三方从**相同 raw 输入**开始，任一侧都**不获得作者整理的 correct state 特权**。机制比较应让双方共同可用的 encoder、reranker、reader 与模型能力一致，或把差异单列为条件；不能给一侧更强组件后把全部收益归给结构。每次 **retain／simplify／reject** 都须命名被处置的具体假设、实现版本或配置，以及适用条件。检索候选、实际 context 与最终使用是需要观察的作用路径，不是必须固定相同的中介变量。

| 具体处置对象 | retain | simplify | reject |
|---|---|---|---|
| 具体 encoder／rerank／selection 组合 | 相对其他语义配置与字面控制，改善任务完成和来源使用，成本可接受 | 复杂组合的增益有限，更简单语义配置已足够 | 某个策略在相同 raw 输入下带来更多错误或不当使用且无对等收益；这只否定该策略，不否定向量语义检索的设计要求 |
| B 的某个修订／派生／编排机制及其“额外结构值得成本”假设 | 在共同组件与相同 raw 输入下，改善任务完成或实验内修复成本，作用路径有证据 | 消融某层后收益仍在，或 A 加较简单选择已满足该条件下需求，则移除该层 | 旧值持续生效／邻域受损先否定该版本在该条件下履约，定位 bug、修复或记录未修复；只有相关比较持续显示额外结构无相应收益且代价更高，才支持停止投入这个有界设计方案 |
| C 的具体学习／组织机制与迁移假设（尚未排定） | 迁移收益可观察、可回滚、可归因 | 所测收益可由更简单机制实现，则简化该实现 | 该实现不满足回滚／归因要求则停用；有界迁移假设需由对应比较否证，不由一处实现故障否定整个学习方向 |

压力测试允许得出“这个更复杂方案在这些条件下不值得其成本”的结论。单个 bug、配置失败或一次胜出都不是对整类架构的判决；更宽的路线取舍须有能区分实现缺陷、共同组件能力与结构贡献的比较证据。

## 10. 执行计划

角色用职责而非虚构人名。work packages 的目标是产生**实际周期产出**，而不只是计划片段或验收判据；它们可在平行 track 上推进。

| WP | 负责角色 | 依赖 | 周期产出 | acceptance evidence |
|---|---|---|---|---|
| A 案例与事件族 | case owner ＋ 独立评审 | 现有 seeds | 复核后的 Q1–Q3 family | 每个 family 有 bounded probe contract、controls 与 reviewer disposition |
| B 系统 readiness 与 native seam | system-study owner | 四份 source studies | 逐对象的 exact object／seam／pre-run 清单 | pinned commit、clean checkout、边界声明齐全 |
| C 对照与运行记录 | execution engineer | 获接受的 execution envelope；A 的相关 exposure；B 中相应对象已就绪 | 对照输出、受控 native runs 与 run records | run record 绑定 subject／adapter／config／condition／exposure，含错误与 rerun |
| D museum 读者端与 exhibits | system-study owner ＋ 编辑 | 静态分支只需 B；运行 exhibit 另需相关 C／E 证据 | atlas 读者端实现、静态 exhibit，随后运行 exhibit | reader journey 可走通、judgement history 有版本；运行 exhibit 附 executed record |
| E incubator 机制压力测试 | design owner ＋ execution engineer | 获接受的 execution envelope；相关 case exposure 与实验配置就绪 | A/B、加工、更正传播与选择机制的执行性观察和设计处置 | executed mechanism evidence 支撑 retain／simplify／reject，或具体说明证据不足；C 的迁移研究继续开放 |
| F synthesis | 编辑 ＋ 独立评审 | A–E 中**任何**已成熟批次 | comparative essay 的 claim-to-evidence trail | 每条 claim 有证据类型与范围；按批次独立成型 |

- **C 的前置**：一次获接受的 execution envelope（参见 proposed [ADR-0009](../decisions/ADR-0009-exploratory-research-boundary.md) 的 study envelope 概念）与相关 case exposure。**exploratory、未评审的输出不必等待全部 semantic review** 才能记录；但 accepted claim、case acceptance 与语义结论仍需相应评审。
- **E 的验收**需要已执行的机制证据与对应设计处置。若证据不能区分竞争解释，记录未决与下一项能区分它们的观察，不强迫产出架构胜负。
- **F 按批次并行**：synthesis 可为任一已成熟批次先产出 claim-to-evidence trail，不采用“A–E 全部完成才汇总”的 convoy。
- **D 分叉**：静态 exhibit 从现在起就基于现有 source work 推进；运行 exhibit 等到相关 C／E 证据到位。

**首个执行包候选：** [`RC-005 + Mem0 执行包`](../experiments/rc005-native-execution-packet.md) 是本周期的具体下一步。它把 18 份输入的隔离 reader 预检、强原文基线、固定 Mem0 OSS 的 native 摄入／检索、延迟观察和进程恢复纳入同一个 proposed envelope；配置、cell 数、费用估算与硬上限由该包维护，本文不复制一份配置真源。源码核验和离线输入验证不是 native 可运行证明，实际 readiness 的缺口在包内明确列出。

预检的退出条件是输入与记录路径检查完成，对具体 case 歧义与 reader 可用性已有处置；不要求高分或全部语义评审完毕才进入 native 阶段。发现实质歧义则处理受影响的 probe，保留原结果，不通过挑选高分来“修好”预检。Native 安装、无网 smoke、首次有界 provider 调用及必要接入修复拟包含在同一范围内，避免完成预检后再设计第二个执行包。

随后按完整周期继续接入其他异质系统，保留其 native 和 fixed-reader 边界，再扩展 Q1–Q3 中具有独立困难来源的 families。RC-005 只有一个 family，首包不能证明跨系统优劣、持续 co-evolution 或更广架构结论；新材料若反过来参与调参，重新计入 development。

## 11. 运行记录、证据包与成本

run record／evidence bundle 的要求（概念层面，不是 canonical API／schema）：绑定 exact subject 与 adapter identity、**effective config**（含 harness、tools／hooks、context policy 与相关依赖）、input view、condition、exposure／budget、reader regime、每次尝试与错误、rerun 原因、实际使用（检索候选／进入 context／最终 output 三层）以及 missingness 标记。需要断言的重复变异性要多次运行并保留全部分布，而不是只留最好一次。

**成本分两笔，分开记录，不能相加成一个数**：

- **货币支出**：模型／embedding 调用、后台维护、retrieval、repair，以及基础设施对应的直接费用；
- **人工时间**：作者、评审、修复与运营的工时。人工时间**不得**在货币行里重复计入。

**answer slot 的枚举**：按 family／world／checkpoint／config／control／repeat 的研究设计列出有意义的 cell，不做完整 Cartesian product，也不根据已经看到的答案挑选条件。**Ingest reset／reuse 策略会改变成本与状态**，须单独记账；twins 和独立重复不能共用可变 memory，冻结前缀的安全快照复用也要记录来源与恢复方式。

首包的枚举与数值估算见[执行包](../experiments/rc005-native-execution-packet.md)。其中 18 份 RC-005 view × 3 次重复 = 54 个**预检**回答位置，不是独立案例数，也不是包括 native 摄入／维护在内的全包调用数。缩减或扩展 cell 时重算工作量，并保留未执行条件。

估算货币费用时，先将每个可收费操作归入 ingestion／embedding、maintenance、retrieval、answer、repair／retry／judge 之一，再用计划次数乘以该操作的费用估计，最后加直接基础设施费用；同一次调用不重复计费。执行后用可用的实际 usage／billing 核对，无法取得的记 unknown。人工小时另表相加。先用获准首包测得单位成本与调用数，再估计全周期；扩展到新对象、长历史或后台维护时更新估计，不把首包单价外推成固定承诺。

**cap 记账**：stage cap 必须覆盖**失败尝试、重试与 judge 调用**；每次 dispatch 前预留保守额度，并采用 max-bounded 操作，避免超支。执行包给出具体 provider／model 与 stage／global cap 的推荐值；**推荐不是已批准预算**。达到约定 cap 或出现 invalid exposure／config 时停止支出，本地分析可以继续。

**观察时序与恢复边界**：每个更正实验记录 write 提交／回执的含义、原生 ready 信号或其缺失、即时与等待后 probe 的实际时间、最长观察期限和期间成本。不按“终于答对”决定何时停止等待。新 reader 请求、持久状态重开与进程重启分开举证；fixture 的 session 数字只表达虚构顺序。具体时点由各执行包固定，未知阶段保持 unknown。

**收益口径**：固定历史重放可报告任务完成情况、已有充分历史仍发生的不必要追问、以及实验内修复所需额外操作／调用／人工时间。它们只是未来使用收益的线索，不证明真实用户长期节省的解释时间或情感劳动。当前研究不因此引入真实参与者长期研究。

争议语义需要**独立人类评审**；model cross-review 不构成人类 calibration。精确检查（token 存在／缺失、twin 绑定）不需要人类仪式。**自动化 semantic judge 只有在被显式选择时才作为诊断**，永不成为已批准的 hard semantic scorer 或人类 calibration 的替代。

## 12. 发布与参与

- source study、架构研究、文章与常规文档更新按其自身证据与仓库现有授权发布；**不把每次 routine 提交都变成一次新的 publication 决定**。
- 需要独立授权的是：public hosting、正式 release、license 选择、public exploratory evidence 的发布，以及对外 outreach。
- comparative essay 保留 **claim-to-evidence trail**，thesis 不预定；Relata 与 AMS 的 broader inquiry 与长篇写作保持独立，本周期不把它们收窄到这三个问题。
- public-source participation 不需要维护者 endorsement；未来可邀请 light reproduction／counterexample／review（每次均在获授权后进行），本周期不进行外部 outreach。
- **raw private data 永不进入仓库**；贡献路径是 abstract Incident Seeds 与 consented synthetic derivation，不依赖私有数据。
- 进一步的外部提交与 leaderboard 属未来工作，在跨系统**可比性可被论证**之前推迟，并说明理由。

## 13. 处置与下一步决定

本计划建议采用三问题结构、容量目标、readiness matrix、两种比较边界、静态与运行 exhibit、incubator 三方向及分开的费用／人工时间口径。固定重放与共同演进分别研究，reference excerpt 限定为诊断对照。外部正式提交与 leaderboard 留待可比性和发布政策成立；D-006／D-005／learning transfer 沿第 4 节继续研究，本轮不声称覆盖。Museum 的读者端实现、公开阅读形态与真实运行展品均保留为整轮目标，按各自证据和授权分别交付。

处置中要显式保留的取向：

- **complete-system 与 fixed-reader 两条比较线保持分离**，不合成一张总表；
- 记录本轮可观察的**正面收益**（任务完成、不必要追问、实验内修复操作与成本）与**全生命周期成本**（ingestion／maintenance／retrieval／answer／repair），而不只记违规；
- **评审分歧要保留并记录**，不用 human calibration 的虚构来粉饰尚未发生的评审；
- **exploratory 与 formal claim 明确区分**，前者可先于语义评审，后者仍需相应证据；
- 三个问题各有**独立 flagship target**；
- **轻量外部贡献**（reproduction／counterexample／review）在获授权后进行，且不依赖私有数据；
- **leaderboard 雄心推迟**，直到跨系统可比性被论证。

进入实测前需要决定：是否接受 [ADR-0009](../decisions/ADR-0009-exploratory-research-boundary.md) 所提例外，以及确切执行包的 provider／model、账号使用与 stage／global cap。这些可以在一次完整范围决定中落实，不必逐次审批已纳入的条件。Public hosting、公开探索性结果包、正式 release、license 与 outreach 保留各自权限；常规公开源码文档维护沿用既有 repo 授权。
