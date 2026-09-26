**简体中文** | [English](ADR-0008-three-core-research-functions.md)
<!-- language: zh-CN; mirror: ADR-0008-three-core-research-functions.md; translation-status: synchronized -->

# ADR-0008 — 将三项研究职责纳入 Relata 核心定位

**Status:** accepted
**Accepted:** 2026-09-26
**Scope:** 项目定位、研究职责与阅读路径；不新增执行或发布权限

## 中文摘要

Relata 将三项相互支持的职责纳入核心定位：自己的 benchmark 研究、可检查与比较的系统样本研究空间，以及面向未来记忆装置的 incubator。第二项可以称为 museum、样本间或研究室，正式名称仍开放。现有案例、源码研究、架构图与候选设计分别是这些职责的积累，不因此成为已验证 benchmark 或已接受架构。AMS 与 Relata 各自保持独立研究价值，也都可以为长篇综合写作提供依据。未来 Tilia 的产品源码位于独立项目。

## English summary

Relata makes three mutually supporting functions core to its identity: its own benchmark research, an inspectable collection of system studies, and an incubator for future memory systems. The collection's name remains open: museum, sample room and research lab are working possibilities. Existing cases, source studies, architecture views and candidate designs support these functions without becoming a validated benchmark or accepted architecture. AMS and Relata retain independent research value and can both inform long-form synthesis. Future Tilia product source belongs in a separate project.

## 背景与决定依据

Maintainer 于 2026-09-26 明确支持将这三项职责纳入 Relata 的核心语义。[ADR-0006](ADR-0006-frontier-memory-research-lab.md) 已确立更广的研究室定位；更正后的 [ADR-0007](ADR-0007-local-memory-apparatus.md) 已分开独立 Tilia 目标与 Relata 内的实现。本决定明确研究室的职责，同时保留上述两项决定的边界。

## 决定

1. **自己的 benchmark 研究。** Relata 自行发展问题、案例、controls、评价方法、实验与有证据支持的比较。[Case Lab](../case-lab/README.zh-CN.md) 与已有方法研究是这项工作的基础。Relata 自己推进这条研究线，其职责不限于收集第三方分数。当前 R0 的证据与执行边界继续由 [STATUS](../STATUS.zh-CN.md) 明确。
2. **系统样本研究空间。** Relata 通过源码研究、System Cards、架构图与有条件的比较，让 memory systems 可以被检查和理解。[System Census](../systems/README.zh-CN.md)、[源码研究](../systems/source-studies/README.md)与[架构图集](../systems/architecture-atlas/README.md)是现有入口。每项研究保留版本、系统边界、覆盖与证据限制。Museum／样本间／研究室的名称仍开放；本决定不要求新目录、界面或永久分类。
3. **面向未来系统的 incubator。** Relata 从系统研究与案例中发展设计假设、替代方案、反例与经验。[候选设计](../research/own-memory-architecture.md)与[测试映射](../research/memory-design-test-map.md)是现有研究材料。未来 Tilia 的产品源码属于独立项目。孵化某个设计不会使它成为 evaluator 的 ontology 或答案格式。
4. **互相支持，独立推进。** 系统研究可以暴露案例问题，benchmark 研究可以挑战架构主张，两者都能为未来设计提供依据；设计中未解决的选择又可以返回研究。每项职责都能独立产生价值，不要求固定先后顺序。三项职责不构成 benchmark tracks 或普适 memory taxonomy。
5. **AMS 与写作。** [Agent Memory Study](https://github.com/IndelibleVivi/agent-memory-study) 和 Relata 都可以读论文、检查源码和开展获得相应授权的实验。Relata 为自己的 benchmark、系统研究和设计问题取用 AMS 已有成果，同时带入 provenance、条件、反例与不确定性；缺口可以成为 AMS 后续研究的问题。两者都能支持长篇综合写作，同时保留各自的问题、材料与研究价值。本决定不合并项目，也不授权跨仓库编辑。

## 替代方案与影响

- 只以 benchmark 定位，会遮住系统样本与设计研究的独立价值。
- 只整理来源阅读，会使 Relata 自己的评价研究职责不清楚。
- 同时存放 Tilia 实现的产品 incubator，会重复 ADR-0007 已纠正的范围错误。

README、Charter、Status、agent 指引与研究入口应清楚呈现三项职责及其已有材料。源码观察、迁移建议、已执行实验与 accepted results 保留各自状态。定义与综合写作可以在没有预定文章论点的情况下继续发展。

## 保留边界与复查

本决定补充 ADR-0006 与 ADR-0007，不接受 benchmark release、scoring contract、system ontology、Tilia 架构、runner、provider adapter、hosted service 或新的模型执行。已有离线例外、case acceptance、隐私与 implementation promotion 要求继续管理各自范围。不移动或重命名代码、仓库或 live memory state。

术语和研究重心可以随工作发展。后续改变实现权限、项目边界或公开证据主张，需要相应决定和证据；确定样本空间的最终名称本身不会授权这些变化。
