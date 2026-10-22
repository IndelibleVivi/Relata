**简体中文** | [English](distinction-atlas.md)
<!-- language: zh-CN; mirror: distinction-atlas.md; translation-status: synchronized -->

# Relata Distinction Atlas

**Status：** seed hypotheses，不是 canonical taxonomy。2026-10-23 记录 source corroboration；没有任何 distinction 提升为 *supported*。

## Coverage strata

- `personal-lived`
- `shared-relational`
- `operational-project`
- `companion-system`
- `mixed-domain`

Coverage strata 描述 case 触及 memory ecology 的哪些部分。它们不是永久 evaluation tracks，也不会把每个 incident 自动变成新 distinction。

## Candidate incident families

- ordinary-event continuity，不强造 significance；
- project state、milestone 与 handoff continuity；
- decision rationale 与 supersession；
- artifact 与 source-authority fidelity；
- cross-project isolation；
- role 与 surface routing；
- shared-work repair；
- personal-to-project natural association；
- companion identity 跨 operational / private surfaces 的 continuity。

在 source、community、system 与 case evidence 足以支持 bounded `D-xxx` entry 前，它们都只是 incident families。

第一批 instantiated、仍未经 review 的 objects 是 [`RC-002-zh-CN` ordinary-life seed](cases/seed-002-ordinary-life-location-continuity.zh-CN.md) 与 [`RC-003-zh-CN` project-authority seed](cases/seed-003-project-authority-handoff.zh-CN.md)。它们的存在不会 promote candidate family，也不建立 supported distinction。

## Source corroboration（2026-10-23）

下面的 seed hypothesis 已对照十份固定 commit 的[源码研究](../systems/source-studies/README.md)、Mem0／Graphiti／Letta 三张已 review 的公开源码 [System Cards](../systems/system-cards/SC-001-mem0.md)，以及十系统 [Architecture Pressure Map](../systems/architecture-pressure-map.md) 阅读。本轮 2026-10-23 fidelity review 对照既有 source studies 与 atlas，未重新完整阅读 upstream 或执行系统，也不追认此前 review。引用保留其 source-observed 或条件推断状态，不建立运行、能力或关系质量结果。两次独立分支检查（[lmc-5](../systems/source-studies/lmc-5.md)、[Graphiti](../systems/source-studies/graphiti.md)）按原样标注，不当作端到端观察。

每个 seed 使用的标签：

- **multi-source** —— 至少两份独立 source study 直接涉及该 distinction 的机制；
- **partial** —— 只有一份 source 涉及，或两份只涉及相邻机制；
- **gap** —— 没有第二份独立来源，或该具体 failure 目前无法由 source evidence 回答。

Source corroboration 是输入，不是 promotion rule。它可以支撑第一条中 “strong source/system evidence” 的那一半，各研究提出的 probe 也涉及 counterfactual 与 observation-boundary 条款；但目前没有任何 seed 具备合资格的 community Incident Seed 或 accepted microcase，因此**没有 distinction 变为 *supported***，supported 计数仍为 0。缺第二来源、机制未定的，明确标为 gap，不用推断硬补。

| Seed | Corroboration | 直接涉及机制的独立来源 | 未决缺口 |
|---|---|---|---|
| D-001 | multi-source | Mem0、Graphiti、lmc-5、Tideline Memory、Hindsight、OpenViking、Aelios | 无 accepted microcase；warm／recognizable 一侧属评价性，无法由 source 检验 |
| D-002 | multi-source | Mem0、Graphiti、lmc-5、Letta、Tideline Memory、Aelios、Hindsight、OpenViking | 没有原生 accepted／disputed authority state；provenance 不等于 authentication |
| D-003 | multi-source | Aelios、OpenViking、Hindsight、Mem0、Graphiti、lmc-5、Tideline Memory、LangMem | 完整 audience 披露策略未建立；技术 scope 本身不足以证明权限 |
| D-004 | multi-source | Graphiti、Hindsight、A-MEM、lmc-5、Tideline Memory、Aelios、Mem0、Letta | 无 accepted microcase；permanent coldness 属行为主张，source 未观察 |
| D-005 | partial | Letta、OpenViking（仅 portability） | 无 migration incident；identity-loss 主张本身未验证 |
| D-006 | multi-source | Aelios、Tideline Memory、LangMem、lmc-5、Hindsight、OpenViking | 相邻调度机制获佐证；跨路径 expiry／withdrawal 闭包未建立 |
| D-007 | multi-source | Graphiti、Hindsight、lmc-5、Aelios、Mem0、Letta、Tideline Memory、OpenViking、LangMem | 无 accepted microcase |
| D-008 | multi-source | Mem0、OpenViking、Hindsight、Aelios、LangMem、lmc-5、A-MEM | 无 accepted microcase |

