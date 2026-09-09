**简体中文** | [English](STATUS.md)
<!-- language: zh-CN; mirror: STATUS.md; translation-status: synchronized -->

# Relata 当前状态

**Project：** Relata
**Phase：** R0 — Research Foundation
**Implementation：** repository checks 与离线合成执行演练；没有 accepted benchmark implementation
**Remote/publication：** public source repository；没有 formal release
**Case release：** none
**Protocol version：** none
**Scoring contract：** none

## 当前 authority

当前 working authority 包括 `CHARTER.md`、`RESEARCH_QUESTIONS.md`、`ASSUMPTION_REGISTER.md`、`docs/terminology.md`、`governance/` 与 `decisions/` 下的 accepted records；相应中文文档同步维护。`AGENTS.md` 将这些边界转化为工作约束。Draft 0.1 继续作为 non-normative reasoning history。

[ADR-0005](decisions/ADR-0005-offline-pilot-tooling.zh-CN.md) 记录 maintainer 对可替换、内置合成材料演练工具的窄范围授权。它不接受研究协议或系统能力结论。下方正式 implementation-boundary promotion gate 不作为这项离线工程检查的前提。

## Evidence state

| Artifact | State | Accepted evidence |
|---|---|---|
| Evidence Cards | 2 accepted | EC-001 public-boundary/causal-limit findings；EC-002 observation/scorer-binding limits 与 released-corpus no-impact finding；只在各自 authorization 内有效 |
| Claim boundaries | 双语 candidate study | CL0–CL6、lanes、cells、adapter classes 仍为提议；无 accepted result unit 或 publication policy |
| System Cards / Architecture Pressure Maps | templates only | 0 reviewed cards/maps |
| Distinction Atlas | 6 seed hypotheses | 0 supported distinctions |
| Pilot 001 | clinic-ready case、manual plan、candidate E0 pack | 无系统运行、acceptance 或人工校准；只有 authored anchors |
| RC-002 / RC-003 / RC-004 | 未经 review 的 seeds | 无模型/系统评测或 balanced pilot set；已修 RC-003 probe 和 RC-004 explicit accord，没有提升状态 |
| Mixed-domain routing | question、incident families、scope-conditioned seed | RC-004 仍未经 review；metadata-only 的 prior shortcut 尚未实测 |
| Offline RC-002 rehearsal | 已实现，scripted-only，两条历史 × 五种条件 | 验证 exposure、隔离、错误记录、证据校验、盲审包生成等工程链路；无 memory-system evidence |
| Evaluator calibration | plan 与 authored E0 fixtures | 无 reviewer data 或 validated boundary；评审包必须保留治理该回答的证据 |
| Community contribution path | public-safe governance/templates | restricted contribution path 尚未实际使用 |

Template、合同修正、生成的 fixtures 与通过的 plumbing tests 都不证明 memory method 有效。语义判断继续 pending，不生成综合分或能力分数。

## 当前 research target

建立长期 mixed-role 关系中可 bounded evaluation 的 memory/continuity constructs；确定哪些失败需要历史才能区分；寻找能保留不同架构的观察边界；区分 deterministic、semantic 与 legitimate disagreement；让 contributors 无需转移 raw private conversations 就能共同设计研究。

## Immediate work

现在即可运行[离线演练](experiments/offline-rehearsal.md)，无需等待别人提交分数。基于公开源码审查的 System Cards、community review 和其他 case 工作可以并行。这个脚本不授权调用模型 provider。

后续经验性工作仍包括：获得不同架构的 reviewed System Cards 与 Architecture Pressure Map；在使用 E0 语义边界前完成 dry review；review RC-002/003/004，并在 live studies 前明确 history exposure 与 controls。收集 sensitive contributions 前先选择 restricted consent-record stewardship。D-006 仍需要 community-grounded prospective-intention authority，并明确不会偷带 PM-Bench task-handle architecture 的观察边界。

## 尚未声称

没有 universal relationship-quality measure、排名、canonical ontology、validated judge/panel、formal third-party submissions、protected hidden cases，或 privacy/safety/health/relationship certification；不代表亲密关系的完整多样性。Pilot 001 和 RC-002 scripted rehearsal 不覆盖完整 mixed-domain ecology。Companion/system continuity 仍未经测试。

## Working promotion gate

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
