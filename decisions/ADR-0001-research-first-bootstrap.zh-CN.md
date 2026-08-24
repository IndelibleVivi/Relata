**简体中文** | [English](ADR-0001-research-first-bootstrap.md)
<!-- language: zh-CN; mirror: ADR-0001-research-first-bootstrap.md; translation-status: synchronized -->

# ADR-0001 — Relata 从 Research Program 与 Case Lab 开始

**Status：** accepted
**Scope：** R0 — Research Foundation

## 中文摘要

Relata 从 research program 与 Case Lab 开始，而不是先做完整 evaluation platform。R0 通过 exact-source Evidence Cards、community Incident Seeds、System Cards / Pressure Maps、Distinction Atlas、minimal synthetic cases、controls 与 evaluator calibration 来建立 evidence；implementation 只限于直接保护 case validity 与 reproducibility 的 tooling。

## English summary

Relata begins as a research program and Case Lab rather than a complete evaluation platform. R0 builds evidence through exact-source research, community incidents, system census, bounded cases, controls, and evaluator calibration. Implementation is limited to tooling that directly protects validity and reproducibility.

## Context

Target Architecture Draft 0.1 在 Relata 尚未验证 constructs、cases、architecture boundary、evaluator rubric 或 community participation model 前，就指定了一套成熟 evaluation platform。

## Decision

Relata 从以下工作开始：

- exact-source Evidence Cards；
- community Incident Seeds；
- architecture System Cards 与 Pressure Maps；
- Distinction Atlas；
- minimal synthetic cases 与 controls；
- evaluator calibration；
- evidence-backed decisions。

Implementation 只包括直接支持 case validity 与 reproducible pilots 的 tooling。

## Deferred alternatives

- 立即实现 protocol 与 runner；
- long synthetic relationship worlds；
- hosted benchmark services；
- Leaderboard 与 Arena；
- sealed challenge infrastructure。

## Consequence

Early progress 以更清晰的 constructs、更强的 cases、architecture coverage 与 useful failure evidence 衡量，而不是 feature count。

## Reversal gate

只有 `STATUS.md` 中 working promotion gate 满足，或后续 accepted decision 明确修改该 gate，project 才能选择第一条 executable boundary。
