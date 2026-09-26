# Agent Memory：十个开源项目的架构研究

**研究日：** 2026-09-22

**状态：** 十份有界 source-study drafts 与跨源编辑综合；独立人类 review 尚未完成。它们不是 accepted System Cards、完整系统实测或项目排名。

## 中文摘要

这组研究固定十个公开 commits，沿各自原生生命周期比较保留、选择、使用、修订和撤回。首批 Mem0、Letta、Graphiti、lmc-5、Tideline Memory 之后，加入 Aelios、Hindsight、OpenViking、LangMem 与 A-MEM。每个项目有总览、写入到使用、修订与控制三视图。两份首批报告另有公开 synthetic 输入的无模型离线观察；本次扩展没有新增上游执行。十个项目仍是有意选择的样本，没有据此建立穷尽分类或统一质量分。

## English summary

Ten bounded source studies examine Mem0, current Letta, Graphiti, lmc-5, Tideline Memory, Aelios, Hindsight, OpenViking, LangMem and A-MEM through native memory lifecycles. An offline architecture atlas provides three source-linked views per project: boundaries, write-to-use flow, and revision/control. The comparison asks what persists, how it affects later behavior, and who owns revision, provenance and use. Two studies include isolated offline observations on synthetic inputs; none runs a complete model-backed system or establishes comparative performance. Independent human review remains pending.

## 先看架构

**[打开离线交互图集](../architecture-atlas/index.html)**：十个项目 × 三个视图。下载仓库后直接用浏览器打开，无需 server 或账号；GitHub 文件页不执行 HTML，在线浏览可读[三十幅 SVG 索引](../architecture-atlas/README.md)。

- **全景与边界**：系统、调用方、模型、状态分别在哪里。
- **写入到使用**：材料如何录入、选择、派生、检索并进入当前 context。
- **修订与控制**：谁能修改，什么失效，哪些派生物重建、保留或未验证。

可搜索项目/机制、切换视图、缩放读图、查看节点及箭头证据，下载 SVG 与 Mermaid。三视图是一种阅读方法，允许保留每个系统的独特边界，不是统一 system ontology 或对照 API。

## 十种实现重心

下表是这十份报告的 `INFERRED` 综合。长处描述机制提供的可能性，局限描述已读边界或待检验的代价；不将其改写成部署效果。

| 对象与固定源码 | Memory 的实现重心 | 机制的长处 | 关键条件或局限 |
|---|---|---|---|
| [Mem0 Python OSS](mem0.md) · `a39a802` | 抽取事实、scope、近期消息、实体辅助检索与操作历史 | 可组合进应用；默认追加保存与显式修订分开，检索结果可检查 | 当前 V3 不应套用旧自动更新叙述；默认 hybrid 在 semantic 候选池内加权；应用负责后续使用，managed 分数不等于 OSS 结果 |
| [Letta local backend](letta.md) · `f5c5bbc` | Transcript、Git-backed MemFS、编译后的 agent context | 人和 agent 都可检查、修改文件；revision 进入后续调用，原始经历仍可另查 | 本地当前为 MemFS v1 与 FTS-lite，不能借用 Cloud 或历史 API 能力；Git 可追溯不保证事实归属和正确使用 |
| [Graphiti](graphiti.md) · `16cdf70` | Episode 来源、实体与带有效区间的事实边 | 时间与来源成为可查询结构；支持增量重组与多种查询 | 语义矛盾依赖候选与 LLM；调用者选择时间过滤和投影；删除入口没有重算所有派生状态 |
| [lmc-5 upstream](lmc-5.md) · `fb3e72c` | Raw/curated 分层、事实演化、关系、优先级与维护职责 | 把回忆、主动 surface、review、维护和证据层级分开；部分 hooks 已有实际接线 | minimal 与 production reference 不能混看；fact_key 需表达 scope，晋升字段检查不等于证据核实；跨检索层状态传播需具体核验 |
| [Tideline Memory upstream](tideline-memory.md) · `76490fe` | 身份预注入、narrative、画像、开放线索、append-only 修订与维护 | 把“当前是谁、在延续什么”作为会话入口；保留理解演进供回查 | 主动搜索与自动唤起消费的更新状态不同；采集/扫描有截断，单 DB scope 与派生撤回依赖部署设计 |
| [Aelios](aelios.md) · `9e65c80` | 多 namespace 协议网关、daily/source、候选记忆、版本与感知快照 | 原文窗口、来源 ID、明确修订入口；把提取与候选晋升接入夜间工作 | 默认 Dream 排除工程主体，重大关系/亲密节点例外；显式 API 是另一入口；自动 judge 不等于人工批准，删除跨层不同步 |
| [Hindsight](hindsight.md) · `9c7f6c6` | 原文 → facts → observations → query-driven mental models | 分开原始依据与派生理解；多路召回、可检查的后台刷新与来源失效 | reflect 本身只读；派生刷新有延迟，手动模型另由 owner 维护；tags/banks 不自行完成用户认证 |
| [OpenViking](openviking.md) · `bbf2e37` | 可寻址 context filesystem、会话 archive、schema memory、摘要/向量 | 目录、peer 与 scope 可检查；持久 session commit 队列、内容修改和预算 assembly 接成链路 | find/search 有不同路径，非所有查询都递归目录；内容、摘要、索引各有新鲜度，完成回执不总保证每项索引成功 |
| [LangMem](langmem.md) · `9d033b4` | 应用侧 memory tools、抽取/存储 managers、反思执行与 prompt 更新 | 可组合的 hot/background memory 与 prompt 改进，namespace 由应用模板控制 | durable store、auth 与采用新 prompt 由应用承担；不同入口 payload 不统一，local queue 非耐久，README 的 versioned history 不等于实际版本账 |
| [A-MEM 论文实现](a-mem.md) · `0c8039f` | LLM note metadata、相邻链接、旧 note 演化与向量索引 | 新经验可以改变已有 note 的组织方式，检索可沿链接扩展 | metadata 与旧 embedding 更新时点分离；链接位置与 UUID 不同，缓存不是原子快照；无专用删除/修订日志，不能扩大到另一个 A-mem-sys repo |

