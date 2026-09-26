# Memory 设计的可检验维度图（proposed）

**Status:** proposed research map；不是 accepted ontology、评分表、评测协议或 system 结果。
**用途:** 连接现有研究与面向独立 Tilia 目标的[自有架构候选](own-memory-architecture.md)，允许竞争设计接受同样的检验；不由某个候选反向决定合格答案。更正后的 ADR-0007 不提供实现授权；保留的[本地工程记录](../experiments/local-memory-apparatus.md) 只记录非常早期实验中明确操作下的机制检查，不表示正式 Tilia、本文四组广义实验或现有 cases 已完成。Tilia 的向量语义检索要求仍待设计和实现。
**来源版本:** Relata `4bd0603` 的公开研究材料；本图最初仅转移固定版本研究，没有更新上游或运行 system under study。后续本地工程观察单独记录，不回填成来源研究的结果。
**主要来源:** [STATUS.md](../STATUS.md)、[CHARTER.md](../CHARTER.md)、[ASSUMPTION_REGISTER.md](../ASSUMPTION_REGISTER.md)、[agent-memory-inquiry](../research/agent-memory-inquiry.md)、[distinction-atlas](../case-lab/distinction-atlas.zh-CN.md)、`case-lab/cases/` 五篇、[RC-001 E0 pack](../case-lab/reviews/RC-001-e0-calibration-pack.zh-CN.md)、[claim-boundary](../research/claim-boundary-study.zh-CN.md)、[source-studies README](../systems/source-studies/README.md) 与十报告。
**标签:** 沿用 [research/README](README.md) 的证据分层；source-observed 在本文只描述固定源码所见，不表示 runtime-observed。本文所有**新维度、实验、自有设计推断均标 `proposed`**；未改动任何 source study、Case Card 或 Evidence Card 的接受级别。

## 中文摘要

本图把已有测试问题、五张 Case Cards 与十个 source studies 接成一组可检验的设计压力。它提出 10 个 `proposed` 维度，每个维度给出真实来源、当前案例覆盖、要求结果而非内部结构的架构责任、正例与反例/对照、需要保留的观测，以及设计反例与案例／归因限制。它不造总分、不建永久 ontology、不把研究假设写成已证能力；完全机械检查、需语义/人类评审、尚无案例三种状态分开标注。十个项目各提一条可采用/须改变/应拒绝的机制建议，附 repo 相对报告链接与固定源码 evidence。最后给出四个尚未执行的实验设计和比较纪律，为可反驳的架构设计提供依据。当前 RC-001 仍 `clinic-ready` 未运行，RC-002~005 仍为未评审种子，D-006 仍缺 community-grounded authority。

## English summary

This proposed map turns existing test questions, five Case Cards and ten pinned source studies into testable design pressure for a future from-scratch memory design. It names 10 `proposed` dimensions, each with real sources, current case coverage, an outcome-level architecture responsibility, positive/negative controls, observations to preserve and design counterexamples and case/attribution limits. No composite score, permanent ontology or formal precision is produced; mechanical checks, semantic/human review and case-free gaps are separated. Each of ten systems contributes one adopt/change/reject mechanism candidate with a pinned source link. Four unexecuted experiment designs keep current-only, full-history, full-search/simple-file, reference-context and native-path controls. RC-001 remains unrun; RC-002~005 remain unreviewed seeds; D-006 still needs community-grounded authority.

## 1. 使用方式与边界

- 本图是**设计压力清单**，不是 rubric，也不是「合格记忆系统」定义。维度可以合并、拆分或删除（`proposed`）。
- 每个维度只要求**可观察结果**（response / action / declared artifact），不要求离散 object、图、schema、write/search API 或任何内部阶段；opaque 系统可用 response lane 参与，缺 trace 记 `unknown` 而非 failure（[claim-boundary §7](../research/claim-boundary-study.zh-CN.md)）。
- source study、source-observed 机制与「已证运行效果」严格分开：源码存在不等于触发，触发不等于影响最终行为（[source-studies README](../systems/source-studies/README.md)）。
- 暂将设计压力整理为 10 项：「时间/修订」与「修复后保留」共享部分机制，后者还需观察未受影响的邻域。编号只是本研究的阅读索引，不是被接受的量表。

## 2. 建议进入 verify 的十项维度（各 `proposed`）

