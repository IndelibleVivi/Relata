# 经验怎样形成可用方法：组织、综合与后续行动

**状态：** bounded source-based comparative study / authored development worksheets；2026-10-26。源码事实、编辑推断和原创合成情境在下文分别标明。没有运行 system under study、调用 provider、独立人类评审或接受新 case。

## 中文摘要

经验可以使旧材料更容易找到、使跨事件理解被重复取用，也可以改变下一次工作的指令。这三种改变把工作移到了不同时间和不同组件，不能用“发生了学习”一并概括。本研究沿固定版本的 A-MEM、Hindsight 和 LangMem，比较它们改变的对象、进入后续任务的入口与尚未承担的判断；再用访谈整理与共同创作两条作者化时间线，展开适用、例外、反馈修订与保留能力。由源码和材料可以支持的判断是：**适应机制的价值取决于它替后续使用承担了哪部分工作，以及为此失去了哪些可改变的选择。** 预先形成的方法可以省去重复整理，也会把先前情境的判断带入新任务。收益、自动形成范围与长期共同使用仍须分别观察，简单原文、短方法和无历史方案都能推翻复杂机制的优势解释。

## English summary

This bounded study compares three different changes at pinned source revisions: A-MEM reorganizes notes and their retrieval paths; Hindsight maintains derived observations and mental models while keeping reflect read-only; LangMem can return or separately store revised prompts whose adoption belongs to the application. These changes move work across time and component boundaries. They do not establish a shared learning outcome. Two original adult synthetic worksheets trace method formation, application, exceptions, revision and retained abilities. Their histories, feedback and candidate methods are authored, not system outputs or independent evaluation data. The study identifies conditional opportunities for reusable understanding and lower repeated effort, alongside premature generalization and maintenance costs. Raw-history, search, short-method, original-prompt and no-history controls remain capable of defeating the proposed benefit. No new execution envelope, accepted rubric, ranking or Tilia architecture is introduced.

## 经验的价值，可能发生在再次提问之前

一个 agent 做完三次访谈比较后，留下一条“下次先列原话、来源和解释”的方法。第四次，新的材料确实更快进入了可核对的结构。这里有几种可能：它检索到了前次范例；它读到一份已经整理好的方法；它的工作指令已经改变；或者当前要求本来就足够清楚，没有历史也会完成。看见一份正确的表格，不能判断哪条解释成立。

但把这些差异只写成“尚未证明学习”，也会漏掉值得研究的正面机制。一个重复发生的整理步骤若能在事后完成，下一次就不必从头重建。短综合可以降低寻找分散经历的负担；有条件的方法可以把解释变成下一次的准备；合适的链接可以让后来发生的事情改变旧材料的可读关系。问题是这些准备会留下什么，怎样进入下一次任务，以及谁还要判断这次是否适用。

本研究提出一个有条件的解释：**适应把部分工作提前，也提前作出了一部分选择。** 原文方案将较多解释留到使用时；派生综合在此前合并材料；指令改写更进一步，为后续行为设置默认倾向。提前处理可能有帮助，也可能把后来才显露的用途差异压掉。这不是三系统的能力排序，而是从它们的实际对象与写入、读取路径提出的比较问题。

本研究与 [continuity benefit study](continuity-benefit-study.md) 共享 necessity／benefit 的区分：历史不是唯一合法答案的来源，也仍可能减少重复解释或支持持续工作。这里新增的对象是**多次经历形成方法、方法在后来情境中被采用或停用的过程**，不是重新定义所有 memory。

## 三条真实路径，把工作放在不同位置

