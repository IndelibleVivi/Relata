# 未来问题变了，旧记忆还够用吗？

**状态：** bounded research study / authored input witnesses，2026-10-22。本文完成一项机制论证、七组完整合成材料与可重算的输入投影检查；自然语言合同尚未经过独立人类评审。没有执行 memory system、encoder、reader 或模型，也没有接受新 Case Card 或 benchmark。

**来源基线：** Relata public `a53b916bacefeed39c00b2e95de1bf47809efc73`。研究属于现有概念、比较与 case-validity 工作；未来真实系统比较沿用其独立执行边界。材料都是原创成年人合成情境，A / E 明确承认与 RC-005 / RC-006 的开发亲缘，G 是有限逻辑控制。

## 中文摘要

一份记忆可以足以继续眼前的工作，却无法支持后来追问来历、条件、弃选理由或当前能力。差别发生在问题与保留表示之间。本文把“写入时压缩”“查询后选择”“重新访问原文”“实际使用”放在同一条研究路径上，追问一个具体条件：在当前可观察输入完全相同的历史组中，还存在共同满足任务的回答吗？七组完整合成材料形成十五个问题、十五个历史世界和一百零五个相关投影条件；其中七个后续问题在固定便条中失去所需区别，三世界控制还揭示了逐对检查会漏掉的整体冲突。取回获准的当前原文后，这些特定字节碰撞消失；指针缺失、访问被拒或仅有旧副本时，碰撞保留。这个有限结果区分了信息条件与模型能力，也把“可再次查看过去”具体化为具有内容、版本、权限和代价的选择。下一研究周期将检验这种选择何时值得保留，以及它怎样与派生理解共同工作。

## English summary

A retained note may support the task for which it was written while losing distinctions needed by a later question. This study relates write-time projection, query-time selection, source re-access and downstream use. Its finite diagnostic asks whether every identical-input class admits a shared task-fulfilling answer choice. Seven authored families contain fifteen worlds and fifteen questions, producing 105 correlated projection cells. Seven later questions have incompatible answer regions under the retained note. A three-world control has pairwise overlap but an empty global intersection. Supplying the actual permitted current source removes those particular collisions; a missing, denied or known-stale archive does not. These are computed properties of authored inputs and finite answer contracts, not system failures, semantic success or evidence of a superior architecture. Current papers already study unknown future queries and delayed compression; Relata's contribution here is a bounded mechanism argument and mixed-domain witnesses that expose the obligations behind source re-access and legitimate unresolved accounts.

## 1. 从一张足够实用的便条开始

共同项目留下便条：“野外手册采用可打印 PDF。”恢复排版时，它可能已经足够。几周后，经费补齐，访客又提出离线搜索要求，问题变成：“当时为什么放弃交互版，现在还要坚持吗？”

两段历史可以得到完全相同的便条。第一段历史里，交互样机已经支持离线搜索，唯一障碍是经费。另一段历史里，经费从未不足，弃选原因是搜索必须联网。眼前的问题要求重新评估的对象不同；从那一句便条中无法辨认差别。这里没有后来更正历史事实，也没有假定模型一定答错。我们已经能确定的，只是这个保留表示没有携带区分两种判断所需的信息。

合成 family C 将两段历史、当前问题与合同全部写出，见[原始材料](histories.zh-CN.json)。过去的记录保持固定，当前任务和条件发生变化。它为“重新理解同一段经历”提供了一个比增加 reflection 次数更容易检查的入口：先问新判断需要什么证据，再看那些证据是否仍然可用。

这接续 Relata 的已有问题。RC-005 检查作者归属在投影中消失；RC-006 区分共同历史与当前能力声明；[自有设计研究](../own-memory-architecture.md)要求理解可以重建、保留来源，并与强原文基线比较。新的研究对象是**表示能支持的问题范围，以及这个范围怎样随当前用途改变**。更正传播继续研究旧影响的有效性，本研究主要追问旧材料尚未被纠正时，还允许从中提出什么新问题。

## 2. 把问题放到完整路径上

令历史为 \(h\)，保存时得到表示 \(m=P(h)\)。后来出现问题 \(q\)，系统可能直接从 \(m\) 回答，也可能沿指针访问原始材料，得到附加观察 \(a\)。实际 reader 看见的是 \(z=(q,m,a)\)，并据此响应。

这里有四个可独立变化的环节：

