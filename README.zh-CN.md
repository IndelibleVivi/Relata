**简体中文** | [English](README.md)
<!-- language: zh-CN; mirror: README.md; translation-status: synchronized -->

# Relata

**Relata** 是一个开放、由社区活经验参与塑造的**前沿记忆研究室**。它定义、综合与评判 agent memory、开源架构及其长处与局限的证据，研究范围同时包含长期人机关系内外的使用情境。中文是 R0 的主要工作与社区语言，英文入口同步维护。

> Agent 记住过去究竟意味着什么，不同系统怎样实现它，又怎样在变化的任务、生活和关系中支持连续性？

## 三项核心职责

Relata 将**自己的 benchmark 研究、系统样本研究空间，以及面向未来记忆装置的 incubator**结合起来。[ADR-0008](decisions/ADR-0008-three-core-research-functions.zh-CN.md) 将这三项相互支持的职责纳入项目核心定位。

| 职责 | Relata 要发展什么 | 从这里进入 |
|---|---|---|
| 自己的 benchmark | 问题、案例、controls、评价方法、实验与有证据支持的比较 | [Case Lab](case-lab/README.zh-CN.md)、[当前证据](STATUS.zh-CN.md) |
| 系统样本研究空间 | 可检查的记忆架构、源码研究与有条件的比较；museum／样本间／研究室的名称仍开放 | [System Census](systems/README.zh-CN.md)、[十份源码研究](systems/source-studies/README.md)、[架构图集](systems/architecture-atlas/README.md) |
| 面向未来的 incubator | 可以用于 Tilia 等独立系统的设计假设、替代方案、反例与经验 | [候选设计](research/own-memory-architecture.md)、[案例—测试映射](research/memory-design-test-map.md) |

系统研究可以暴露案例问题，评价可以挑战架构主张，两者又为未来设计提供依据；每项职责也有独立的研究价值。Benchmark 正在发展，现有系统样本包含研究 drafts，未来 Tilia 的产品源码属于独立项目。

