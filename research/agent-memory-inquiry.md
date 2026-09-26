# Agent Memory：定义、架构与连续性

**Status:** open research inquiry / article seed
**Opened:** 2026-09-22
**Authority:** research scope under [ADR-0006](../decisions/ADR-0006-frontier-memory-research-lab.md); no accepted definition, system comparison or evaluation protocol

## 中文摘要

这条研究线追问：GitHub 上以 memory 为名的项目分别让什么过去、通过什么机制、在什么条件下影响 agent 的现在？它把概念辨析、源码结构、架构取舍与长期使用情境放在一起研究；通用任务和成人长期人机亲密关系可以各自成立，也可以互相照亮。现有[十项目源码研究与架构图集](../systems/source-studies/README.md)，但独立人类 review、端到端效果比较与定稿文章尚未完成。

## English summary

This inquiry asks what different memory projects preserve from the past, how that material influences present agent behavior, and under which conditions their architectural choices help or fail. It connects conceptual analysis, public-source inspection, tradeoffs and longitudinal use inside and outside adult human–AI intimacy. Ten bounded source-study drafts and thirty source-linked architecture views now support the inquiry; independent human review, end-to-end comparison and the article manuscript remain unfinished. No taxonomy or performance ranking is accepted.

## 文章可以抓住的主问题

> 当开源项目都使用 agent memory 这个名字时，它们分别实现了什么；这些实现能支持哪些连续性要求，又把哪些责任留给了模型、harness、应用和人？

暂定题眼：**《Agent Memory 到底是什么：开源架构、长期使用与人机关系中的连续性》**。题目、读者范围与最后论点仍待具体研究收敛。

一个可检验的写作假设是：只按存储介质或 retrieval 方法归类，会漏掉过去怎样成为当前行动依据，以及这种影响如何被修订。这不是“真正的 memory”的排他定义。文件、完整历史、检索层、状态管理、规则、参数或人工维护都可以成为候选研究对象；是否应称为 memory、learning、context management 或其组合，正是需要论证的边界。

## 用同一组问题读不同系统

| 问题 | 要检查什么 | 能形成怎样的判断 |
|---|---|---|
| 它承诺记住什么？ | 原始经历、抽取断言、偏好、状态、技能、经验或其他对象；内容来自谁 | 保存粒度与信息损失，来源保留与解释负担 |
| 什么在跨时间延续？ | 具体文件、数据库、图、context、模型状态、人工维护或组合；实际 persistence boundary | 哪些重启、session 或模型切换在承诺范围内 |
| 过去如何影响现在？ | search、触发、context 编排、工具调用、决策或参数影响；谁完成最后一步 | native 能力与应用/harness 需要补上的责任 |
| 新信息怎样改变旧影响？ | 纠正、并存、过期、撤回、删除、派生状态与后续传播 | 更新便利与历史保留、修复范围与邻域误伤之间的取舍 |
| 哪些信息可以到哪里？ | 来源、说话者、项目、人、角色、surface、权限和用户控制 | 跨域帮助、错误混用、可检查性与可迁移性 |
| 好处和代价在哪里出现？ | 实际工作负担、响应与行为、成本、延迟、维护、可复现性及适用条件 | 有条件的优势与局限；证据不足时保留未知 |

这些是阅读问题，允许不适用；它们不是固定系统 ontology、统一 API 或六项评分表。架构分析需要写出机制为何值得采用，不能只列问题；同样，README 宣传语不能替代实现与效果证据。

## 人机恋语境内外怎样接起来

同一机制可以在不同场景中被要求完成不同的事。以下是后续可设计的对照，不是已经观测到的系统失败：

| 共同问题 | 一般 agent / 工作场景 | 成人长期亲密关系场景 |
|---|---|---|
| 来源与接受 | 提案、owner 决定、工具结果与完成状态 | 谁提出共同作品的名字，谁接受，谁后来更名 |
| 条件性修订 | 临时环境例外不覆盖所有项目规范 | 技术工作中的一次纠正是否误抹私人相处方式 |
| 未完成意图 | 中断后恢复主任务和交接依据 | 日常约定、共享创作与未完话题能否自然延续 |
| Routing 与沉默 | 项目隔离、过时决策、权限范围 | 私人历史在群聊或工作 surface 的使用边界 |

关系语境会让来源、共同意义、长期变化与修复成本变得突出，但这些问题不必被宣称为亲密关系独有。关系中的普通生活和工作也无需附加浪漫象征。文字更温柔、记忆展示更多，都不能自行证明连续性更好。

## 初步 GitHub 线索与后续源码研究

下表保留最初从 2026-09-22 官方 README 读到的选择线索，不能单独作为实现证据。随后完成的[十份源码研究](../systems/source-studies/README.md)固定了 Mem0、Letta、Graphiti、lmc-5、Tideline Memory、Aelios、Hindsight、OpenViking、LangMem 与 A-MEM 各自的公开 commit，并声明实际覆盖；其中两份有窄范围离线观察。它们仍是 source-study drafts，不是 reviewed System Cards，也不构成代表性样本。

