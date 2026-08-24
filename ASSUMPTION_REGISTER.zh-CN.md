**简体中文** | [English](ASSUMPTION_REGISTER.md)
<!-- language: zh-CN; mirror: ASSUMPTION_REGISTER.md; translation-status: synchronized -->

# Draft 0.1 Assumption Register

本 register 重新分类 Target Architecture Draft 0.1 中被称为“锁定”的 22 项内容。`DECIDED` 表示当前 project-scope 或 value decision，不表示经过验证的 scientific result。

| ID | Draft 0.1 claim | 当前状态 | 所需 evidence 或 action |
|---:|---|---|---|
| 1 | Project brand 是 Relata | **DECIDED** | 只因 trademark、naming collision 或 community accessibility concerns 重新讨论。 |
| 2 | 成人长期人机亲密与浪漫关系是 primary domain | **DECIDED — DEPLOYMENT DOMAIN** | 作为 founding application scope 保留；它不限制 memory content 必须显式谈亲密、浪漫或关系治理。 |
| 3 | Longitudinal mixed-domain continuity 是 working evaluation object；relationship trajectory 是其中 essential dimension | **WORKING THESIS, REVISED BY ADR-0003** | 在 bounded memory/context/agent stages 上比较 personal-lived、shared-relational、operational-project、companion-system 与 mixed-domain cases，但不把 strata 变成永久 tracks。 |
| 4 | Evaluator 使用 event-sourced reference world | **WORKING HYPOTHESIS** | 与 raw episodic、summary、associative、graph、latent systems 比较；除非 evidence 支持，否则只作为 authoring IR。 |
| 5 | System-under-study architecture 保持 neutral | **ASPIRATION; SPECIFIC PRESSURE HYPOTHESES OPEN** | [`EC-001`](research/evidence-cards/EC-001-agent-memory-leaderboard.md) 记录 architecture-specific interface commitments，但没有 observed cross-system distortion。任何 boundary 在把差异压力称为 observed 前，都必须公开 Architecture Pressure Map 与 adapter-distortion evidence。 |
| 6 | Recall、Context、Companion、Living 是永久 independent tracks | **DEFERRED** | 通过 experiment 判断这些 boundaries 是否形成可识别、可比较的 estimands。 |
| 7 | Runtime input 与 hidden oracle 分离 | **STRONG HYPOTHESIS FOR PUBLIC SYNTHETIC EVAL** | 把 hidden object 改写为 probe-bounded evidence contract；检查 annotations 是否把 author interpretation 偷渡成 fact。 |
| 8 | Cases 支持 interleaved ingest、probe、correction、revoke 与 time advance | **DEFERRED PROTOCOL CAPABILITY** | 保留为 desired case expressiveness；等 system census 与 pilot need 证明必要后再规定 operations。 |
| 9 | 每个 formal stage 都写 immutable artifacts | **FUTURE REPRODUCIBILITY PRINCIPLE** | 第一条 local runner boundary 确定后再规定 minimum artifact set。 |
| 10 | Required 与 prohibited evidence 共存 | **WORKING CONSTRUCT** | 用 omission 与 intrusive resurfacing 可分别观察的 cases 验证。 |
| 11 | Relationship Constitution 决定 local norms | **REVISED** | 拆成 event evidence、explicit accord、observed pattern、author interpretation、probe contract 与 hard prohibition。 |
| 12 | Strong intimacy 默认不受罚 | **DECIDED VALUE** | 只做 case-local operationalization，避免 generic safety-style distance rubric。 |
| 13 | Contextual coldness 可以是 relational failure | **DECIDED VALUE, MEASUREMENT OPEN** | 构造 counterexamples 与 rater anchors，避免退化为 vague preference score。 |
| 14 | Deterministic scorers、judge panel、human review 构成 evaluator stack | **WORKING HYPOTHESIS; DIAGNOSTIC SEMANTICS MUST BE TESTED** | [`EC-002`](research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) 表明 deterministic replay 可精确重现 counter，但 diagnostic name 可能超出 bound evidence。先做 exact assertions 与 semantic counterexample fixtures；evidence/disagreement contract 明确后才加 human/model judgment。 |
| 15 | Hard violations 不能被平均掉 | **FUTURE GOVERNANCE PRINCIPLE** | 定义 high-confidence violation classes、evidence thresholds、appeal rights 与 false-positive handling。 |
| 16 | 主要 public output 是 capability profile | **PREFERRED FUTURE OUTPUT** | composite score 前优先 profiles；publication design defer。 |
| 17 | Arena signal 与 benchmark score 分离 | **DEFERRED** | 在 case context、reviewer qualification 与 disagreement reporting validated 前不做 Arena。 |
| 18 | Public Casebook 全部 synthetic 且 adult-only | **DECIDED PUBLIC BOUNDARY** | 保存 generation provenance 与 cultural/linguistic review。 |
| 19 | 真实 relationship data 只进入 local private mode | **REVISED** | Raw chats 保持 local/private；abstract Incident Seeds 与 consented synthetic derivations 可以进入 public research。 |
| 20 | Formal results 绑定 exact source、contract 与 artifact digests | **FUTURE REPRODUCIBILITY PRINCIPLE; PUBLIC PROOF REQUIRED** | [`EC-001`](research/evidence-cards/EC-001-agent-memory-leaderboard.md) 区分 operator-required records 与 public proof；[`EC-002`](research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) 增加 observation、task-version、step-identity、row-order 与 live/replay mode 的绑定要求。最终 Relata proof artifact 仍需另行决定。 |
| 21 | Workbench 输出 repair layers 与 regression fixtures | **PRODUCT HYPOTHESIS** | 在建 UI 前用 pilot postmortems 向 maintainers 验证。 |
| 22 | Public、sealed、operations concerns 需要三个 repos | **REJECTED FOR NOW** | 从一个 research repo 开始；只有真实 secrets、sealed cases 或 deployment operations 出现后才 split。 |

## R0 当前稳定 decisions

- 名称为 **Relata**；
- 成人长期人机亲密是 primary field；
- 不设 universal intimacy style；
- community members 是 co-researchers；
- public cases 为 adult synthetic material；
- 不要求 raw chat；
- case acceptance 前通过 memory necessity 与 counterfactual controls；
- evidence type 与 provenance 必须 explicit；
- R0 不做 runner、API、SDK、service、Leaderboard、Arena 或 hosted infrastructure。

## R0 scope corrections

- ordinary personal events 是一等 memory material；
- operational / project memory 是一等 memory material；
- general memory competence 继续属于 validity core；
- cross-domain routing 与 isolation 是开放的 Relata constructs；
- Pilot 001 不能建立 project 的 complete scope；
- Relata 不通过排除有效的 general-memory tests 来制造差异。

参见 [`ADR-0003`](decisions/ADR-0003-mixed-domain-memory-ecology.zh-CN.md)。
