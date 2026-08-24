# Relata Source and Evidence Workflow

Relata research is organized around decisions and cases, not a pile of summaries. A source name, paper title, repository, or benchmark mentioned in Draft 0.1 carries no current evidentiary weight until the exact object is pinned and reviewed in an Evidence Card.

## Current evidence spine

| Card | Status | Current use |
|---|---|---|
| [`EC-001 — Agent Memory Leaderboard public evaluation boundary`](evidence-cards/EC-001-agent-memory-leaderboard.md) | accepted | narrow use for RQ1/RQ6/RQ7, Assumptions 5/20, and System Census pressure questions; no AML score or validity endorsement |
| [`EC-002 — PM-Bench observation and scorer binding`](evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) | accepted | narrow use for RQ6/RQ8, D-006, and Assumptions 14/20; no PM-Bench score invalidation, model-failure label, or interface adoption |

## Candidate methodology studies

| Study | Status | Current use |
|---|---|---|
| [`Candidate Claim-Boundary Study`](claim-boundary-study.md) ([中文](claim-boundary-study.zh-CN.md)) | proposed; unvalidated | pressure-test the distinction between bounded outcomes, history dependence, memory contribution, stage localization, and comparison eligibility across RQ1/RQ6/RQ7/RQ8/RQ11; no accepted result schema, observation lane, adapter threshold, or publication policy follows |

Candidate methodology is editorial research material, not accepted evidence that a method works. It must be revised or accepted through the decision and review path named in the study before it can govern a run or public claim.

## Evidence classes

| Class | Meaning | Typical artifact |
|---|---|---|
| Exact-source | Directly supported by a pinned paper, repository, dataset, specification, or platform contract | Evidence Card |
| Reproduced observation | Observed by running or tracing the exact object under recorded conditions | Evidence Card / probe record |
| Community-grounded | Abstracted from a contributor’s lived relational or operational experience under recorded permissions | Incident Seed |
| System-observed | Derived from an actual architecture, supported interface, trace, or contributor-reviewed description | System Card / probe report |
| Synthetic-case | Produced inside a controlled adult synthetic case | Case Card / pilot artifact |
| Human judgment | A reviewer’s bounded assessment under a stated role and evidence view | review record |
| Editorial inference | Project interpretation joining other evidence | distinction note / decision record |
| Unresolved | Missing, opaque, contradictory, or not yet checked | explicit open item |

Editorial inference must never be presented as source fact or community testimony.

## Claim labels inside research artifacts

Use one of these labels when the status is not obvious:

- `SOURCE-CLAIMED` — the exact source says it;
- `REPRODUCED` — Relata observed it under recorded conditions;
- `INFERRED` — the author interprets evidence;
- `CONTRADICTED` — relevant evidence conflicts;
- `UNVERIFIED` — existence, scope, or behavior has not been checked;
- `OUT-OF-SCOPE` — deliberately not examined.

`SOURCE-CLAIMED` is not the same as `REPRODUCED`. An inaccessible hosted stage remains `UNVERIFIED`, not silently inferred from public code.

## Operational workflow

### 1. Name the decision target

Before collecting sources, state which research question, distinction, case, assumption, or proposed decision could change. A source with no decision target stays in `source-map.md` rather than becoming an Evidence Card.

### 2. Pin the exact object

Record the public locator and the smallest identity that makes the object stable: paper version or DOI, repository commit or release, dataset version, documentation revision, and access date. Separate public source, hosted behavior, and third-party description.

### 3. Declare coverage before interpretation

Record which files, sections, samples, scripts, or runtime paths were read or executed, and what was not inspected. Do not imply whole-project review from a README, paper abstract, or one successful command.

### 4. Trace one real lifecycle

For an evaluation or software system, follow at least one sample through its actual observable path: input, memory or state operation, answer/action consumer, scoring or review, and result artifact. Mark hidden stages and manual intervention.

### 5. Build the claim ledger

For each claim transferred to Relata, record its label, exact supporting location, limitations, and affected project artifact. Preserve counter-evidence and architecture-specific assumptions.

### 6. Review source fidelity

A reviewer checks that the pinned object exists, coverage is stated honestly, source claims are not stronger than the evidence, and inference is marked. Reproduction is required only when a claim depends on runtime behavior and the object is runnable; otherwise the limitation stays visible.

### 7. Transfer, do not merely summarize

An accepted Evidence Card must change or support at least one of:

- a research question or assumption;
- a Distinction Atlas entry;
- a case or control;
- a System Census dimension;
- a decision record;
- an explicit rejection of a proposed mechanism.

### 8. Supersede explicitly

If the source, interpretation, or project decision changes, mark the old card `superseded`, link its replacement, and update every current artifact that relied on it. Do not silently rewrite historical evidence.

## Artifact path

```text
source-map candidate
→ pinned Evidence Card draft
→ source-fidelity review
→ accepted or rejected card
→ distinction / case / assumption / decision
→ pilot evidence
```

Use [`evidence-card-template.md`](evidence-card-template.md) and store populated cards in [`evidence-cards/`](evidence-cards/README.md).

## Acceptance minimum

An Evidence Card is not `accepted` unless it identifies the exact object, declares read/execution coverage, separates source claims from observation and inference, records unavailable boundaries, links a concrete Relata consumer, and includes a review decision.