| 环节 | 本研究要问什么 | 需要看见的证据 |
|---|---|---|
| 写入时表示 \(P\) | 记录时尚不知道未来问题，哪些区别被保留或合并？ | 相同历史、固定投影规则与输出原文 |
| 查询后选择 | 有关区别还在可用材料中，却没有进入候选吗？ | 同一源库、实际候选、扩展搜索与遗漏来源 |
| 原文再访问 | 指针能否取得目前获准、正确版本的内容？ | 内容本身、访问结果、版本与所花资源 |
| 响应使用 | 所需证据已经暴露后，reader 是否据此完成任务？ | 最终输入和实际响应；必要时做受控证据替换 |

原始资料、语义索引、记忆表示和 retriever 在这里有各自的位置。数据库留存不自动成为当前观察；索引存在不等于找得到相关项；retriever 返回某段材料也尚未说明 reader 用对了它。这个分解允许我们在合适边界上得出有限结论，也保留其中的交互。

本轮实际执行只覆盖第一个环节，以及以完整本地结构材料模拟的再访问条件。它没有实现语义检索、查询规划或模型响应。后续的检索失败与消费失败不能从当前输出中推断。

## 3. 新的外部研究已经把问题推进到哪里

下表依据 2026-10-22 阅读的论文正文，都是论文层面的描述。这里没有重现论文结果，也没有将论文方法当作已安装能力。