### X1 历史依赖性与保留收益 · proposed
- **来源:** [CHARTER 3.7](../CHARTER.md)（memory necessity）、[RC-001 §9 MN gate](../case-lab/cases/pilot-001-current-state-without-erasure.md)、[claim-boundary CL3](../research/claim-boundary-study.zh-CN.md)。
- **现有案例覆盖:** RC-001 已写 MN gate 与 C0/C1/C2/C3/C4；RC-002 §8、RC-003 §8、RC-005 §6 各写 current-only/full-history 计划。**全部未运行** → 无运行证据。
- **架构责任（要求结果）:** 在 current turn 相同的历史反事实对上，correct region 必须依赖 case-bounded 历史，只读 current turn 的路径不能同时满足两侧。
- **正例 / 反例·对照:** 正例 = history-bearing 两侧均正确；反例 = current-only 与 no-memory 对 twins 产生同一 policy（RC-001 §9；RC-003 §8）。
- **需保存观测:** 两侧输出、condition、input view、configured subject identity、evaluator 记录（CL1–CL3 required）。
- **设计反例:** 在允许使用历史的条件下，系统仍对两个需要不同回答的历史给出同一错误策略；这否定该条件下的连续性表现，但不自动定位到某个 memory 阶段。
- **案例 / 归因限制:** current-only 只命中一侧是无历史统一猜测的可能表现，并不否定 memory necessity。若可用当前信息同时可靠满足两侧，或 correct regions 实际重叠，才需检查历史必要性／信息泄漏；有限采样的不确定性另行报告。
- **检查类型:** 机械（twin/condition 绑定）+ 语义（correct region）。

### X2 跨 session 与重启持久性 · proposed
- **来源:** [RC-002](../case-lab/cases/seed-002-ordinary-life-location-continuity.zh-CN.md)（cross-session）、[RC-003](../case-lab/cases/seed-003-project-authority-handoff.zh-CN.md)（cross-session handoff）、[RC-005 §5](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md)（session 仅作者化顺序）、[offline-rehearsal](../experiments/offline-rehearsal.md)（scripted session 非重启）。
- **现有案例覆盖:** RC-002 view 明确「至少一个新 session 后」；RC-005 与离线 rehearsal 明确声明**无真实等待、重启、压缩或迁移**。无案例验证真正 durability。
- **架构责任（要求结果）:** 材料越过一个 session 边界（必要时进程重启）后仍可影响后续正确行为；「同一 context 内的连续」不算。
- **正例 / 反例·对照:** 正例 = 后续 session 独立提问仍正确；反例 = 仅同 session 注入即丢。机制对照见 [Letta messages.jsonl](../systems/source-studies/letta.md)、[OpenViking archive/live](../systems/source-studies/openviking.md)。
- **需保存观测:** session 边界、restart/reload 事件、写入时刻与复用时刻、可见 message 文本。
- **设计反例:** 在装置承诺的新 session 或实际重启边界后，已提交材料无法恢复或不再被使用。
- **案例 / 归因限制:** 同进程内存可以支持特定 session 边界，但不能证明进程重启或故障后的 durability；scripted session signal 不证明真实边界。
- **检查类型:** 机械（边界/时刻记录）；真实重启下的语义判断仍待授权。

### X3 当前状态、时间与修订（supersession / coexistence） · proposed
- **来源:** [RC-001](../case-lab/cases/pilot-001-current-state-without-erasure.md)（Twin B correction）、[RC-003](../case-lab/cases/seed-003-project-authority-handoff.zh-CN.md)（L-01/L-02）、[D-001/D-004](../case-lab/distinction-atlas.zh-CN.md)、[agent-memory-inquiry §理解更新周期](../research/agent-memory-inquiry.md)。
- **现有案例覆盖:** RC-001 Twin B 与 RC-003 Twin B 都把 superseding 作为 twin 变量；RC-005 更名叠加较晚旧稿。均未运行；RC-003 §16 仍待决定 rationale 的最小区间。
- **架构责任（要求结果）:** 在 current probe 相同时，later accepted 修订应改变当前 correct region；历史版本可保留供 audit，但不得作为当前依据。
- **正例 / 反例·对照:** 正例 = 依 current 状态回答且保留历史可查；反例 = stale 值当 current，或旧新被压平。机制对照见 [Graphiti valid_at/invalid_at](../systems/source-studies/graphiti.md)、[lmc-5 fact_key supersede](../systems/source-studies/lmc-5.md)。
- **需保存观测:** 修订事件、生效时刻、current/history 两侧输出、被选中的版本。
- **设计反例:** 已明确生效的修订后仍用失效版本指导当前工作，或把只适用于局部条件的修订扩大到其他有效情境。
- **案例 / 归因限制:** 若 twin 的正确区域无法区分当前／历史状态，应修改案例；这不证明架构失败，也不证明该维度没有价值。
- **检查类型:** 机械（twin 差异、精确 target）+ 语义（是否误用历史）。

