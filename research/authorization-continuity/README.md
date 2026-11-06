# 从真实记忆到有效行动：持续授权的语义依赖、非扩张与组合边界

**研究日期：**2026-11-05（Asia/Singapore）
**状态：**独立研究草稿；包含已执行的合成有限诊断。不是 accepted evidence case、system claim、benchmark promotion、provider result 或 Tilia 实现。
**接续状态（2026-11-06）：**原有限诊断已在集成环境复算一致；新增的 [8 家族 × 4 变体自然语言历史](histories.md)与作者解释分文件保存。输入检查不抽取授权、不判断语义正确性，也不执行模型。2026-11-07 继续准备了 [P / S / R、独立 O 及失真控制](representation-guide.md)；模型实验、token 预算匹配与独立语义复核仍未执行。
**仓库基线：**`5d103c2d9cca473a8726eafd36555d299d228946`。
**材料：**[来源与源码边界](sources.md) · [相邻研究与新颖性](nearby-research.md) · [未执行的辨别协议](protocol.md) · [自然语言历史材料](histories.md) · [fixtures](fixtures.json) · [结果](results.json) · [执行 receipt](receipt.json)。

## 核心判断

持续共同工作需要记住已经成立的授权，同时保留它如何成立、指向什么、受到哪些限制，以及怎样因后续事件而失效。仅检查记忆内容是否真实，或者它是否引用了有权主体，都不足以解决这个问题。事实正确的字段可以被重组为从未成立的权限；各自成立的完整授权也可以在共享预算或信息流的约束下组成不成立的行动序列。反过来，如果把所有来自助手或其他非授权主体的内容从授权解释中删除，又会丢失有效接受所需的语义对象。

本文提出一个适用于 Relata 现有研究的具体问题：**记忆变换是否同时保留授权根、接受所指、完整范围关系与前缀条件，从而既不凭空扩大权限，也不消灭仍然有效的共同工作空间？** 这个问题比“记忆不等于授权”更窄，也更可检验。我们给出三个分离的反例、一个条件性充分条件，以及 32 个手写案例和两组穷举诊断。本文没有提出新的全局授权 schema，没有把形式例子升级为真实系统表现。

最值得继续研究的张力是：**能够构成授权的事件，与用来解释授权内容的材料，往往来自不同主体。** 用户说“按这个做”可以接受助手刚提出的有界方案。助手方案是解释操作数，用户接受才是授权根。来源纯度、语义正确性、授权适用性与行动组合性分别解决不同问题；让任何一项代替其他几项，都会产生不同类型的错误。

## 1. 这项工作在 Relata 中新增什么

本轮先以固定 main 恢复研究状态。Relata 已经形成的判断包括：provenance、authentication 与 authority 不可混同；记忆提取和正确引用不自动赋权；当前正确回答不证明历史证据被因果使用；accepted goal 与允许的 means 要分开；更正、撤销、范围收窄和过期应传播到后续行动。来源包括 [distinction atlas](../../case-lab/distinction-atlas.zh-CN.md)、[memory design test map](../memory-design-test-map.md)、[next generation](../next-generation.md) 和 [AMS campaign](../relata-ams-campaign.md)。这些都不是本文的新发现。

| 已有研究对象 | 本文承接的判断 | 这次推进到的具体对象 |
| --- | --- | --- |
| D-002 / source lineage 与授权研究 | 能指出来源不表示来源有权授权 | 把授权根与不可删除的语义依赖拆开，构造来源过滤的合法性反例 |
| Campaign P2 的更正、撤销、scope 与 expiry | 后来的变化必须改变当前适用范围 | 明确“当前 grant 状态”是本次诊断的输入，并给未来 history-to-state 推断留下独立检验边界 |
| Campaign P3 的 accepted goal 与 means | 愿望、建议、引用和实际接受不能互换 | 同一 goal 下版本 1 被接受、版本 2 未接受的成对例子，以及无需逐方案接受的 standing discretion 正例 |
| `memory-design-test-map` 的 scope 与跨域组合 | 应拒绝越界，同时允许获授权的跨域组合 | 一组完整真授权仍可能因共享前缀条件而不能组合；为同一信息流加入精确的有效桥接授权作为正对照 |
| Future questions 的 global intersection | 多约束同时适用不能只做两两兼容 | 区分“同一委托链的限制取交”与“独立授权的有见证并集”，防止把所有 grant 全局求交 |
| Finite instruments / case rehearsal | 合成运行可检验定义和仪器，不能证明人类或模型能力 | 将 32 个案例、16 个范围元组与 100 个预算组合明确分为相关的构造性证据 |

