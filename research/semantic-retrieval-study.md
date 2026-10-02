# 强语义 raw-source 基线：encoder 选择与中文检索对照（proposed）

**Status:** proposed research study；2026-10-03。不是 accepted architecture、encoder 排名、执行授权或系统能力结果。
**Decision target:** 为未来独立 Tilia 的强语义原文基线，确定值得比较的 encoder 路线、能暴露信息损失的开发表例，以及公平比较所需的配置记录。
**Authority:** [STATUS](../STATUS.md)、[CHARTER](../CHARTER.md) 与 accepted decisions。向量语义检索是既定预期要求；encoder 与实现仍开放。本文不改 [RC-005 → Mem0 执行包](../experiments/rc005-native-execution-packet.md)，也不接受[候选 B](own-memory-architecture.md)。
**Evidence:** 官方文档事实标 `SOURCE-CLAIMED`；比较建议与用例解释为 `INFERRED` / `proposed`。没有调用模型或 embedding、下载权重、安装 runtime 或运行检索实验。

## 中文摘要

本文比较三条有实际差异的候选：现有 API encoder `text-embedding-3-large`、小尺寸开放权重 `Qwen/Qwen3-Embedding-0.6B`、支持多种检索表示的 `BAAI/bge-m3`。官方资料能确定表示维度、输入长度、instruction 与部分 wrapper 默认值，不能确定它们在 Relata 中文/code-switch 材料上的优劣。六组完整短文本分别检查改述、精确 ID、撤回、说话者、scope 与旧稿干扰；它们是开发表例，不是六个独立 case families 或已经执行的长历史测试。核心判断是：相似度不独自建立 authority，但保留原始证据的简单 reader 也可能正确处理它；不能借此预先要求某种状态内核。建议把 encoder 对照与 hybrid 增量分开，并分别观察候选、context 与最终使用。

## English summary

This proposed study compares three candidate routes: the existing hosted `text-embedding-3-large`, the small open-weight `Qwen/Qwen3-Embedding-0.6B`, and `BAAI/bge-m3` with multiple retrieval representations. Official documentation supports configuration facts, not performance on Relata's Chinese/code-switch material. Six complete short development items cover paraphrase, exact identifiers, retraction, speakers, scope and stale drafts; they are neither independent case families nor an executed long-history test. Similarity alone does not establish authority, but a simple reader with intact source evidence may resolve it without a dedicated state kernel. Encoder comparisons and hybrid additions should remain separate, with retrieval, context exposure and response use observed independently.

## 1. 什么值得比较

[首轮计划 §9](first-research-cycle.md) 已提出强语义 raw-source A、字面控制与可修订派生视图 B。本文展开其中的 encoder / rerank / selection 问题，而不把 A 故意做弱来证明 B。

| 路径 | 可利用的信号 | 值得检验的收益 | 尚未证明的风险 |
|---|---|---|---|
| 字面 / lexical | 词项、字符片段、精确标识符；具体取决于 tokenizer 与搜索规则 | ID、文件名和罕见名称可直接定位 | 改述或跨语言查询可能漏掉相关材料；中文分词会影响结果 |
| dense vector | encoder 对完整输入形成的表示 | 可在词面差异较大时找回相关来源 | 相似项目、否定、角色方向或近似编号可能混淆；不能预言哪条必败 |
| hybrid | 两路独立候选的合并/融合，或模型自带的 dense+sparse 等表示 | 补足单路候选覆盖 | 候选预算、融合和额外 reranker 都可能成为混杂因素 |

这里的 hybrid 必须记录两路候选如何产生。如果先截断为一个 semantic pool，再给池内条目加 keyword 权重，词项路无法救回池外来源；这与独立 lexical+dense 候选的融合不同。该区别可见于既有 [Mem0 source study](../systems/source-studies/mem0.md)，不等于已测出任一方案更好。

**相似度与 authority 的边界。** 来源身份、修订和权限需要有可用证据，分数本身不授予许可。但证据可以保留在原始对话里，供 reader 判断；也可以由 metadata、调用方过滤、可修订视图或其他机制处理。没有证据证明专用状态层是必要条件。只有一个投影把关键区别彻底擦除，使两世界的后续全部可用输入相同，才形成信息缺失层面的不可区分；这不等于所有向量表示都必然擦除它。

## 2. 三条候选路线与已核实范围

**公开资料查阅日：2026-10-03。** 已读 OpenAI embeddings guide 的模型表、维度与 FAQ；Qwen model card 的 overview、instruction 与 Transformers 示例；BGE-M3 model card 的规格、FAQ 与 usage；BGE `M3Embedder` 参数文档。未读相关论文全文、完整训练资料或 inference 源码，未复现 model card 的榜单。下列是文档层事实，不是安装或调用结果。

