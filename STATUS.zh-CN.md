**简体中文** | [English](STATUS.md)
<!-- language: zh-CN; mirror: STATUS.md; translation-status: synchronized -->

# Relata 当前状态

**Project：** Relata
**Phase：** R0 — Research Foundation
**Identity：** 前沿记忆研究室；通用 agent memory 与成人长期亲密关系都是研究情境
**Implementation：** repository checks、离线合成执行演练、candidate 输入准备/核验/投影审计、两份局部源码诊断与独立 repo 的本地明确输入记忆装置；没有 accepted benchmark implementation
**Remote/publication：** public source repository；没有 formal release
**Case release：** none
**Protocol version：** none
**Scoring contract：** none

## 当前 authority

当前 working authority 包括 `CHARTER.md`、`RESEARCH_QUESTIONS.md`、`ASSUMPTION_REGISTER.md`、`docs/terminology.md`、`governance/` 与 `decisions/` 下的 accepted records；相应中文文档同步维护。`AGENTS.md` 将这些边界转化为工作约束。Draft 0.1 继续作为 non-normative reasoning history。

[ADR-0005](decisions/ADR-0005-offline-pilot-tooling.zh-CN.md) 记录 maintainer 对可替换、内置合成材料演练工具的窄范围授权。它不接受研究协议或系统能力结论。下方正式 implementation-boundary promotion gate 不作为这项离线工程检查的前提。

[ADR-0006](decisions/ADR-0006-frontier-memory-research-lab.md) 接受研究室定位扩展、独立的概念、架构和综合研究，以及两份有界离线源码诊断。成人长期亲密关系继续是 founding focus。这项范围决定不提升证据状态、不接受文章论点，也不授权模型/provider 执行。

Maintainer 于 2026-09-26 补充长期目标：让研究为从空 repository 独立编写自有 memory 架构与可运行装置积累依据。当前成果是[候选设计](research/own-memory-architecture.md)与[测试映射](research/memory-design-test-map.md)。随后的继续实现按 [ADR-0007](decisions/ADR-0007-local-memory-apparatus.md) 限定：在独立 repo 编写并测试明确输入的本地装置；[工程记录](experiments/local-memory-apparatus.md) 管理实际执行状态。这不增加模型/provider 权限，也不接受架构优越性。

## Evidence state

| Artifact | State | Accepted evidence |
|---|---|---|
| Evidence Cards | 2 accepted | EC-001 public-boundary/causal-limit findings；EC-002 observation/scorer-binding limits 与 released-corpus no-impact finding；只在各自 authorization 内有效 |
| Agent-memory inquiry / 文章方向 | 开放研究问题、AMS 连接与初步综合 | 无 accepted definition、穷尽综述或文章正文 |
| 开源架构研究 | 10 份有界 drafts：Mem0、Letta、Graphiti、lmc-5、Tideline Memory、Aelios、Hindsight、OpenViking、LangMem、A-MEM | 固定源码观察；lmc-5 与 Graphiti 另有窄范围离线诊断；无独立人类 review、accepted System Card 或模型参与的比较结果 |
| [架构图集](systems/architecture-atlas/README.md) | 10 份模型、30 幅 SVG/Mermaid 与离线交互 reader | 绑定源码的图示；没有新增上游运行或能力测量 |
| 自有 memory 设计 / 案例—测试映射 | proposed 架构、controls 与推翻条件 | ADR-0007 选取候选 B 做窄范围本地工程实验；没有 accepted 普适 schema 或能力结果 |
| [本地记忆装置](experiments/local-memory-apparatus.md) | 已实现并本地提交；源码未公开发布 | 110 项工程测试与 38 步／21 项断言的子进程 demo；只有明确合成输入与脚本消费，没有语义效果结果 |
| Claim boundaries | 双语 candidate study | CL0–CL6、lanes、cells、adapter classes 仍为提议；无 accepted result unit 或 publication policy |
| System Cards / Architecture Pressure Maps | templates only | 0 reviewed cards/maps |
| Distinction Atlas | 6 seed hypotheses | 0 supported distinctions |
| Pilot 001 | clinic-ready case、manual plan、candidate E0 pack | 无系统运行、acceptance 或人工校准；只有 authored anchors |
| RC-002 / RC-003 / RC-004 | 未经 review 的 seeds | 无模型/系统评测或 balanced pilot set；已修 RC-003 probe 和 RC-004 explicit accord，没有提升状态 |
| Mixed-domain routing | question、incident families、scope-conditioned seed | RC-004 仍未经 review；metadata-only 的 prior shortcut 尚未实测 |
| Offline RC-002 rehearsal | 已实现，scripted-only，两条历史 × 五种条件 | 验证 exposure、隔离、错误记录、证据校验、盲审包生成等工程链路；无 memory-system evidence |
| RC-005 / CT-AUTHORSHIP | seed；选自 2026-09-22 提案；输入工具已实现 | 18 份待答输入；一个家族的 3 个相关 checkpoint 在去掉 speaker 后发生字面碰撞；无独立人类 review、系统回答或 Memory Necessity Gate acceptance |
| Evaluator calibration | plan 与 authored E0 fixtures | 无 reviewer data 或 validated boundary；评审包必须保留治理该回答的证据 |
| Community contribution path | public-safe governance/templates | restricted contribution path 尚未实际使用 |

