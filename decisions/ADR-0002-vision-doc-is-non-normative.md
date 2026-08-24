[简体中文](ADR-0002-vision-doc-is-non-normative.zh-CN.md) | **English**
<!-- language: en; mirror: ADR-0002-vision-doc-is-non-normative.zh-CN.md; translation-status: synchronized -->

# ADR-0002 — Target Architecture Draft 0.1 Is Non-Normative

**Status:** accepted  
**Scope:** current and future work unless superseded

## 中文摘要

Target Architecture Draft 0.1 作为 historical north-star provocation 保存，不是 implementation authority。任何 code、schema、track、evaluator 或 repo split 都不能只引用 Draft 0.1 作为理由；current authority 来自 Status、Charter、Assumption Register、governance documents 与 accepted decisions。

## English summary

Target Architecture Draft 0.1 is preserved as a historical north-star provocation, not implementation authority. No code, schema, track, evaluator, or repository split may rely on the draft alone; current authority comes from the Status, Charter, Assumption Register, governance documents, and accepted decisions.

## Context

The draft is explicitly proposed and unbuilt, yet its final section locks 22 decisions spanning ontology, tracks, scoring, repositories, and infrastructure.

## Decision

Preserve the draft under `docs/vision/` with an authority banner. Use it as a hypothesis inventory and design provocation only.

Current authority is defined by `STATUS.md`, `CHARTER.md`, `ASSUMPTION_REGISTER.md`, governance documents, and accepted decision records.

## Consequence

No code, schema, track, evaluator, or repository split may cite Draft 0.1 alone as justification.
