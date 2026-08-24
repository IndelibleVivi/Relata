**简体中文** | [English](ADR-0002-vision-doc-is-non-normative.md)
<!-- language: zh-CN; mirror: ADR-0002-vision-doc-is-non-normative.md; translation-status: synchronized -->

# ADR-0002 — Target Architecture Draft 0.1 是 Non-Normative

**Status：** accepted
**Scope：** current and future work unless superseded

## 中文摘要

Target Architecture Draft 0.1 作为 historical north-star provocation 保存，不是 implementation authority。任何 code、schema、track、evaluator 或 repo split 都不能只引用 Draft 0.1 作为理由；current authority 来自 Status、Charter、Assumption Register、governance documents 与 accepted decisions。

## English summary

Target Architecture Draft 0.1 is preserved as a historical north-star provocation, not implementation authority. No code, schema, track, evaluator, or repository split may rely on the draft alone; current authority comes from the Status, Charter, Assumption Register, governance documents, and accepted decisions.

## Context

Draft 明确处于 proposed / unbuilt 状态，但 final section 却锁定了 ontology、tracks、scoring、repositories 与 infrastructure 在内的 22 项 decisions。

## Decision

在 `docs/vision/` 下保留带 authority banner 的 draft。它只作为 hypothesis inventory 与 design provocation 使用。

Current authority 由 `STATUS.md`、`CHARTER.md`、`ASSUMPTION_REGISTER.md`、governance documents 与 accepted decision records 定义。

## Consequence

任何 code、schema、track、evaluator 或 repository split 都不能只引用 Draft 0.1 作为依据。