Template、合同修正、生成的 fixtures 与通过的 plumbing tests 都不证明 memory method 有效。语义判断继续 pending，不生成综合分或能力分数。

## 当前 research target

定义并批判性研究 agent memory 的概念、开源架构与证据。比较不同实现保留什么、过去的经验怎样影响当前行为，以及架构选择在什么条件下有用或失效。在通用 agent 和长期 mixed-role 关系中研究这些问题，保留历史依赖 controls、尊重架构差异的观察边界，以及保护隐私的社区参与。

## Immediate work

用[自有记忆设计研究](research/own-memory-architecture.md)与[测试映射](research/memory-design-test-map.md)，以现有案例和更简单的 controls 检查候选内核、派生视图与 context 边界。分开源码观察、设计假设和执行结果；已知案例是开发表例，不能冒充 held-out validation。ADR-0007 已给出具体本地实现／执行范围；工程记录须保留已测机制、实际消费者和仍待回答的语义问题。这不表示跨系统 benchmark 计划已完成。

从[十份源码研究 drafts](systems/source-studies/README.md) 推进 [agent-memory inquiry](research/agent-memory-inquiry.md)：review source fidelity、检查竞争解释，收敛独立文章的论点。选定的公开 AMS 研究可以带着原有证据限制进入问题设计。这项研究独立于 live evaluation 与 case promotion gate 推进。

现在即可运行[离线演练](experiments/offline-rehearsal.md)，无需等待别人提交分数。基于公开源码审查的 System Cards、community review 和其他 case 工作可以并行。这个脚本不授权调用模型 provider。

依据 ADR-0001 的 validity/reproducibility tooling 范围，现在可以使用 [RC-005 输入审计](experiments/continuity-input-audit.md)，下一项是 review 作者归属与继续制作手记的 contract。该工具只准备输入，不接受 Continuity Trials 提案的其余内容，也不扩大模型执行权限。

后续经验性工作仍包括：获得不同架构的 reviewed System Cards 与 Architecture Pressure Map；在使用 E0 语义边界前完成 dry review；review RC-002/003/004，并在 live studies 前明确 history exposure 与 controls。收集 sensitive contributions 前先选择 restricted consent-record stewardship。D-006 仍需要 community-grounded prospective-intention authority，并明确不会偷带 PM-Bench task-handle architecture 的观察边界。

## 尚未声称

没有 universal relationship-quality measure、排名、canonical ontology、validated judge/panel、formal third-party submissions、protected hidden cases，或 privacy/safety/health/relationship certification；不代表亲密关系的完整多样性。Pilot 001 和 RC-002 scripted rehearsal 不覆盖完整 mixed-domain ecology。Companion/system continuity 仍未经测试。

## 跨系统 evaluation 的 working promotion gate

这项 gate 管理现有 case-evaluation programme 的 implementation boundary 与 coverage claims，不决定一篇源码研究、概念论述或比较文章是否可以开始。

Accepted cross-system implementation-boundary decision 仍需：

- 至少五个 bounded distinctions 获得 multi-source support；
- 至少三个 materially different systems 有 reviewed System Cards 与 boundary analysis；
- 至少一张 pilot 通过 Memory Necessity Gate；
- ordinary-life、operational/project、shared-relational 与 mixed-domain routing/isolation cases 各自运行后，才可提出 full-scope coverage claim；
- reviewer disagreement 已记录并用于修改 rubric；
- consent-to-synthetic-publication path 已在不转移 raw chat 的条件下走通；
- accepted decision 明确 excluded systems 与 adapter distortion。

这些是可修订的 governance thresholds，不是 validated scientific sample sizes。离线工程例外不满足上述任何条件，也不授权 full-scope claim。将来的 coverage claim 还必须说明被排除或未经测试的 companion/system continuity。

## 仍需 maintainer 决定

Formal release/case-publication policy，以及 code、document、synthetic-data、contribution licenses，仍需在 release 或 accepted result publication 前决定。社区收集前仍需确定 restricted identifying consent-record storage。RC-001 semantic-equivalent guarantees 继续属于待 dry review 与 Case Clinic 的 bounded human-review proposal，没有授权自动 hard semantic scorer。
