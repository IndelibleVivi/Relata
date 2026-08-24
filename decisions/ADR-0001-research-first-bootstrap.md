[简体中文](ADR-0001-research-first-bootstrap.zh-CN.md) | **English**
<!-- language: en; mirror: ADR-0001-research-first-bootstrap.zh-CN.md; translation-status: synchronized -->

# ADR-0001 — Begin Relata as a Research Program and Case Lab

**Status:** accepted  
**Scope:** R0 — Research Foundation

## 中文摘要

Relata 从 research program 与 Case Lab 开始，而不是先做完整 evaluation platform。R0 通过 exact-source Evidence Cards、community Incident Seeds、System Cards / Pressure Maps、Distinction Atlas、minimal synthetic cases、controls 与 evaluator calibration 来建立 evidence；implementation 只限于直接保护 case validity 与 reproducibility 的 tooling。

## English summary

Relata begins as a research program and Case Lab rather than a complete evaluation platform. R0 builds evidence through exact-source research, community incidents, system census, bounded cases, controls, and evaluator calibration. Implementation is limited to tooling that directly protects validity and reproducibility.

## Context

Target Architecture Draft 0.1 specifies a mature evaluation platform before Relata has validated its constructs, cases, architecture boundary, evaluator rubric, or community participation model.

## Decision

Relata begins with:

- exact-source Evidence Cards;
- community Incident Seeds;
- architecture System Cards and Pressure Maps;
- a Distinction Atlas;
- minimal synthetic cases and controls;
- evaluator calibration;
- evidence-backed decisions.

Implementation is limited to tooling that directly supports case validity and reproducible pilots.

## Deferred alternatives

- immediate protocol and runner implementation;
- long synthetic relationship worlds;
- hosted benchmark services;
- leaderboard and Arena;
- sealed challenge infrastructure.

## Consequence

Early progress is measured by clearer constructs, stronger cases, architecture coverage, and useful failure evidence rather than feature count.

## Reversal gate

The project may choose its first executable boundary only after the working promotion gate in `STATUS.md` is met or is explicitly revised through a later accepted decision.