### X4 来源、作者与接受状态（inference ≠ fact） · proposed
- **来源:** [D-002](../case-lab/distinction-atlas.zh-CN.md)、[RC-003 §6](../case-lab/cases/seed-003-project-authority-handoff.zh-CN.md)（decision acceptance）、[RC-005 §3](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md)（原名提出者）、[CHARTER 3.5](../CHARTER.md)。
- **现有案例覆盖:** RC-005 用替换 e2/e3 说话者做 provenance twin；RC-003 用 accepted/superseded decision。仅作者语义论证，无独立人类 reviewer、无 system 输出。
- **架构责任（要求结果）:** 相同 content 在不同 authority path 下应产生不同正确归属；companion inference 不得变成 stable user fact。
- **正例 / 反例·对照:** 正例 = 指出「最初由谁提出、由谁接受」；反例 = 泛说「我们一起做的」或把推断写成用户事实（RC-005 §3 must_not）。机制对照见 [Aelios authored_by/version](../systems/source-studies/aelios.md)、[Hindsight source_memory_ids](../systems/source-studies/hindsight.md)。
- **需保存观测:** speaker role、session、surface、proposal/acceptance 事件、输出里的归属措辞。
- **设计反例:** 在明确要求来历的任务中把提出者、接受者或推断者混为一谈，或让相似内容覆盖已有来源。
- **案例 / 归因限制:** 若任务不需要区分两种 authority path，就不能用该任务证明来源能力；需改进案例的观察问题。
- **检查类型:** 语义/人类评审为主（RC-005 明示未做 automatic semantic scorer）。

### X5 条件作用域与混合领域 routing / isolation · proposed
- **来源:** [RC-003](../case-lab/cases/seed-003-project-authority-handoff.zh-CN.md)（Lantern vs Atlas 隔离）、[RC-004](../case-lab/cases/seed-004-private-greeting-public-template.zh-CN.md)（scope-conditioned routing pair）、[D-003](../case-lab/distinction-atlas.zh-CN.md)、[CHARTER 3.15](../CHARTER.md)、[RQ11](../RESEARCH_QUESTIONS.md)。
- **现有案例覆盖:** RC-004 textual probe byte-identical、target metadata 有意不同 → **不是 pure historical twin**；RC-003 用 merged/scoped 控制计划。C0 metadata-only prior shortcut **尚未实测**。
- **架构责任（要求结果）:** 按当前 scope 和具体授权选择可用材料，允许获准的跨域组合；unrelated scope 不得覆盖当前 source-local fact。RC-004 的 private/public token 互斥是这个 case 的局部要求。
- **正例 / 反例·对照:** 正例 = private 用 private token、public 用通用 placeholder；反例 = 双向泄漏或拼接两 token（RC-004 §6）。机制对照见 [Graphiti group_id](../systems/source-studies/graphiti.md)、[Aelios namespaces](../systems/source-studies/aelios.md)、[OpenViking peer/scope](../systems/source-studies/openviking.md)。
- **需保存观测:** target metadata、selected scope、另一 scope 是否进入 rendered context、routing 是否由 adapter 提前完成。
- **设计反例:** public 场景泄露只获准 private 使用的材料，或项目 A 的修订覆盖项目 B 仍有效的事实。
- **案例 / 归因限制:** 若成功由 metadata-only prior 或 adapter 提前筛选解释，不能归功于被测内核的 routing；可描述 combined pipeline 的实际表现。
- **检查类型:** 机械（token 存在/缺失、twin identity）+ 语义（是否泄漏 owner-specific 语言）。

