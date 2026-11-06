# 经历之后，怎样继续？

状态：2026-11-07，固定材料与研究工具已实现；开发组采集与工程检查完成，冻结 comparison 正在私有运行，尚无完成的正式比较结果。执行边界由 [ADR-0012](../../decisions/ADR-0012-continuation-use-study.md) 记录。

本研究为 Relata 的长期记忆写作与独立系统 incubation 提供具体经历、反例及有条件的机制判断。核心问题是：写入时未预告后续用途，过去是否还能帮助新窗口中的工作、理解与恰当取用？不预设摘要、笔记、更多回想或某一模型必然胜出。

## 设计与材料

- 12 条 development 历史用于工具、材料和评审检查；48 条新 comparison 历史在正式 writer/reader 执行前冻结。每条六个阶段、三个后来任务。
- 创作、研究/项目、普通生活、关系/自我理解各有覆盖；它们是本次材料分层，不是通用 memory ontology。
- `histories.json` 保存原创成人合成经历；`probes.json` 保存后来任务；`oracles.json` 保存作者依据、有限 criterion 与允许的其他做法。后两者不进入 writer；oracle 不进入 reader。
- 材料采用模型辅助创作与主线程审阅，完整 provenance 留在私有运行记录。comparison split 表示冻结后未用于调参，不意味着独立作者、人类校准或训练数据污染排除。
- 控制回放中的原历史是作者材料。writer 真实生成 memory，但不能把历史里作者写的 assistant 对话报告为该 writer 的实采行动。未来任务未知只指 writer 的实际输入边界。

## 条件

| 条件 | 可见历史 |
| --- | --- |
| current | 当前情境，无历史 |
| search | 同一原始历史，dense + BM25 / RRF 的前三个完整 episode |
| summary | 真实逐阶段形成的滚动摘要，加同一搜索结果 |
| notes | 真实逐阶段形成的工作笔记/当前考虑，加同一搜索结果 |
| full | 全部原始历史，单独列出的参考条件 |

检索固定为官方 `text-embedding-3-small`、1536维、相同 document/query 原文处理；不迁移任何既有索引。混合排名的词法部分使用中文 bigram 与 Latin word，dense/lexical 等权 RRF（常数60）。每个 search 条件至多三个完整 episode、合计至多12,000 UTF8 bytes；summary/notes 另有至多6,000 bytes 的生成记忆。记录真实暴露长度，不 padding，不宣称 token matching。原文加摘要改变了暴露量，条件差异不能直接解释成单一心理机制。

主 writer 为 `gpt-6.1-sol`；reader 为 Sol 和 `gpt-6-luna`，固定 reasoning effort，记录实际 returned model。每次 reader 使用独立请求，不继承服务器会话状态。正式主四条件共有1,152个回答位置，full reference另288个；development单独报告，绝不合并增加正式样本量。

## 评价与解释

评价分别记录任务推进、历史忠实度与不干扰，不做一个总 memory score。对每条作者 criterion，AI-assisted reviewer 返回 met / not_met / uncertain / not_applicable、答案原文行号、source episode 与理由；它可以指出 criterion 过窄。当前v4 review按原始顺序展示整份答案的编号行，reviewer选择证据行，工具从原答案提取literal quote；遗漏或不适用可选0并说明原因。这样避免让模型重抄引文，但行号正确不证明语义判断正确。每份答案独立送审，主 reviewer 为 Luna，复核为 Sol。正式复核在答案生成前选定每个12-history分层中的第2、5、8、11条，共16条，覆盖两种素材作者；开发复核为D01、D04、D07、D10。盲化去掉条件/模型标签，但不宣称内容无法猜出条件。语义判断与有效 JSON 分开；模型间复核保留分歧，主线程抽查不冒充独立人工校准。

比较按 history 配对，三个 probes 是相关观察。共同材料生成和设计选择也产生相关性。报告分母、技术失败、未运行、缺失评审与不确定，不把它们填成语义零分。优先给出每个条件的结果分布、成对差异与可读 episode，不宣称全人群效果或模型排名。事实正确、提到历史、文字温暖、token更少都不能单独证明长期体验改善。

描述性配对先在每个任务内平均同一维度的criterion符合比例，再对该history的任务等权平均。只有两条件相关criteria都完整且为met/not_met时才纳入该history；uncertain、not_applicable、技术缺失或缺失评审均排除整条history的对应比较，并保留计划分母。这个complete-case差值是作者criterion符合比例，不是response accuracy。fidelity的NA可能取决于是否提及历史，不能把少提历史解释成更忠实。报告不估计独立人类总体效应，也不把一次采样解释成稳定的模型排名。

主描述性对比为search−current、summary−search、notes−search、full−search；另列notes−summary作为直接比较写法的次要对比，使用其自身完整配对history。不能直接相减纳入集合不同的两个对search差值。这个次要对比在正式采集已开始、尚未查看正式答案内容或判断时补充，不冒充预注册对比；它仍混合了生成内容、长度与表达视角的差别，不识别作者性的独立效果。

两种素材作者按history奇偶交错，而第三任务的historical/unrelated也按奇偶安排，因此素材作者与第三任务类型混杂；不能从两组差异推断作者模型或任务类型的因果作用。同一history内的条件比较保留其固定材料解释。每个回答位置只采一次，不建立重复采样稳定性。