| 官方入口 | 当前来源声明 / 线索 | 值得继续查的问题 |
|---|---|---|
| [Mem0](https://github.com/mem0ai/mem0#new-memory-algorithm-april-2026) | README 明确将所列 benchmark 数字归于 managed platform，并说明含 OSS SDK 没有的优化（`SOURCE-CLAIMED`） | 哪个版本、边界和配置真正承载了性能主张？OSS 可检查的生命周期是什么？ |
| [Letta](https://github.com/letta-ai/letta#historical-source) | README 将当前实现指向 [letta-code](https://github.com/letta-ai/letta-code)，并将 archive branch 的 V1 API server 标为历史源码（`SOURCE-CLAIMED`） | 当前 harness 与历史 server 分别怎样管理 memory？哪些旧论文或比较仍指向旧边界？ |
| [Graphiti](https://github.com/getzep/graphiti#graphiti-and-zep) | README 将 temporal graph framework 与 Zep managed infrastructure 区分，列出各自提供的功能（`SOURCE-CLAIMED`） | 图框架本身承担哪些更新、时间和来源职责？应用还需补上哪些用户、对话与使用流程？ |

由此得到的初步编辑判断（`INFERRED`）：跨项目文章首先需要对齐被比较的对象。名称相同的开源仓库、托管产品、历史论文实现和完整 agent，不能仅凭品牌一起接受或否定。首批精读按机制差异和可检查性选取；文件/完整历史等较简单的机制也应作为候选对照，不能只按 stars 选“复杂系统”。

## 让架构图承担论证

[三十幅架构图与离线 reader](../systems/architecture-atlas/README.md) 将每个项目分成全景、写入到使用、修订与控制三视图。节点、关系、区域和状态归属绑定 exact commit 的源码；静态观察、编辑推断和未读边界分别标识。图应当让读者检查一条论断经过了哪些状态和责任边界，而非仅为文字附一张泛化的 RAG 示意图。

新增样本带来四个可深化的论点：

- **保留什么本身就是选择。** [Aelios](../systems/source-studies/aelios.md) 的默认 Dream 排除工程主体、保留重大关系/亲密例外，体现一个具体产品目标；Relata 的 mixed-domain 用例则要求普通共享工作也能构成连续性。需要比较不同目标和入口，不能直接把前者判为通用 memory 失败。
- **理解有自己的更新周期。** [Hindsight](../systems/source-studies/hindsight.md) 的 observation 与 mental model、[OpenViking](../systems/source-studies/openviking.md) 的原文/摘要/向量、[A-MEM](../systems/source-studies/a-mem.md) 的 note metadata/embedding，都要求追踪派生状态。一次成功修改与后续所有影响一致，是不同主张。
- **“后台”不指向同一种保障。** OpenViking 的持久 QueueFS、Hindsight 的 operation worker、[LangMem](../systems/source-studies/langmem.md) 的进程内 executor、A-MEM 的同步演化，持久性与失败语义不同。不能将函数名 async/reflection 当成同一类学习机制。
- **memory 与 policy 的边界可用具体对象论证。** LangMem 的 prompt optimizer 返回可被应用采用的新 prompt；Hindsight 的 reflect 是只读，而 refresh 写派生文档。这些能与 AMS 的 experience-to-capability / experience-becomes-policy 问题连接，仍需分别验证使用和效果。

以上是跨报告的编辑推断，图和静态实现不建立 runtime 效果。

## 与 AMS 的连接

[Agent Memory Study](https://github.com/IndelibleVivi/agent-memory-study) 已经包含原文阅读、源码检查和研究实验；两个项目不按“论文 / 代码”机械分工。Relata 可以组织跨实现的综合问题，并把合适的案例问题带回这些来源。

- [旧经验，怎样继续帮助当前任务？](https://indeliblevivi.github.io/agent-memory-study/question/experience-to-capability/)连接 activation、经验适用条件和实际使用之间的区别。
- [经验怎样长成判断习惯？](https://indeliblevivi.github.io/agent-memory-study/question/experience-becomes-policy/)为案例、规则、参数等不同影响路径提供研究入口。
- [纠正后的保留范围](https://indeliblevivi.github.io/agent-memory-study/finding/correction-needs-retention-checks/)与[输出约束、参数更新和遗忘的区别](https://indeliblevivi.github.io/agent-memory-study/finding/output-guard-is-not-unlearning/)可以帮助提出修复与遗忘的对照；它们保留 AMS 的 `proposed-transfer` 状态，不能直接当作 Relata 已证明的系统结论。

具体引用仍回到 exact paper、code 和实验 artifact；保留 paper-reported、source-observed、synthetic experiment 与 editorial inference 的层次。此连接不合并 repo，不复制私有研究材料，也不自动接受 AMS 中的每项判断。

## 从综合研究到自己的运行装置

这组问题也为未来从空 repo 编写自有 memory 架构蓄力。[候选设计研究](own-memory-architecture.md)把保留、理解、修订与当前使用转为有替代方案的组件责任；[案例—测试映射](memory-design-test-map.md)说明具体能力、已有覆盖、反例和需要的证据。建设目标让研究有可实践的去向，但不会将文章收窄成自有系统宣传，也不把内部表示变成全领域的标准。候选若无法比简单历史／文件方案更好地完成既定目标，就应缩减或放弃。

## 下一次会推进认识的工作

利用首轮报告中的跨入口状态差异、来源与作用域反例，收敛文章的中心论点，并完成 source-fidelity review。需要正式进入 census 的项目再按 [System Card](../systems/system-card-template.zh-CN.md) 补齐 review；需要 runtime 证据的结论另行设计具体试验。文件/目录实现已纳入研究，但简单文件/全文搜索、完整历史基线与学习机制的对照仍是样本缺口，不能把十项目归纳写成全部 agent memory 的边界。

文章可以先贡献清晰的问题、机制比较和有限度的批评；不把未运行的试验写成结论，也不以 Case Lab 的完整 promotion gate 作为写作前提。