### X6 正确沉默（检索 ≠ 可用性 ≠ 回应适当性） · proposed
- **来源:** [CHARTER 3.6](../CHARTER.md)、[D-003](../case-lab/distinction-atlas.zh-CN.md)、[RC-001 §8 must_not](../case-lab/cases/pilot-001-current-state-without-erasure.md)、[RC-004 公开/私密边界](../case-lab/cases/seed-004-private-greeting-public-template.zh-CN.md)、[RQ5](../RESEARCH_QUESTIONS.md)。
- **现有案例覆盖:** RC-001 Twin B 禁表现 revoke 前后的精确短语；RC-004 禁 public 出现 private token。**禁止证据的机械面已设计，适当性判断仍全待评审**。
- **架构责任（要求结果）:** 需要区分 required evidence 与 prohibited use：被检索到或保留的材料不必进入 context/response。
- **正例 / 反例·对照:** 正例 = 敏感/跨 audience 材料保留在 audit 但不驱动输出；反例 = 为展示 continuity 而重 surface，或把 private language 移入 public（RC-001 §8、RC-004 §6）。机制对照见 [lmc-5 surface redact vs recall 默认不 redact](../systems/source-studies/lmc-5.md)、[Aelios diary 不当事实作答](../systems/source-studies/aelios.md)、[Hindsight strict tags](../systems/source-studies/hindsight.md)。
- **需保存观测:** 哪些 material 可 reach、是否进入 rendered context、final output 是否出现 prohibited content。
- **设计反例:** 在禁止使用或不适当的当前情境中，旧材料仍进入最终回应；另一方面，必要材料也不应因全局屏蔽而无法用于获准情境。
- **案例 / 归因限制:** 精确 string 检查只支持已冻结的字面边界；不能凭 blacklist 通过宣称未枚举的语义泄漏也被解决。
- **检查类型:** 机械（frozen token / prohibited evidence 缺席）+ 语义（未枚举的泄漏、必要展示 vs 过度展示）。

### X7 修复后保留与过度纠正 · proposed
- **来源:** [D-001/D-004](../case-lab/distinction-atlas.zh-CN.md)、[RC-001 Twin B](../case-lab/cases/pilot-001-current-state-without-erasure.md)、[agent-memory-inquiry §条件性修订](../research/agent-memory-inquiry.md)。
- **现有案例覆盖:** RC-001 两面失败都写出（重复 stale 短语 vs overrepair 成 cold/procedural）；RC-001 §12 明确 warmth 阈值留 human review。未运行。
- **架构责任（要求结果）:** correction 应持续生效，但不抹掉整个 domain；revoked 项不得回归，未 revoke 的支撑面应保留。
- **正例 / 反例·对照:** 正例 = 停用短语但保持熟悉 presence；反例 = 延时后 relapse，或 correction 扩成永久冷处理（RC-001 §13；E0 B-03/B-05）。
- **需保存观测:** immediate/delayed/neighboring-context 三次探测输出、后续 session 是否复发。
- **设计反例:** 纠正后旧影响在后续实际使用中复发，或局部修复抹掉未被撤回的熟悉互动／其他项目能力。
- **案例 / 归因限制:** single-shot 成功不足以主张持续性；需要真实后续边界与邻域对照，不能把 authored 时间标签当长期观察。
- **检查类型:** 机械（精确短语 count）+ 语义（warmth / overrepair 阈值）。

### X8 未完成意图与活跃线索（prospective / open thread / handoff） · proposed
- **来源:** [D-006](../case-lab/distinction-atlas.zh-CN.md)、[EC-002 §12](../research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md)、[RC-003 handoff](../case-lab/cases/seed-003-project-authority-handoff.zh-CN.md)、[RC-005 p3「接着完善」](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md)。
- **现有案例覆盖:** RC-003 测 cross-session handoff 的当前 authority；RC-005 p3 测 short「接着」是否唤起既有要求。**D-006 prospective 无 case**，仅 EC-002 提供 scorer-contract 限制。
- **架构责任（要求结果）:** 在 valid future trigger 出现时行动，并在 expiry/withdrawal/scope change 后保持沉默；state availability、observation、action eligibility 与 actual action 分开（EC-002 C-03/C-05）。
- **正例 / 反例·对照:** 正例 = trigger 命中时执行且过期后不执行；反例 = false wake（过期仍触发）或静默漏掉 valid trigger。机制参考 [lmc-5 open threads/current-state TTL](../systems/source-studies/lmc-5.md)、[Tideline open threads](../systems/source-studies/tideline-memory.md)。
- **需保存观测:** intention 的 availability 时刻、是否被 observe、是否 action-eligible、final action、expiry/withdraw 事件。
- **设计反例（尚无现成 case）:** 保留的有效意图在约定触发条件下被遗漏，或撤回／过期后仍促成行动。
- **案例 / 归因限制:** 当前请求已完整指定行动时，成功不证明保留意图起作用；action 权限、触发观察与 memory availability 必须分开。
- **检查类型:** **尚无案例**；D-006 promotion 仍需 community-grounded incident + bounded relational counterfactual + architecture-neutral observation boundary + accepted microcase（[distinction-atlas Promotion rule](../case-lab/distinction-atlas.zh-CN.md)）。不得用虚构案例冒充现成评测资产。