采样沿用现有 [learning exhibit](../systems/architecture-atlas/index.html#exhibit/learning/understand) 的三个实现。它们有可核查的不同变化对象，不构成穷尽分类；本研究没有覆盖参数学习、所有 memory 产品或这些项目的最新版本。完整边界与旧研究覆盖见 [A-MEM](../systems/source-studies/a-mem.md)、[Hindsight](../systems/source-studies/hindsight.md)、[LangMem](../systems/source-studies/langmem.md)。

| 固定实现 | 这条路径真正改变什么 | 怎样进入后续使用 | 仍由别处承担的判断 |
| --- | --- | --- | --- |
| A-MEM `0c8039f`，robust 路径 | 新 note 的 links；被选旧 note 的 context／tags；到相应时点重建的检索索引 | 向量选择 seed，读取当前 note，单跳展开 links；QA 消费返回材料 | 哪种关系值得保留，选中经历是否适用，回答如何采用 |
| Hindsight `9c7f6c6` | facts 支持的 observations；可刷新的 mental model 内容及相应状态 | recall／reflect 取用事实、综合或模型；具体应用消费返回结果 | 综合是否正确、范围是否合适、何时触发、怎样用于行动 |
| LangMem `9d033b4` | optimizer 返回的候选 prompt；独立 stateful graph 可条件性覆盖 Store 中 prompt | 调用方须保存／选择并接入实际 agent；该 agent 再处理新任务 | 候选是否应启用、在哪些任务启用、怎样判断收益与回退 |

这张表是源码路径的编辑比较，不能用来宣称它们实际减少了多少步骤、学会了什么或谁更可靠。下文按路径给出相应固定源码，完整锚点见文末。

### A-MEM：组织变了，不等于每条选择路径都变了

`process_memory` 可以修改邻居的 context／tags，也可给新 note 建 links；旧 content 仍在。随后检索先用向量选择位置，再读取当前对象及单跳 links。因此组织变化有两种不同的进入机会：影响以后被选中的对象，或改变已选中对象交给 reader 的材料。[A5][A5] [A6][A6]

这里有一个比“演化不等于学习”更具体的区别。修改旧 metadata 的路径不同时重算旧向量；`consolidate_memories` 才从当前 notes 重建 retriever。**在重建之前，旧向量可以仍影响选择，新 metadata 却已经影响返回文本。** 因而“索引没刷新，所以演化完全没有进入使用”与“metadata 已改，所以检索已改善”都过强。真正的观察要分开选中集合与返回内容。[A4][A4] [A5][A5] [A7][A7]

若后来的逐字稿经验使旧访谈 note 的 context 增加用途条件，它可能帮助 reader 辨认例外；若新的描述抹平了原先差异，也可能误导。保留 content 给核查留下机会，但是否回看、是否正确识别用途仍非这条写路径的保证。上述帮助与损害是条件推演，未测实际排名或回答。

### Hindsight：把综合留住，与临时作一次推理不同

consolidation 形成与来源 facts 关联的 observations；mental model 则提供可持久刷新的综合对象。`reflect` 自身是只读查询与推理，不能把一次返回文字写成系统已经形成了新的长期理解。refresh 调用相关推理并在成功路径写回，才是另一个状态变化。[H11][H11] [H17][H17] [H18][H18] [H19][H19]

持久综合的条件价值是：对于反复出现的“我们怎样整理比较稿”，应用有机会重复取用整理好的理解，而不必每次重新拼三次经历。与此同时，更新周期使“已知一条例外”与“当前综合已体现例外”成为两个问题。不能只查看原事实或一次 refresh 的完成标志，就推定下一次使用必定受益。

这条研究不能省略源码中的反证。refresh 排除自身 ID，区分 full／delta，使用 snapshot cutoff／可见 watermark；若干空结果、未应用更新或错误分支会保留旧内容，成功后再更新 mental model，并有相应 embedding 和可配置 history 路径。[H18][H18] [H19][H19] [H20][H20] 因此不能写成“毫无循环或失败保护”。这些保护支持的是特定实现条件，不是综合语义正确、全部间接依赖无循环或长期收益。保留旧内容同时保护可用性并可能延长旧理解的使用期；哪一面主导，要看当时任务和实际状态。

### LangMem：方法变成指令后，采用成为独立责任

prompt optimizers 可以将轨迹、feedback 和原 prompt 转成候选指令；gradient 路径也会在无轨迹或无需更新的分支返回原 prompt。多 prompt 路径可选择模块并保留未选模块。这些都不意味着每次反思必然修改，更不是模型权重训练。[L16][L16] [L17][L17] [L18][L18] [L20][L20]

独立 stateful graph 读取 Store 中的 prompt，仅在模型给出 update 条件时保存；部署 wrapper 返回 `updated_prompts`，所读函数不负责把它启用到 agent。[L21][L21] [L33][L33] 这不是缺少一种理所当然的产品功能：可组合库允许应用决定采用策略。它对比较的要求是，必须把承担这份责任的应用算进边界。

指令适应有机会避免每个任务先检索一段经验、再重建一次方法。但它也可能让本来局部的经验持续占据后续任务的行为入口。一个“所有访谈都压成表”的候选即使保留了模板变量、写入了 Store，仍会在逐字稿任务中出错。反过来，正确候选没有被应用启用时，后续不变也不能直接归因为候选无效。**产生、保存、采用和受益必须各有相应证据；其中任何一项都不能由另一项代签。**

## Worksheet A：同样是访谈，方法为什么应当改变

完整作者材料由 [`exhibits.json`](../systems/architecture-atlas/exhibits.json) 的 `learning.episodes` 与各 condition 的 `workedExample` 唯一维护。可直接在 [交互版](../systems/architecture-atlas/index.html#exhibit/learning/understand) 或 [同源 Markdown 版](../systems/architecture-atlas/exhibits.md#learning) 阅读当时可见经历、当前任务、候选方法、多种允许做法与误判。这里解释其推理，不复制第二份逐字历史。

林澄与 agent 连续完成三次社区刊物的访谈比较：先把说话者分开，再保留同一人的时间条件，最后避免给未解释的行为补理由。“原话／来源／解释”的表有一个可理解的用途：把原话与编辑推断分开，帮助核查。第三次的设定只认可比较稿中使用它，没有约定以后所有访谈采用同一格式。

| 阅读时点 | 作者改变的条件 | 有根据的判断 | 不能借此证明什么 |
| --- | --- | --- | --- |
| [形成方法](../systems/architecture-atlas/index.html#exhibit/learning/understand) | 三次经历都属于比较稿 | 可以提出带用途条件的方法，也可以先保留原文 | 重复三次就足以发现通用规律 |
| [用于新材料](../systems/architecture-atlas/index.html#exhibit/learning/act) | 新受访者，仍需比较 | 方法可帮助组织；具体动机必须来自新原话 | 表格正确就证明历史是必要的或已有迁移收益 |
| [局部例外](../systems/architecture-atlas/index.html#exhibit/learning/exception) | 用途变为核对逐字稿 | 保留停顿、重复和顺序，不能用表替代 | 拒绝这次采用就等于忘记或原机制无价值 |
| [反馈后再使用](../systems/architecture-atlas/index.html#exhibit/learning/repair) | 纠正“所有”，后来再次做比较稿 | 保留比较方法，修订适用范围；同时再查逐字稿条件 | 只修好一个样本就保住了全部旧能力 |
| [无关任务](../systems/architecture-atlas/index.html#exhibit/learning/retain) | 当前只需数字排序 | 直接完成，不展示历史、不强制方法 | 一个简单不干扰对照代表全面能力保持 |

这个序列将**同类材料**与**同种任务**拆开：原文都是访谈，目标却可能是比较、逐字核对或与访谈无关。它给“适用范围”以可辨认内容，不只是给条目增加一个 `scope` 字段。若未来实验直接把“比较／逐字”真值标签交给方法形成者，最难的自然语言识别已经被作者代做；那只能测试给定表示下的后续环节。

五个时点属于同一个作者化 family。林澄的反馈、错误续写、M0／M1／M2 都由作者设定；不是已观察的使用改善。尤其 M1、M2 是解释用候选，不能把它们喂给系统后再声称系统自己从经历发现了方法。当前指令明确的时点允许无历史方案完成，合法澄清也不被人为移出答案域。它们研究的首先是帮助、误泛化和不干扰，不通过现有 Memory Necessity Gate。

## Worksheet B：共同创作中，熟悉做法可以保留而不总被采用

这一条材料原生维护在本节。所有人物均为原创合成成年人；它是第二个作者化情境，未被接入 subject、exporter 或评审工具。它借用 CB-005 的局部例外原则，但改变了任务机制：过去形成的是共同创作方法，而非称呼使用范围。它不是第二个独立验证的 incident，也不代表长期关系的整体质量。

**可见经历。**

1. 许遥第一次与 agent 写一个渡口场景时说：“先给三个不同走向，我想比较后再选；没选的别写进已经发生的故事。”她选了雨夜误船，其余方案保留为草案。
2. 第二次需要设计山间旅馆的开场，她又要求先比较不同走向；选定“陌生人留下地图”，未采用“旅馆停电”。这次也明确区分已选故事和候选。
3. 第三次，她说：“我们卡在要往哪里写时，三条分支很好用。不过别把这当成每次续写都要经过的仪式。”

**形成方法的时点。** 当前任务是“把我们目前写作时有用的办法留一下”。作者提出的候选 W1 是：“方向未定时先给少量不同分支；一旦选定，继续既定故事，不把未选候选写成历史。”一种合法做法是保存 W1 并保留选择记录；另一种是保留可检索原稿，遇到需要时再归纳。直接把候选写成“每轮先给三个分支”是与第三次经历冲突的过度概括。

**实际适用的时点。** 许遥开始另一篇故事：“这次写海边小站，我还没决定人物为什么留下，先看看不同方向。”W1 在此有明确适用机会。可以提出几个不同动机，并等她选择；新人物动机仍是当前创作，不能抄成旧故事里陌生人的既定动机。此时 no-history reader 同样可完成，历史的潜在作用是少重讲协作办法，而不是独占合法答案。

**不适用的时点。** 随后她选择“留下修好坏钟”，并说：“就沿这个继续一小段，先别停下来问我下一步。”此时合适的动作是沿已选方向续写；再次列三个替代方案会打断当前推进。也不能把“不要此刻问”泛化为永远取消共同选择。熟悉的协作方法有价值，当前不采用其中一个步骤也有价值。

**反馈与保留。** 作者故意设定 agent 又给了分支，许遥回应：“我只是在方向没定时要比较。已经选好了就写；以后我说想比较时，你还是可以给不同方案。”候选 W2 可以把这个条件写得更清楚。接下来的成对检查应同时包含“继续坏钟场景”和“另一个故事还未选方向”；只有前者会把永久取消分支误判为修复成功，只有后者又看不到过度提问的负担。若改写的新指令把未选的“旅馆停电”带成已发生情节，则出现另一个保留／来源问题，不能用流畅续写抵销。

**含混与普通生活控制。** 若她后来只说“再看看”，且局部上下文不足以判断是重看当前稿还是探索其他方向，可以作简短澄清；作者不要求系统猜中隐含意图。再给一个与创作无关的完整当前任务：“帮我把明天要带的雨伞和充电线列成清单。”直接列两项即可，不应为了体现连续性而回顾故事，也不该引入未请求的三分支。它检查一个普通生活用途中的不干扰条件，不要求日常事件承载浪漫象征。

这条情境把**持续协作的顺畅**与**记忆的显式展示**分开。即使长期共同工作确实减少了解释负担，这个收益也不能由话语温暖、token 更少或作者设置的反馈自动建立。真实时间、感受和关系中的意义需要自己的观察与研究授权。

## 能够推翻优势解释的比较，怎样设计才不偷换工作

以下是候选研究设计，不是已执行的协议，也不激活新的 runner 或 study。

先分开两个问题。**给定同一个方法，系统是否正确消费它？** 可以比较原 prompt、带方法 prompt、检索到的方法或原始经历，检查当时真正交付的材料与后续行为。**系统能否从经历形成合适的方法？** 则必须将作者答案和适用标签留在外面，观察候选如何产生，再使用独立设计的新任务。消费给定 M2 的成功不能同时回答第二个问题。

| 比较项 | 保持哪些共同条件 | 允许它推翻什么 |
| --- | --- | --- |
| 当前任务／无历史 | 同一 reader 与当前指令；历史确不必要的时点照常保留 | “任何正确结果都由记忆带来” |
| 完整历史 | 同一组原文；说明暴露预算、截断与顺序 | “必须先压成方法才能完成” |
| 原文搜索 | 相同可访问历史；记录 query、窗口与实际交付内容 | “复杂组织才有能力找到这段经验” |
| 作者短方法 | 明标人为给定，不能含新问题的答案；计入制作来源 | “重复综合本身值得持续支出”，但不能证明自动形成 |
| 原 prompt／候选 prompt | 同模型、任务、工具与明确启用的版本；保留未改任务 | “返回一个新 prompt 就已有正向适应” |
| 机制的局部消融 | 在已接受的具体边界内分别固定候选或交付内容 | 定位某条路径的作用；不能把诊断补救自动当无偏因果分解 |

原文较长与方法较短会改变实际暴露量。可以同时问现实配置下的端到端使用效果和受控暴露下的机制问题，但不能只裁掉原文的一部分，就宣称它是强完整历史对照。原文加方法也不是自动更强：重复、冲突和上下文占用会改变 reader 的工作。上述问题沿用 [已有 Mem0 比较](../systems/source-studies/mem0.md) 与 [future-question study](future-question-memory/README.md) 的边界，不能把保留充分性直接提升为使用效果。

结果至少分开记录：候选是否形成；是否持久；实际启用／交付了什么；合适任务是否推进；不适用时是否停止；原能力是否保留；是否存在合法未决或技术失败。技术失败不能当作语义零分，未采用也不能与采用后无效合并。反馈和时点共享同一 history，不按独立样本计算。

成本也需要看全：首次整理、持续刷新／重编码、在线检索与推理、版本维护、错误修复以及人的重复解释。对于相似任务频繁出现、方法较稳定的场景，提前整理有机会摊薄每次重建的负担；任务变化快、应用次数少或误泛化昂贵时，原文和按需理解可能更划算。这是条件判断，没有给它编造一个已测的盈亏阈值，也不把人的解释劳动折算成 token 分数。

## 与 AMS 的分工：承接已有区别，追到具体实现

本次读取了 AMS 的 [旧经验，怎样继续帮助当前任务？](https://indeliblevivi.github.io/agent-memory-study/question/experience-to-capability/) 与 [经验怎样长成判断习惯？](https://indeliblevivi.github.io/agent-memory-study/question/experience-becomes-policy/) 的公开专题正文。两页均为开放问题／跨源编者论述：前者把候选竞争、范围识别和下游帮助分开；后者结合其报告的受控研究讨论给定特征与局部更正后的保留问题。本次未打开所有底层研究原始材料或重新运行实验，因此这些报告保留 AMS 自己的证据状态。

Relata 从这里承接的是研究约束：不能让人工给定表示提前替系统完成关键识别；纠正时同时检查应改和应保留；允许简单案例、原方法和 no-memory 加总成本推翻复杂方案。这里新交付的是三条 pinned 实现中这些问题具体落在哪里，以及两条可以逐段质疑的协作时间线。它不复制一个学习实验来证明相同区别，也不用 AMS 的结构化结果填补本研究的自然语言和长期使用证据。

## 三项职能各自留下的东西

**Benchmark research** 获得了两条有明确适用／例外／修订／保留条件的开发材料，以及“形成方法”与“消费给定方法”的区分。下一步语义 review 要检查合法行动域是否被作者写窄、局部上下文是否已经泄漏答案、独立任务是否真正独立；本研究没有接受 rubric、case 或评分合同。

**System collection** 获得了可以直接阅读的比较论证与五个展开时点。读者能从当前情境进入三系统的选择、综合或指令路径，再返回原条件；原三十幅图仍由模型唯一维护，没有另画一套不同的系统拓扑。新材料说明哪些边界值得看，也保留已有 safeguard 与当前未读部分。

**Incubator** 获得的是可以支持或反对设计的条件：高复用、相对稳定的共同工作可能值得持久综合；更直接的指令采用也意味着更广的干扰面；保留原文能提供复查机会，却不能代替应用判断。应按真实用途比较组织、综合、指令及简单方案，不把它们装成预设的统一流水线，不将 candidate B 提升为答案。独立 Tilia 的语义检索要求、产品体验和架构选择保持自己的边界。

目前可成立的成果是这个有界解释和可检查材料；自动范围识别、新任务收益、长期共同演化与维护成本仍是开放的经验问题。

## 源码核对、作者材料与未覆盖范围

本次定点复核了三个现有 pin 的公开源码：A-MEM 的 `add_note`／`consolidate_memories`、`process_memory`、raw retrieval 与 SimpleEmbeddingRetriever；Hindsight 的相关 consolidation action、只读 reflect、mental model refresh／持久化与若干失败保护；LangMem 的 optimizer dispatch、prompt-memory、gradient 关键分支、multi-prompt、stateful graph 和部署 wrapper。没有重新审计三仓全部源码、所有异常／并发／依赖、完整 QA harness、LangMem metaprompt 内部、论文结果或真实部署。

源码核对通过公开网页内容完成。网页抽取的归一化行号与 GitHub 物理行号不同，故保留既有模型的 exact commit／GitHub anchors，并用函数和语句核对；没有将抽取器行号替换为新的来源锚点。本文的实现结论是静态 source observation，其运行保障与效果未被本次验证。AMS 仅阅读上述专题正文，不把其链接到的全部材料标为已读。

Worksheet A 的原文／候选由 `exhibits.json` 维护并投影为 HTML 和 Markdown；Worksheet B 的原文／候选由本文维护。两者是完全原创合成、成人、作者知道未来问题及分析的 development materials。A 的五个阅读条件与 B 的多个时点不构成独立验证样本；没有 held-out、真实人类 feedback 或社区 incident 主张。材料没有进入 RC-005／P0／future-question 执行包，也没有新增 provider、外部评审、hosting 或结果发表权限。

## 固定来源

- A-MEM： [A4 写入与重建][A4] · [A5 选择与返回][A5] · [A6 metadata 演化][A6] · [A7 embedding 检索][A7]。
- Hindsight： [H11 consolidation][H11] · [H17 reflect][H17] · [H18 refresh][H18] · [H19 保留／持久化][H19] · [H20 更新与 history][H20]。
- LangMem： [L16 dispatch][L16] · [L17 prompt memory][L17] · [L18 gradient][L18] · [L20 multi-prompt][L20] · [L21 stateful][L21] · [L33 wrapper][L33]。

[A4]: https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer_robust.py#L352-L409
[A5]: https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer_robust.py#L411-L459
[A6]: https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer_robust.py#L463-L540
[A7]: https://github.com/WujiangXu/A-mem/blob/0c8039f28fdcc08189a23c07a3437d9d2482f9c2/memory_layer.py#L554-L610
[H11]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L2166-L2345
[H17]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L15004-L15135
[H18]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L17129-L17335
[H19]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L18010-L18208
[H20]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L18300-L18480
[L16]: https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/prompts/optimization.py#L260-L268
[L17]: https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/prompts/stateless.py#L149-L243
[L18]: https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/prompts/gradient.py#L318-L360
[L20]: https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/prompts/optimization.py#L375-L456
[L21]: https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/prompts/stateful.py#L16-L54
[L33]: https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/graphs/prompts.py#L23-L67
