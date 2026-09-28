**简体中文** | [English](ADR-0009-exploratory-research-boundary.md)
<!-- language: zh-CN; mirror: ADR-0009-exploratory-research-boundary.md; translation-status: synchronized -->

# ADR-0009 — 分开有界探索性执行与 Benchmark Promotion

**Status：** proposed；尚未 accepted 或 activated
**Prepared：** 2026-09-27
**Scope：** [首轮研究计划](../research/first-research-cycle.md)的候选执行边界；本草案不授予执行、支出、hosting 或结果发布权限

## 中文摘要

建议为有明确对象、公开成人合成材料、配置、预算与停止条件的探索性实测建立独立边界，使其能够先于正式 benchmark promotion 产生有界观察。一个获准研究包内的重复运行、诊断与条件变化无需逐项重新审批；越出对象、数据、费用或外部操作范围才需要新决定。本文仍为 proposed；既有 STATUS、CHARTER 与 AGENTS 的执行限制保持有效。计划、代码、运行证据、案例接受、比较主张和公开发布是不同状态。

## English summary

This proposal would permit bounded exploratory studies before formal benchmark promotion, through a named study envelope covering exact subjects, public adult synthetic material, configurations, resource limits and stopping conditions. Authorized repetitions, diagnostics and condition changes would not need individual approvals. The draft changes no current authority: execution, case acceptance, comparative claims and publication remain distinct decisions with their own evidence.

## 背景与证据

[ADR-0008](ADR-0008-three-core-research-functions.zh-CN.md)接受 benchmark 研究、系统样本空间与 incubation 三项相互支持且独立的职责。[STATUS](../STATUS.zh-CN.md)记录了十份源码研究 drafts、离线图集、RC-002 scripted rehearsal 与十八份 RC-005 待答输入，但没有模型参与的比较结果。[测试映射](../research/memory-design-test-map.md)已经提出对照与尚未执行的机制问题。

[ADR-0005](ADR-0005-offline-pilot-tooling.zh-CN.md)允许窄范围脚本演练，不提供 provider adapter 或真实系统执行权限。现有跨系统 implementation gate 保护的是更广的评价 programme。单独建立有界探索路线，可以取得修订案例、揭示 adapter 贡献、挑战候选设计所需的观察，同时保留正式比较要求。这是 governance 提议，不是任何候选系统或 evaluator 已经就绪的证据。

## 拟议决定

### 1. 接受窄范围例外

如果本 ADR 获得接受并同步进入当前权威文档，它将允许**在 maintainer 授权的研究执行范围内**使用 study-specific connectors、隔离的受测环境、模型调用和证据记录。某个已命名对象必需的本地数据库或进程可以纳入该范围。它不授权稳定的跨系统 API、通用 benchmark runner、SDK、hosted orchestration、公开服务、Leaderboard、Arena 或 canonical ontology。

执行范围记入对应 study 的既有记录；适用时使用 [pilot record](../experiments/pilot-record-template.md)。它是一份可读的约定，不是新增的强制 runtime schema。一份范围约定可以涵盖多个已命名对象、案例与配置区间，不必为其中每次运行或条件重新授权。

### 2. 把实际权限落实到具体对象

执行受测系统前，需要在获准范围中落实以下事实与选择：

| 项目 | 获准范围必须明确什么 |
|---|---|
| 研究问题与受测对象 | 问题、公开源码 revision 或产品版本、complete-agent／memory-support／combined 边界、纳入的案例或有界 family 生成范围 |
| 输入与暴露 | 公开成人合成来源与 revisions、locale、允许历史、evaluator 隔离、固定重放或共同演进互动、隔离测试 state |
| Effective configuration | Model/provider 与 endpoint 类别、reader/harness、prompts、tools/hooks、context policy、相关依赖、允许变化和 adapter 贡献；记录中不含凭据 |
| 资源与外部影响 | 获准 provider/account 使用、费用上限与币种、包含的 ingestion/embedding/maintenance/review 调用、用量记录、重试预留及允许本地进程；hosting 与外部操作另行列明或排除 |
| 证据与停止条件 | 本地产物位置、可观察阶段、原始结果和失败、review 需要、主张限制、操作者及停止／恢复条件 |

进入候选名单不等于已安装或已就绪。订阅、凭据、公开 endpoint 或可用 connector 不构成调用权限。通过浏览器手动调用模型仍属于 subject execution，换通道不能绕过此边界。研究输入不能从工程环境继承私人记忆、无关账号 context 或 evaluator key。

拟议 [RC-005 → Mem0 执行包](../experiments/rc005-native-execution-packet.md)给出具体候选，包含预检转 native、write／ready／probe 时点、进程恢复边界和资源上限；源码研究记录不能证明 native 可运行。本 ADR 与完整执行范围可以一并接受。Provider、账号授权或费用上限仍未落实的范围，不能启动依赖它们的调用；既有权限内的公开输入准备与源码研究可以继续。

### 3. 在获准范围内允许有用的迭代