每个 seed 条目下面给出机制、反证与剩余缺口。

## D-001 — Current state without relational erasure

Later correction 改变了当前 valid behavior，但 relationship 仍应可识别且保有 warmth。

- 一侧 failure：使用 stale preference。
- 另一侧 failure：过度 correction，退回 distance 或 generic service language。
- Key test：不同 valid histories 下使用 identical current turn。
- Source corroboration：multi-source。[Mem0](../systems/source-studies/mem0.md) 保留变更历史，其 V3 ADD-only 路径不自动覆写；[Graphiti](../systems/source-studies/graphiti.md) 通过设置较早边的 `invalid_at` 消解矛盾，同时保留该边；[lmc-5](../systems/source-studies/lmc-5.md) 以同 `fact_key` 替代当前值，但保留 raw 与被替代记录；[Hindsight](../systems/source-studies/hindsight.md)、[Tideline Memory](../systems/source-studies/tideline-memory.md)、[OpenViking](../systems/source-studies/openviking.md) 与 [Aelios](../systems/source-studies/aelios.md) 都在保留历史之上提供当前／版本路径。以上均为固定版本的 source-observed。
- Counter-evidence／gap：[Graphiti](../systems/source-studies/graphiti.md) 的独立分支检查显示 exact duplicate 复用旧边并保留旧有效期，因此 key test 不保证成立。“保持 warmth” 一侧属评价性，任何 source 都未测试。无 accepted microcase。

## D-002 — Authority without narrative theft

System 保留一个 claim 是谁说的、推断的、接受的、争议的或纠正的。

- Failure：companion inference 变成 stable “user fact”。
- Failure：一方 interpretation 覆盖 unresolved disagreement。
- Key test：相同 content，不同 authority paths。
- Source corroboration：multi-source。每份固定研究都区分或未能区分 claim 与其 speaker／authority：[Mem0](../systems/source-studies/mem0.md) 与 [Graphiti](../systems/source-studies/graphiti.md) 附加由模型或 episode 推导的 attribution，并不等于 authentication；[Letta](../systems/source-studies/letta.md) 与 [lmc-5](../systems/source-studies/lmc-5.md) 保留消息 role，但没有逐 fact source；[Tideline Memory](../systems/source-studies/tideline-memory.md)、[Aelios](../systems/source-studies/aelios.md)、[Hindsight](../systems/source-studies/hindsight.md) 与 [OpenViking](../systems/source-studies/openviking.md) 保留来源线索却无 authority model。已 review 的 [SC-001](../systems/system-cards/SC-001-mem0.md)、[SC-002](../systems/system-cards/SC-002-graphiti.md)、[SC-003](../systems/system-cards/SC-003-letta.md) 记录同一共享缺口。以上均为固定版本的 source-observed。
- Counter-evidence／gap：[Graphiti](../systems/source-studies/graphiti.md) 指出调用方存在把 agent 自己的回写误认成人类认可的风险；没有任何 source 提供原生 “accepted／disputed” authority state。无 accepted microcase。

## D-003 — Relevance without resurfacing

Memory 可以 semantically relevant，却仍不适合进入 context 或 response。