[Agent Memory Study（AMS）](https://github.com/IndelibleVivi/agent-memory-study) 的阅读、源码调查与实验可以带着原有证据限制进入 Relata。两个项目都可以支持长篇综合写作，同时保留各自的问题与研究材料。

## 从一个具体问题开始

[研究室愿景与能力版图](research/lab-development.md)解释当前阶段、方向风险与连续建设结构。要检查一个 memory 问题，打开[五问题离线 reader](systems/architecture-atlas/index.html#questions)，或直接阅读 [GitHub 版展品](systems/architecture-atlas/exhibits.md)：未来用途变化、检索后的交付、更正传播、适时浮现、经验如何改变理解与做法。它把十个固定源码模型接到具体情境、条件对照、节点证据与研究去向。

Clone 后直接在浏览器打开 `systems/architecture-atlas/index.html`；无需 server、账号或网络。条件切换展示静态编辑分析，点击节点可进入既有三视图再返回原问题。GitHub 文件页不执行 HTML，可读同源生成的 Markdown 与 SVG。展品没有模拟回答或发布私有运行结果。

[经验适应研究](research/experience-adaptation-study.md)沿笔记组织、持久综合与指令采用展开两条作者化纵向情境。在[学习展品](systems/architecture-atlas/index.html#exhibit/learning/understand)中，五个阅读时点分别呈现当时可见的经历、当前任务与候选方法；可展开作者分析、比较机制，再从源码节点返回原条件。这是开发材料，不是系统输出或已测学习效果。

## 记忆生态

通用 agent memory 与成人长期人机亲密关系都有独立研究地位。亲密与浪漫关系继续是 founding focus；现有 Case Lab 将普通生活、共同关系经历、项目决策与材料，以及跨模型和实例的 companion/system continuity 作为长期混合领域记忆生态研究。普通事件无需被加工成浪漫象征才有研究价值。

[ADR-0006](decisions/ADR-0006-frontier-memory-research-lab.md) 确立了这次定位扩展。定义、架构研究、综合文章与批评和 cases 一样，都是研究产出。[Agent-memory inquiry](research/agent-memory-inquiry.md) 连接独立文章方向、选定的公开 AMS 研究与[十份有界源码研究](systems/source-studies/README.md)。[架构图集](systems/architecture-atlas/README.md) 提供三十幅绑定源码的 SVG 与离线交互 reader。这些是研究 drafts，尚不是穷尽综述或比较性能结果。

Relata 追问什么被保留、唤起、纳入上下文、使用、修正，或适当地保持沉默。事实回忆、时间推理、来源忠实、抗干扰、scope isolation 和 full-history/full-search controls 继续有价值，但需要说明各自的观察边界。

## 为自有 memory 系统积累设计

研究可以为未来从空 repository 独立编写的记忆系统 **Tilia** 蓄力。Tilia 是独立的长期目标；Relata 继续是研究室。[候选设计](research/own-memory-architecture.md)与[案例—测试映射](research/memory-design-test-map.md)把既有研究转为选择、controls 与反例，不锁定 Tilia 架构。其预期设计需要向量语义检索，编码器与模型选型仍开放。

目前独立 repo 中已经有一份非常早期的明确输入实验，沿用历史工作名 `relata-memory`，并有自己的 private remote。源码尚未公开发布，现有能力是字面搜索与脚本消费。更正后的 [ADR-0007](decisions/ADR-0007-local-memory-apparatus.md) 记录了把研究目标误读成开工指令的范围错误；保留实验不表示它成为正式 Tilia 或持续实现任务。[工程记录](experiments/local-memory-apparatus.md) 保留有边界的检查结果，不声称语义记忆效果。研究室的其他研究产出继续有独立价值。

## 当前阶段

**R0 — Research Foundation。** 两张窄范围的 source Evidence Cards 已 accepted。RC-001 为 clinic-ready；RC-002/003/004 仍是未经 review 的 seeds。三张 public-source System Cards 与十系统 pressure map 已按既有研究做有界 source-fidelity review。尚无 accepted cases、validated evaluators、语义系统评测结果或排名。证据限定见[系统集合](systems/system-cards/README.md)。

2026-10-22 的[未来问题与记忆研究](research/future-question-memory/README.md)推进下一方向：后来任务改变时，保留表示需要支持哪些区别，以及重新访问来源何时能找回它们。七组作者化材料、十五个问题与可重算的 input-only 诊断，展示答案区域冲突、三世界全体交集控制，以及来源缺失／拒绝／旧副本条件。这些是输入的计算性质，语义合同尚待独立评审；没有给记忆系统评分。运行 `python3 -B tools/future_question_inputs.py audit` 可查看结果。

固定 future-question study 另有[离线 review 闭环](research/future-question-memory/README.md#离线-responsereview-闭环)：准备224份输入正文并隔离作者key、核验、导入外部已提供回答、导出盲评、追加判断并重算明确分母。精确有理数 ideal-lookup 上限描述作者有限合同，不是模型实测成绩。[五组 benefit/control 材料](research/continuity-benefit-study.md)补充必要性研究，保留原有 acceptance gate。

具名 RC-005 研究已有[首次盲评离线工作流](case-lab/reviews/workbench/README.md)与[独立浏览器评审台](case-lab/reviews/workbench/index.html)：在双栏阅读区核对完整历史与原样回答，按三个可回访步骤记录判断，保留草稿与明确修订，交回累计判断；工作区面板集中管理评审者代号、草稿恢复与可选本机保存。作者侧 CLI 核验原关闭导出、追加新判断并报告分歧。七项作者练习包可在无 provider 的情况下走完整流程；工具实现不建立人类校准或系统效果。

软件现有 public repository checker 和一个**离线 RC-002 执行演练**：用明确标识的脚本替身，在两条合成历史下分别运行五种条件，保存证据并导出盲审包。测试只建立工程链路行为，不调用模型，也不产生语义分数或能力分数。完整证据状态见 [STATUS](STATUS.zh-CN.md)。

新增的离线输入工具为 **[RC-005 / 共同作品来历](case-lab/cases/seed-005-shared-work-authorship.zh-CN.md)** 准备并核验 18 份待答输入，检查输入投影是否抹掉说话者区别。该 case 仍是 authored candidate，独立人类 review 与 case acceptance 尚未完成。命令与边界见[输入审计说明](experiments/continuity-input-audit.md)。

较广的[首轮研究计划](research/first-research-cycle.md)仍为 proposed。[ADR-0009](decisions/ADR-0009-exploratory-research-boundary.zh-CN.md) 于 2026-10-23 接受，仅激活 [RC-005 → pinned Mem0 执行包](experiments/rc005-native-execution-packet.md)。固定 study CLI 覆盖 54 个 reader 预检、36 个强原文对照和 54 个 native 回答位置；源码实现与离线 plumbing 检查不证明真实可运行性或语义成功。选用既有 generation entitlement 与本地 Qwen3-Embedding-0.6B-Q8_0/1024；全包最多 300 chat／500 embedding client dispatch，包含失败及诊断，不充值、不走收费 fallback。Native state、attempts、回答和未评审材料留在 ignored local artifacts。纯离线 `export-review` 可生成单独匿名包；private 对应表和带条件标签的内部记录由 operator 保留。正式 benchmark promotion、其他 study、Tilia 产品实现、公开结果、hosting、外联与 license 保留各自边界。[ADR-0010](decisions/ADR-0010-bounded-provider-compatibility-checks.zh-CN.md) 仍是独立兼容性例外；配置匹配的接口证据可复用。

**P0 扩展（2026-10-23）：** 指定 RC-005 研究另含[固定 capture 的 reader 后续包](experiments/rc005-exposure-followup.md)：18 份原 immediate capture × 三种投影，最多新增 54 次 DSF reader dispatch，新增三臂统一 4096 completion 上限，不重新摄入／检索／embedding，共用原 300 chat／500 embedding 累计账本。原 144 位置和回答不改写。[Relata × AMS campaign](research/relata-ams-campaign.md)保留各自研究问题与证据；P1–P6 设计不激活其他 provider 或真人研究。

后续[更正并发 challenge](research/correction-race-challenge.md)补充作者化交错顺序、反事实历史与恢复对照；[Hindsight 固定源码核查](research/stale-write-source-audit.md)检查已有保护机制。两份仍为研究 draft，没有系统运行或漏洞结论。

三份有界研究材料把这些职能接起来：未经评审的 [RC-006 companion 迁移 seed](case-lab/cases/seed-006-companion-migration-continuity.zh-CN.md)、基于既有固定源码研究的[更正传播比较](research/correction-propagation-study.md)，以及[多语言语义检索研究](research/semantic-retrieval-study.md)。它们推进案例、竞争解释与研究选择；没有新增 accepted case、系统结果或已选定的 Tilia 架构。

## 为什么暂时不建平台

尚未接受 canonical ontology、system protocol、scoring contract、benchmark release、Leaderboard、Arena、SDK、service 或 hosted infrastructure。[历史架构草案](docs/vision/relata-target-architecture-draft-0.1.md) 继续是 non-normative；[assumption register](ASSUMPTION_REGISTER.zh-CN.md) 保留各项处置。

[ADR-0005](decisions/ADR-0005-offline-pilot-tooling.zh-CN.md) 允许可替换的离线试验工具，无需等待第三方交分数。它不授权 provider adapters、私人材料或公开表现结论。ADR-0010 的窄 provider 兼容性 smoke 与这套工具分开，也不授权 memory-system run。Accepted cross-system boundary 仍受正式 promotion gate 约束。

## 已经开始的研究

[EC-001](research/evidence-cards/EC-001-agent-memory-leaderboard.md) 研究 AML 的公开观察边界与因果归因限制；[EC-002](research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) 研究 PM-Bench 的 observation/scorer binding，并记录 released corpus 没有观察到 step-order 分数影响。两者均未采用或验证来源 benchmark。

现在可以在本地直接演练，需要 Python 3.10+，不安装第三方依赖。每次使用新的输出目录，其父目录必须已存在：

```sh
python3 -B tools/synthetic_pilot.py run --output experiments/artifacts/rc002-demo
python3 -B tools/synthetic_pilot.py verify experiments/artifacts/rc002-demo
```

[演练说明](experiments/offline-rehearsal.md) 解释五种条件、subject/evaluator 视图、盲审包、完整性校验、错误处理和限制。RC-001 人工校准、seed refinement 与基于公开源码的 System Cards 可以并行。[原执行路径](START_HERE.zh-CN.md) 继续作为研究指导；离线例外不将它升级为 accepted protocol。

## 参与方式

社区成员以 co-researchers 身份参与。贡献可以是 exact-source [Evidence Card](research/evidence-card-template.md)、抽象 [Incident Seed](community/incident-seed-template.zh-CN.md)、使用原生词汇的 [System Card](systems/system-card-template.zh-CN.md)、[case review](case-lab/README.zh-CN.md) 或治理批评，无需提供 raw chat。

Consent 按每份 contribution 选择，不构成阶梯。请阅读 [consent modes](community/consent-levels.zh-CN.md) 与 [participation principles](community/participation-principles.zh-CN.md)。Sensitive collection 前仍需确定 restricted consent-record stewardship。

## Public repo 与 privacy

公开可见允许检查，不授权把 raw private conversations、identifying consent records、credentials、restricted system details 或 private review material 放进仓库。CLI 只运行内置、虚构、成年人的材料。Checker 读取 Git 的 public working set，不递归检查被忽略的本地试验记录。

Public licenses 仍是[开放决定](governance/licensing-decision.md)。源码分支不代表 formal release 或 accepted result publication。

## Repository map

[Charter](CHARTER.zh-CN.md)、[research questions](RESEARCH_QUESTIONS.zh-CN.md)、[status](STATUS.zh-CN.md)、[assumptions](ASSUMPTION_REGISTER.zh-CN.md)、[terminology](docs/terminology.zh-CN.md)、[language policy](docs/language-policy.zh-CN.md)、[source research](research/README.md)、[systems](systems/README.zh-CN.md)、[cases](case-lab/README.zh-CN.md)、[community](community/participation-principles.zh-CN.md)、[governance](governance/public-private-boundary.md)、[decisions](decisions/README.md)、[vision history](docs/vision/README.md)。

## Authority 与检查

依次遵循 STATUS、CHARTER、ASSUMPTION_REGISTER、accepted decisions、research/governance/case materials，最后是 non-normative vision history。在 repo root 运行：

```sh
python3 -B tools/check_repo.py
python3 -B -m unittest discover -s tests -v
```

检查覆盖 public-file structure、links、双语声明与配对修改、选定的 case markers，以及隔离的执行与证据回归；不证明中英语义等价、reviewer agreement、memory necessity、长期记忆保留或系统质量。