### X9 派生状态与跨层传播一致性 · proposed
- **来源:** [agent-memory-inquiry §理解有自己的更新周期](../research/agent-memory-inquiry.md)、[source-studies README 四问题](../systems/source-studies/README.md)、[D-004](../case-lab/distinction-atlas.zh-CN.md)。
- **现有案例覆盖:** 五个 case 都只评 final response/artifact；**无案例直接测 derived layer**。此维主要靠 source studies 的静态机制与提议探针支撑。
- **架构责任（要求结果）:** 派生材料（摘要、画像、observation、embedding、current-state 快照）在来源被修订/撤回后，不得继续以旧值影响当前行为；一次成功修改与「所有后续影响一致」是两个主张。
- **正例 / 反例·对照:** 正例 = 源改动后各可见层收敛到 current；反例 = 源已改但旧 embedding/摘要/画像仍 surface（[Tideline amendment 与 T1 不同步](../systems/source-studies/tideline-memory.md)、[A-MEM neighbor metadata vs embedding](../systems/source-studies/a-mem.md)、[Hindsight observation invalidation](../systems/source-studies/hindsight.md)、[Aelios 删除跨层不同步](../systems/source-studies/aelios.md)）。
- **需保存观测:** 每层的 current 值、写入/刷新时刻、哪些层可 reach、最终 response 用的是哪层。
- **设计反例:** 来源已明确修订或禁止使用，但旧派生物仍让新的 context／行为采用失效内容；晚到任务恢复被撤回的影响。旧 embedding 尚未刷新本身不必然等于语义失败，还需观察候选和实际使用。
- **案例 / 归因限制:** 不可见的派生层记 `unknown`。最终输出可支持输出层判断，不能单独证明每个派生层均已收敛，或定位某层失败。
- **检查类型:** 机械（层值/时刻）+ 语义（是否仍以旧值驱动行为）；当前**无对应 case**。

### X10 可检查性、可观测边界与归因 · proposed（横切）
- **来源:** [claim-boundary lanes L1–L4、adapter classes A0–A5、§7 unknown 是 evidence state](../research/claim-boundary-study.zh-CN.md)、[EC-001](../research/evidence-cards/EC-001-agent-memory-leaderboard.md)、[RQ7](../RESEARCH_QUESTIONS.md)。
- **现有案例覆盖:** 各 case 都要求 final artifact + 可用 intermediate；RC-004/RC-003 明确 adapter-created routing 需标 attribution risk。无 reviewed System Card / Architecture Pressure Map。
- **架构责任（要求结果）:** 每条结果须声明 subject（complete agent / memory-support / native diagnostic / combined pipeline）、input view、condition、evaluator contract 与 preserved evidence。
- **正例 / 反例·对照:** 正例 = 绑定的 scoped claim；反例 = 把 opaque stage 记成失败，或用 final success 反推 memory mechanism。
- **需保存观测:** exact subject/config/adapter identity、case revision、input view、observed vs opaque stages。
- **设计反例:** 对自有装置承诺可检查的路径，无法恢复一次提交、投影或实际消费所对应的版本／条件，因而无法诊断已经发生的错误。
- **案例 / 归因限制:** 无法拆开 adapter 与内核时，只描述观测到的整体表现；opaque 系统不因缺少内部 trace 自动失败。
- **检查类型:** 机械（artifact 绑定）+ 语义/人类评审（归属与不可见边界）。

## 3. RC-001 ~ RC-005 与 D-006 现在的支撑边界