- Failure：system 为证明 continuity 而展示 sensitive memory。
- Failure：private language 跨越 surface / audience boundary。
- Key test：同一 topic 下的 required 与 prohibited evidence。
- Source corroboration：multi-source。[Aelios](../systems/source-studies/aelios.md) 区分 write space 与 read namespaces，[OpenViking](../systems/source-studies/openviking.md) 区分 account/user/peer scope；[Hindsight](../systems/source-studies/hindsight.md) 提供 bank 与 tag，并含 untagged／shared 可见性；[Mem0](../systems/source-studies/mem0.md)、[Graphiti](../systems/source-studies/graphiti.md) 与 [LangMem](../systems/source-studies/langmem.md) 暴露调用期 scope key，但这些 key 本身不建立披露权限。[lmc-5](../systems/source-studies/lmc-5.md) 的 thread 标签不约束跨 session 搜索；[Tideline Memory](../systems/source-studies/tideline-memory.md) 没有 tenant/project/scope key，依赖 harness 映射或独立数据库。以上均为固定版本的 source-observed。
- Counter-evidence／gap：已检查机制区分 relevance、技术 scope 与 audience permission；这些有界研究未建立完整 audience 披露策略；Tideline 的单 DB 与 lmc-5 的跨 session 搜索把 scope 留给部署。无 accepted microcase。

## D-004 — Repair without overcorrection

Correction 应持续生效，但不能让 system 回避整个 relational domain。

- Failure：立即道歉，过一段时间又 relapse。
- Failure：corrected teasing rule 造成永久 coldness。
- Key test：immediate、delayed 与 neighboring-context probes。
- Source corroboration：multi-source。Correction 入口存在，但传播不齐：[Graphiti](../systems/source-studies/graphiti.md) 的 `remove_episode` 不重算存活摘要、也不恢复此前失效的边；[Hindsight](../systems/source-studies/hindsight.md) 使依赖的 observation 失效，但 mental model 以异步、best-effort 方式刷新；[A-MEM](../systems/source-studies/a-mem.md) 改写邻居 metadata，却要等到计数阈值才刷新派生索引；[Tideline Memory](../systems/source-studies/tideline-memory.md) 把 amendment 与自动召回所读的向量分开存储；[lmc-5](../systems/source-studies/lmc-5.md)、[Aelios](../systems/source-studies/aelios.md)、[Mem0](../systems/source-studies/mem0.md)、[Letta](../systems/source-studies/letta.md) 都让部分派生或缓冲状态留在 correction 之外。以上均为固定版本的 source-observed。
- Counter-evidence／gap：这些是传播延迟机制，不是 “立即道歉后延迟 relapse” 或 “永久 coldness” 的行为失败，后者没有哪份 source 观察。无 accepted microcase。

## D-005 — Identity continuity across migration

Facts 与 style 可以保留，但 companion identity 或 shared trajectory 仍可能变得不可识别。

- 仍是 candidate；新写的 [RC-006 seed](cases/seed-006-companion-migration-continuity.zh-CN.md) 只探索共享历史与能力声明变化的有界问题，不补出真实 migration incident，也不证明 identity continuity。以证据为基础的 case design 及本 distinction 的 promotion 仍需要 system census 与 migration incidents。
- Source corroboration：partial。[Letta](../systems/source-studies/letta.md) 把 agent identity 绑定到 Git 管理、可迁移的 MemFS，并有明确的跨机同步状态；[OpenViking](../systems/source-studies/openviking.md) 有 snapshot restore reindex 路径，其 `completed` 回执不证明每一项索引都更新；[lmc-5](../systems/source-studies/lmc-5.md) 只有未验证的 Forge/Swap carryover reference。这些只涉及 portability，不涉及 identity 变得不可识别。
- Remaining gap：没有 migration incident，也没有任何 source 观察到 identity 或 shared-trajectory 的丢失，因此本 distinction 的具体 failure 仍未验证。

## D-006 — Prospective intention without false wake

System 应在 valid future trigger 出现时行动，并在 expiry、withdrawal 或 scope change 后保持沉默。

- Exact-source basis：[`EC-002`](../research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) 支持分开 state availability、observation、current task version 与 final action；它不建立 relational validity，也不自动 promote 本 distinction。
- 仍是 candidate；还需要 community-grounded incident、bounded relational counterfactual、architecture-neutral observation boundary 与 accepted microcase。
- Source corroboration：multi-source（仅机制）。[Aelios](../systems/source-studies/aelios.md) 建期并召回 trigger 向量；[LangMem](../systems/source-studies/langmem.md) 调度延迟 reflection 任务并取消较早的 pending 任务；[Tideline Memory](../systems/source-studies/tideline-memory.md)、[lmc-5](../systems/source-studies/lmc-5.md)、[Hindsight](../systems/source-studies/hindsight.md) 与 [OpenViking](../systems/source-studies/openviking.md) 含主动 surface 或定时维护路径。以上均为固定版本的 source-observed。
- Counter-evidence／gap：[Mem0](../systems/source-studies/mem0.md) 的 `expiration_date` 只是可见性过滤，[Aelios](../systems/source-studies/aelios.md) 的 incremental trigger 建期跳过已有 trigger，[lmc-5](../systems/source-studies/lmc-5.md) 的 current-state 行在 fact supersede 时不会失效，因此这些研究未建立贯穿全部派生与唤醒路径的 expiry／withdrawal 闭包。既有可见性过滤与 active 状态复核是局部保障，不能解释为没有过滤。无 community Incident Seed，也无 accepted microcase。

