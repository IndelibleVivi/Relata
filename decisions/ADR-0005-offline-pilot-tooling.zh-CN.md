**简体中文** | [English](ADR-0005-offline-pilot-tooling.md)
<!-- language: zh-CN; mirror: ADR-0005-offline-pilot-tooling.md; translation-status: synchronized -->

# ADR-0005 — 允许可替换的离线试验工具

**Status:** 2026-09-09 maintainer 已授权的工程范围；未接受研究协议
**Scope:** 内置公开合成材料的执行演练与 repository checks

## 决定

Maintainer 在源码审查后授权继续实现，在独立分支交付，不合并、不部署、不操作真实数据、不调用付费模型。依据 ADR-0001 对 validity 与 reproducibility tooling 的许可，Relata 可以用明确标识的脚本替身执行内置 RC-002 transport fixture，保存步骤、输入、输出，验证证据绑定，并导出盲审包。

这项范围不等待别人提交分数、外部 System Cards 或人工校准完成。它不开放通用 agent API、provider integration、私人数据导入、公开分数登记或 benchmark runner。脚本接口和本地证据格式都是可替换的工程细节，尚未成为跨系统 observation 或 scoring contract。

## 边界

CLI 只接纳内置、虚构、成年人的材料。不需要凭据、模型调用、外部命令、任意 adapters 或私人材料。所有产物必须标识为 scripted plumbing rehearsal。这些测试不提升 case 状态、六项尚无支持的 distinction hypotheses、reviewer calibration 或系统能力证据。

Promotion gate 继续约束 accepted cross-system implementation boundary 与公开研究结论。正式协议、模型执行、私人 regression、release 和更广泛的架构比较仍需各自的决定或授权，不能借本例外进入 R0。

## 结果与撤回

首个实现限定为一个本地脚本和一个脚本替身，无第三方依赖，不自动 retry/resume。每次尝试使用新输出目录；中断或损坏的证据会被保留或拒绝，不能静默升级为完成。

公开源码审查形成的系统描述、其他 cases 和人工 review 可以并行。此处不建立新的 evidence count 或 scientific sample-size 门槛。当 pilot evidence 支持更好的执行边界时，可以移除或替换这些工具，保留旧源码身份和旧 run records。
