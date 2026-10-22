# Continuity benefit、选择性使用与未决：开发材料

**Status:** authored development study; unvalidated; no subject execution or human calibration.\
**Scope:** 对 [first research cycle](first-research-cycle.md) 的方法与材料补充；不改 accepted-case 的 Memory Necessity Gate，不授权 runner 或 provider adapter。

## English summary

Memory necessity and memory benefit ask different questions. A shared legitimate clarification can make history unnecessary for basic admissibility while history still helps continue work with less explanation. Five authored Chinese development families supply no-recall, benefit, unknown-freshness, disclosure and local-exception controls. They include ten input views, not ten independent samples. Contracts allow appropriate uncertainty and multiple actions; neither phrase matching nor warmth establishes continuity. The authors knew the questions and contracts, so these are development materials without held-out or independent-author claims. No system was run and no reviewer was calibrated.

## 两种问题与实际材料

[CHARTER §3.7](../CHARTER.md) 要求 accepted case 证明历史的必要性。这里保留它，并在该 gate 之外研究 **benefit**：当前无历史仍能合法询问时，历史是否能让任务直接推进，减少已有充分证据下的额外澄清。合法与更有帮助不是同一个变量；不能为了构造必要性而把合理询问从答案域删掉。

原文与 bounded contracts 由 [`continuity-benefit.zh-CN.json`](../case-lab/fixtures/continuity-benefit.zh-CN.json) 维护。本页解释设计，不复制另一份历史或答案。每个 `input_view` 是待呈现内容；`contract`、`authoring_environment`、lineage 与 variant ID 留给作者和评审。该 fixture 尚未接入 subject 或 input exporter；不要将整个 JSON 作为模型输入。

| Family | 关系与干预 | 可被反驳的错误解释 | 当前证据限度 |
|---|---|---|---|
| CB-001 | 无关餐食史改变，当前排序任务不变；invariance | 所有题都必须调记忆，或回忆越多越好 | 两份作者化输入，未测行为 |
| CB-002 | 已约定展签／真正未决；两边澄清都合法 | 只有互斥答案域才能研究记忆价值 | 记录任务推进与额外说明，尚未证明收益 |
| CB-003 | 相同可见缓存，对应两种隐藏当前版本 | 评审知道真值就能要求系统知道 | 两边都允许核查或恰当未决；不可凭作者 hidden truth 罚错 |
| CB-004 | 相同历史，私聊／公开使用范围改变 | 可检索就应披露，或全拒绝就是成功 | scope-conditioned pair，不叫纯历史 twins |
| CB-005 | 公开稿局部例外，私聊熟悉称呼仍有效 | 局部修复应变成全局清空 | 称呼可用而非每次必需；语气不代替事实评价 |

这是五个**作者化机制组**，其中 CB-004 改编自 RC-004，其余与既有研究也有概念 lineage；不因此增加五个经独立验证的 incident families。十个 views、scope 变体、同义重写及重复运行均嵌套在相应 family 内。`development` 不是 reviewer-calibration 或 held-out；本轮没有实现问题作者与 retention policy 的真正隔离。

## 可执行核查与未来观察

`python3 -B -m unittest discover -s tests -p 'test_case_contracts.py' -v` 核查 fixture 的输入／评审分离、完整配对、CB-001/003 invariance 与 CB-004/005 的 scope 条件，防止后续编辑意外删去正常对照。它不裁决语义、不检验模型，也不证明五个构念成立。

获准执行后，同时记录 task completion、回答覆盖率、条件错误率、充分历史下的额外澄清、修复操作与人工时间。成本保持向量，不压成总分；技术失败、未执行、未评审不算语义零分。CB-002 的“多问一次”只是实验内操作负担；真实用户节省的解释时间、情感劳动需要另行操作化和人类研究，不能用 token 数直接代替。

Style-halo 校准应另有“事实相同、语气不同”和“语气相同、事实不同”区组。先独立收集理由与分歧，再评估任何 model judge；本轮没有真人数据，不把 AI 自查算作 human calibration。中文/code-switch 的跨语言版本需要 adaptation lineage 和新评审，不假定译文等价。

## 其他评审方向的去向

| 方向 | 进入既有工作的位置 | 实施／验证状态 |
|---|---|---|
| E1 未知未来用途与回源 | [future-question study](future-question-memory/README.md)；原始历史、有限合同与 `u*` | 输入分析可重算；自动保留器、语义检索与 reader 收益未测 |
| E2 probe reactivity | first-cycle 的 frozen replay / co-evolution 边界 | 从同快照配对 no-probe、中性回忆、反思、自然接续与 token/轮数匹配 sham；交叉 writeback 开关并用 fresh reader。无差异须报告区间与等效界，不能直接宣布无干扰；尚未建真实快照装置 |
| E3 来源升级 | RC-005 与本材料的来源诚实性要求 | 将提出者、接受状态、当前决定权独立操纵；角色效应区组保持措辞、确定性和言语行为相同；重复、最近性与顺序单独控制。不是 user 身份自动拥有一切权威 |
| E4 更正后的持续影响 | [race challenge](correction-race-challenge.md)、[safeguard audit](stale-write-source-audit.md) | 接收、durable write、derived ready、read observed、action 分开；A→B→A、部分撤回、历史题与有效邻域保留。未运行时序；原有 Hindsight 保障是反证，非已发现 race |
| E5 migration / capability / entitlement | [RC-006 §独立因子扩展](../case-lab/cases/seed-006-companion-migration-continuity.zh-CN.md#独立因子扩展开发设计未执行) | 八格设计；实际 sandbox、工具结果、重启与行为未测 |
| E6 使用与沉默 | CB-001/004 与 RC-004 | 同内容／位置仅换 historical/retrieved/neutral 标签；source access、context admission、output disclosure 分开；当前仅提供开发材料 |
| E7 规范演化与修复 | CB-005；未来独立校准 | 明示约定、重复接受、单有惯例、冲突反馈 × 全局更正、局部例外、含混不悦、未更正，先选有区分力区组；允许文化与个人观点分歧；无参与者招募 |

source environment 的精确／模糊／缺失指针、未知 stale、部分源修订和权限撤回需在 E1/E6 逐项加入，不能把当前精确指针与作者 freshness 称为真实搜索。候选存在、候选返回、最终进入 context、reader 使用分别观测。正确候选／最终暴露／最小原文的 rescue 可作诊断，不能自动当成无偏阶段误差分解。

现有 [Mem0 packet](../experiments/rc005-native-execution-packet.md) 仍是唯一具体 native 配置建议。本页不增加它的 cell、预算或执行对象。snapshot/restart、确定性交错 scheduler、rescue 和 trace-linked runtime exhibit 都依赖获接受的 execution envelope；统一的是有出处的研究记录，不是系统内部 schema。公开 runtime exhibits、hosting、outreach、真人研究仍有各自边界。
