[简体中文](ADR-0004-r0-bilingual-documentation.zh-CN.md) | **English**
<!-- language: en; mirror: ADR-0004-r0-bilingual-documentation.zh-CN.md; translation-status: synchronized -->

# ADR-0004 — R0 Uses Chinese-First Bilingual Documentation

**Status:** accepted
**Scope:** public documentation and research artifacts during R0
**Accepted:** 2026-08-24

## 中文摘要

R0 以中文作为当前主要工作与社区参与语言，同时维护完整的英文公共入口。稳定的 core authority 使用英文 `.md` 与中文 `.zh-CN.md` 配对；code、schemas、IDs、CLI、failure codes、artifact filenames 与 exact source terms 保持英文。Evidence Cards、System Cards、ADRs 与 working reviews 至少提供双语摘要；locale-sensitive case 的跨语言版本是有 provenance 关联的 adaptation，不是假定语义等价的机械翻译。

## English summary

R0 uses Chinese as its primary working and community-participation language while maintaining complete English public entrypoints. Stable core authority uses paired English `.md` and Chinese `.zh-CN.md` files. Technical identifiers remain English. Evidence Cards, System Cards, ADRs, and working reviews provide at least bilingual summaries. Cross-language versions of locale-sensitive cases are provenance-linked adaptations, not presumed-equivalent translations.

## Context

Relata's present contributors primarily work in Chinese, while future international researchers, maintainers, and source readers need a durable English route. Requiring Chinese contributors to cross English-only authority creates unnecessary friction. Treating every artifact as a mechanically mirrored translation would create a different defect: case language, code-switching, private register, cue force, tokenization, and reviewer interpretation may change under translation.

## Decision

1. Chinese is the primary R0 working and community-participation language. English remains a complete public entrypoint and research surface.
2. Stable core documents use reciprocal English `.md` and Simplified Chinese `.zh-CN.md` pairs. A semantic edit to one member requires the paired member in the same change.
3. Code, schemas, field names, IDs, CLI commands, failure codes, artifact filenames, exact source terms, and `AGENTS.md` remain English. Chinese documents explain them without translating canonical identifiers.
4. Evidence Cards, System Cards, accepted ADRs, and actively maintained review documents provide bilingual summaries. They do not require duplicate long bodies when one language preserves the source or authoring context better.
5. Locale-sensitive Case Cards and Incident Seeds preserve their original locale. A cross-language version receives its own variant identity and provenance link, such as `RC-002-zh-CN` and `RC-002-en-adaptation`.
6. `tools/check_repo.py` verifies pair existence, reciprocal links, machine-readable synchronization declarations, paired Git changes, required case metadata, and Pilot 001's scope/baseline markers. It does not claim semantic translation equivalence.
7. Target Architecture Draft 0.1 remains an untranslated, non-normative historical artifact. Translating it would consume effort and risk inflating its authority.

## Consequences

- Current contributors can enter through a Chinese README and execution path without losing English interoperability.
- Stable authority gains an explicit drift contract and lightweight repository enforcement.
- Translation review remains a human responsibility; `synchronized` means the maintainers declare that the pair reflects the same current decision, not that automation proved equivalence.
- Case adaptations must record language-dependent changes rather than hiding them behind a shared case ID.

## Review and reversal gate

The required-pair set may change when audience, maintenance capacity, or artifact authority changes. Any reduction must preserve usable Chinese participation and English public access and must be recorded in the language policy and a later accepted decision when it changes this authority.
