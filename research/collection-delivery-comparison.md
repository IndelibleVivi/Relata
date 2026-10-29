# 从取回到用上：记忆系统在何处交出责任

**证据性质：authored-source synthesis。** 本文于 2026-10-29 对读 Relata 已有 source studies、Atlas models 与 exhibits，形成一份有界比较。它没有重新检查上游最新版本，没有新增上游执行、provider 请求或独立人类评审；文中的源码事实沿用固定版本研究的证据与未读范围。这里提出的是可被后续观察推翻的解释，不是系统排名或 accepted System Cards。

一条记忆已经被找到，却没有改变当前回答，问题可能发生在检索之后。时间字段仍在图中，应用只交出一句事实；方法已经存入 Store，agent 使用的 prompt 却没有更新；旧来源已经撤回，先前编译好的上下文仍在。把这些情况统一叫作“记忆没有用好”，会遮住最值得修理的地方。

本文主张：**记忆系统的比较必须同时说明它保留了什么、把什么交给下一层，以及哪一层实际承担当前判断。纠错与经验迁移也要沿同一条交接链观察。** 这个主张不要求所有系统实现完整 agent。库把一部分工作交给应用，可以是清楚且有价值的边界；研究的责任是把这份工作记入比较对象。

## 四个固定对象，四种交付边界

本文选取四个具名对象。它们分别提供可检索事实、时间化关系、派生综合和指令适应的可检查路径，不是覆盖所有 memory 系统的分类。

| 固定对象 | exact commit 与本仓库来源 | 本文使用的 Atlas 锚点 |
| --- | --- | --- |
| Mem0 Python OSS | `a39a802bbc93e85b820078cd3c4dbaf53af25dbe`；[原研究](../systems/source-studies/mem0.md)、[model 与 pinned sources](../systems/architecture-atlas/models/mem0.json) | flow：`select → results → use`；S8、S9、S16 |
| Graphiti OSS library | `16cdf7045378c8d53ae01f94e2fa60d238cb0f68`；[原研究](../systems/source-studies/graphiti.md)、[model 与 pinned sources](../systems/architecture-atlas/models/graphiti.json) | flow：`facts / filter / projection / generation`；S20、S22、S27、S29、S30 |
| Hindsight 默认 SQL 路径及所读可选集成 | `9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55`；[原研究](../systems/source-studies/hindsight.md)、[model 与 pinned sources](../systems/architecture-atlas/models/hindsight.json) | flow：`recall / reflect / integration / appmodel`；S14、S17、S29、S30 |
| LangMem library 与所读 prompt 路径 | `9d033b47d9ce53e37e92c92241b0496c0278932e`；[原研究](../systems/source-studies/langmem.md)、[model 与 pinned sources](../systems/architecture-atlas/models/langmem.json) | revision：`optimizer / promptout / stateful / promptstore`；S16—S21、S33 |

表内 source IDs 在各自 model 内解释，不能跨项目混用。model 的 source 表固定了上游 blob、commit 与行号；原研究保留覆盖、竞争解释和未验证范围。这些版本不能代表同名 hosted 产品，也不能因接口相近而替换为新版本。

