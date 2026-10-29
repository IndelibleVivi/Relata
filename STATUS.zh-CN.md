**简体中文** | [English](STATUS.md)
<!-- language: zh-CN; mirror: STATUS.md; translation-status: synchronized -->

# Relata 当前状态

**2026-10-30 本地开发状态：** [ADR-0011](decisions/ADR-0011-local-research-studio.zh-CN.md) 接受本地 Research Studio 实现：canonical SQLite／artifacts、版本化双 Atlas、固定 run／review rounds、三个确定性仪器和四种分离导出。见[使用说明](docs/studio.md)、[来源文章](research/collection-delivery-comparison.md)和[计算报告](research/finite-instrument-report.md)。这是 source implementation 与本地工程／有限算法工作，不是正式 release、hosting、独立校准或新系统性能证据。

本地 Study 分析工作台已支持私人作者解释、精确观察／判断引用、不可变修订、评审变化提示与另写主张。这些是作者分析，不是自动语义评判或已接受结果。

**P0 扩展（2026-10-23）：** 指定 RC-005 研究另含[固定 capture 的 reader 后续包](experiments/rc005-exposure-followup.md)：18 份原 immediate capture × 三种投影，最多新增 54 次 DSF reader dispatch，新增三臂统一 4096 completion 上限，不重新摄入／检索／embedding，共用原 300 chat／500 embedding 累计账本。原 144 位置和回答不改写。[Relata × AMS campaign](research/relata-ams-campaign.md)保留各自研究问题与证据；P1–P6 设计不激活其他 provider 或真人研究。

**Project：** Relata
**Phase：** R0 — Research Foundation
**Identity：** 前沿记忆研究室；通用 agent memory 与成人长期亲密关系都是研究情境
**Core functions：** 自己的 benchmark 研究；系统样本研究空间（museum／样本间／研究室名称开放）；面向未来独立记忆装置的 incubator
**Implementation：** 本地 Research Studio（ADR-0011）；repository checks、离线合成执行演练、固定研究的输入/投影分析与外部 response/review 导入、两份局部源码诊断，以及一项已接受、运行记录保留在私有侧的 operator-owned provider 兼容性检查边界；另保留独立的早期记忆工程实验作为研究材料，不作为 Relata 产品；没有 accepted benchmark implementation；另有 accepted ADR-0009 下的固定 RC-005 native-study CLI，真实运行证据独立保存。
**Remote/publication：** public source repository；没有 formal release
**Case release：** none
**Protocol version：** none
**Scoring contract：** none

## 当前 authority

当前 working authority 包括 `CHARTER.md`、`RESEARCH_QUESTIONS.md`、`ASSUMPTION_REGISTER.md`、`docs/terminology.md`、`governance/` 与 `decisions/` 下的 accepted records；相应中文文档同步维护。`AGENTS.md` 将这些边界转化为工作约束。Draft 0.1 继续作为 non-normative reasoning history。

[ADR-0005](decisions/ADR-0005-offline-pilot-tooling.zh-CN.md) 记录 maintainer 对可替换、内置合成材料演练工具的窄范围授权。它不接受研究协议或系统能力结论。下方正式 implementation-boundary promotion gate 不作为这项离线工程检查的前提。

[ADR-0006](decisions/ADR-0006-frontier-memory-research-lab.md) 接受研究室定位扩展、独立的概念、架构和综合研究，以及两份有界离线源码诊断。成人长期亲密关系继续是 founding focus。这项范围决定不提升证据状态、不接受文章论点，本身也不授权模型/provider 执行。

Maintainer 于 2026-09-26 澄清：长期 **Tilia** 目标与 Relata 当前研究范围分开。Relata 的[候选设计](research/own-memory-architecture.md)与[测试映射](research/memory-design-test-map.md)可以为未来独立系统提供依据，不授权立即实现，也不锁定架构。[ADR-0007](decisions/ADR-0007-local-memory-apparatus.md) 已纠正协调者先前的范围误读。已经写出的 `relata-memory` 保留为非常早期的本地实验，其证据见[工程记录](experiments/local-memory-apparatus.md)。Tilia 需要向量语义检索；现有实验只有字面搜索，编码器与模型选型仍开放。

[ADR-0008](decisions/ADR-0008-three-core-research-functions.zh-CN.md) 接受三项职责作为 Relata 的核心定位。Benchmark 仍在发展；源码研究与架构图构成已有系统样本积累；候选设计支持未来孵化。这项定位决定不改变证据状态或执行边界。未来 Tilia 的产品源码属于独立项目。Relata 与 AMS 各有独立研究价值，也都能为长篇综合写作提供依据。

