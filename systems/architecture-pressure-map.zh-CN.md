[English](architecture-pressure-map.md) | **简体中文**
<!-- language: zh-CN; mirror: architecture-pressure-map.md; translation-status: synchronized -->

# Architecture Pressure Map

**Status：** 第一张 census pressure map；十份有界研究的公开源码综合；不是运行、能力或排名结果。
**Basis：** 固定 commit 的静态 source study，另有两段隔离的源码分支离线核对。这里的 `N` 指固定版本中 source-observed，绝不代表已核实的运行行为。
**配套 cards：** [`SC-001` Mem0](system-cards/SC-001-mem0.zh-CN.md) · [`SC-002` Graphiti](system-cards/SC-002-graphiti.zh-CN.md) · [`SC-003` Letta](system-cards/SC-003-letta.zh-CN.md)

本图记录十个架构在 [`EC-001`](../research/evidence-cards/EC-001-agent-memory-leaderboard.md) 与 [System Census 流程](README.zh-CN.md#census-workflow) 打开的 pressure 维度上的位置。行是拟议的 observation demand，不是普适能力清单，也不是评分 rubric。阅读时配合 [System Card 模板](system-card-template.zh-CN.md) 图例与[十份 source study](source-studies/README.md)。

图例：`N` system-native 且固定版本 source-observed · `E` 原生边界之外的 adapter-emulated · `O` 该边界 opaque · `U` 该版本 unsupported · `?` unknown 或未检查 · `—` not applicable。

**Fidelity review：** 2026-10-23，仅对照既有 source studies 与 atlas models；未重新完整阅读 upstream 或执行系统。此前的 review 来源未建立。

## 代表系统与证据绑定

| 键 | 系统 | Source study | 固定版本 | 证据级别 | Reviewed card |
|---|---|---|---|---|---|
| MEM | Mem0 Python OSS | [mem0.md](source-studies/mem0.md) | `a39a802` | 静态源码 | [SC-001](system-cards/SC-001-mem0.zh-CN.md) |
| LET | Letta local backend | [letta.md](source-studies/letta.md) | `f5c5bbc` | 静态源码 | [SC-003](system-cards/SC-003-letta.zh-CN.md) |
| GRA | Graphiti | [graphiti.md](source-studies/graphiti.md) | `16cdf70` | 静态源码 + 离线分支核对 | [SC-002](system-cards/SC-002-graphiti.zh-CN.md) |
| LMC | lmc-5 upstream | [lmc-5.md](source-studies/lmc-5.md) | `fb3e72c` | 静态源码 + 离线分支核对 | 无 |
| TID | Tideline Memory | [tideline-memory.md](source-studies/tideline-memory.md) | `76490fe` | 静态源码 | 无 |
| AEL | Aelios | [aelios.md](source-studies/aelios.md) | `9e65c80` | 静态源码 | 无 |
| HIN | Hindsight | [hindsight.md](source-studies/hindsight.md) | `9c7f6c6` | 静态源码 | 无 |
| OVI | OpenViking | [openviking.md](source-studies/openviking.md) | `bbf2e37` | 静态源码 | 无 |
| LAN | LangMem | [langmem.md](source-studies/langmem.md) | `9d033b4` | 静态源码 | 无 |
| AMEM | A-MEM 论文实现 | [a-mem.md](source-studies/a-mem.md) | `0c8039f` | 静态源码 | 无 |

三张 reviewed cards 是深化；矩阵仍覆盖全部十份 study，以免比较仅限 carded systems。每个 cell 都是关于固定版本的静态源码观察，不是实测结果。

## Pressure 矩阵

| 拟议观察或要求 | MEM | LET | GRA | LMC | TID | AEL | HIN | OVI | LAN | AMEM |
|---|---|---|---|---|---|---|---|---|---|---|
| 接收有序历史或事件流 | N | N | N | N | N | N | N | N | N | N |
| 暴露独立的 write 或 ingest 操作 | N | N | N | N | N | N | N | N | N | N |
| 暴露各入口的完成信号 | O | N | N | O | O | O | O | O | O | O |
| 返回 retrieval 或 activation 候选 | N | N | N | N | N | N | N | N | N | N |
| 返回 rendered model context | E | N | E | N | N | N | E | N | E | N |
| 生成最终回答或行动 | U | N | E | E | E | E | N | U | E | N |
| 保留来源或 provenance 引用 | O | N | N | O | O | N | N | N | O | U |
| 暴露 current、historical 或 conditional state | O | N | N | N | N | N | N | N | O | O |
| 区分人的陈述与 companion inference | O | O | O | O | O | O | O | O | U | U |
| 通过可见路径支持 correction 或 revocation | N | N | N | N | O | N | N | N | N | U |
| 支持未来意向的触发或唤醒行为 | U | ? | U | O | O | O | O | O | O | U |
| 暴露 inspection 或 explanation | N | N | N | N | N | N | N | N | N | N |
| 支持 model、instance 或 surface 迁移 | ? | N | ? | O | ? | O | ? | N | ? | ? |
| 暴露技术分区或 scope key | N | N | N | O | U | N | N | N | N | U |
| 建立超出调用方 scope 映射的项目隔离保证 | O | O | O | O | U | O | O | O | O | U |
| 保留 artifact 与 source authority | O | O | O | O | O | O | O | O | U | U |
| 暴露修订、版本或替代状态机制 | O | N | N | N | N | N | N | N | U | U |
| 按 role 或 surface routing | O | O | O | O | O | N | O | N | O | U |
| 暴露保留来源或历史材料的回查入口 | O | N | N | N | N | N | N | N | O | O |
| 避免跨域 context contamination | O | O | O | O | O | O | O | O | O | U |
| 无需 provider 调用即可静态检查源码 | N | N | N | N | N | N | N | N | N | N |
| 能绑定精确、可观察的版本或配置 | N | N | N | N | N | N | N | N | N | N |

## 必读解释

对每个 `E`、`O`、`U`、`?` cell，说明其证据与后果。未列出的 cell 为 `N`，即固定源码中可见该机制。`O` 与 `U` 是不同发现，都不表示“较差”。这里的 boundary 分别观察系统、应用侧 adapter、opaque composite 或范围外能力，每个 cell 指明是哪一种。

**第 3 行，各入口的完成信号。** LET 的文件/Git commit 与 GRA 的 awaited write 在所检查入口记 `N`，不证明之后的语义使用。MEM（返回 ADD/history 不证明逐条持久或可检索）、LMC（current-state/vector 可能滞后 supersede）、TID（amendment commit 先于 best-effort 派生更新）、AEL（人类输入 await，但 assistant 输出稍后记录）、HIN（异步 operation ID 仅表示提交）、OVI（snapshot completed 可掩盖 reindex 错误）、AMEM（metadata/index 更新分离）记 `O`。LAN 记 `O`：hot tool 与异步 store manager 等待各自 Store 操作，但本地 reflection queue 非耐久、远端 future 是提交确认，同步 mutation 的完成还存在未验证源码疑点。依据为各 source study 的写入/修订段与 LangMem“延迟与回执”；不推导全系统耐久就绪保证。

**第 5 行，rendered model context。** 由系统自身产出面向模型的 context 记 `N`：LET 编译 system prompt；LMC SessionStart 恢复启动上下文；TID 注入 identity/分层上下文；AEL 把临时 patch 追加到当前 user turn；OVI 返回 `AssembleResult`；AMEM 的 harness 构造 prompt。组装落在调用方或示例代码的记 `E`：MEM 无 `chat`；GRA 示例拼接 `edge.fact`；HIN 的 LiteLLM callback 只是一个可选 integration；LAN 的 prompt callback 是 guide 示例。

**第 6 行，最终回答或行动。** 边界包含生成的记 `N`：LET 运行 agent；HIN 的 `reflect` 合成回答；AMEM 的 harness 作答。生成在 memory 层之外的记 `E`：GRA/TID/AEL/LAN 使用外部应用或模型；LMC 注入 context 但主 agent 生成。无生成路径的记 `U`：MEM 无 `chat`；OVI 返回 context，最终使用未知。

**第 7 行，provenance。** `N`：LET 保留 message ID/role/时间戳与 Git commit；GRA 保留 episode UUID 与双时间边；AEL 保留 source messages 与 `authored_by`；HIN 保留 `source_memory_ids` 与 document ID；OVI 保留 version/source/freshness metadata。`O`（来源存在但弱或由模型产生）：MEM 的 `attributed_to` 是 LLM 输出；LMC 的 curated `source` 是路径/trace 且未强制 speaker/subject；TID 的 `source_links` 可选且未核验；LAN 无版本账。`U`：AMEM 不填结构化 provenance。

**第 8 行，current/historical/conditional state。** `N`（暴露 supersession 或版本状态）：LET Git history；GRA `valid_at`/`invalid_at`；LMC current/review/superseded；TID amendments 与 effective text；AEL versions 与 `includeHistory`；HIN invalidation archive 与 model history；OVI version 与 archive/live。`O`：MEM 有 `created_at` 与 history 但无 current-vs-historical 查询语义；LAN 只暴露当前 key，其 versioned history docstring 不被写路径支持；AMEM 改写 context 且无修订历史。

**第 9 行，人的陈述与 companion inference。** 没有 carded system 干净区分两者，这正是 D-002 命名的压力。部分线索但无 authority model 的记 `O`：MEM（role 抽取 + LLM `attributed_to`）、LET（role 与 Git author，但无事实级来源）、GRA（episode 来源，调用方仍有把 agent 回写误认成人类认可的风险）、LMC（“user said/assistant replied” 原子，但 curated schema 未强制 speaker）、TID（USER/ASSISTANT 标记与 `entities_role`）、AEL（`authored_by` 加 judge，但非认证）、HIN（调用者提供来源语境，bank 显示名不是 narrator）、OVI（按规则 self/peer 分离，非同意）。`U`：LAN 由模型决定权威；AMEM 只有 speaker 字符串。该行是对观察边界的事实，不是缺陷标签。

**第 10 行，correction 或 revocation 路径。** 有可见路径的记 `N`（附已记录 caveat）：MEM update/delete；LET `memory delete`；GRA `remove_episode`；LMC supersede 与 patrol；AEL upsert/supersede/archive/delete；HIN invalidate/edit/delete；OVI content write 与 rm；LAN update/delete 工具。`O`：TID 有可见纠错路径，但所列 MCP tools 无 delete/forget。`U`：AMEM 无 correction 或 delete API。

**第 11 行，未来意向触发或唤醒。** `O` 表示相邻的维护或上下文供给机制，不表示已建立意向执行合同：TID 注入开放 threads 并做 DREAM 维护；LAN 调度 reflector，远端可用 `after_seconds`；LMC 有 cron/sweep；AEL 有 Dream 与联想 trigger 向量；HIN 刷新 mental model；OVI 调度资源刷新/session commit。各 source study 未建立贯穿这些路径的有效意向触发与撤回/过期处理保证。`U`：MEM 是可见性过期，GRA 是有效时间字段，AMEM 在所代表边界无 wake 路径。`?`：LET scheduler 未检查。未来计划文本仍可能被存储，存储与唤醒执行不同。

**第 13 行，迁移。** `N`：LET 文件与 Git 可迁移，Cloud 跨机器同步；OVI 有 snapshot/restore reindex 路径。已有 reference pattern 或 provider 绑定但执行未证的记 `O`：LMC Forge/Swap 是部署 reference；AEL 绑定 Cloudflare 与 provider 路由。未调查迁移的记 `?`：MEM、GRA、TID、HIN、LAN、AMEM。

**第 14 行（技术分区 key）与第 15 行（项目隔离）。** 第 14 行 `N` 仅指源码可见的 key：MEM scope ID、LET agent/conversation、GRA group_id、AEL 读写 namespace、HIN bank/带 scope 的 SQL、OVI account/user/peer、LAN namespace template（见各 source study 的 scope 段）。LMC 记 `O`：thread 标签不约束 fact_key 或跨 session 搜索。TID 与 AMEM 在所代表边界无原生多 scope key，记 `U`。第 15 行对有技术 scope 或依赖调用方/部署映射的八项记 `O`：key 不建立独立的项目授权隔离保证；TID、AMEM 仍为 `U`。HIN 的 tags/untagged 可见性需明确处理。AEL 的 legacy 无主向量兜底涉及存活状态/来源背书，不是跨 namespace 泄漏的证据。

**第 16 行，artifact 与 source authority。** 几乎所有系统保留引用而无 authority model，故多记 `O`：MEM 的 LLM `attributed_to`；LET 有 Git author 但无事实归属；GRA 来源连接但无真实性担保；LMC 的 evidence 存在性 gate 不核验引用存在；TID 可选 `source_links`；AEL 的 `authored_by` 无认证；HIN 的 source ID 与 best-effort grounding；OVI 的 version/source metadata。`U`：LAN 与 AMEM。这是最尖锐的共性缺口，也是 D-002 与 “artifact and source authority” incident family 仍开放的原因。

**第 17 行，修订/版本/替代机制。** `N`：LET、GRA、LMC、TID、AEL、HIN、OVI 暴露源码可见的版本、amendment 或失效机制（来源同第 8 行），不建立已接受决定的权威或正确语义替代。`O`：MEM 的显式 update/history 未持久化 prompt 所说修订 lineage。`U`：LAN 所代表写路径只替换当前 key；AMEM 改写 context 而无修订历史。

**第 18 行，role/surface routing。** `N` 只描述 AEL gateway identity/read namespaces 与 OVI URI/actor-peer scope 的技术路由（见各 source study 生命周期段），不等于 audience 同意。MEM、LET、GRA、LMC、TID、HIN、LAN 依赖调用方映射或缺少已检查的 role/surface 路径，记 `O`。LAN 的 hot/background 分离改变更新时机，不是 role/surface routing。AMEM 在所代表边界记 `U`。

**第 19 行，保留来源或历史材料回查。** `N` 记录回查入口，不表示完整原史覆盖：LET transcript search；GRA episode lookup（原文保留可选）；LMC raw search；TID MCP 搜索经重写/截断的 narrative、context 与 amendment；AEL 原文窗口（默认原消息保留七天）；HIN documents/chunks；OVI archive messages.jsonl（见各 source study 保留/检索段）。`O`：MEM history/近期缓冲无 full-search 合同；LAN 分开 checkpointer 与 Store；AMEM corpus index 可滞后。强 full-history/full-search 对照还需独立建立允许来源的完整性、保留与实际 exposure，此处不认证这种对照。

**第 20 行，跨域 contamination。** 依赖调用方提供 scope 的九项记 `O`：MEM、LET、GRA、LMC、TID、AEL、HIN、OVI、LAN（HIN 另有 untagged 默认可见）。`U`：AMEM 无多域隔离。没有代表系统在自身词汇中原生路由个人、关系与项目材料，因此该行是共性压力而非差异点。

**第 21 行，无 provider 调用的静态检查。** 十项均为 `N`，由固定版本 source study 证明可静态检查。无模型执行是另一个问题：仅 LMC、GRA 有已记录的隔离离线分支核对，使用合成输入与文档注明的替身，见 source-studies/README.md。十系统完整 native 的无 provider 运行未建立；没有运行记录或依赖数据库不能证明不可能。第 22 行绑定精确源码 commit，不绑定已安装或 live 配置。

## Protocol-bias record

本矩阵自身就是一种会偏爱或抹掉架构的 protocol。Relata 必须显式携带的偏置：

- 要求 “retrieval 或 activation 候选” 会偏爱 vector/graph 服务，而不利于 file-first 或 Git-first 系统，后者的对应事件是文件读取或 diff，而非排序候选列表。
- 要求 “rendered model context” 会偏爱 harness-gateway（LET、AEL），不利于 library（LAN）与 service（MEM），并会迫使 adapter 重建 Relata 声称要观察的组装。
- 要求边界内 “最终回答或行动” 会偏爱完整 agent，排除有效的 memory layer。
- 把返回材料对象当作证据，可能测到的是 adapter 而非系统；MEM、GRA、HIN 与 LAN 的组装属于调用方或示例代码。
- 强制跨域路由或强制多项目 key 会排除合理的单 scope 设计（TID、AMEM）与把 scope 交给 harness 的 file/Git 设计（LET）。
- full-history 或 full-search 对照要求保留原始历史，会惩罚只存派生状态的系统；它应作为标注清楚的 control 运行，而非原生能力测试。
- 静态源码观察不能建立运行行为。本图每个 `N` 都指 “固定源码中存在”，绝不是 “已观察其工作”，两段离线核对是隔离的源码分支核对，不是端到端结果。

对 Relata 的后果：逐行逐系统标明该 boundary 观察的是系统、adapter、opaque composite 还是空，并保持 excluded 或 adapter-distorted systems 可见。不要把这些后果折叠成单一分数，也不要由外部行为推断未观察的内部架构。

## 限制

十份 study 都是未经独立人类 review 的 source-study draft；分类是对固定源码的编辑判断，两段离线核对只覆盖特定源码分支。本图不建立性能、能力、安全、保留或关系质量结论，也不选定 benchmark interface 或偏好架构。