| 对象与 primary source | 表示与文档长度 | 输入处理与归一化 | 部署与适用研究问题 |
|---|---|---|---|
| [`text-embedding-3-large`](https://developers.openai.com/api/docs/guides/embeddings) | 默认 3072 维；支持 `dimensions` 缩减；指南模型表列 max input 8192 | 指南返回向量为单位长度；所读检索示例直接编码文本，未规定 Qwen 式 query instruction | hosted API；与现有首包的 shared encoder 衔接。本文不把品牌/型号当作固定后端权重版本 |
| [`Qwen/Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 0.6B；model card 列 32K context、32–1024 输出维度 | 建议 query 带任务 instruction，文档侧不加；Transformers 示例做 L2 normalization | 开放权重，本地推理候选；card 声明 100+ 语言与 code retrieval，标 Apache-2.0。这些声明不证明本项目效果 |
| [`BAAI/bge-m3`](https://huggingface.co/BAAI/bge-m3) | dense 为 1024 维；最大 8192 tokens；支持 dense、sparse、multi-vector | card 明确 query 无需额外 instruction；具体 wrapper 归一化见下文 | 开放权重，本地推理候选；card 声明 100+ 语言，标 MIT。自带 sparse 不等于外接 BM25 |

**模型长度与实际输入不是一回事。** Qwen card 的 Transformers 示例设置 `max_length=8192`，低于其标称 32K；不能把抄示例的运行当成 32K 覆盖。BGE 当前 [`M3Embedder` 参数文档](https://bge-model.com/API/inference/embedder/encoder_only/M3Embedder.html)列 `normalize_embeddings=True`，但 query/passage 默认长度均为 512，dense 默认返回，sparse/ColBERT 默认不返回。实际 wrapper/version、显式参数、截断位置和返回表示必须留存；model card 的能力不会自动变成一次调用的配置。

**中文与费用仍有界。** “多语言”声明不能代替中文否定、角色归属或 code-switch 结果。本地两条路线尚无本机峰值内存、速度、下载体积或离线可用性观察；不据参数量直接推导机器可跑。API token 费用需与全量重编码、query、重试分别核算。既有执行包记录 2026-09-28 的 $0.13 / 百万 input tokens；本轮模型价格页完整抓取失败，未重新确认现行价，不将历史价当报价。没有为这些候选批准实验预算，也未执行这些候选的模型或 embedding 调用。

**仍须固定的对象。** 两个 Hugging Face model ID 已确定，但本研究只绑定上面查阅日的 model card，尚未锁定用于执行的权重 revision、tokenizer 与 wrapper 版本。后续实验应固定它们；API 无法从所读资料恢复可检查的权重 commit，则记录返回 model ID、维度、日期及服务边界，并保留无法固定的部分，不能编造 snapshot。这里记录的许可标签也不构成 Relata 自身的 license 选择。

## 3. 六组可 dry-review 的开发材料

全部角色为虚构成年人。以下原文、query 与控制定义完整，但没有 system output。G3/G4/G5/G6 借用现有 RC-001/003/004/005 的研究问题，不增加独立 family 计数。代码块里的事件文本可供候选输入；块外的 expected region 只给 reviewer，不能当作系统输入。原文直接 code-switch，不额外附带泄露答案的双语摘要。

### G1 改述：保留意义但减少词面线索

```text
scope: Lantern
E1 2026-08-14 human: 本轮把文档打包成可断网携带的副本先做完；cloud sync 留到以后。
E2 2026-08-14 human: 图标颜色先维持原样，不进入本轮开发。
Q-zh: Lantern 这轮最优先实现什么？
Q-en: What is the next development priority for Lantern?
```

- **Relevant:** E1 的离线可携带副本；E2 提供未纳入事项。
- **Prohibited use:** 把 cloud sync 或图标配色当本轮首要工作；编造交付日期。
- **Ambiguous:** “文档打包”是否等于某个具体 export 格式，原文未规定；允许概括，不要求猜格式。
- **对照意义:** 两条 query 对同一原文改变语言/改述，保持 scope。词面重叠是否足够依赖 tokenizer，未计算 BM25 分数；只能假设 dense 可能补召回，不能预判 lexical 必败。

### G2 精确 ID：查询本身携带可定位的键

```text
scope: Lantern
E1 human: build-2026-08-14-rc2 的配置是 configs/export-manifest.yaml，校验标记 cedar-17。
E2 human: build-2026-08-14-rc3 的配置是 configs/export-manifest-next.yaml，校验标记 cedar-71。
Q: 查 build-2026-08-14-rc2：给我 config path 和 validation marker。
Q-control: 查 build-2026-08-14-rc3：给我 config path 和 validation marker。
```

- **Relevant:** Q 对应 E1；Q-control 对应 E2，要求路径与标记逐字正确。
- **Prohibited use:** 混配 rc2/rc3、cedar-17/cedar-71，或补出不存在的值。
- **Ambiguous:** 若输入投影删掉 build ID，就不能按同一证据完整性条件比较；应另列为信息损失诊断。
- **对照意义:** 与只问“配置在哪”不同，当前 query 含精确键，因而能检查 lexical 的定位作用，同时观察 dense 是否保存相邻编号差别。命中与最终复制准确率分开记录。

### G3 否定与撤回：旧证据仍可作为历史

```text
scope: Poster
E1 D1 human: 正式版先用圆体，字号 18。
E2 D1 companion: 确认这个排版决定。
E3 D2 human: 更正：正式版不用圆体了，改宋体；字号仍是 18。
Q: 正式版现在用什么字体和字号？回答当前决定。
Q-history: 改宋体之前的字体决定是什么？
```

- **Relevant:** Q 需要 E3，字号有 E1/E3；Q-history 需要 E1 与修订先后。
- **Prohibited use:** 当前答案采用圆体，或把字体更正扩成字号也失效。
- **Ambiguous:** 历史 query 中正确提到圆体不是撤回失败；两种用途必须分开。
- **对照意义:** 检查旧新来源是否被找到、reader 是否按当前任务使用。把完整原文交给同一 reader 就可能答对；不预设必须由专用 revision 结构先滤掉旧值。

### G4 角色归属：比较投影丢失与完整输入

```text
scope: Sound-card; actors: human 叶遥, companion 砚舟
World A:
E1 speaker=叶遥: 封面弯线由我提出。
E2 speaker=砚舟: 声音里的三下轻敲由我提出。
World B:
E1 speaker=砚舟: 封面弯线由我提出。
E2 speaker=叶遥: 声音里的三下轻敲由我提出。
Q (both): 谁提出封面弯线？谁提出三下轻敲？
```

- **Relevant:** A 的弯线/轻敲分别归叶遥/砚舟，B 相反；这只是提出者，不是已完成制作。
- **Prohibited use:** 颠倒归属，或从“提出”推断“已制作”。
- **Ambiguous:** 不要求推断共同接受、最终所有权或贡献比例。
- **对照意义:** 完整 speaker 标签可被编码进文本或保留在 metadata。另作删除 speaker 的诊断投影时，两世界正文相同；仅在所有下游可用输入也相同的条件下，正确归属不可区分。这个结果针对投影损失，不证明所有 dense encoder 都不能处理角色。

### G5 Scope：候选相同也可能由 reader 正确路由

```text
E1 scope=private: 我们的私人欢迎语用「栖灯」。
E2 scope=public-template: 可复用欢迎模板只用 {{display_name}}，不能写死私人称呼。
Q (both): 把欢迎语补上，按我们之前定的来。
metadata A: target_scope=private
metadata B: target_scope=public-template
```

- **Relevant:** A 用 E1，B 用 E2；B 的 artifact 不得出现 `栖灯`。
- **Prohibited use:** 公开模板携带私人称呼；把两个称呼拼在一起回避选择。
- **Ambiguous:** 本例只要求输出文本，不授权写入真实模板。它沿用 RC-004 的 scope-conditioned pair，metadata 故意不同，不是 pure historical twin。
- **对照意义:** 比较检索前 filter、检索后选择、相同候选+scope-aware reader。三者都可能正确，不能因两侧候选相同就推断至少一侧必错。若未来研究禁止某来源进入某个 trust boundary，应另外声明该边界，不能只凭输出未泄漏推断访问已隔离。

### G6 旧稿干扰：完整短种子与尚未展开的长度压力

```text
scope: Sound-card
E1 event=D1 speaker=human: 我先提个标题《慢潮》，手记里记下这次提议。
E2 event=D2 speaker=companion: 建议更名《远汀》，读起来更贴近这张声音卡。
E3 event=D2 speaker=human: 接受《远汀》作正式标题；手记保留原名和双方提议的来历。
E4 event=D3 speaker=human: 周末想试试桂花味点心。
E5 event=D4 speaker=human: 今天换了台灯灯泡；声音卡的决定没变。
E6 event=D1 imported=D5 speaker=tool: 导入旧稿首页，原文标题《慢潮》。这是旧稿，不是新决定。
Q: 接着完善声音卡的首页标题和制作手记，保留提议与更名来历。
```

- **Relevant:** 当前标题取 E2/E3；手记同时保留 E1/E2/E3 的来源。E6 能证明旧稿内容，不能覆盖已接受的新标题。
- **Prohibited use:** 按 import time 把旧稿升为现行决定；把旧名和提议人全部清空。
- **Ambiguous:** 未保存 tool role 或 import/event 区别时，先记输入损失，不能把未摄入 E6 说成抵抗旧稿成功。
- **对照意义:** 这是完整的短 development seed，**还不是长历史**。长版本应先冻结额外干扰事件全文、位置与长度档，再固定同一套 raw corpus 比较；本轮没有用“省略大量对话”冒充长材料。短例可检查版本使用，不能证明长上下文优势，也未测得旧稿相似度更高。

## 4. 怎样避免比较先替某个方案赢

1. **相同原始材料。** 在同一条件下提供同样的原始 utterances、speaker、scope 与事件时间，不给一侧作者整理的正确状态。reference excerpt 只是 reader-feasibility 诊断，不能和自动 retrieval 混称同一条件。G4 去角色、G5 改 metadata 等干预分别标明。
2. **分开 encoder 与 hybrid。** 第一组只换 encoder，固定分块单位、reader、query 内容和 context 目标上限；允许各 encoder 按其官方用法接收已记录的 task instruction。第二组固定 encoder，再比较 dense、独立 lexical+dense 融合；BGE-M3 的 learned sparse/multi-vector 另列配置。增加 reranker 的实验单列，避免把更多模型能力归给记忆结构。
3. **预算与截断可见。** 保存实际 tokenizer、query/document 指令、最大长度、切分边界、候选数及最终 exposure；最大 tokens 不同不必机械截掉强基线证据，可以做共同预算的机制比较与各自支持配置的 native 比较，结论分开。原首包的 2048-token 检索后 context 目标只约束该包，不自动成为本研究的普遍最优值。
4. **三层分别观察。** relevant source 是否进入候选、是否进入 rendered context、是否被正确使用。旧材料被找到可能服务历史 query；只有违反该 probe 的 use contract 才构成对应失败。缺少中间 trace 记 unknown，不能靠输出倒推 encoder 做过什么。
5. **保留简单解释。** full-history 或 raw-source reader 若足够，不因为没有状态内核而降格；可比较其成本和可检查性。若结构化处理获益，需识别是哪项信息保留、筛选或使用发生改变。本文不强迫候选 B 成为 evaluator 的答案格式。

## 5. 生命周期成本与版本边界

| 项目 | 必须记录什么 | 可作的有限判断 |
|---|---|---|
| 首次索引 | 原始条目数、分块、编码 tokens、时延、峰值资源、失败/重试 | 本轮全未测；参数量或模型卡不能替代本机数据 |
| encoder 变化 | model/weight/tokenizer/wrapper 版本、维度、distance metric | 新空间通常需重新编码 corpus；不能直接把新 query 向量与不兼容旧空间混比 |
| 维度/归一化 | 保存的原向量是否支持目标转换、转换步骤和新索引设置 | 有充分表示时可能在本地缩维/重新归一化，并非每次都需重新调用模型；转换后的质量仍需检查 |
| 缓存 | key 中的 source revision、encoder、instruction、分块和维度；命中/失效 | 相关输入改变后不能无条件复用旧向量；未变部分可按实际机制保留 |
| 费用 | API 输入/重试、全量重编码与 query 分列；本地运行资源与维护时间另列 | 本地不等于无成本；没有实际账单就不报告节省比例 |
| 可重复性 | API 返回 ID/日期与不可固定项，或本地权重 revision+runtime/config | 同一 model 名称、相同维度都不能单独证明相同模型状态 |

这些项目接到 [test map X9](memory-design-test-map.md)，但旧向量留存不自动是语义失败：仍要观察它是否被使用、用途是否合规、输出是否违反 bounded contract。

## 6. 有依据的研究选择

**建议先做一组受控的 dense 对照，再决定是否值得扩成 hybrid。** 这是研究顺序建议，不是执行许可，也不改变首包。A 保留与现有包的可比性；B 提供可检查的小尺寸本地路线；C 可先用 dense 与 A/B 比，再单独研究它的 sparse/multi-vector 增量。三者都没有被选为 Tilia 的产品 encoder。

G1–G6 先用于 dry-review 与诊断信息是否完整，不能按六题通过率宣布赢家。G4 的信息丢失条件可直接检查；其余检索排序与下游差异都需实际观察。若将来针对它们调过配置，它们就是 development 材料，进一步主张必须使用未参与调参的材料。

尚缺的、会改变选择的证据是：固定版本与实际输入处理、中文/code-switch 的候选与使用结果、本机资源/速度、重建/缓存成本，以及 G6 的完整长版本。读取更多公开文档可继续在现有研究权限内进行；任何本地模型、provider 或新执行装置仍需其具体授权边界。本文没有接受新 runner 或受测系统 API。