操作者可以重复运行、检查失败、修 connector 缺陷和改变已声明条件，无需每次返回审批。记录实际配置与全部 attempts。如果修复改变了系统收到的内容或究竟由谁完成任务，标记受影响 runs，只重跑恢复有效解释所需的比较，并保留早先失败。

当资源上限不足以覆盖下一项有界操作、实际输入暴露违反研究约定、对象／配置身份未确定或 state 隔离失败时，暂停依赖的执行。范围内修复并验证后可以继续；只有扩大对象、数据、资源或外部操作范围才需要新授权。本地分析无需一同暂停。不启动无界自动重试；失败与修复调用同样计入费用。Provider 计费延迟时，在派发前预留保守额度。

### 4. 分开证据层级

探索记录可以说明某个已命名配置在指定条件下产生了保存的回答或行动。这不自动接受 case、证明 memory necessity、定位机制、验证 semantic evaluator 或给产品排名。

Current-only 与 ingest-then-disable 是不同 controls。完整历史、可搜索原文、作者挑选的 reference context 与 supported native conditions 回答不同问题。完整原生系统与固定 reader 的 memory component 不自动可比。Adapter 补出的抽取、来源、时间过滤、routing 或 state 属于 combined pipeline。缺少可观察性保持 unknown，不自动记失败。[Claim-boundary labels](../research/claim-boundary-study.zh-CN.md)仍是候选术语；本 ADR 不整体接受其 ladder 或 schema。

探索输出可以先于独立语义 review 产生，并标为 unreviewed。Case acceptance 与有争议的语义结论仍需要对应 review evidence 和分歧记录。精确产物检查无需仪式性人工批准；模型交叉评审不等于独立人类 calibration。这里不产生 automatic hard semantic scorer。

### 5. 分开记录、发布与部署

原始工作输出继续留在既有 ignored local artifact 区域，见 [experiments](../experiments/README.md)。公开源码与合成输入不意味着所有 runtime logs 都适合公开：凭据、私人 context、私有服务细节和识别性 review 数据不进入 Git。

公开探索性展品需要明确选择并 review 的 packet，以及适用的发布和权利决定。展品保留 exact object、conditions、缺失证据和未经 review 的判断。执行许可不自动发布结果、授予 licenses、发送邀请或部署网站。已有源码研究和本地 reader 开发保留独立范围；公开 hosting 仍需对应权限。

## 与既有 authority 的关系

**仍为 proposed 时：** 既有 gate 不变。[STATUS](../STATUS.zh-CN.md)、[CHARTER](../CHARTER.zh-CN.md)、[ASSUMPTION_REGISTER](../ASSUMPTION_REGISTER.zh-CN.md) 与 [AGENTS](../AGENTS.md)继续管理当前权限。首轮研究计划是 planning material；它与本 ADR 的存在都不允许据此开始实现或模型执行。

**接受时：** 在同一改动中更新 STATUS、CHARTER、ASSUMPTION_REGISTER、AGENTS 与受影响双语入口，明确该有名有界的探索例外不要求先完成正式跨系统 implementation promotion gate。该 gate 继续管理可复用评价边界的 promotion 与正式 coverage/comparison claims；不能静默删掉其中 distinctions、System Cards、memory necessity、reviewer disagreement、contribution path 或 adapter pressure 的要求。若这些要求本身需要调整，另记具体变更与理由，不能把本例外当作整体删除。

ADR-0007 的更正继续有效。本提案不接受候选 B 为 Tilia 架构，不授权继续开发保留的 `relata-memory` 实验产品，不导入私人 memory，也不把某系统内部 schema 变成 evaluator 答案格式。另行获准的 research prototype 是 system under study，不是已接受的产品设计。

## 替代方案与后果

| 方案 | 后果 |
|---|---|
| 仅保留当前离线例外 | 源码研究与输入准备继续；模型实测仍不在 accepted execution boundary 内 |
| **推荐：按明确范围开展探索性研究** | 允许目标明确的观察和迭代，保留成本／数据决定权、架构差异与证据状态 |
| 现在授权通用评测平台 | 在接口扭曲和维护需要尚未被证实前承诺共用接口与运行体系；本提案不推荐 |

拟议例外减少已确定实验内部的反复许可问题，同时要求首次执行包足够具体。公开源码研究无需被研究项目 maintainer 背书。社区参与仍是可选路径；restricted contributions 保留 consent 与 stewardship 要求，本 ADR 不授权 outreach 或 human-participant study。

## Review、接受与撤回

Maintainer 可在阅读研究计划与具体执行范围后接受、修改或拒绝这一边界。接受须明确 scope 并更新上方 authority surfaces；source commit 或 tests 通过都不充分。随后研究在自身资源／证据边界处停止，不成为永久启用的无限执行许可。

整轮回顾时决定例外到期、在新范围内延续，或为后续 implementation decision 提供依据。保留与计划相悖的观察，记录实质性排除。将来接受平台、排名规则、release、网站部署或 Tilia 实现时，仍须分别识别对应决定。
