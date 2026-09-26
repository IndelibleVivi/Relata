**简体中文** | [English](RESEARCH_QUESTIONS.md)
<!-- language: zh-CN; mirror: RESEARCH_QUESTIONS.md; translation-status: synchronized -->

# Relata Research Questions

每个 research question 应指明与 claim 对应的证据：按需要使用 exact sources、community-grounded incidents、system observations、synthetic cases 或 controls。概念或源码研究不必包含每一种 evidence route。漂亮定义本身不证明 runtime behavior，也不自动解决竞争解释。

## RQ1 — 我们究竟在评估什么？

可能的 objects 包括 memory engine、context compiler、完整 companion agent、relationship trajectory、mixed-domain memory ecology、repair process 或 user-governance surface。

**所需 evidence：** competing decompositions、causal controls，以及能说明各 boundary 下哪些 failures 可以或不能归因的 pilot observations。

## RQ2 — 被记住的 object 是什么？

Candidate objects 包括 raw episodes、ordinary events、people and places、claims、facts、preferences、project state、artifacts 与 source authority、tasks 与 blockers、decisions 与 rationale、milestones、working context、external references、handoff state、unfinished threads、rituals、roles、interpretations、relationship state、future intentions、unresolved tensions，以及 model / instance identity。有些系统可以维持 continuity，却不暴露离散的 “memory object”。

**所需 evidence：** System Cards，加上 materially different architectures 处理同一种 personal、relational、operational 或 companion-continuity phenomenon 的 incidents。

## RQ3 — Authority、perspective、consent 与 disagreement 怎样工作？

Relata 必须区分 speaker、subject、recorder、interpreter、accepter、corrector、revoker 与 scope holder。它也必须保留 unresolved disagreement，不强造 false consensus。

**所需 evidence：** 涵盖 companion inference、third-party claims、jointly accepted interpretations、corrections、revocations 与 contested relational meaning 的 cases。

## RQ4 — 什么是 current state、history、transition 与 conditional coexistence？

“Latest wins” 有时正确，有时会造成破坏。多个 states 可能按 surface、trigger、role、time 或 explicit condition 共存。

**所需 evidence：** 只有 transition 或 condition 改变的 counterfactual twin groups。

## RQ5 — 什么时候 relevant memory 应当保持沉默？

Retrieval relevance、context eligibility 与 response appropriateness 是三个不同问题。

**所需 evidence：** 涉及 sensitive resurfacing、private/public boundaries、unrelated vulnerability 与 memory-display behavior 的 incidents 与 cases。

## RQ6 — 如何做 memory contribution 的 causal identification？

好回答可能来自 current turn、model priors、system prompt、persona 或 memory。坏回答也可能发生在 retention、state change、activation、context construction 或 response use。

**所需 evidence：** current-turn-only、no-memory、full-history/full-search、bounded-context、reference-context 与 system-native controls；在相关处加入 cross-domain ablation，以及 project-isolated 与 merged-history comparison；只在系统实际暴露 intermediate artifacts 时保存它们。

## RQ7 — 什么 system-under-study boundary 能比较系统而不抹平系统？

Write/search operations、evidence recall、rendered context 与 complete-agent interaction 暴露不同 capabilities，也引入不同 distortions。

**所需 evidence：** 跨 materially different systems（包括 opaque systems）的 Architecture Pressure Maps 与 adapter-distortion reports。

## RQ8 — 哪些 judgments 可复现？

有些 assertions 可以 exact；有些需要 bounded semantic judgment；还有一些始终具有 cultural 或 relational contestability。

**所需 evidence：** annotation anchors、blind review、reviewer-group comparison、disagreement analysis；model-judge audits 只能在 human review contract 稳定后加入。

## RQ9 — 真实经验应怎样进入 synthetic public casebook？

Relata 需要 lived expertise，但不能把 private relationships 变成 harvested datasets。

