**简体中文** | [English](README.md)
<!-- language: zh-CN; mirror: README.md; translation-status: synchronized -->

# Relata

**Relata** 是一个开放、由社区活经验参与塑造的**前沿记忆研究室**。它定义、综合与评判 agent memory、开源架构及其长处与局限的证据，研究范围同时包含长期人机关系内外的使用情境。中文是 R0 的主要工作与社区语言，英文入口同步维护。

> Agent 记住过去究竟意味着什么，不同系统怎样实现它，又怎样在变化的任务、生活和关系中支持连续性？

## 记忆生态

通用 agent memory 与成人长期人机亲密关系都有独立研究地位。亲密与浪漫关系继续是 founding focus；现有 Case Lab 将普通生活、共同关系经历、项目决策与材料，以及跨模型和实例的 companion/system continuity 作为长期混合领域记忆生态研究。普通事件无需被加工成浪漫象征才有研究价值。

[ADR-0006](decisions/ADR-0006-frontier-memory-research-lab.md) 确立了这次定位扩展。定义、架构研究、综合文章与批评和 cases 一样，都是研究产出。[Agent-memory inquiry](research/agent-memory-inquiry.md) 连接独立文章方向、选定的公开 AMS 研究与[十份有界源码研究](systems/source-studies/README.md)。[架构图集](systems/architecture-atlas/README.md) 提供三十幅绑定源码的 SVG 与离线交互 reader。这些是研究 drafts，尚不是穷尽综述或比较性能结果。

Relata 追问什么被保留、唤起、纳入上下文、使用、修正，或适当地保持沉默。事实回忆、时间推理、来源忠实、抗干扰、scope isolation 和 full-history/full-search controls 继续有价值，但需要说明各自的观察边界。

## 为自有 memory 系统积累设计

研究室也为从空 repository 开始、独立编写自己的 memory 架构与可运行装置蓄力。[候选设计](research/own-memory-architecture.md)与[案例—测试映射](research/memory-design-test-map.md)把既有研究转为明确的选择、controls 与反例，比较连续性收益、修订和 scope 使用，也保留完整历史／简单文件搜索作为强对照。目前交付的是设计研究，尚未构建新的 memory runtime；研究室的其他研究产出继续有独立价值。

## 当前阶段

**R0 — Research Foundation。** 两张窄范围的 source Evidence Cards 已 accepted。RC-001 为 clinic-ready；RC-002/003/004 仍是未经 review 的 seeds。尚无 reviewed System Cards、accepted cases、validated evaluators、真实系统结果或排名。

软件现有 public repository checker 和一个**离线 RC-002 执行演练**：用明确标识的脚本替身，在两条合成历史下分别运行五种条件，保存证据并导出盲审包。测试只建立工程链路行为，不调用模型，也不产生语义分数或能力分数。完整证据状态见 [STATUS](STATUS.zh-CN.md)。

新增的离线输入工具为 **[RC-005 / 共同作品来历](case-lab/cases/seed-005-shared-work-authorship.zh-CN.md)** 准备并核验 18 份待答输入，检查输入投影是否抹掉说话者区别。该 case 仍是 authored candidate，没有独立人类 review 或系统评测。命令与边界见[输入审计说明](experiments/continuity-input-audit.md)。

## 为什么暂时不建平台

尚未接受 canonical ontology、system protocol、scoring contract、benchmark release、Leaderboard、Arena、SDK、service 或 hosted infrastructure。[历史架构草案](docs/vision/relata-target-architecture-draft-0.1.md) 继续是 non-normative；[assumption register](ASSUMPTION_REGISTER.zh-CN.md) 保留各项处置。

[ADR-0005](decisions/ADR-0005-offline-pilot-tooling.zh-CN.md) 允许可替换的离线试验工具，无需等待第三方交分数。它不授权 provider adapters、私人材料或公开表现结论。Accepted cross-system boundary 仍受正式 promotion gate 约束。

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
