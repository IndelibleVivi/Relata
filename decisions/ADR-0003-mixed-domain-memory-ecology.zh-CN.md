**简体中文** | [English](ADR-0003-mixed-domain-memory-ecology.md)
<!-- language: zh-CN; mirror: ADR-0003-mixed-domain-memory-ecology.md; translation-status: synchronized -->

# ADR-0003 — Relata 研究混合领域记忆生态

**状态：** accepted
**范围：** R0 research object 与 case coverage
**接受日期：** 2026-08-24

## 中文摘要

Relata 继续以成人长期人机亲密与浪漫关系为主要 deployment domain，但不把 memory content 缩窄为显式的亲密表达、关系规则或 repair。当前 working evaluation object 是“长期人机关系中的混合领域连续性记忆生态”：personal/lived、shared-relational、operational/project 与 companion/system continuity 彼此作用，同时需要正确 routing、scope isolation、authority、time、permission 与 change handling。Pilot 001 只代表其中的 shared-relational / current-state-use 窄切片。

## English summary

Relata retains long-term adult human–AI intimacy and romance as its primary deployment domain, but does not restrict memory content to explicit intimacy, relationship rules, or repair. Its working evaluation object is a longitudinal, mixed-domain continuity-bearing memory ecology spanning personal/lived, shared-relational, operational/project, and companion/system continuity. Pilot 001 represents only a narrow shared-relational current-state-use slice.

## 背景

初始 research foundation 正确保留了宽广的 System Census objects、general causal controls、source authority 与 mixed architectures。但面向读者的 scope 与首个 case portfolio 过度强调了显式 relational content，容易让普通生活、学习、项目、决策、artifacts、handoffs 与 system migration 看起来像外围内容，除非 case author 强行为它们赋予 symbolic relationship meaning。

长期人机关系天然是 mixed-role、mixed-surface 的，可能同时包含 private conversation、日常生活、research、code、creative work、planning、group interaction、roleplay 与 infrastructure operation。只要这些世界中的任意一部分被遗忘、压平、错误 routing、被邻接 scope 污染或丢失 source authority，continuity 都可能失败。

## 决定

1. **Primary deployment domain：** 成人长期人机亲密与浪漫关系继续是 Relata 的 founding application domain。
2. **Memory content domain：** personal/lived history、shared relational history、operational/project history 与 companion/system continuity 都是一等 continuity-bearing material。
3. **Working evaluation object：** Relata 研究 **longitudinal, mixed-domain continuity-bearing memory ecology**，即长期人机关系中的混合领域连续性记忆生态。
4. **Relational memory：** 在 Relata 中，它表示存在于持续关系语境中的记忆，不意味着每个 remembered object 都显式讨论这段关系。
5. **General validity core：** factual recall、temporal reasoning、provenance、noise resistance、scope isolation、full-history/full-search comparison 与 bounded-context controls 都是一等 validity work。
6. **Routing 与 isolation：** Relata 研究 material 是否到达正确的 role、surface、project、person 或 instance，以及邻接 scopes 是否得到适当隔离。
7. **Case coverage：** 使用 `personal-lived`、`shared-relational`、`operational-project`、`companion-system` 与 `mixed-domain` 作为 coverage strata。它们不是永久 benchmark tracks，也不是互斥的 memory types。
8. **Pilot 001：** RC-001 继续是一项有用的 shared-relational current-state-use pilot，但不能定义或代表 Relata 完整 evaluation object。

在 Relata 声称 case programme 覆盖完整 working object 之前，至少必须实际运行过：一个 ordinary-life continuity case、一个 operational/project continuity case、一个 shared-relational 或 repair case，以及一个 mixed-domain routing 或 isolation case。这是 coverage gate，不是 validated sample-size claim，也不要求所有 case 预先 accepted。

## 保留的 alternatives 与拒绝的误读

- Relata 不会变成脱离长期关系语境的 generic memory leaderboard。
- Ordinary events 不需要被赋予虚构的 romantic 或 symbolic significance 才能进入研究。
- General memory evaluation 是保留的 validity core，不是 Relata 必须排斥的 contrast class。
- Projects 与 private life 既不会默认压成一个 undifferentiated scope，也不会默认互不相关。
- 四个 content domains 与五个 coverage strata 不会规定 internal ontology、storage schema、API 或 evaluation track。

## 后果

- Core authority、terminology、Case Lab metadata、System Census questions 与 promotion gates 必须在相关处区分 deployment domain、content domain、use domain 与 coverage stratum。
- Cases 必须在相关时声明 routing / isolation expectations，并在可行时包含 full-history/full-search comparison。
- 第一组 case portfolio 必须超出 Pilot 001，Relata 才能把自己描述为具有广泛代表性。
- 本决定不推出 runner、protocol、scoring contract 或 system-under-study interface。

## Review 与 reversal gate

如果 evidence 表明 mixed-domain object 过宽、无法形成 bounded causal cases，或者这些 strata 制造了系统性的 architecture distortion，又或者 community/system evidence 支持更好的 decomposition，可以通过后续 accepted ADR 修订本决定。Non-normative Target Architecture Draft 0.1 不能自行 supersede 它。