**所需 evidence：** per-contribution consent records、abstract Incident Seeds、contributor 对 synthetic derivation 的 review、data minimization 与诚实的 withdrawal process。

## RQ10 — 怎样的 Relata 才对 builders、researchers 与 relationship communities 有用？

研究的证据应支持理解或行动：澄清概念、帮助架构选择、区分 relational distinction、定位 system diagnosis、形成 regression case、修复 governance，或明确限制 claim。

**所需 evidence：** source studies 与研究判断的实际取用记录；pilot postmortems 说明 contributors 与 maintainers 能否在不重建 hidden evaluator reasoning 的前提下定位 failure 或 ambiguity。采用本身不证明有益。

## RQ11 — Mixed memory domains 如何 coexist 与 route？

Personal life、shared relationship history、operational projects 与 companion identity 应如何相互影响，而不被压成一个 profile，也不跨 roles、surfaces、projects、people 或 instances 泄漏？

**所需 evidence：** multi-project / multi-surface System Cards；cross-domain Incident Seeds；routing / isolation counterfactuals；full-history/full-search 与 system-native baselines；以及同一 memory 在某个 role 中 valid、在另一个 role 中却 distracting、private、stale 或 misleading 的 cases。

## RQ12 — 不同项目说的 agent memory 是什么？

Memory、persistence、context management、retrieval、state、learning 与 experience reuse 在具体实现中怎样重叠或区分？什么过去被保留、怎样影响现在、这种影响存在于哪里？文件、完整历史、外部存储、agent 控制的 context 与学习后的变化，都是待检查对象，不是预设 taxonomy。

**所需 evidence：** 与 exact paper / source paths 对应的竞争定义、原生生命周期描述，以及会改变边界判断的反例。[Agent-memory inquiry](research/agent-memory-inquiry.md) 开始这项工作，但尚未接受定义。

## RQ13 — 开源 memory 架构有哪些有条件的长处与局限？

哪些选择在 fidelity、change handling、scope isolation、实际帮助、可检查性、可迁移性、成本与维护之间取舍？公开实现提供什么，模型、harness、应用或人还要补上什么？比较 actual version / config，并区分 library、完整 agent、托管产品与历史实现。

**所需 evidence：** source-reviewed System Cards、可检查的机制比较，以及足以支持各项 outcome claim 的证据。论文或厂商报告的分数不会自动成为公开 repo 的结果。源码分析可以指出设计取舍，而不声称已经测到系统失败。

## RQ14 — 哪些结论可以跨通用与亲密使用情境迁移？

Task-oriented agents、普通生活与成人长期亲密关系共享哪些 continuity 要求，哪些要求取决于局部情境？同一架构怎样支持 project authority、shared authorship、scoped correction、unfinished intentions 与 appropriate silence，同时不把情境视为可互换？

**所需 evidence：** 可对照且保留差异的使用场景、明确的局部期待、源码机制与 bounded observations。关系特定要求不能成为隐藏的通用产品要求；通用 benchmark 成功也不直接证明关系连续性。

## RQ15 — 独立编写的自有 memory 系统应先验证哪种架构？

围绕独立的长期 **Tilia** 目标，源码研究和案例要求怎样帮助我们设计有连续性收益、可纠正、按 scope 使用、可检查和可迁移的 memory 系统？哪些责任需要显式状态，哪些由完整历史、可搜索文件或宿主 agent 就能更简单地承担？同样的标准能否暴露自有候选的弱点，而不偏爱它的表示方式？这项研究问题不在 Relata 内启动实现；向量语义检索是 Tilia 预期设计的必要能力。

**所需 evidence：** 带替代方案的[候选架构](research/own-memory-architecture.md)、记录覆盖缺口和推翻条件的[案例—测试映射](research/memory-design-test-map.md)，以及后续对实际使用、成本、修复和持久性的有界观察。既有开发表例不是 held-out validation；scripted 状态检查不证明语义 memory 质量。