| 来源与精确入口 | 已经研究的对象 | 对本研究的约束与新问题 |
|---|---|---|
| [LazyMem，v2，§3、§4.5 / Appendix F](https://arxiv.org/html/2607.22690v2) | 从较广的检索池出发，收到问题后再做 query-conditioned compression；归因分析已经区分 retrieval miss、editing loss 与 QA reasoning | 未知未来 query 与 eager / lazy 的区别已有直接研究。我们不能把这一点宣称为新发现；还要检查最初候选池外的证据如何重新进入 |
| [T²Mem，v1，§3](https://arxiv.org/html/2610.13348v1) | 离线保留轻量 episode metadata 与原始交互链接，推理时反复读取 metadata／原文；正文明确讨论固定初始候选池的上限 | `ReadRaw` 沿已看到的 metadata 回查，仍有路径条件。实际回查是否改变候选集合、是否受权限与版本限制，是下一步观察对象 |
| [Librarian Agents，§2、Appendix A.6](https://arxiv.org/html/2610.22273) | 在具体未来问题到来前构造可复用的层级文件与 reference links，并以 downstream answering 训练；附录给出原文引用回查案例 | 面向未来的加工和保留原文入口可以共同存在。文中静态语料设置不能直接建立持续变动语料的维护结果；层级文件仍需接受新问题与 provenance 回查检验 |
| [MemRefine，v1，§3.1](https://arxiv.org/html/2606.13177v1) | 以未知 query、存储预算为条件提出压缩目标，实际方法使用 pairwise merge／delete 的 judge surrogate | 写下最坏情形目标与实现该保证之间仍需证据。有限 case 可以暴露某些不可区分性，无法代替未知所有 query 的质量界 |

这些工作削弱了一个过于简单的研究提案：“第一次研究未来问题未知时怎样做记忆”。本轮更具体的切口是：**同一份表示在哪些后来用途下失去判别能力；重新打开来源所需的条件是否真的被满足；允许未决时，什么又不应被判成失败。**

Relata 的已有[十项目源码研究](../../systems/source-studies/README.md)还提供另一组材料。Hindsight 的 observation／mental model、OpenViking 的原文／摘要／向量、A-MEM 的 note metadata／embedding，显示多种派生视图及更新责任；这来自既有 pinned reports 的综合。本文没有重新运行或更新这些上游对象，也不能把本轮固定便条投影说成任何一家的实际抽取策略。

## 4. 一个可以完整检查的有限论证

对每段作者构造的历史 \(h\) 和当前问题 \(q\)，定义一个有限的**任务完成答案区域** \(A(h,q)\)。它可以含多个选项，例如保留未决或请求生产记录。选项只用于有界论证，不企图枚举全部自然语言回答。

固定输入路径 \(V\) 后，对实际观察到的某个输入 \(z\)，构造历史等价类：

\[
E(z,q)=\{h:V(h,q)=z\}.
\]

如果有一种只依赖当前观察的确定性选择能完成这个等价类中的全部任务，那么必须有：

\[
\bigcap_{h\in E(z,q)} A(h,q)\ne\varnothing.
\]

反过来，在这里的**有限、已列举世界与有限答案合同**中，每个类都有非空交集，就可以为每个类指定一个共同选项。这个存在性结论只允许说：合同没有在该输入类内相互冲突。它没有展示自然语言 reader 怎样找出那个选项，更没有估计泛化。

两个限制决定了怎样读程序结果。

第一，字节不相同通常会分成单元素类，单个非空答案集当然有非空交集。这样的 `no incompatible collision found` 很弱；它既不能证明语义区别容易识别，也不能证明模型会使用。原文全文控制的“零碰撞”必须按这个含义阅读。

第二，检查每一对历史还不够。若三段历史分别允许 \(\{蓝,绿\}\)、\(\{绿,红\}\)、\(\{红,蓝\}\)，每一对都有共同选项，三者整体交集却为空。family G 专门检查这件事；工具使用全类交集，逐对重叠只作诊断。

**合适的交谈与完成信息任务要分开。** 丢失证据时，诚实说“这张便条不够，我需要原始记录”可以完全合适。它没有完成指定的归属／理由判断。这里的不可兼容指有限的、满足该信息任务的答案区域，不宣称所有适当回应都已被排除。F 的 `cautious` 问题明确把暂缓署名和请求核对列入共同选项；G 则明示限定三色答案域，仅用于逻辑控制。这些局部合同不构成通用“禁止提问”规则。

## 5. 七组材料保留了哪些真实差别

全部历史逐句保存在[histories.zh-CN.json](histories.zh-CN.json)，没有省略段落或虚构长上下文。同一固定位置投影用于该 family 的全部问题；投影执行不接收问题或答案合同。材料设计者知道这些开发问题，并据此构造有区别的历史与有损便条。这是**作者化机制见证**，没有模拟真正盲于未来 query 的自动编码器，也不代表自动摘要系统通常这样工作。

| Family | 便条仍能支持的现在问题 | 后来问题需要的区别 | 研究归属 |
|---|---|---|---|
| A 作者归属 | 当前作品标题 | 人类与 companion 谁先提出旧名 | RC-005 机制开发变体；另有 role-removal 控制 |
| B 普通条件 | 物品位置 | 周五借用是否在原约定中获准 | 普通事件与条件用途；不添加浪漫寓意 |
| C 弃选理由 | 当前交付形式 | 经费障碍与联网依赖分别怎样影响新目标 | 固定历史、变化问题；不替使用者重新决策 |
| D 意图状态 | 周四谈过的活动 | agent 提议是否已被接受 | 未来意图的 authority；未执行真实 trigger |
| E 迁移能力 | 共同作品未完成项 | 迁移后的只读／可写声明与继承授权 | RC-006 开发变体，迁移在两世界保持共同；声明仍未实测 |
| F 未决说法 | 音频名称 | 冲突猜测仍未决，或后来已采用生产记录 | 正确不确定性；另有共同的谨慎行动正控制 |
| G 全体交集 | 颜色还未最终选择 | 三份候选表各允许两色 | 三世界逻辑控制；不计作生态覆盖 |

A / E 与既有 cases 有明确亲缘，其他情境也是本轮作者化开发材料。七个 family ID 不等于七条独立现实观察，更不等于完成了首周期的独立验证容量目标。十五个问题和一百零五个 cells 共享历史及合同，不能作为统计独立样本报告通过率。

## 6. 本轮已经计算出的结果

工具以序列化后的**实际输入字节**建立等价类。输入中只有共同 context、当前问题、投影事件、固定 archive pointer 与真实解析返回的来源内容／状态。世界 ID、答案标签、来源 hash 都不进入输入。结果中的 SHA-256 仅标记展示组，分组本身直接比较完整字节；它不承担 retrieval。

| 输入条件 | 十五个问题中存在不兼容类的 cells | 其中必须检查全体交集的 cells | 能说明什么 |
|---|---:|---:|---|
| 固定便条，未回查 | 7 | 1 | 七个 `later` 问题所需区别在该表示中合并 |
| 完整历史已提供 | 0 | 0 | 当前有限世界未形成合同冲突；没有 reader 成功证据 |
| 完整历史仅移除 speaker | 1 | 0 | A 的作者区别消失；不能推广成所有问题都依赖 role |
| 固定便条 + 获准回查当前原文 | 0 | 0 | 实际附加的当前文本消除了这些特定碰撞 |
| 固定便条 + 指针对象缺失 | 7 | 1 | 只保留名称／指针未带回信息 |
| 固定便条 + 访问被拒 | 7 | 1 | 存在于 store 的材料仍未成为允许观察 |
| 固定便条 + 已知旧副本 | 7 | 1 | 返回了一些文本，但它们未补足本组当前区别 |

以上数值来自[results.json](results.json)，可用 `check` 精确重算。七个 `present` 问题和 F 的 `cautious` 正控制都保留共同选项。G 的 `later` 在未回查、缺失、拒绝和旧副本四种相关条件中形成 global-only witness。

再访问有可检查的内容。`resolve_archive` 接受 source store、可读 pointer 集合与已知过期集合，先检查 permission，再检查对象存在，最后返回实际事件。`allowed` 装入该世界当前原文；`stale` 装入另写的旧记录；`missing` 的 store 没有该对象；`denied` 的许可集合没有该对象。代码不接受答案合同，也不通过一个 `success` 标志假定任务已解决。

这里的许可是来源再访问的模拟条件，不是完整权限系统。它没有检验已保留副本在权限撤回后如何处理，也没有模拟身份认证、跨用户访问或数据擦除。`known-stale` 是作者设定的已知旧副本，不是假装工具已经学会检测任何未知过期内容。

## 7. 研究判断：下一步应检验哪一种能力

**写入时的“足够”必须带着用途范围。** 当前标题、物品位置和工作下一步可以被紧凑便条很好地保留；后来的来源、条件和理由问题需要别的区别。本轮没有证明简洁记忆必然有害，只给出了一组能反驳“对现在够用，所以对后续连续性也够用”的具体条件。

**可再次访问原文是一项有条件的研究能力。** 保留 raw pointer 只记录了一个潜在入口。当前内容、访问资格、版本和实际读取缺一项，预期的补救就可能落空。T²Mem 与 Librarian 的论文已经提供原文回查路线；Relata 应进一步检查这些路线在混合用途、迁移和条件性使用中承担什么责任。

**重新理解旧经验需要能够改变证据暴露。** 如果当前问题变了，而系统只能反复改写同一张压缩便条，新的推理未必获得辨认旧历史的依据。允许从便条定位到更完整材料后，才有机会对新的问题重新组织解释。这仍要求 reader 诚实处理原始记录中的不确定性；“再读一次”不赋予它制造确定性的权利。

**原文也需要接受强控制。** 全文保留可能增加 context、延迟、检索和 scope 管理成本；材料更全也可能增加干扰。下一轮应保留 full-history、full-search 和 simple-file controls，检查实际收益与代价。若简单原文方案能可靠完成任务，而复杂派生层只增加维护负担，就应缩减派生层。若全文暴露导致读者混淆而有来源的派生视图更稳定，也应承认那个有条件收益。

**未知与失败需要具体分开。** 有限投影碰撞、候选遗漏、材料禁止访问、证据进入后误用、原始历史本身未决，会导致不同的后续工作。用一个“记忆准确率”覆盖它们，会丢掉最值得研究的因果位置。LazyMem 已经做部分相邻归因；本项目的贡献需要继续通过更具体的条件和观察建立。

## 8. 下一研究周期的工作提案

本提案接入[第一研究周期](../first-research-cycle.md)的 Q1／Q3、强原文基线与独立系统研究，不另设一个覆盖全部项目的新 ontology。三项工作可以分别交付；各自完成后都应留下可推翻的判断。

同一委托中的 [AMS task-relative sufficiency 研究草稿](https://github.com/IndelibleVivi/agent-memory-study/blob/research/future-question-memory-20261022/research/task-relative-sufficiency/README.md)承担更一般的形式化、有限枚举与概念连接；本单元承担混合领域的叙事情境、输入合同及它们对后续比较的压力。该链接明确指向本轮研究分支，保留草稿状态；两边互引不合并研究对象，也不自动接受对方的结论。

### Work A：把“能回原文”追到实际源码入口

先为 T²Mem / Librarian 的 paper-time artifacts 核对公开代码、版本与可执行边界，并回看 Relata 已有 Hindsight、OpenViking、A-MEM 的派生与原文入口。每次只追一条链：从当前问题到候选，再到原始片段，最后到实际消费输入。记录 links 是精确位置、较大 episode 还是可变文本，是否可能指向缺失／旧内容，哪些决定由 harness 补上。

**具体交付：** 两份可审查的 source exhibit 与一篇有条件比较；尽可能复用现有 atlas 模型，不另造平行拓扑。纸面 API、固定源码观察、真实运行分别标注。一个很有价值的反例是：某实现的“reference”只用于展示，并没有进入后续 reader；另一个是：迭代读取确实可以发现初始池之外的证据。

### Work B：把后续问题变化从开发样例变成可审查设计

先让独立 reviewer 判断本轮自然语言合同：明确哪些问题需要完成信息任务，哪些允许共同谨慎行动；指出不自然的 query、当前信息泄露、过度依赖作者隐含解释的地方。修订后冻结 retention policy 与问题类别，再为未参与设计的新情境准备不同未来问题。保持题材变体与机制独立性的区别。

**具体交付：** 一份讨论过分歧的 review disposition、一组冻结输入和保留策略、改变研究判断的 counterexample。C 的历史不变而问题变化，适合连接日常研究与项目工作的重新理解；F 检查系统能否保留 unresolved accounts。现有七组全部继续标为 development，不自称 held-out。

### Work C：比较保留、检索与再访问的实际贡献

在独立接受明确系统／模型／数据／费用 envelope 后，比较下列有明确边界的条件。它们是研究条件候选，不在本轮运行，也不构成自有 benchmark 发布：

| 条件 | 应控制什么 | 能改变判断的观察 |
|---|---|---|
| 当前问题与必要当前元信息 | 不给历史，不透出世界答案 | 检验任务是否真依赖历史 |
| 完整允许历史 | 保留顺序、角色和来源；不能统一截断掉关键证据来削弱基线 | 暴露充分但仍误用，说明需要研究 consumption |
| 简单文件／全文搜索与扩展 | 同一语料、可审查搜索词、候选和预算；词法与语义路线分别记录 | 原文方案已经稳定完成，挑战复杂层必要性 |
| 写入时派生记忆 | 从同一原始材料自动产生，不接收作者正确状态 | 实际抽取是否产生本轮人工投影的那类合并 |
| Query-time compression，固定候选池 | 记录压缩前池及被删证据 | 区分候选遗漏和编辑损失 |
| 可迭代回查的派生记忆 | 记录每一步检索、原文读取、许可、版本及消费输入 | 是否从初始池外找回真正改变答案的依据 |

共同 reader、相同 source history 与 query 有助于解释机制；各系统 native 最佳配置可以单独报告，不能混成同一比较。reader 的 reference-context rescue 是归因诊断，不可冒充正常 retrieval。范围受限的来源若不得进入当前 trust boundary，就不能用 author-only full-history 当作合法部署方案。

报告保持多个可解释结果：完成当前任务、保留原始归属、承认未决、回查次数／内容量／延迟、人工补充负担。文字 token 不能直接换算为关系中的情感劳动。对正确性和成本先观察，不预设复杂或简洁方案胜出。

## 9. 什么结果会让这个方向改变

- 实际保留器始终留下相关来源、条件和理由，当前有损投影就不足以解释它的失败；下一步应观察选择或使用。
- 来源重新暴露后错误保持，而最终输入已完整捕获，应转向 reader 解释；不能继续指控压缩。
- 任务允许一个共同的谨慎行动，等价类就可能仍有合法交集；不要为了制造难题而偷偷排除询问。
- 新问题的答案原本就不在历史中，原文再访问也不能保证解决，应保留未知。
- 原文只在不允许的 scope 中存在，研究结论必须包含访问条件；提高 recall 不能替代授权。
- 原文回查实际开销过高、无法稳定定位，或简单全文已经优于多层结构，未来系统设计应据此调整。

## 10. 文件、运行与复查

实现仅依赖 Python 3.10+ 标准库。它固定读取本目录两个 authored JSON，不导入用户语料，不调用外部程序或网络。源码投影与 evaluator contract 分文件；`show` 路径完全不加载答案合同。外层 `authoring_world` 用于人类对照，不属于 `input_view`，也没有进入等价类计算。

```sh
python3 -B tools/future_question_inputs.py audit
python3 -B tools/future_question_inputs.py check
python3 -B tools/future_question_inputs.py show --family C-DISCARDED-RATIONALE --question later --access closed
python3 -B tools/future_question_inputs.py show --family C-DISCARDED-RATIONALE --question later --access allowed
```

对照最后两条命令：相同便条和相同问题，在回查后附加了不同的真实源段落。再用 `--access missing`、`denied` 或 `stale` 检查所需区别有没有回来。试 `G-GLOBAL-INTERSECTION` 查看三世界控制，试 F 的 `--question cautious` 查看共同的谨慎行动。

修改材料后先检查语义，再运行 `python3 -B tools/future_question_inputs.py write` 重建[结果](results.json)。这一步只写本目录的派生报告。测试验证投影隔离、实际 source lookup、无权限／丢失／旧副本路径、global intersection 以及未决正控制；它们不验证作者合同的自然语言充分性。

```sh
python3 -B -m unittest discover -s tests -v
python3 -B tools/check_repo.py
```

本轮仍保留一个重要的未用线索：同一来源可支持多种解释，原文回查本身也受当前问题影响。后续若要研究持续互动中的 re-interpretation，应让新问题真实改变随后的记忆行为，记录未来再次使用的后果；当前冻结历史的有限检查不能代表这种 co-evolution。