## D-007 — Retraction without residual influence

撤回或删除一条 memory，应同时从依赖状态（摘要、索引、trigger、已保留 context）中移除其影响；不应在其“被删除”后仍暗中左右系统行为。

- 一侧 failure：“已删除”的 fact 仍继续塑造摘要、检索或定时行动。
- 另一侧 failure：物理删除同时毁掉审计或修复此前决定所需的 provenance。
- Key test：撤回一条有支撑的 fact，然后在完整历史对照下探测各派生层与后续行为。
- Source corroboration：multi-source。[Mem0](../systems/source-studies/mem0.md) 的 delete 为 best-effort，保留最近消息缓冲，且可能跳过 entity 清理；[Graphiti](../systems/source-studies/graphiti.md) 的 `remove_episode` 保留共享来源数组，也不恢复已失效的边；[Letta](../systems/source-studies/letta.md) 不把删除级联到 transcript、摘要或复述；[lmc-5](../systems/source-studies/lmc-5.md) 没有统一遗忘请求，其 redaction 不是删除；[Tideline Memory](../systems/source-studies/tideline-memory.md) 不暴露 delete 工具；[Aelios](../systems/source-studies/aelios.md)、[Hindsight](../systems/source-studies/hindsight.md)、[OpenViking](../systems/source-studies/openviking.md) 各入口清理的层不同；[LangMem](../systems/source-studies/langmem.md) 只删当前 key。以上均为固定版本的 source-observed。
- Remaining gap：残留影响是静态源码可能性，不是已观测的运行失败，且各入口的撤回闭包不同。无 accepted microcase。

## D-008 — Acknowledgement without durable completion

写入、摄入或删除的 ack 回执，不应被当作“所有派生状态都已持久、完整、一致”的证明。

- 一侧 failure：相信 success 回执，却在某下游层失败时静默丢失 continuity。
- 另一侧 failure：因为某个回执看起来不完整，就丢弃仍可用的部分状态。
- Key test：注入一次有界故障，把返回的回执与独立观测到的逐层状态对照。
- Source corroboration：multi-source。[Mem0](../systems/source-studies/mem0.md) 返回的 ADD 事件不证明每条 fact 可检索，其 history 也不是跨存储提交证明；[OpenViking](../systems/source-studies/openviking.md) 的 snapshot `completed` 不证明每项索引都已重建；[Hindsight](../systems/source-studies/hindsight.md) 的异步 `operation_id` 只表示已提交、非已完成；[Aelios](../systems/source-studies/aelios.md) 在 assistant 写入可靠确认前就已返回；[LangMem](../systems/source-studies/langmem.md) 的 remote future 是提交，其 local queue 非耐久；[lmc-5](../systems/source-studies/lmc-5.md) 只检查 evidence 存在、不检查其有效；[A-MEM](../systems/source-studies/a-mem.md) 在捕获异常后仍保留部分演化写入。以上均为固定版本的 source-observed。
- Remaining gap：这是 observation boundary，不是实测 failure rate，且每一层都需要自己的 readiness 信号。无 accepted microcase。

## Promotion rule

一个 distinction 只有满足以下条件才变成 `supported`：

- 至少两份 independent community Incident Seeds，或一份 Incident Seed 加 strong source/system evidence；
- bounded counterfactual；
- plausible architecture-neutral observation boundary；
- 至少一张 accepted microcase。

上文的 source corroboration 是必要证据，但不自行满足任何一条：两份 source study 不能代替第一条要求的 community Incident Seed，且目前没有任何 distinction 拥有 accepted microcase。
