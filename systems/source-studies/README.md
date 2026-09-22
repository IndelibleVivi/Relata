# Agent Memory：首轮开源架构研究

**研究日：** 2026-09-22

**状态：** 五份有界 source-study drafts 与跨源编辑综合；独立人类 review 尚未完成。它们不是 accepted System Cards、完整系统实测或项目排名。

## 中文摘要

这轮研究沿 Mem0、当前 Letta、Graphiti、lmc-5 和 Tideline Memory 的原生生命周期读源码，比较它们保留什么、怎样影响后续行为，以及修订、来源和使用责任落在哪里。两份报告另有公开 synthetic 输入的无模型离线观察；其余为静态源码研究。五个项目展现了不同的 memory 工程对象，没有据此建立穷尽分类或统一质量分。

## English summary

Five bounded source studies examine Mem0, current Letta, Graphiti, lmc-5 and Tideline Memory through native memory lifecycles. The comparison asks what persists, how it affects later behavior, and who owns revision, provenance and use. Two studies include isolated offline observations on synthetic inputs; none runs a complete model-backed system or establishes comparative performance. Independent human review remains pending.

## 五种实现重心

下表是这五份报告的 `INFERRED` 综合。长处描述机制提供的可能性，局限描述已读边界或待检验的代价；不将其改写成部署效果。

| 对象与固定源码 | Memory 的实现重心 | 机制的长处 | 关键条件或局限 |
|---|---|---|---|
| [Mem0 Python OSS](mem0.md) · `a39a802` | 抽取事实、scope、近期消息、实体辅助检索与操作历史 | 可组合进应用；默认追加保存与显式修订分开，检索结果可检查 | 当前 V3 不应套用旧自动更新叙述；默认 hybrid 在 semantic 候选池内加权；应用负责后续使用，managed 分数不等于 OSS 结果 |
| [Letta local backend](letta.md) · `f5c5bbc` | Transcript、Git-backed MemFS、编译后的 agent context | 人和 agent 都可检查、修改文件；revision 进入后续调用，原始经历仍可另查 | 本地当前为 MemFS v1 与 FTS-lite，不能借用 Cloud 或历史 API 能力；Git 可追溯不保证事实归属和正确使用 |
| [Graphiti](graphiti.md) · `16cdf70` | Episode 来源、实体与带有效区间的事实边 | 时间与来源成为可查询结构；支持增量重组与多种查询 | 语义矛盾依赖候选与 LLM；调用者选择时间过滤和投影；删除入口没有重算所有派生状态 |
| [lmc-5 upstream](lmc-5.md) · `fb3e72c` | Raw/curated 分层、事实演化、关系、优先级与维护职责 | 把回忆、主动 surface、review、维护和证据层级分开；部分 hooks 已有实际接线 | minimal 与 production reference 不能混看；fact_key 需表达 scope，晋升字段检查不等于证据核实；跨检索层状态传播需具体核验 |
| [Tideline Memory upstream](tideline-memory.md) · `76490fe` | 身份预注入、narrative、画像、开放线索、append-only 修订与维护 | 把“当前是谁、在延续什么”作为会话入口；保留理解演进供回查 | 主动搜索与自动唤起消费的更新状态不同；采集/扫描有截断，单 DB scope 与派生撤回依赖部署设计 |

五者使用不同的技术词汇，也有重叠与组合空间。这是有意选择的首轮样本，不代表 GitHub 全貌；没有完整覆盖文件式基线、完整历史基线、参数学习、所有小型项目或中文使用效果。

## 这轮研究怎样推进 “what is agent memory?”

一个可继续检验的工作视角是：在明确的 agent 与时间边界内，找出**过去产生的哪些状态被带到后来、经什么路径改变当前理解或行动、这种影响又怎样修订**。它没有预先要求数据库、离散 fact 或检索 API，也不以“叫 memory”作为能力证明。这仍是比较工具，不是必要充分的正式定义；它与 learning、context management 的边界需要继续论证。

从这五份报告可以提出三个更具体的问题：

1. **存储中的区别会不会进入实际使用？** Graphiti 的时间/来源字段可能在应用只拼接 `fact` 时被丢掉；Letta 的文件修订要经过 commit 与重新编译；Tideline 的 amendment 主动搜索与自动唤起不同步。这些是不同机制，不能统一称为“忘了”。
2. **改变一处，会改变哪些后续影响？** 新事实、旧摘要、历史消息、向量、图边和画像可能走不同更新路径。应分别问保留历史、修正当前行动依据、撤回未来使用与物理清除，而非用一个 delete 按钮代替全部语义。
3. **哪一部分由系统原生承担？** lmc-5 的部署接线、Mem0 的应用侧上下文使用、Graphiti 的查询选择和 Letta/Tideline 的模型整理职责都要进入比较边界。为系统补上的能力与系统自身实现，需要分别记录。

这组问题在人机恋语境内外都成立，但具体期望不能互换。项目里“谁批准交付”与共同作品“谁起名、谁接受”都涉及来源和接受；一次技术纠正是否覆盖私人习惯，则涉及适用范围。比较应保留这些具体差异，不把亲密语气或高情绪权重视作普遍更好的 memory。

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

这是两份固定源码的研究附件，没有跨系统 runner、评分或 provider adapter。十个后续自然语言 synthetic probes 仍只是报告中的建议，尚未执行。任何端到端试验需要另行落实对象、条件、成本与执行权限。

## 阅读与复核

每份报告保留 exact commit、pinned blob/行号、覆盖与未读范围、竞争解释和未验证效果。报告通过并行 agent 源码研究形成，协调者完成跨报告边界检查、引用定位检查与上述观察的复跑；这不代替独立人类 review，不提升 accepted Evidence Card 数量。

从[研究室 inquiry](../../research/agent-memory-inquiry.md)继续连接 AMS、文章主问题与后续证据；从 [System Census](../README.zh-CN.md)查看正式 System Card 的路径。
