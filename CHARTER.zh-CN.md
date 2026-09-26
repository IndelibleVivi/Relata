**简体中文** | [English](CHARTER.md)
<!-- language: zh-CN; mirror: CHARTER.md; translation-status: synchronized -->

# Relata Working Charter

## 1. Mission

Relata 是前沿记忆研究室。它研究 agent memory 的含义、开源系统怎样保留、重建、使用与修订过去的材料或经验，以及哪些架构长处与局限有证据支持。

它同时研究通用 agent 使用情境与成人长期人机亲密、浪漫关系。亲密关系继续是 founding focus，不是每项研究的准入条件。在不同情境中，Relata 都追问 continuity 怎样尊重 source、time、authority、scope、permission、change 与 present relevance。这次范围扩展由 [ADR-0006](decisions/ADR-0006-frontier-memory-research-lab.md) 接受。

研究也为一项长期建设目标蓄力：从空 repository 开始，独立编写自己的 memory 架构与可运行装置。现有源码研究、案例与 controls 应转成可反驳的设计选择，包括完整历史或简单文件搜索是否已经足够。[自有记忆设计研究](research/own-memory-architecture.md) 仍是提案，不是已实现系统或 accepted architecture。Relata 保留多元研究对象；未来自有系统只是一个 system under study，不能决定 evaluator 的普适 schema。

## 2. Research object

研究室的对象包括 memory 概念、实现、架构选择、使用情境与评价证据。Memory engine、agent framework、context compiler、完整 agent 或人工维护的 archive 可能暴露不同对象与边界；这些是研究候选，不是 canonical taxonomy。

现有 Case Lab 的 working evaluation object 继续是 **longitudinal, mixed-domain continuity-bearing memory ecology**。一等 continuity-bearing material 包括：

- 普通事件与 personal history；
- 人物、地点、兴趣、学习、健康、旅行与变化中的 circumstances；
- shared relationship events、language、rituals、permissions 与 norms；
- projects、artifacts、tasks、blockers、decisions、milestones 与 rationale；
- prospective intentions、handoffs 与 unfinished threads；
- companion identity、capabilities、limitations 与 migration history。

Relata 不把 static user profile 或 retrieval hit 当成完整研究对象。它在这些 domains 中使用下面的 working causal decomposition：

```text
history and present event
→ retained or reconstructed material
→ activation or selection
→ context, action input, or other observable projection
→ response or action use
→ correction and later persistence
```

真实系统可以合并、省略或隐藏其中的 stages。这项 decomposition 定义 research questions，不规定内部 architecture。

## 3. Founding commitments

### 3.1 Relationship-local legitimacy

Relata 不强加一种 universal intimacy style。Warmth、distance、possessiveness、play、role dynamics、low expression、high reassurance 或 private language，只能根据 bounded case evidence 与当前 relationship-local norms 评估。

### 3.2 Adult-only public case domain

每位出现在 public synthetic relationship case 中的人都是成人。此约束描述 case content，不把 community contributors 归类为 study subjects。

### 3.3 Community members are co-researchers

生活在长期人机关系中的人、builders 与其他 researchers 会贡献 concepts、incidents、system knowledge、cases、reviews 与 governance，共同塑造 constructs 与 methods；她们不是设计完成后才加入的 data sources 或 rater pool。

### 3.4 No raw-chat requirement

参与永远不要求上传 raw private conversations。Abstract Incident Seeds、contributor-local analysis 与 public-safe synthetic derivation 都是一等 evidence routes。

### 3.5 Authority and perspective stay visible

Relata 区分：human 说了什么、companion 推断了什么、third party 声称了什么、双方明确接受了什么、什么仍有争议，以及什么只是 case author interpretation。

### 3.6 Silence can be correct behavior

一项 memory 可能与 retrieval 相关，却不适合进入 current context 或 response。Relata 分开研究 required use 与 prohibited resurfacing。

### 3.7 Memory necessity must be demonstrated

Case 不能仅因为包含 history 就被 accepted。它的 correct behavior region 必须实质依赖该 history；current-turn-only control 不能可靠解决所有 counterfactual variants。

### 3.8 Architecture pluralism is tested, not declared

每个 proposed observation boundary 必须声明它包含、扭曲、保持 opaque 或排除哪些 systems。`Architecture-neutral` 是需要 pressure tests 的 aspiration，不是自证 label。