比较采用 Atlas 的 [delivery](../systems/architecture-atlas/exhibits.md#delivery)、[revision](../systems/architecture-atlas/exhibits.md#revision) 与 [learning](../systems/architecture-atlas/exhibits.md#learning) 三个问题。它们的条件是编辑阅读视角，未产生任何新的系统输出。

## 找到、交付、消费，分别允许什么结论

retrieval 指选出候选；delivery 指把选中对象投影、裁剪或综合为下一层实际可见的材料；consumption 指 reader 或 agent 解释材料并形成当前回复或行动。三者可能在一个函数内，也可能跨库、应用和模型发生。这个区分用于定位证据，不是规定一个通用 API。

Mem0 的固定 Python OSS 路径按 scope 搜索条目。默认 hybrid 先取得 semantic 候选，再在池内加入 BM25 与 entity 分数；关键词命中不能把池外对象救回来。search 返回条目而非最终回答，所读版本的 `chat` 未实现。它的交付终点允许应用自行选择 reader、预算和动作策略。因此，检索返回正确条目，足以支持“这次被选到了”；它还不能支持“当前请求已经正确使用了这条历史”。应用只送正文、保留完整返回对象或重新写摘要，已经构成不同的 delivery 条件。[Mem0：检索、返回与应用责任](../systems/source-studies/mem0.md#检索与注入决定哪些理解能够参与当前任务)。

Graphiti 把另一种区别保存在对象里：事实边可以带 episode 来源以及事实有效时间和图处理时间。这个结构支持当前与历史问题使用不同过滤。但默认 `SearchFilters` 的时间条件为空，所读官方 agent 示例只拼接 `edge.fact`。由此不能推断 Graphiti 必然混淆历史：应用可以明确选时间，也可以保留完整字段；同样不能从图中有字段推断生成模型见到了它们。若当前任务错把旧约定当成新约定，应先检查搜索参数和实际投影，再判断 reader 是否误读。[Graphiti：时间与来源兑现的层次](../systems/source-studies/graphiti.md#时间冲突与来源兑现到哪一层)。

Hindsight 又将部分消费前移。`recall` 返回选择材料，`reflect` 使用只读 tools 进行有依据的综合；所读 LiteLLM callback 可在应用模型调用前注入 recall 或 reflect 内容。把 reflect 结果与另一个系统的原始条目交给同一 reader，并不只是比较存储：前者已经增加了一次推理，其模型与成本必须计入条件。callback 的接线是比“API 返回”更接近使用的证据，仍不是外部模型实际遵从或动作成功的证据。[Hindsight：写入、读取与应用](../systems/source-studies/hindsight.md#写入后台归纳读取与使用)。

这三种交付终点都可以有用。共同 reader 比较适合问“这些材料怎样支持同一种消费”；各自原生应用比较适合问“这个完整配置最终怎样完成任务”。两种问题不能共用未经说明的系统名称。更完整的 harness 会承担更多工作，也带来配置、调用、维护和归因成本；它不因职责更多便自动胜出。

## 纠正一处，后来的哪一次读取会改变

假设旧材料曾支持“周五散步”，后来这条安排不再成立。今天应停止邀约，回顾过去仍可解释当时的安排；若仅撤回一个未经认可的转述，还可能存在独立有效来源。三项任务需要不同的 probe evidence contract，不能由一个 delete 回执替代。

Mem0 的显式 update 可以替换文本和向量，delete 可以删除主条目并写入含旧文本的 history；默认 ADD-only 抽取并不取消这些入口。但近期消息缓冲、其他派生事实与应用副本不由单条删除一并撤回。保留审计历史有其价值，不能据此直接判“删除失败”；反过来，删除主向量也不能证明旧内容不再影响后来一次抽取或应用输出。[Mem0：更新、删除与派生影响](../systems/source-studies/mem0.md#来源角色时间与派生影响)。

Graphiti 的时间失效路径结合候选检索、LLM 判断与区间规则。它可以保留过去有效的事实，适合历史查询；默认不滤历史因此不单独构成缺陷。另一方面，所读 `remove_episode` 入口没有重算保留实体的摘要，也没有完整处理所有幸存来源连接。已有[离线分支观察](../systems/source-studies/observations/graphiti-observed.json)记录了删除首、次来源的不同请求；那是先给定候选与内存替身后触发的指定源码分支，本文没有重跑，更没有证明真实自然语言输入会走到同一分支。[Graphiti：更新与撤回](../systems/source-studies/graphiti.md#scope更新与撤回)。

Hindsight 提供了不能忽略的反例：并非所有派生层都缺少来源失效机制。事实编辑或来源删除可使相关 observations 失效，幸存事实重新等待归纳；自动管理的 mental models 有后续刷新路径。与此同时，手动模型由 owner 维护，刷新存在延迟和失败保留内容的分支。因此它反驳“派生理解必然无法纠正”的说法，也未证明“删除即刻使所有下游理解同步正确”。[Hindsight：派生状态与刷新边界](../systems/source-studies/hindsight.md#更正删除与派生状态)。

较精确的问题遂成为：旧影响经过哪些真实 read paths 进入后续使用，更新后它们分别何时改读新依据？在只使用当前事实条目的应用里，另造完整传播系统未必必要；在重复消费长期综合的应用里，只修事实却不观察综合层可能漏掉关键路径。传播范围应由真实使用决定，而不是由图画得多完整决定。

## 经验迁移增加了一种更远的交接

从经历形成新 note、持久综合或候选 prompt，都可能把一部分工作提前。Hindsight 的 observations 与 mental models 可以让跨事件理解被重复取用；但一次只读 reflect 不是持久学习。LangMem 的 optimizer 则可依据轨迹和 feedback 返回新 prompt，独立 stateful graph 可条件性保存；返回 `updated_prompts` 仍不代表宿主已启用它。[Hindsight 原研究](../systems/source-studies/hindsight.md)、[LangMem：procedural 路径](../systems/source-studies/langmem.md#5-procedural-memory改写指令是独立状态)。

这里的核心风险是适用判断被提前固定。过去三次访谈比较适合去重归纳，下一次访谈可能要求逐字保留。同为“访谈”不能替代当前目的。若修复办法是全面停用，下一次真正需要比较时又可能失去帮助。Atlas learning 展品及[经验适应研究](experience-adaptation-study.md)把例外、修订后有效邻居和无关简单任务留在同一阅读序列中。它们是作者材料，未证明上述系统实际迁移成功或失败。

也存在足够简单的竞争解释：当前要求已经清楚，原 prompt 或原文 reader 便能完成；短方法可能只是重复当前指令。只有看到候选的产生、保存、启用和新任务表现，才能分别讨论 formation 与 consumption。若两者之间没有启用证据，把行为不变归因为“方法无效”便跨过了尚未检查的交接。

## 对未来系统的三个可判错认识

第一，**返回字段的保存只有在任务需要的区别仍在上游对象里时，才可能修复 delivery 损失。** 可在同一检索结果上对照正文投影与完整投影，另保持顺序、预算和 reader 条件。如果完整字段无相关区别、或字段已经完整送达仍持续错误，就应把解释转向 formation、选择或 consumption，不能继续归咎于 adapter。这个认识不预言完整投影必然更好；冗余和预算挤占也可能使它更差。

第二，**纠错应观察实际再次读取的层，而不以最早 mutation 的成功代替收敛。** 可分别记录来源、live 对象、派生理解、实际上下文与最终行为的时间顺序。如果简洁的重新取证已可靠完成当前任务，额外多层传播的必要性便受到反证；若派生层在原生保护下已及时收敛，也应撤回“必须补上新机制”的设计要求。

第三，**适应的收益必须经得住局部例外和有效邻居同时出现。** 应将原 prompt、可搜索旧经验、短人工规则和候选方法置于可比较条件，保留当前指令足够的控制。如果复杂机制没有更少的重复工作、没有更好的使用，或者更容易损害有效邻居，未来系统应缩小它的职责，而不是只增加反思次数。

这些认识给 Tilia 等未来设计提供问题，不授予任何架构实现权。现有材料没有端到端中文使用、真实权限配置、长期交互、独立评审、延迟成本或反应性回写的比较数据。参数学习与强原文／全文搜索基线也尚未形成完整样本覆盖。当前能够交出的作品是一条清楚的阅读路径：从固定来源追到交付对象，再问它怎样影响当前判断；下一轮研究应允许任何一层的新证据改变这条解释。
