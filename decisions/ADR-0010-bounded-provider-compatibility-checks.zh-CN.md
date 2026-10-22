**简体中文** | [English](ADR-0010-bounded-provider-compatibility-checks.md)
<!-- language: zh-CN; mirror: ADR-0010-bounded-provider-compatibility-checks.md; translation-status: synchronized -->

# ADR-0010：有界 provider 兼容性检查

**Status：** accepted
**Accepted：** 2026-10-23
**Scope：** 由 operator 管理的公共接口边界兼容性检查；不授权记忆系统评测或通用执行

## 中文摘要

Maintainer 另行接受一项很窄的 provider 兼容性检查，用于确认已授权接口能否解析普通请求与返回、呈现 usage 与模型或服务身份，并返回具有稳定批量顺序的有限 embedding 结果。它只使用公开原创合成文本，不做记忆能力、案例、排名或语义正确性评估。本文不激活 proposed [ADR-0009](ADR-0009-exploratory-research-boundary.zh-CN.md) 的通用探索包，也不批准 [RC-005 → Mem0 执行包](../experiments/rc005-native-execution-packet.md) 的 native 路径、144 个回答位置或 USD 10 预算。精确运行观察留在私有 operator 记录；本公共决定不发布运行结果。

## English summary

The maintainer separately accepted a narrow provider compatibility check. It verifies that authorized interfaces can parse ordinary requests and returns, expose usage and model or service identity when available, and return bounded embeddings with stable batch order. It uses only public original synthetic text and evaluates no memory capability, case, ranking or semantic correctness. This decision does not activate proposed [ADR-0009](ADR-0009-exploratory-research-boundary.md) as a general exploratory envelope or approve the native path, 144 answer positions or USD 10 budget in the [RC-005 → Mem0 packet](../experiments/rc005-native-execution-packet.md). Exact runtime observations stay in private operator records; this public decision publishes no runtime result.

## 背景与授权

Maintainer 于 2026-10-23 允许有限测试模型调用。Generation 应使用已可用的 generation entitlement，不充值、不使用收费 fallback。Embedding 应使用已可用的本地 Qwen 或 Workers AI，不充值，也不选择其他收费 provider。实际账号身份、凭据、endpoint 细节、余额与私有配置不进入本公共记录。

这是一项独立、自足的工程兼容性例外。它不是对 ADR-0009 的接受，后者仍为 **proposed**；它也不把 RC-005 执行包变成已获授权的 study。对通用 runner、adapter、service 或系统评测的既有禁止继续有效。

## 决定

### 1. 固定请求范围

协调者为首批检查选择以下累计 dispatch 预算；这些数字是本批执行选择，不是 maintainer 对以后所有范围内测试施加的限制：

- generation 总计最多 6 次请求，每次 output limit 不超过 2,048 tokens；
- embedding 总计最多 4 次请求，每批最多 8 条文本；每条都是不超过 2,000 字符的公开原创合成材料；以及
- 失败、timeout 与 malformed client dispatch 都计入各自总量。client 不做自动 retry。下游 provider 重试或 pool fallback 可能 opaque，必须记录这一限制，不能声称 dispatch 次数约束了全部 upstream attempts。

所有输入必须是公开原创合成文本。检查可以使用已有 generation entitlement，以及已有本地 Qwen 或 Workers AI embedding 路径。不得充值、选择收费 fallback 或增加其他 provider。任何目标路径缺少授权时，应停止该路径，不能扩大范围。

### 2. 只检查可观察兼容性

本检查只观察：

- 请求是否被接受，返回是否可以解析；
- 按接口声明处理普通文本与 JSON-object response forms 的情形；
- usage 与 effective model 或 service identity 是可见、缺失还是不足以归属；
- embedding 返回是否呈现向量维数与全部 finite numeric values；以及
- embedding batch 对提交的合成文本是否保持输入顺序与条数。

缺失的 usage 或 identity 字段记为 unavailable，不能靠假设补出。有效返回只能说明 transport 与 shape compatibility，不验证回答质量、memory、retrieval、retention、correction、routing、关系行为或任何受测系统。

### 3. 证据与发布边界

本检查由 operator 管理。本决定不提供公共 replay command；repository 也没有与之对应的可执行入口。若日后把 operator 报告并入公共文档，它只能写明 provider category、请求次数、纯合成输入边界、解析与可见性观察、embedding dimension、finite-value 结果、batch-order 结果和已记录失败，不能暴露私人 account、endpoint、credential、balance、route、worker 或 artifact 细节。

本文是授权记录，不是 runtime 报告。精确执行状态与观察留在私有 operator 记录，本文未采用公共 result packet；授权本身不是成功证据。

### 4. 明确排除

本决定不授权：

- memory-system、case、benchmark、semantic judgment 或 scoring run；
- RC-005 的 144-answer 计划、Mem0 安装或 ingestion、index migration 或 native system comparison；
- 通用 adapter、runner、SDK、API、service、hosted operation 或 deployment；
- 真实私人对话、personal continuity、production memory 或任何非合成 corpus；
- 公共 result packet、外部 outreach 或 operator artifact 发布；
- 超过上文所列 provider categories 的 model/provider 选择；或
- 对 release、licensing、case acceptance 或跨系统 promotion gate 的任何改变。

## 与 ADR-0009 和 RC-005 执行包的关系

ADR-0009 仍为 proposed，不授予 exploratory envelope。RC-005 执行包整体仍为 proposed、未获批准。其 OpenAI direct API 配置、具名模型设置、144 个回答位置与 USD 10 cap 是历史规划建议；对于当前方向，它们已被上文 quota-first 界限取代，不是当前 provider 或 account 的前提。未来的 native 执行包仍需单独接受，并完整对齐 provider、预算、数据与观察条件。

[ADR-0005](ADR-0005-offline-pilot-tooling.zh-CN.md) 的 scripted rehearsal 仍为离线；RC-005 input-only audit 也仍只处理输入。本兼容性例外不会把任一项扩展成 subject execution facility。

## 后果与停止规则

本检查可以建立有限的接口兼容性，并保留明确 unavailable 的证据；不能建立系统质量或研究结果。本批到所选 dispatch 上限或真实的数据、provider、支出边界时停止，并保留失败记录。Maintainer 已授予的合成材料与资源范围内，operator 可以自行选择并记录后续有限兼容性批次，不必重复索取许可。新增支出、私人资料外发、生产变更或 memory-system study 仍需各自适用的授权。

## 复查与撤回

Maintainer 可以暂停、收窄或取代本例外。实际兼容性观察不会提升 ADR-0009、RC-005 执行包、任何 case 或任何系统能力主张。日后若决定公开兼容性摘要，必须继续区分 observation、inference 与 pending evidence，并通过 repository 的公共文档检查。