Maintainer 于 2026-10-22 要求为 Relata + AMS 提出并实现下一研究方向，本轮在此落成[未来问题研究](research/future-question-memory/README.md)与固定材料的输入有效性诊断。该研究只使用原创合成材料，不执行 subject、provider、私人语料或外部服务；不接受 ADR-0009、系统 evaluator、scoring contract 或任何现有 case。

[ADR-0010](decisions/ADR-0010-bounded-provider-compatibility-checks.zh-CN.md) 是独立接受的有限兼容性 smoke 例外。协调者为首批选择最多 6 次 generation dispatch，每次 output limit 最多 2,048 tokens；以及最多 4 次 embedding dispatch，每批最多 8 条公开原创合成文本，每条最多 2,000 字符，client 失败也计入。这些是批次限制，不约束 opaque 的 upstream attempts，也不要求后续范围内有限兼容性测试重新索取已有许可。Generation 使用已有 entitlement；embedding 使用已有本地 Qwen 或 Workers AI，不充值、不启用收费 fallback。只观察解析、普通文本与 JSON-object forms、usage／identity 可见性、向量维数、finite values 与批次顺序。它不接受 ADR-0009、RC-005 执行包或系统 memory 评测；本公共记录没有并入运行观察。

## Evidence state

| Artifact | State | Accepted evidence |
|---|---|---|
| Evidence Cards | 2 accepted | EC-001 public-boundary/causal-limit findings；EC-002 observation/scorer-binding limits 与 released-corpus no-impact finding；只在各自 authorization 内有效 |
| Agent-memory inquiry / 文章方向 | 开放研究问题、AMS 连接与初步综合 | 无 accepted definition、穷尽综述或文章正文 |
| 开源架构研究 | 10 份有界 drafts：Mem0、Letta、Graphiti、lmc-5、Tideline Memory、Aelios、Hindsight、OpenViking、LangMem、A-MEM | 固定源码观察；lmc-5 与 Graphiti 另有窄范围离线诊断；无独立人类 review、accepted System Card 或模型参与的比较结果 |
| [架构图集](systems/architecture-atlas/README.md) | 10 份模型、30 幅 SVG/Mermaid 与离线交互 reader | 绑定源码的图示；没有新增上游运行或能力测量 |
| [问题导向系统集合](systems/architecture-atlas/exhibits.md) | 五个静态展品覆盖十个既有固定模型；离线搜索、任务条件、图／节点深链与生成 Markdown 版本 | 仅为源码综合与阅读路径检查；没有新增上游运行、公开运行展品、人类 review 或排名 |
| [经验适应研究](research/experience-adaptation-study.md) | 三条固定源码机制、两条作者化纵向 worksheet 与学习展品五个展开条件 | 有界源码综合与作者分析；没有 subject 执行、独立校准、accepted case 或已测迁移收益 |
| 自有 memory 设计 / 案例—测试映射 | 为独立 Tilia 目标提供 proposed 架构、controls 与推翻条件 | 候选 B 不是已接受的 Tilia 架构；没有 accepted 普适 schema 或能力结果 |
| [本地记忆装置](experiments/local-memory-apparatus.md) | 范围纠正后保留的非常早期实验；已有独立 private remote，源码未公开发布 | 110 项工程测试与 38 步／21 项断言的子进程 demo；只有明确合成输入与脚本消费，没有向量检索或语义效果结果 |
| Claim boundaries | 双语 candidate study | CL0–CL6、lanes、cells、adapter classes 仍为提议；无 accepted result unit 或 publication policy |
| System Cards / Architecture Pressure Maps | 3 张 source-reviewed public-source cards（[Mem0](systems/system-cards/SC-001-mem0.zh-CN.md)、[Graphiti](systems/system-cards/SC-002-graphiti.zh-CN.md)、[Letta](systems/system-cards/SC-003-letta.zh-CN.md)）与 1 张十系统 [pressure map](systems/architecture-pressure-map.zh-CN.md) | 仅静态源码 review；无 contributor review、accepted-for-census 提升、运行结果或比较结论 |
| Distinction Atlas | 8 seed hypotheses（7 条具 multi-source source corroboration） | 0 supported distinctions；promotion 仍需 community Incident Seed 与 accepted microcase |
| [未来问题与记忆](research/future-question-memory/README.md) | 机制论证、七组作者化材料与 input-only 投影工具 | 15 个问题／15 个世界／105 个相关 cells；固定便条下七个后续问题存在冲突，其中一个须检查全体交集；回查当前原文消除这些字节碰撞，缺失／拒绝／旧副本条件仍保留碰撞；无模型回答、语义验证、accepted case 或架构排名 |
| Pilot 001 | clinic-ready case、manual plan、candidate E0 pack | 无系统运行、acceptance 或人工校准；只有 authored anchors |
| RC-002 / RC-003 / RC-004 | 未经 review 的 seeds | 无模型/系统评测或 balanced pilot set；已修 RC-003 probe 和 RC-004 explicit accord，没有提升状态 |
| Mixed-domain routing | question、incident families、scope-conditioned seed | RC-004 仍未经 review；metadata-only 的 prior shortcut 尚未实测 |
| Offline RC-002 rehearsal | 已实现，scripted-only，两条历史 × 五种条件 | 验证 exposure、隔离、错误记录、证据校验、盲审包生成等工程链路；无 memory-system evidence |
| RC-005 / CT-AUTHORSHIP | seed；选自 2026-09-22 提案；输入工具已实现 | 18 份待答输入；一个家族的 3 个相关 checkpoint 在去掉 speaker 后发生字面碰撞；无独立人类 review、系统回答或 Memory Necessity Gate acceptance |
| [RC-006 companion 迁移](case-lab/cases/seed-006-companion-migration-continuity.zh-CN.md) | seed；authored-unvalidated | 一个合成 family；没有真实迁移、能力观察、独立人类 review 或 Memory Necessity Gate acceptance |
| [更正并发 challenge](research/correction-race-challenge.md)／[Hindsight 保护核查](research/stale-write-source-audit.md) | 作者化开发工作表与固定源码定点检查 drafts | 交错反例与已检查的保护；无 runtime race 结果、新独立 family 或 accepted evidence |
| [更正传播](research/correction-propagation-study.md)／[多语言语义检索](research/semantic-retrieval-study.md) | 比较与设计研究 drafts | 基于来源的比较与 authored 开发表例；没有新系统运行、encoder 定案或 accepted evidence |
| Continuity benefit / selective-use 材料 | 5 组作者化 development families／10 views；RC-006 八格设计 | 无 subject run、独立问题作者、held-out data 或人类校准；accepted-case 必要性 gate 不变 |
| [Future-question 离线 review](research/future-question-memory/README.md) | 固定材料 input export、精确有理数 ideal-lookup 分析、prepare/verify/import/盲评/recompute tooling | 仅本地导入与完整性检查；没有 subject执行、导入研究结果、人类校准或accepted scoring contract |
| [RC-005 首次盲评工作流](case-lab/reviews/workbench/README.md) | 离线浏览器评审台、可恢复草稿／修订、原运行绑定的追加导入／报告 CLI；七项作者练习 | 仅工程工作流与描述性判断记录；无独立人类 review、accepted rubric、新系统运行或公开结果 |
| Evaluator calibration | plan 与 authored E0 fixtures | 无 reviewer data 或 validated boundary；评审包必须保留治理该回答的证据 |
| Community contribution path | public-safe governance/templates | restricted contribution path 尚未实际使用 |
| Provider 兼容性 smoke／[ADR-0010](decisions/ADR-0010-bounded-provider-compatibility-checks.zh-CN.md) | 已接受的有限工程检查；operator-owned，repository 无执行入口或公共 replay command | 仅覆盖请求／返回解析、形式处理、usage／identity 可见性、向量维数、finite values 与批次顺序；运行记录保留在私有侧；无 memory-system 结果、语义主张或发布 |
| [RC-005 → Mem0](experiments/rc005-native-execution-packet.md) / ADR-0009 | accepted 具名探索范围；固定 study 源码 CLI | 144 回答位置；离线 plumbing 已核验；真实运行与语义评审各自留证于私有侧；无 benchmark promotion 或结果发布 |