| 资产 | 现状（来源） | 现在能支撑 | 现在不能支撑 |
|---|---|---|---|
| [RC-001 Pilot 001](../case-lab/cases/pilot-001-current-state-without-erasure.md) | `clinic-ready`，未 run / 未 accepted；[E0 pack](../case-lab/reviews/RC-001-e0-calibration-pack.zh-CN.md) 未 dry-review（§15） | 一个 bounded `shared-relational` current-state-use 区分；精确短语 hinge + bounded semantic 区；完整 twin/controls/attribution 设计 | 无 system run/reviewer 数据；不验证 warmth 阈值、不自动化 semantic-equivalence、不覆盖 full scope |
| [RC-002-zh-CN](../case-lab/cases/seed-002-ordinary-life-location-continuity.zh-CN.md) | seed，unreviewed；MN gate 项多为自评、独立 reviewer 待补（§8/§19） | 打开 ordinary-life coverage；cross-session 位置 twin 设计；significance discipline | 未证明 cross-session retention（session 为作者化顺序）；中文 semantic matcher 未成 fixtures |
| [RC-003-zh-CN](../case-lab/cases/seed-003-project-authority-handoff.zh-CN.md) | seed，unreviewed；无 external review（§19） | 打开 operational-project coverage；supersession twin + 邻近 scope 隔离 distractor | 无 run；handoff realism 未审；Twin B rationale 最小区间未定；merged/scoped fixtures 待补 |
| [RC-004-zh-CN](../case-lab/cases/seed-004-private-greeting-public-template.zh-CN.md) | seed，unreviewed；**scope-conditioned routing pair**，非 pure twin（§4/§8） | 打开 mixed-domain routing；public/private token 的 disjoint 断言；C0–C6 控制计划 | 非 history-only 因果；C0 prior shortcut 未实测；adapter-created routing 归因未决；frozen private-token set 仅 `{栖灯}` |
| [RC-005-zh-CN / CT-AUTHORSHIP](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md) | seed；**18 unanswered input views**；input audit 已实现；MN gate 未通过（§5/§6） | 打开 shared-work provenance + title supersession；exact authored inputs；literal speaker-removal collision 记录 | 无 system/human 证据；三 checkpoint 同属**一个 family**，非独立世界；无 adapter；不得把 scripted output 当结果 |
| [D-006](../case-lab/distinction-atlas.zh-CN.md) | candidate；仅 [EC-002](../research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) 支撑 state/observation/version/action 分离 | 一条 prospective 研究议程与失败类别（false wake、update、expiry） | **无 accepted microcase、无 community-grounded incident、无 architecture-neutral boundary**；不得虚构案例充当评测资产 |

## 4. 十项目各一条机制建议（`proposed` 采用/改变/拒绝）

这些是有条件的设计素材，不要求第一装置实现十项目的全部模块。每条建议须与实际用例和简单方案比较；「采用」仅表示值得验证其机制。