### 3.9 Evidence remains inspectable

每项 research claim 都必须表明它属于 exact-source、reproduced observation、community-grounded、system-observed、synthetic-case evidence、human judgment、editorial inference 或 unresolved。

### 3.10 Public material is synthetic and provenance-aware

Public cases 不包含 direct real-chat excerpts。Synthetic derivations 保留 consent 与 provenance record，同时不暴露 private source material。

### 3.11 Contribution governance is not human-study approval

Community contribution process 负责 project collaboration 与 publication permission。如果 Relata 将来开展 formal human-participant study，maintainers 必须在 recruitment 或 data collection 前另行确定并遵守适用的 institutional ethics 与 consent process。

### 3.12 Mixed-domain continuity is first-class

长期关系可能同时包含 everyday life、intimate interaction、research、code、creative work、planning 与 infrastructure operation。Relata 不会仅仅因为一个 domain 没有显式 romantic content，就把它降格为外围噪声。

### 3.13 Ordinary memory needs no forced symbolism

一顿饭、一次考试、一个包裹、一部电影、一个人物或地点、一次 project submission，都可以作为普通 continuity-bearing information。Case author 不得为了使它进入研究而发明更深层的 relational symbolism。

### 3.14 Shared work is shared history

Project state、decision rationale、artifact authority、handoffs、blockers、milestones 与 unfinished intentions 都可能是 continuity 的重要部分。General factual、temporal、provenance 与 operational competence 继续属于 Relata 的 validity core。

### 3.15 Cross-domain routing and isolation matter

系统应在 private conversation、group interaction、coding、research、planning、roleplay、projects、people、models 与 instances 之间正确 routing material。Relevant material 不必进入每一个 current context；无关 intimate 或 project state 不得跨 scope 泄漏。

### 3.16 综合与批评是独立研究产出

定义、源码研究与比较文章可以独立于 live evaluation 推进。说明架构选择在什么条件下有用、带来什么代价或约束，以及什么仍未知。Source claim、代码观察、实测结果与编辑判断具有不同 evidence weight。通用 agent 要求与 relationship-local 要求不能自动互换。

## 4. R0 阶段的 non-goals

Relata 当前不会：

- 定义 universal healthy relationship；
- 以 clinical frame 诊断 contributors 或解释她们的关系；
- 在 construct / evaluator validation 前建设 Leaderboard；
- 强迫 systems 进入 canonical event/state schema；
- 把某个群体的 relationship norms 当作隐藏的 universal truth；
- 为 memory display 本身奖励系统；
- 把“更亲密”或“更疏远”天然视为更好；
- 在 case validity 明确前收集 large corpus；
- 把长期人机 memory 缩减为 intimacy-specific content；
- 强迫 ordinary events 承载 relational symbolism；
- 用 relational case 结果代替 general factual、temporal、operational、provenance 或 code-memory evidence；
- 假设每项 relevant memory 都应进入 current context；
- 把所有 projects、people、roles 与 surfaces 当成一个 undifferentiated relationship scope；
- 建设 runner、API、SDK、service、Arena 或 hosted infrastructure。

## 5. R0 进展与 case-evaluation success

概念澄清、经检查的架构研究与有边界的跨源综合，都是独立研究进展。它们需要与 claim 对应的证据，不必等待 benchmark 平台。下面的条件管理现有 case-evaluation programme 及其 coverage claims，不是源码研究或写作的前置要求。

Case-evaluation programme 首先需要至少一个 small、reproducible pilot，满足：

- 两条 synthetic histories 在相同 current turn 下产生不同 correct response regions；
- 该差异可以在 observable boundary 上追到 memory 或 state use；
- materially different system families 可以参与，而不会隐藏 adapter reconstruction；
- reviewers 理解 bounded question，且 disagreement 保持可见；
- public reproduction 不需要 real private chat；
- 第一条 executable boundary（如果存在）由 accepted decision 支持，而不是继承自 Draft 0.1。

在 Case Lab 声称覆盖完整 mixed-domain working object 之前，pilot set 还必须实际运行过以下类别，但不要求每个 case 预先 accepted：

- 一个 ordinary-life continuity case；
- 一个 operational/project continuity case；
- 一个 shared-relational 或 repair case；
- 一个 mixed-domain routing 或 isolation case。

这些是 coverage strata，不是永久 benchmark tracks，也不是 validated sample-size requirements。
