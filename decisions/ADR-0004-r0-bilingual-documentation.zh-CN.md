**简体中文** | [English](ADR-0004-r0-bilingual-documentation.md)
<!-- language: zh-CN; mirror: ADR-0004-r0-bilingual-documentation.md; translation-status: synchronized -->

# ADR-0004 — R0 采用中文优先的双语文档

**状态：** accepted
**范围：** R0 阶段的公共文档与研究 artifacts
**接受日期：** 2026-08-24

## 中文摘要

R0 以中文作为当前主要工作与社区参与语言，同时维护完整的英文公共入口。稳定的 core authority 使用英文 `.md` 与中文 `.zh-CN.md` 配对；code、schemas、IDs、CLI、failure codes、artifact filenames 与 exact source terms 保持英文。Evidence Cards、System Cards、ADRs 与 working reviews 至少提供双语摘要；locale-sensitive case 的跨语言版本是有 provenance 关联的 adaptation，不是假定语义等价的机械翻译。

## English summary

R0 uses Chinese as its primary working and community-participation language while maintaining complete English public entrypoints. Stable core authority uses paired English `.md` and Chinese `.zh-CN.md` files. Technical identifiers remain English. Evidence Cards, System Cards, ADRs, and working reviews provide at least bilingual summaries. Cross-language versions of locale-sensitive cases are provenance-linked adaptations, not presumed-equivalent translations.

## 背景

Relata 当前的主要贡献者使用中文工作；未来的国际研究者、maintainers 与 source readers 仍需要持久、完整的英文路径。要求中文贡献者先穿过一层 English-only authority 会制造不必要的 friction。但把所有 artifacts 都当成可机械镜像的翻译，也会制造另一种错误：case 的语言、code-switching、私密 register、cue 强度、tokenization 与 reviewer interpretation 都可能随语言改变。

## 决定

1. 中文是 R0 当前主要工作与社区参与语言。英文继续作为完整的公共入口与研究表面。
2. 稳定 core documents 使用互链的 English `.md` 与简体中文 `.zh-CN.md` 配对。对其中一份进行语义修改时，必须在同一次 change 中同步另一份。
3. Code、schemas、field names、IDs、CLI commands、failure codes、artifact filenames、exact source terms 与 `AGENTS.md` 保持英文。中文文档可以解释，但不翻译 canonical identifiers。
4. Evidence Cards、System Cards、accepted ADRs 与 actively maintained review documents 至少提供双语摘要。若原始 source 或作者语境更适合一种语言，不强制复制两份长正文。
5. Locale-sensitive Case Cards 与 Incident Seeds 保留 original locale。跨语言版本使用自己的 variant identity 与 provenance link，例如 `RC-002-zh-CN` 和 `RC-002-en-adaptation`。
6. `tools/check_repo.py` 检查配对存在、互链、machine-readable synchronization declaration、Git change 是否成对、Case Card metadata，以及 Pilot 001 的 scope/baseline markers。它不声称能验证翻译语义等价。
7. Target Architecture Draft 0.1 继续作为未翻译的 non-normative historical artifact。翻译它会消耗大量精力，也可能错误抬高其 authority。

## 后果

- 当前贡献者可以从中文 README 与 execution path 进入，同时不牺牲英文 interoperability。
- 稳定 authority 获得明确的 drift contract 与轻量 repo enforcement。
- Translation review 仍是人的责任；`synchronized` 表示 maintainers 声明两份文件反映同一项当前决定，不表示自动化证明了语义等价。
- Case adaptations 必须记录 language-dependent changes，不能隐藏在同一个 case ID 后面。

## Review 与 reversal gate

当 audience、maintenance capacity 或 artifact authority 改变时，required-pair set 可以调整。任何缩减都必须保留可用的中文参与路径与英文公共入口；若改变本 ADR 的 authority，还必须在 language policy 与后续 accepted decision 中记录。