Template、合同修正、生成的 fixtures 与通过的 plumbing tests 都不证明 memory method 有效。语义判断继续 pending，不生成综合分或能力分数。

## 当前 research target

定义并批判性研究 agent memory 的概念、开源架构与证据。比较不同实现保留什么、过去的经验怎样影响当前行为，以及架构选择在什么条件下有用或失效。在通用 agent 和长期 mixed-role 关系中研究这些问题，保留历史依赖 controls、尊重架构差异的观察边界，以及保护隐私的社区参与。

## Immediate work

[愿景与能力版图](research/lab-development.md)把完整目标接到当前可用能力。已实现的[五问题 collection reader](systems/architecture-atlas/index.html#questions)与[同源 GitHub 版](systems/architecture-atlas/exhibits.md)提供情境／任务条件 → 跨系统解释 → 固定源码节点／来源 → controls 与研究去向的阅读路径。这是静态源码展品，不新增运行结果或 case acceptance。完整 programme 继续保留概念研究、收益与使用、学习、companion continuity 和社区参与，不被具名 study 取代。

[未来问题研究 Work A–C](research/future-question-memory/README.md)为现有 programme 提供具体的下一研究入口：追踪真实原文再访问，评审用途变化的合同，再在独立接受的执行范围内，以强原文／文件搜索控制比较保留、检索与使用。当前输入结果已在声明的边界内完成。继续区分有限信息丢失、可恢复的候选遗漏和下游使用；后两项仍需实际系统观察。

[ADR-0009](decisions/ADR-0009-exploratory-research-boundary.zh-CN.md) 于 2026-10-23 接受，仅激活 [RC-005 → pinned Mem0 执行包](experiments/rc005-native-execution-packet.md)。固定 study CLI 覆盖 54 个 reader 预检、36 个强原文对照和 54 个 native 回答位置；源码实现与离线 plumbing 检查不证明真实可运行性或语义成功。选用既有 generation entitlement 与本地 Qwen3-Embedding-0.6B-Q8_0/1024；全包最多 300 chat／500 embedding client dispatch，包含失败及诊断，不充值、不走收费 fallback。Native state、attempts、回答和未评审盲包留在 ignored local artifacts。正式 benchmark promotion、其他 study、Tilia 产品实现、公开结果、hosting、外联与 license 保留各自边界。[ADR-0010](decisions/ADR-0010-bounded-provider-compatibility-checks.zh-CN.md) 仍是独立兼容性例外；配置匹配的接口证据可复用。

- **自己的 benchmark：** 通过现有 [Case Lab](case-lab/README.zh-CN.md) 推进案例、controls 与评价方法。在各自既定范围内使用[离线演练](experiments/offline-rehearsal.md)和[candidate 输入审计](experiments/continuity-input-audit.md)，无需等待第三方交分数。离线演练执行明确标记的 scripted double，输入审计不执行 subject；两者不授予 provider 调用权限，也不建立系统质量结论。
- **系统样本研究空间：** 从[十份源码研究 drafts](systems/source-studies/README.md) 与[架构图集](systems/architecture-atlas/README.md) 推进 [agent-memory inquiry](research/agent-memory-inquiry.md)。Review source fidelity，比较机制与竞争解释，将具体问题带入案例或设计研究。这项工作独立于 live evaluation 与 case promotion gate 推进。
- **Incubator：** 用[自有记忆设计研究](research/own-memory-architecture.md)与[测试映射](research/memory-design-test-map.md)，以现有案例和更简单的 controls 检查候选机制，为独立 Tilia 研究向量检索与编码器选项。分开源码观察、设计假设和执行结果；已知案例是开发表例，不能冒充 held-out validation。保留的早期实验是证据，不是继续实现的指令。

围绕三项职责，先取用相关的公开 AMS 成果及其条件和证据限制，再研究具体缺口。定义与长篇综合可以在没有预定论点的情况下发展；写作或其中一项职责都不必等待其余部分全部成熟。

依据 ADR-0001 的 validity/reproducibility tooling 范围，现在可以使用 [RC-005 输入审计](experiments/continuity-input-audit.md)，下一项是 review 作者归属与继续制作手记的 contract。该工具只准备输入，不接受 Continuity Trials 提案的其余内容，也不扩大 ADR-0010 的兼容性边界。

三张 reviewed public-source System Cards 与一张十系统 Architecture Pressure Map 已经存在，第一轮 census 比较的材料已具备。后续经验性工作仍包括：在使用 E0 语义边界前完成 dry review；review RC-002/003/004，并在 live studies 前明确 history exposure 与 controls。收集 sensitive contributions 前先选择 restricted consent-record stewardship。D-006 仍需要 community-grounded prospective-intention authority，并明确不会偷带 PM-Bench task-handle architecture 的观察边界。

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