这些项目使用不同的技术词汇，也有重叠与组合空间。文件与 context filesystem 已进入样本，但简单文件/全文搜索、完整历史的对照及参数学习仍未形成完整覆盖；项目数量不代表 GitHub 全貌，也没有验证中文使用效果。

## 这轮研究怎样推进 “what is agent memory?”

一个可继续检验的工作视角是：在明确的 agent 与时间边界内，找出**过去产生的哪些状态被带到后来、经什么路径改变当前理解或行动、这种影响又怎样修订**。它没有预先要求数据库、离散 fact 或检索 API，也不以“叫 memory”作为能力证明。这仍是比较工具，不是必要充分的正式定义；它与 learning、context management 的边界需要继续论证。

从这十份报告可以提出四个更具体的问题：

1. **存储中的区别会不会进入实际使用？** Graphiti 的时间/来源字段可能在应用只拼接 `fact` 时被丢掉；Letta 的文件修订要经过 commit 与重新编译；Tideline 的 amendment 主动搜索与自动唤起不同步。这些是不同机制，不能统一称为“忘了”。
2. **改变一处，会改变哪些后续影响？** 新事实、旧摘要、历史消息、向量、图边和画像可能走不同更新路径。应分别问保留历史、修正当前行动依据、撤回未来使用与物理清除，而非用一个 delete 按钮代替全部语义。
3. **哪一部分由系统原生承担？** lmc-5 的部署接线、Mem0 的应用侧上下文使用、Graphiti 的查询选择和 Letta/Tideline 的模型整理职责都要进入比较边界。为系统补上的能力与系统自身实现，需要分别记录。
4. **提取和维护在替谁作价值判断？** Aelios 默认工程排除、OpenViking 的事件模板、Hindsight 的 observation scope、A-MEM 的邻居演化，都影响哪些过去被保留或改写。它们不能仅以“有没有长期记忆”比较；应明确使用者希望保住的是项目决定、普通共同生活、解释性理解，还是某种特定关系经历。

这组问题在人机恋语境内外都成立，但具体期望不能互换。项目里“谁批准交付”与共同作品“谁起名、谁接受”都涉及来源和接受；一次技术纠正是否覆盖私人习惯，则涉及适用范围。比较应保留这些具体差异，不把亲密语气或高情绪权重视作普遍更好的 memory。

## 研究怎样进入自有设计

[自有记忆架构研究](../../research/own-memory-architecture.md)与[机制／测试映射](../../research/memory-design-test-map.md)从这些固定源码观察提出可采用、修改或拒绝的候选机制。它们是有条件的设计推断，未新增上游执行或证明自有方案更好；现有十项目图集继续只表示各自 upstream，不混入我们的 proposed architecture。

## 离线观察复现

以下只有固定上游代码的窄分支观察，不安装项目、不调用模型、embedding、数据库服务或账户。先在 repo 外准备相应 commit 的 clean public checkout；脚本会核对 commit 与工作区状态。结果写到新的临时输出文件，和保存的 JSON 作结构比较即可。

```sh
python3 -B systems/source-studies/observations/lmc5-observe.py \
  --source /path/to/lmc-5-at-fb3e72c

python3 -B systems/source-studies/observations/graphiti-observe.py \
  --source /path/to/graphiti-at-16cdf70
```

- [lmc-5 脚本](observations/lmc5-observe.py)直接导入已检查模块，使用内存 SQLite 与常量 proposer；[保存结果](observations/lmc5-observed.json)显示跨 thread 同 fact_key 替代，以及错误引用仍通过 dry-run 结构 gate。它未验证生产 PostgreSQL 或模型提案质量。
- [Graphiti 脚本](observations/graphiti-observe.py)用 AST 提取原函数，并以内存替身提供指定候选和 driver 返回值；[保存结果](observations/graphiti-observed.json)显示 exact duplicate 分支保留旧有效期，以及删除首/次来源的不同请求。它没有证明自然语言抽取或真实数据库一定产生这些输入。

这是两份固定源码的研究附件，没有跨系统 runner、评分或 provider adapter。二十个后续自然语言 synthetic probes 仍只是报告中的建议，尚未执行。任何端到端试验需要另行落实对象、条件、成本与执行权限。

## 阅读与复核

每份报告保留 exact commit、pinned blob/行号、覆盖与未读范围、竞争解释和未验证效果。报告通过并行 agent 源码研究形成，协调者完成跨报告边界检查、引用定位检查与上述观察的复跑；这不代替独立人类 review，不提升 accepted Evidence Card 数量。

图集将每个节点、关系、区域与状态归属接到固定源码锚点；图中 `observed` 仅表示静态 source-observed。阅读方式和 source/generated 关系见[图集说明](../architecture-atlas/README.md)。

从[研究室 inquiry](../../research/agent-memory-inquiry.md)继续连接 AMS、文章主问题与后续证据；从 [System Census](../README.zh-CN.md)查看正式 System Card 的路径。