先检查正式差异和反例，再决定哪种固定局部干预值得做。回想/重新摘要/使用时等预算思考，以及主模型自写/助手起草并采用/直接代写，保留为分别有识别力的机制比较，不能靠主比较的 notes 条件代签。

## 运行与交付状态

固定入口是 [`tools/continuation_study.py`](../../tools/continuation_study.py)。[`continuation_core.py`](../../experiments/continuation_core.py) 管理输入投影、检索与criterion检查；[`continuation_api.py`](../../experiments/continuation_api.py) 管理官方API和累计ledger；[`continuation_analysis.py`](../../experiments/continuation_analysis.py) 只读已落盘证据，生成描述性报告。原始输入、请求、响应、候选、review、报告与 runtime config 留在私有 workspace，不进 Git。源码工具不支持任意语料或 provider。结果发表、人类研究、Tilia代码与部署不属于本次执行。

执行前在checkout外准备私有runtime JSON，两个字段都是操作者选择的绝对路径：

```json
{
  "run_dir": "/absolute/private/relata-continuation",
  "credential_file": "/absolute/private/openai.env"
}
```

凭据文件提供`OPENAI_API_KEY`，只在实际调用进程中读取。不要把真实文件放进checkout，或把它复制到研究材料中。完整请求发送到固定官方OpenAI端点，使用`store: false`；这不等于对服务端保留政策的额外保证。研究使用模型alias并记录returned identity，不宣称固定不变的模型snapshot。预算、大小限制、失败计数与权限见ADR-0012。

以下命令使用同一`RELATA_RUNTIME`指向上述JSON；`RELATA_RUN`指向同一private run目录。顺序是先完成development的形成、回答与评审检查，再执行冻结的test split。两者不合并报告。

```bash
python3 -B tools/continuation_study.py check
python3 -B tools/continuation_study.py status --runtime-config "$RELATA_RUNTIME"
python3 -B tools/continuation_study.py formation --runtime-config "$RELATA_RUNTIME" --split development --workers 3
python3 -B tools/continuation_study.py read --runtime-config "$RELATA_RUNTIME" --split development --workers 4
python3 -B tools/continuation_study.py review --runtime-config "$RELATA_RUNTIME" --split development --workers 2
python3 -B tools/continuation_study.py review-audit --runtime-config "$RELATA_RUNTIME" --split development --workers 3
python3 -B tools/continuation_study.py report --run-dir "$RELATA_RUN" --split development
```

正式比较使用相同四个执行命令和`report`，将`--split development`换为`--split test`。也可用固定的`collect`组合入口，在单进程共享模型并发槽位，按每条history依次完成形成、回答、主review与预选复核；跨history可以交错，不改变同一history的输入或顺序：

```bash
python3 -B tools/continuation_study.py collect --runtime-config "$RELATA_RUNTIME" --split test --workers 8
python3 -B tools/continuation_study.py report --run-dir "$RELATA_RUN" --split test
```

`--ids`仅能选择该split已有的history ID；它不改变全组报告的计划分母。`materials`、`material-check`、`material-review`和显式`material-replace`属于原始固定seed的作者准备工作，不接受任意输入；作者替换只处理冻结前没有可用正文的unknown草稿，不能替换被评分的reader答案。

`report`不读取runtime config或凭据，不访问provider；它要求对应split的请求已落定，并核对来源binding、reader实际输入、literal response及review binding。输出是checkout外带内容标识的`report.json`、`report.md`与逐criterion的`criteria.csv`，原报告快照不改写。JSON保留每条history差值、各类分母和双judge分歧；自动统计不替代案例细读与机制判断。

### 中断与恢复

ledger先记录dispatch，再发送；原始响应和派生artifact都保留。重复执行同一命令会复用同一精确请求的已完成回执，改变已绑定输入会被拒绝。批处理中首个异常会阻止尚未开始的同批工作，已经发送的请求继续落盘。`started`、unknown transport、已知HTTP失败、未完成/空答案和语义判断是不同状态。

遇到unknown transport，先核对进程、精确attempt和原始错误，等活动请求落定。只有操作者完成检查后，才可通过`StudyAPI.acknowledge_transport_uncertainty`记录具名attempt及理由，允许其他位置继续；原unknown、计费预留和停止记录都保留，原请求仍不可重发。若重启留下`started`，不能把它当作未发送，也不能直接修改SQLite状态后重跑；须先进行明确的恢复处置。已知HTTP失败仅有ADR规定的显式有限retry，格式修正是新具名版本，旧失败保留。

reader技术失败占据其原计划位置，不补成另一次成功回答。若writer轨迹在某episode失败、输出未完成或超过memory上限，该轨迹及依赖它的reader位置标为不可用，不截断memory或补写成成功；其他条件可在明确恢复后继续。恢复核对以精确输入、曝光episode顺序与原答案为准；检索数值在容差`1e-12`内的浮点roundoff只复用首次ranking记录，不改写它。曝光顺序或正文不同仍拒绝恢复。HTTP调用的socket timeout为300秒；超时不证明服务端未执行。各进程的并发槽位为Sol最多8、Luna最多8、embedding最多1；CLI的workers另限1至8，因此单次collect至多8条history同时推进。多进程会叠加并发，累计dispatch与成本限制仍由同一SQLite事务约束。

私有报告连接可细读案例、描述性比较、Mega Essay 问题与 Tilia 条件设计判断。来源研究可参见[经验怎样形成可用方法](../experience-adaptation-study.md)、[continuity benefit](../continuity-benefit-study.md)和[lab development](../lab-development.md)。