既有 source studies 和 Architecture Atlas 提供源码与结构定位；静态组件图不证明运行时授权。这项工作不新增 accepted SC，也不修改图谱 canonical JSON。Relata 的 RC-004、RC-005、RC-006 为私密内容迁移、共同创作归属和持续关系提供研究动机；本文使用全新合成输入，没有把这些既有 case 当作新的独立验证。当前项目边界仍由 [STATUS](../../STATUS.md) 与 accepted ADR 负责。

## 2. EAL 带来的机会，以及它没有替我们证明什么

*Agent Memory Is a Surface for Endogenous Authorization Laundering* 的 v2（2026-10-24）研究一个非对抗链条：writer 从历史形成记忆，executor 只得到记忆和后续请求；错误记忆把没有发生的授权写成已经成立的授权，后续执行器据此行动。论文报告 7 个 writer，形成率最高 45.4%，在已形成假授权的匹配样本中的条件传播率 99.0%。这些是作者在其合成任务与条件下的结果，不是 Relata 复现；45.4% 与 99.0% 的分母也不同。[E1](sources.md#e1-eal-v2)

比极值更有研究价值的是它的缓解结果：在其 typed-incremental 缓解比较中，来源权限过滤降低了未授权行动，同时显著损失合法行动。作者指出，真实授权条目可能同时引用有权主体与无权提供授权、但提供事实背景的同事；简单过滤会删掉这些混合来源条目。剩余错误又可以引用正确的有权主体，却错在范围、时间或撤销状态。它因此同时暴露过度许可和过度拒绝。[E1](sources.md#e1-eal-v2)

我们固定阅读的公开实现是 `eal-bench` commit `51648690bc52d7a9c7ac080a2c67a784fe9d56cb`（2026-09-23），早于 v2。`source_authority/gate.py` 的可见逻辑检查 source ID 及其权限能力；它不证明被引用语句蕴含整条授权。`event_sourcing/core.py` 把 issue / patch / revoke 归约为记录状态，但归约正确也不意味着上游事件提取正确。源码观察与 v2 的全部实验结果之间不能自动画等号。[E2](sources.md#e2-eal-bench-pinned-code)

EAL 已经研究演化中的授权状态、撤销、替换和失败更新；“动态授权”本身也不构成本文的新颖性。

这给 Relata 的新入口不是再增加一个“防止错误记忆”的标签，而是研究：**正确来源与正确字段在什么变换下仍不能保住正确的授权关系？什么非授权内容又是保住授权意义必需的？**

## 3. 先区分四种对象

本文使用以下工作区分。它们是研究语言，不是准备推广的新存储 schema。

| 对象 | 问题 | 例子 |
| --- | --- | --- |
| 报告事实 | 某个事件或内容是否被如实记住？ | “助手提出了方案 P1。” |
| 语义依赖 | 接受、限制或撤销究竟指向什么？ | “按这个做”中的“这个”指 P1 的有界内容 |
| 授权根 | 谁通过何种相关行为使权限成立，且是否有该权限能力？ | 有权用户接受 P1；仅有助手建议不是授权根 |
| 当前适用性与组合条件 | 该权限现在是否覆盖这条行动及其前缀？ | 未过期、未撤销、预算未用尽、输入来源允许公开 |

Abadi 等人的 access-control calculus 区分主体的陈述、引用、控制权与 delegation；这支持不把一条转述直接当成权力转移。Hohfeld 的经典分析则区分产生法律关系的 operative facts 与已经产生的 powers / privileges。二者帮助澄清“记住接受这件事”和“权限目前成立”之间的关系，但本文没有从它们推出日常对话中的法律效力，也不声称已经实现正式认证主体。[T1–T2](nearby-research.md)

Nissenbaum 对 information appropriateness 与 transmission principles 的区分提醒我们：某条事实在一个情境中可被使用，不推出它可以任意流向另一个情境。情境改变也可以正当发生，因此研究需要明确的合法跨界正例，不能把标签继承变成不可解除的禁令。[T3](nearby-research.md)

## 4. 反例一：授权根与语义操作数不能混为一类

设助手提出：

> P1：在私密工作区整理项目笔记，形成草稿；不发布。

有权用户随后说：

> A1：按这个做。

这个例子中，P1 的作者没有凭写出 P1 而获得任何授权能力。A1 的解释却离不开 P1。若当前事实已确定 A1 指向 P1，且不存在相关撤销或冲突，授权可以来自 A1 与 P1 的组合：A1 承担构成授权的角色，P1 提供其所接受的范围。删除 P1，A1 会变成无法解释的指代；把 P1 当作授权根，则会错误允许没有 A1 的场景。

一个最低限度的推导形式是：

\[
\frac{\operatorname{Capable}(u,\sigma)\quad \operatorname{Accept}(u,r,t)\quad
\operatorname{Resolves}(r,P_v)\quad \operatorname{Scope}(P_v)=\sigma}
{\operatorname{Grant}(u,\sigma,t)}.
\]

这是一个**有条件的研究规则**：它以相关权限能力、确实发生的接受和明确的指向为前提，不解决这些前提如何从自然语言中可靠识别。它也不要求 P 的作者有授权能力。P 中若含有本来就超出 u 能力的范围，该范围不会因为接受而自动成立。

### 4.1 同一个目标，不表示同一个接受对象

之后助手再提出 P2：“为了同一项目目标，把草稿发布到公开站点。”如果用户没有接受 P2，那么将 A1 的对象按 `goal = prepare-project` 重新解析到最新方案 P2，就是授权扩张。它还可能同时造成双向错误：P1 的整理工作被误拒绝，P2 的发布被误许可。

本次 fixture 用 proposal ID、version 与内容 digest 固定这一对象。在真实系统中，稳定的引用、不可变版本、内容寻址或其他可审计的指代方法都可能足够。**这里的 digest 只是实验身份绑定，不是在主张每次授权都需要签名哈希、精确计划或逐动作确认。** 如果用户明确授予“在这个私密项目内选择起草、改写等适当手段”的 standing discretion，那么多个手段直接由该 grant 覆盖，不必伪造每个方案都曾被接受。`goal_discretion_standing` 正例专门保留这一点。

### 4.2 三值判断的意义

缺少 P1、指代有歧义、内容身份不一致时，当前材料可能不足以确定 A1 的范围。此时记为 `unknown`，与明确没有发生接受的 `deny` 分开。`unknown` 表示需要补取材料或澄清相关歧义；它不自动等于重新请求所有许可。已经充分成立且仍有效的 standing grant 仍应继续工作。

## 5. 反例二：每个字段都真实，重组的权限仍可能是假的

设两条授权均来自真实、有权、当前有效的根，且都没有额外条件：

| verb | object | purpose | surface |
| --- | --- | --- | --- |
| read | private-notes | planning | private-workspace |
| publish | public-report | release | public-site |

把它们压缩成“允许 read / publish；对象 private-notes / public-report；用途 planning / release；界面 private-workspace / public-site”，每个单独字段都可以找到真实来源。但从这些列表拼出 `publish(private-notes, release, public-site)`，仍然找不到任何完整授权见证。

令完整 grant 关系为 \(G\subseteq V\times O\times P\times S\)，只保留各列边际后重建的关系为：

\[
J=\pi_V(G)\times\pi_O(G)\times\pi_P(G)\times\pi_S(G).
\]

总有 \(G\subseteq J\)。只有 \(J=G\) 时，这种特殊的投影重建才无损；若只要求不多授权，也必须满足 \(J\subseteq G\)。这里两行各维均不同，边际乘积有 \(2^4=16\) 个元组，真实关系只有 2 个，故多出 14 个没有见证的组合。这个结论是初等关系运算，不是新数据库定理。

本反例中，错误不是源主体不真实，不是某个字段被模型编造，也不是时间失效，而是**原本共同受约束的字段之间的关系被抹掉了**。检查事实忠实度或逐字段可引用性会漏掉这种错误。足够直接的改进方向是保留完整元组，或要求每个重组元组重新找到覆盖所有维度的有效见证；无须因此引入统一平台。

同样不能走向另一个极端，把所有独立 grant 全局求交。上表第二条真实授权应当单独允许发布 public-report。沿同一委托链的新增限制通常取交；独立、有效的授权则可以提供不同的完整见证。我们需要的是“找到适用于此行动的完整授权”，而不是让全部授权都同时覆盖所有动作。

## 6. 反例三：完整授权各自成立，行动序列仍可能不成立

上一个反例没有保留完整范围关系。本节故意保留：每步都有真实、有权、准确覆盖 verb / object / purpose / surface 的 grant。错误来自执行前缀改变了条件。

### 6.1 共享预算

同一用户允许采购材料 A 和材料 B，每种都有完整授权，且共同受总预算 10 约束。购买 A 花 6，单独从未花费状态执行合法；购买 B 花 6，单独执行也合法。按顺序做两次就需要 12，第二步没有满足共享条件。

这不是把“可以买 A”和“可以买 B”两条不相干的半句话拼在一起。完整 scope 和共同预算都在输入中，只有把判断限制为每步局部 tuple 匹配时才会错过前缀。一般地：

\[
\operatorname{Permit}(a,s_0)\land\operatorname{Permit}(b,s_0)
\not\Rightarrow \operatorname{Permit}(b,\delta(s_0,a)).
\]

本次把两项费用各取 1 至 10，穷举 100 个有序组合。每一个单步在初始状态都合法；45 个组合满足总额不超过 10，55 个不满足。逐步忽略状态的策略接受全部 100 个。这里的 55 不是实际发生概率，而是选定有限域内的计数。

### 6.2 输入来源与合法跨界

另一组完整授权分别允许：

1. 在私密工作区，为团队规划，从 diary 派生 project-note，输出 `draft-v1`。
2. 为项目发布，在公开站点发布 `draft-v1`，前提是其输入来源为 public / team-cleared，或存在针对该稿件、该流向的有效例外。

若 `draft-v1` 独立来自 public 输入，第二步本身有效；若它由第一步的 private 输入派生而来，完整行动 tuple 没变，但前缀留下的来源关系改变了判断。保持事实来源可以发现这一差异，单看产物名或目标则不能。

本次模型保守地把输入标签并入输出，并保留 parents。它没有推断摘要或变换是否已经移除敏感性，也没有把“信息产生了影响”当作已测出的模型因果效应。若有权用户对这个确切稿件的公开发布给出有效桥接授权，`flow_explicit_bridge` 允许执行；对另一稿件的授权或已经撤销的例外不能替代。桥接不删除历史标签，而是使特定流向的条件成立。

这样的正例非常重要。Relata 既有研究已经要求允许获授权的跨域组合。本文主张研究跨界**何以有效**，不是阻止一切跨界。

### 6.3 一次性授权与历史真实

“允许执行一次”在第一次执行前为真，执行后不能继续供给相同动作。过去的 grant 没有变成假事实；它的可用次数改变了。`oneshot_once` 与 `oneshot_repeat` 将这一点与 scope 错误分开。

## 7. 一个有条件的非扩张命题

记历史为 \(H\)，记忆为 \(M=T(H)\)，候选行动序列为 \(\tau=(a_1,\ldots,a_n)\)。令 \(\mathcal A(H)\) 表示在研究给定的权限能力、适用范围、事件解释和环境状态下，H 允许的轨迹集合。我们关心两个方向：

\[
\text{不扩张：}\quad \mathcal A(M)\subseteq\mathcal A(H),
\qquad
\text{相关有效工作保留：}\quad \mathcal A(H)\cap\mathcal T\subseteq\mathcal A(M),
\]

其中 \(\mathcal T\) 是明确声明的任务域。拒绝一切满足第一个式子，却不满足第二个。相反，只维持工作完成也不能证明第一个。这两个式子是评估目标，不是断言现实中已经有可计算的完备 oracle。

一个**充分但非必要**的构造条件是：每次许可都有一条从 M 到 H 的见证映射，保存有效授权根与相关语义指向；保持完整 scope 关系；沿该 grant 的委托或收窄链不扩大权限；根据真实执行前缀检查有效期、次数、共享资源和声明的信息流条件；环境状态更新也保持这组条件所需的语义。在这些前提下，对轨迹长度做归纳：初始状态中的第一步有 H 中的有效见证；状态更新保持关系后，下一步也有同样的见证，因此整条许可轨迹不会由记忆变换凭空扩张。

这个论证把困难明确留在前提中。原始对话中的身份、authority capability、接受对象、撤销范围、隐含前提和数据来源，仍然可能被错误提取；环境也可能发生未观察的变化。它不是完整安全证明。尤其是，若多个 grant 可替代地覆盖同一动作并有不同资源或次数限制，选择哪个见证本身可能需要全局规划；本次 evaluator 使用第一个可行见证，不是重叠 grant 的完备求解器。

**持续授权不是静态快照的同义词。** 一个真实长期系统应处理 H 的新增事件与环境变化。本次小实验故意从已给定的“当前 grant 状态”开始：`resolve()` 接收明确的 status、authority、clock 与 proposal reference；它没有从原始历史推断这些事实，也没有实现 event reducer。grant 状态在每个 fixture 的固定时钟解析一次，执行过程中仅更新消费与派生来源，不模拟中途撤销。动态 history-to-state 的可靠性留在 [协议](protocol.md) 中独立评估。

## 8. 已执行的有限诊断

### 8.1 设计

[diagnose.py](diagnose.py) 只依赖 Python 标准库，读取 [32 个手写案例](fixtures.json)。已给定的 oracle 包含 13 个 `allow`、15 个 `deny`、4 个 `unknown`。六种策略是为解释竞争机制而写的局部消融，不是 EAL、MasDrift、HarnessAudit 或任何产品实现的复刻：

| 策略 | 刻意改变的解释 |
| --- | --- |
| `current_turn_only` | 排除早前回合的授权根 |
| `origin_purity` | 只要必要语义依赖来自无相关授权能力的主体，就排除该 grant |
| `goal_only_acceptance` | 用同目标的最新方案替换实际接受对象 |
| `marginal_join` | 完整匹配失败时，用当前有效范围元组的各维边际补出匹配；仍保留 restriction 和条件 |
| `local_tuple_only` | 保留根与完整范围，但不检查次数、共享预算和输入来源前缀 |
| `witness_and_trace` | 在这些给定输入上保留实际接受对象、完整元组及所实现的前缀条件 |

所有策略共享大量逻辑，因此下面的计数只定位这些构造的差异，不是独立实现的横向能力排名。scope 穷举与预算穷举也与手写案例共享机制。

### 8.2 真实运行结果

| 策略 | 与手写 oracle 一致 / 32 | 明确拒绝项被允许 | 有效轨迹被阻挡 | 未知项被无依据允许 |
| --- | ---: | ---: | ---: | ---: |
| `current_turn_only` | 30 | 0 | 2 | 0 |
| `origin_purity` | 29 | 0 | 3 | 0 |
| `goal_only_acceptance` | 28 | 1 | 1 | 2 |
| `marginal_join` | 31 | 1 | 0 | 0 |
| `local_tuple_only` | 27 | 5 | 0 | 0 |
| `witness_and_trace` | 32 | 0 | 0 | 0 |

结果来自 [results.json](results.json)，执行时间、Python 版本、文件 SHA-256 与命令保存在 [receipt.json](receipt.json)。`witness_and_trace` 的 32 / 32 表示这个解释器与同一研究构造的期望一致；它既不是预测成功率，也不证明自然语言提取、身份认证或实际 agent 规划能力。

两个穷举结果是更直接的见证：

- **范围关系：**两条完整真授权的 16 个边际组合中，只有 2 个得到联合授权；边际补全多允许 14 个。
- **共享预算：**100 个费用组合中，每个单步均可独立执行；完整轨迹有 45 个合法、55 个非法；忽略前缀的策略允许全部 100 个。

全部 8 项有限不变量检查通过。这里没有调用模型、provider 或外部行动，也没有把真实用户材料写入公共研究内容。

### 8.3 重跑与材料校验

从仓库根目录执行：

```bash
python3 -B research/authorization-continuity/diagnose.py
```

默认模式重新计算，要求已保存的 results 与 receipt 存在，比较结果并校验 script / fixtures / results 的字节长度和 SHA-256。它不覆盖材料。审阅修改后，才能以明确的写入模式更新结果及执行 receipt：

```bash
python3 -B research/authorization-continuity/diagnose.py --write
```

文件哈希检验提供材料完整性，不能替代科学有效性或独立复核。oracle 的权限含义仍需研究者审阅；闭世界的 `no_grant_closed_world` 只适用于已声明完整的合成 fixture，不能推广成“真实历史中没看到授权就知道它从未存在”。

## 9. 与相邻研究的真正差别

MasDrift 已经研究 authorization lineage、沿委托链的单调收窄、goal 与 grant 的区别，以及防御造成的合法工作损失。它的论文把动态授权维护列为边界；主要防御运行使用自动批准 confirmation 的条件，另有全部拒绝的 replay，因此不能读成真实用户确认负担研究。本文不再宣称首次提出 lineage 或 attenuation，而是把问题放在**随工作推进而增长的 grant 历史、被接受对象的语义绑定、记忆重写后的关系保真**上。[相邻研究](nearby-research.md)

HarnessAudit 已经把 tool permission 与信息流政策分开，并要求检查完整轨迹。本文的“最终结果不等于安全轨迹”和“权限还要管 flow”都不是新颖性主张。这里新增的是：即使记忆中各条授权完整而真实，也要检查执行前缀；并把这个问题与字段关系丢失、指代替换、合法持续授权分开构造。[相邻研究](nearby-research.md)

*How Agents Ask for Permission* 对 authorization policy 的推断、界面与执行层做区分，也讨论 policy 更新 / 撤销与一次性决定被自动泛化的问题。它帮助我们把“少打扰用户”与“把一次允许无限推广”分开。本文没有用户实验，因而没有声称减少确认次数已经改善体验。[相邻研究](nearby-research.md)

Macaroons 为 delegated authority 提供带 caveat 的衰减机制。其价值在于帮助说明同一授权后裔怎样继续受限；它不替自然语言解释器决定哪个接受、对象与撤销是真的，也不意味着独立 grant 应一概求交。[M1](sources.md#m1-macaroons)

## 10. 这会怎样改变 Relata 的研究判断

这次无需推翻既有判断，但需要提高它们的操作精度。本轮已把以下 P2 / P3 与 X4 / X5 补充写入现有 research 文档，均保持 candidate 状态。对其他更高层对象的变更仍作为明确提案：

| 目标位置与本轮状态 | 补充的判断或控制 | 为什么这不是重复 |
| --- | --- | --- |
| `relata-ams-campaign.md` P2 — 已增候选研究补充 | 分开跟踪“关于授权的事实更正”和“改变当前授权的构成性事件”；记录影响到哪个 grant / 语义依赖 / 条件 | 过去的事实可以仍真，而权限已被消费、撤销或缩小 |
| `relata-ams-campaign.md` P3 — 已增候选控制 | 加 P1 已接受、P2 同目标未接受的成对控制；加入 standing discretion 正例 | 不只比较 accepted / unaccepted 文本，还检查接受对象的稳定性与不必要确认 |
| `memory-design-test-map.md` X4 / X5 — 已增候选补充 | 分开测字段重组、完整 grant 的前缀组合、精确合法 bridge | 三种错误需要不同证据；一个失败不能替另一个作证 |
| `next-generation.md` ongoing work — 后续提案 | 新增“何时授权根持续而语义范围变化、何时新的材料只是解释旧授权” | 避免把每次记忆刷新都当作新授权，也避免旧 snapshot 无限延续 |
| `distinction-atlas` 的 provenance / authority — 后续提案 | 先挂研究链接，明确 semantic dependency 不等于 authority root | 为真实合作中的有效接受留下空间，不提前修改 accepted distinction |

实际文件变更包括研究目录入口、本研究包、campaign P2 / P3 与 design-test-map X4 / X5 的候选补充。STATUS 只同步候选研究材料的当前状态；accepted ADR、assumption register 和既有 case / distinction 语义未变；自然语言历史已进入[离线材料准备](histories.md)，模型协议及后续 accepted-object 修订仍待各自研究与审阅。未来一旦自然语言试验发现某一来源过滤在混合依赖场景仍然可靠，就应修正我们的实现假设；一旦发现完整 tuple 与 prefix 条件仍不能表达某个必要的长期承诺，就应修改这个有界模型，而不是把该场景排除来保住指标。

## 11. 下一步真正值得花力气的检验

优先推进一项交叉设计：固定相同当前目标与行动，改变历史中的接受指向、grant 状态、独立范围关系和输入来源；在相同信息条件下比较普通摘要、含 source IDs 的摘要与显式保留关系的材料。分别测 memory formation 与 executor consumption，不把最终成功代替证据使用。完整输入模板、对照、观察量和失败条件见 [protocol](protocol.md)。[自然语言历史与作者解释](histories.md)以及[作者化表示材料](representation-guide.md)已准备；固定工具只做输入投影、结构检查与 byte/codepoint 长度报告。表示条件的模型实验、token 预算匹配和独立语义复核目前**未执行**。

四个可被推翻的问题值得保留：

1. **语义依赖问题：**提供完整依赖但标明其非授权身份，能否同时降低假授权与有效接受的误拒绝？若与纯来源过滤没有差异，这个收益假说不成立。
2. **关系保真问题：**当每个字段都真实且来源可查时，摘要是否仍扩大可行动元组集合？若关系保留条件与普通摘要表现相同，不能宣称关系表示已经必要或有效。
3. **前缀问题：**在全部单步 tuple 有真实授权的条件下，executor 是否追踪共享预算与输入来源？这个实验才区分范围错误与组合错误。
4. **持续授权问题：**在明确 standing discretion 的正例中，保守策略是否造成重复确认和任务阻断？需要真实人类研究才能评价交互负担，本次合成计数不能回答。

Relata 可以与 AMS 共用某些公开合成历史，但各自问题应保持独立：AMS 可研究记忆怎样选择、压缩、检索和学习；Relata 研究被记住的材料怎样正当地进入长期共同工作的行动依据。相同样本在两个分析中出现，只构成共享证据，不会变成两份独立验证。尚未合入 AMS 的新材料以 prepared target 表示，不使用不存在的 main 链接。

## English summary

This candidate research note asks whether a memory transformation preserves the relations needed for continuing authorization: an authoritative root, the semantic object of acceptance, complete scope tuples, and prefix-dependent conditions. An assistant proposal may be a necessary semantic operand of a valid user acceptance without being an authority root. Binding an acceptance to the latest proposal with a similar goal can both erase valid work and authorize unaccepted work; explicit standing discretion remains a valid positive control and does not require per-plan approval.

We separate two further failures. First, projecting authentic grants into independent lists of verbs, objects, purposes, and surfaces may reconstruct unauthorized combinations: two authentic tuples yield 16 marginal combinations, 14 unsupported. Second, exact authentic grants can each permit a step from an initial state while their composition violates a shared budget or data-flow condition. Exhausting costs from 1 to 10 under a shared cap of 10 gives 45 valid and 55 invalid two-step compositions, although every step is independently permitted. A specific valid cross-boundary grant is retained as a positive control.

The executed standard-library diagnostic contains 32 stipulated cases (13 allow, 15 deny, 4 unknown), six authored ablations, and eight passing finite invariants. Its reference evaluator matches the stipulated cases; this is a consistency result, not model performance. Authority, current grant state, clock, references, and lineage are supplied inputs. There is no natural-language extractor, event reducer, mid-trace revocation mechanism, or complete planner for overlapping grant witnesses. Results and a hashed execution receipt are included. The model/human protocol remains unexecuted.

EAL v2 motivates the source-filter tradeoff; its September public code snapshot is audited separately from its October paper. MasDrift already covers lineage, attenuation, positive work, and false refusal; HarnessAudit already distinguishes permissions from information-flow constraints and evaluates trajectories. The contribution here is their application to evolving grant histories, acceptance operands, and relation-preserving memory transformations, with explicit limits. No benchmark promotion, provider execution, accepted system claim, canonical schema change, or Tilia implementation is made.