| 项目（报告 · 固定 evidence） | 机制建议 | 帮助条件 | 代价 / 须警惕 |
|---|---|---|---|
| [Mem0](../systems/source-studies/mem0.md) · [main.py#L1628](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/main.py#L1628-L1731) | **采用**显式 update/delete 与 change history 分离于自动抽取 | scope 由 caller 显式给出 | ADD-only 冲突累积；`attributed_to` 非来源认证；单条 delete 不撤来源（[storage.py#L257](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/storage.py#L257-L324)） |
| [Letta](../systems/source-studies/letta.md) · [memory.ts#L289](https://github.com/letta-ai/letta-code/blob/f5c5bbce6e9394b30c626909315c2b3acc665672/src/tools/impl/memory.ts#L289-L350) | **采用**可人工检查的 Git-backed memory 文件 + transcript/compiled context 分离；**改变**为不依赖 Git 提供事实级归属 | 人或 agent 愿意显式编辑并提交 | delete 不级联 transcript/summary/Git 历史；抽象与适用性依赖模型判断 |
| [Graphiti](../systems/source-studies/graphiti.md) · [edge_operations.py#L538](https://github.com/getzep/graphiti/blob/16cdf7045378c8d53ae01f94e2fa60d238cb0f68/graphiti_core/utils/maintenance/edge_operations.py#L538-L572) | **采用** bi-temporal（`valid_at/invalid_at` vs `created_at`）+ episode 来源链 | caller 显式选择时间过滤 | 默认 `search` 时间过滤为 None；矛盾判定依赖 LLM；`remove_episode` 不重算摘要/不恢复旧边（[graphiti.py#L1824](https://github.com/getzep/graphiti/blob/16cdf7045378c8d53ae01f94e2fa60d238cb0f68/graphiti_core/graphiti.py#L1824-L1852)） |
| [lmc-5](../systems/source-studies/lmc-5.md) · [store.py#L874](https://github.com/wuxuyun0606-collab/lmc-5/blob/fb3e72c9ee7357c8b17311097b0750082a8a1237/src/lmc5/store.py#L874-L887) | **采用** raw/curated 分层 + fact_key supersession + hit 带 trace；主动 surface gate 严于 recall | 稳定采集、review、fact_key 明确表达 scope 与对象身份、持续维护 | 离线观察显示跨 thread 同 key 替代、gate 只查「有 source」不查存在；vector 通道可能仍返回旧值（[vector_pgvector.py#L195](https://github.com/wuxuyun0606-collab/lmc-5/blob/fb3e72c9ee7357c8b17311097b0750082a8a1237/extras/pgvector_backend/vector_pgvector.py#L195-L245)） |
| [Tideline Memory](../systems/source-studies/tideline-memory.md) · [server.py#L1609](https://github.com/ennisaaaaaaaa-stack/tideline-memory/blob/76490fe2c422f1213e735e63c289fef5ae8044f6/server.py#L1609-L1684) | **采用** identity-first 注入 + open threads + append-only amendment 且可主动检索 | 部署纪律与维护脚本 | 主动搜索与自动唤起消费不同更新状态；截断（2000/500 字符）；单 DB 无 tenant scope；无删除传播 |
| [Aelios](../systems/source-studies/aelios.md) · [memories.ts#L385](https://github.com/wusaki0723/Aelios/blob/9e65c802ec1c13a68d22a68c5c9d7cdce385e041/src/db/v2/memories.ts#L385-L586) | **采用** fact_key/version/supersede 与版本指针 + 独立 precious/glossary；**改变**默认工程主体排除与删除跨层不彻底 | namespace 一写多读、显式 fact_key | 默认 Dream 排除工程主体（[dreamExtract.ts#L95](https://github.com/wusaki0723/Aelios/blob/9e65c802ec1c13a68d22a68c5c9d7cdce385e041/src/memory/dreamExtract.ts#L95-L161)）；自动 judge；删除不撤原消息/日记/快照 |
| [Hindsight](../systems/source-studies/hindsight.md) · [writes.py#L240](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memories/pg/writes.py#L240-L338) | **采用** derived observation 绑 `source_memory_ids` + 源移除时失效重建；**改变**为不假设同步彻底擦除 | 抽取质量、来源 ID、scope 正确 | 模型调用 + 多层状态 + 异步新鲜度；手动 mental model 由 owner 维护；tags 非 ACL（[tags.py#L1](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/search/tags.py#L1-L88)） |
| [OpenViking](../systems/source-studies/openviking.md) · [fs_service.py#L401](https://github.com/volcengine/OpenViking/blob/bbf2e37f88b8b15482edb83be41feb3ed510d03a/openviking/service/fs_service.py#L401-L474) | **采用**可寻址可编辑 context filesystem + 显式 account/user/peer scope + archive/live/derived 分离 | 归属与授权由上层正确提供 | 删除/摘要/索引非原子；`completed` 回执不保证每项索引更新；配置模式与异步阶段多 |
| [LangMem](../systems/source-studies/langmem.md) · [extraction.py#L1006](https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/knowledge/extraction.py#L1006-L1084) | **采用** hot-path tools 与 procedural（prompt）同 factual memory 分账 + namespace template | 应用自备 durable store/auth/采用新 prompt | 无内建 provenance/version/durable queue；候选检索上限使旧事实可能不进修订（[tools.py#L263](https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/knowledge/tools.py#L263-L355)）；两入口 payload 不兼容 |
| [A-MEM](../systems/source-studies/a-mem.md) · [memory_layer_robust.py#L463](https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer_robust.py#L463-L540) | **借鉴并改变**新经验重组旧 note 的邻域演化；验证关联是否帮助后续任务，并补 refresh/provenance/delete 合同 | 新经验确实需要重组旧理解，且刷新契约与实际检索收益可观察 | 旧 note metadata 更新时 embedding 不刷新、默认 evo_threshold=100 才重建（[#L352](https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer_robust.py#L352-L409)）；positional links 脆弱；无更正/删除 API |

## 5. 拟议实验设计（全部 `proposed`、尚未执行）

**候选条件工作表**

下列 C0–C5 仅是本研究的局部标签，不覆盖各 Case Card 的原编号，也不要求每个 case 强制全跑。具体实验要保留原条件与本工作表的映射；native 不支持的消融记不适用／未实现，不用 adapter 默默重建。

| 条件 | 暴露 | 用于 |
|---|---|---|
| C0 current-only | 仅 current probe | 检查 model prior 是否已能解题 |
| C1 no-memory | 同系统按原路径 ingest 后，原生禁用 memory use；其余 reader/context 条件保持可比 | 与从未接收历史的 C0 区分；不支持时不造一个同名替身 |
| C2 full-history | 全部 case-bounded history | 完整信息下可完成性 |
| C3 full-search / simple-file | 平文件 + 全文/关键词搜索；保留实际查询与返回材料 | 强基线，非上界；若同等条件下足够好，就需证明增加复杂度的收益 |
| C4 reference-context | 作者选择的参考材料，明确标注其选择来源与暴露范围 | 检查给定 reader 在这些材料下是否可完成；尚未执行，不是 retrieval 上界 |
| C5 system-native | 经系统 supported boundary | 原生能力与 adapter contribution |

**E-A 历史依赖与保留收益切片** · proposed
- 取一个 twin（优先 RC-001/RC-002），明确选择哪些候选条件与原 Case Card 对应；报告每格的 subject identity、input view、condition 与 response。
- 限制比较：C2/C3 若给更长 history，须同时报告 token 增量与 reader 是否相同；否则按 claim-boundary lanes 记为不同 input view，不得直接排序。

**E-B 修订 → 派生传播切片（X3/X7/X9）** · proposed
- 写旧值 → 明确 correction →（可选）删除来源；分别在 immediate / new session 提问，记录每层 current 值与最终 response。
- 对照 C2/C3 与「无派生状态」路径；用于区分「抽取丢了」「检索没到」「检索到但被派生层覆盖」。

**E-C 作用域/路由对照（X5/X6）** · proposed
- RC-003/RC-004 风格：merged vs scope-isolated vs current-metadata-only。
- 限制比较：若 preprocessor 按 metadata 只喂正确 rule，observed success 的 subject 是 combined pipeline；system routing 记 `unknown`。

**E-D 未完成意图/未来触发（X8）** · proposed（前置门禁）
- 若要形成 D-006 的 Case Lab 能力／关系主张，先满足其 [promotion rule](../case-lab/distinction-atlas.zh-CN.md)，补 community-grounded incident 与 observation boundary。未来独立装置可以在获准的实现任务中用公开 synthetic 输入验证状态／调度机制；这种工程验证不自动成为 D-006 case 或 prospective memory 能力证据。
- 记录 state availability / observation / action eligibility / actual action 四层（对齐 [EC-002 C-03/C-05](../research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md)）。

**比较纪律（irrespective of 实验）**
- input budget / exposure / reader 不等时：记录每格的 exposure 与 reader regime；跨格只描述、不并入同一有序表（[claim-boundary §5](../research/claim-boundary-study.zh-CN.md)）。
- 可借用 claim-boundary 的 A0–A5 区分 adapter 贡献，但这些类别、CL 和 lanes 均为 proposal，不是 accepted result schema。无论标签如何，替系统补出的能力不能归给原系统。
- 严禁把 scripted recall（`tools/synthetic_pilot.py`）或 input projection（`tools/continuity_inputs.py`）当作真实系统效果（[offline-rehearsal](../experiments/offline-rehearsal.md)、[continuity-input-audit](../experiments/continuity-input-audit.md)）。

**开发表例 vs 独立变体（打破自家评自家）**
- 开发表例可用于语义与工程设计，但不能再自称独立验证。锁定具体设计主张后，再形成未参与开发的变体；如继续用于调参，应重新标为开发材料。
- 后续验证保留改述、否定、邻近干扰、不同 family 和竞争解释，记录争议，不预设已接受的计分流程。受测系统不获得 evaluator key、作者 required/prohibited 评分清单、expected labels、未来事件或前题答案；用例允许暴露的历史及其中的撤回／禁止使用事件仍应原样保留，让系统自己正确处理。
- 争议交由与作者不同的 reviewer 判断，disagreement 保留而非平均掉。

## 6. 尚未解决的分歧与缺口

- RC-004 是 **scope-conditioned** 而非 pure twin：其因果措辞不得继承 RC-001（[RC-004 §8](../case-lab/cases/seed-004-private-greeting-public-template.zh-CN.md)）。
- X8（prospective）与部分 X9（derived layer）**无现成 case**；D-006 仍缺 community-grounded authority。
- 中文 semantic-equivalent matcher（RC-002/RC-003 位置与 rationale）尚未成 fixtures；AI-reviewed 语义仍待独立人类 reviewer。
- 十项目是**有意样本**，无 simple file/full-history 与参数学习完整对照（[source-studies README](../systems/source-studies/README.md)）；不得据此推断 GitHub 全貌。

## 7. 这些维度怎样约束候选设计

- 设计取舍要能应对上述可观察反例，同时承认案例无效、证据不足与系统失败是不同结果。
- 需要显式结果的对象：current vs superseded 区分、source/acceptance 归属、scope routing、prohibited use 缺席、derived-layer 收敛、delayed correction 持续。
- 自有候选不因可输出更细的 trace 就自动胜过其他架构。比较的公平性需要 X10 的边界说明；缺少 reviewed Architecture Pressure Map 时不宣称已经架构中立。

---

*本文件为 `proposed` 研究映射；未改变现有证据或 Case Card 的接受级别，也没有建立新的运行效果。*
