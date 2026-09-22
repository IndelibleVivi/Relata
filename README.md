[简体中文](README.zh-CN.md) | **English**
<!-- language: en; mirror: README.zh-CN.md; translation-status: synchronized -->

# Relata

**Relata** is an open, community-grounded **frontier memory research lab**. It defines, synthesizes and critically examines agent memory, open-source architectures and the evidence for their strengths and limitations, inside and outside long-term human–AI relationships. Chinese is the primary R0 working and community language; the English entrypoint is maintained alongside it.

> What does it mean for an agent to remember, how do different systems implement it, and what enables continuity across changing tasks, lives and relationships?

## Memory ecology

General agent memory and adult long-term intimacy are both research contexts. Intimacy and romance remain a founding focus; the existing Case Lab studies ordinary personal life, shared relational experiences, operational/project decisions and artifacts, and companion/system continuity as a longitudinal mixed-domain ecology. Ordinary events do not need invented romantic symbolism to count.

[ADR-0006](decisions/ADR-0006-frontier-memory-research-lab.md) establishes this broader identity. Definition, architecture studies, comparative essays and criticism are research outputs alongside cases. The [agent-memory inquiry](research/agent-memory-inquiry.md) connects a standalone article direction, selected public AMS research and [ten bounded source studies](systems/source-studies/README.md). The [architecture atlas](systems/architecture-atlas/README.md) adds thirty source-linked SVG views and an offline interactive reader. These are research drafts, not an exhaustive survey or comparative performance results.

Relata asks what is retained, activated, admitted to context, used, repaired, or appropriately left silent. Factual recall, temporal reasoning, source fidelity, noise resistance, scope isolation and full-history/full-search controls remain valuable; their observation boundaries must be explicit.

## Current stage

**R0 — Research Foundation.** Two narrow source Evidence Cards are accepted. RC-001 is clinic-ready; RC-002/003/004 are unreviewed seeds. There are no reviewed System Cards, accepted cases, validated evaluators, real system results or rankings.

Software now includes the public repository checker and an **offline RC-002 execution rehearsal**. It runs two synthetic histories across five conditions with a deliberately scripted subject, preserving evidence and exporting a blind packet. Its tests establish plumbing behavior only. No model is called, and no semantic or capability score is generated. Exact evidence status is in [STATUS](STATUS.md).

A second offline tool prepares and verifies **18 unanswered inputs for [RC-005 / shared-work authorship](case-lab/cases/seed-005-shared-work-authorship.zh-CN.md)** and audits whether input projections erase the speaker distinction. The case remains an authored candidate with no independent human review or system evaluation. See the [input audit guide](experiments/continuity-input-audit.md).

## Why the platform is deferred

No canonical ontology, system protocol, scoring contract, benchmark release, Leaderboard, Arena, SDK, service or hosted infrastructure is accepted. The [historical architecture draft](docs/vision/relata-target-architecture-draft-0.1.md) remains non-normative; the [assumption register](ASSUMPTION_REGISTER.md) preserves its disposition.

[ADR-0005](decisions/ADR-0005-offline-pilot-tooling.md) authorizes replaceable offline pilot tooling without waiting for third-party scores. It does not authorize provider adapters, private data or public performance claims. Formal promotion gates still apply to accepted cross-system boundaries.

## Research now in motion

[EC-001](research/evidence-cards/EC-001-agent-memory-leaderboard.md) addresses AML's public boundary and causal limits. [EC-002](research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) addresses PM-Bench observation/scorer binding and records no observed step-order impact on its released corpus. Neither adopts or validates the source benchmark.

Start the local rehearsal now (Python 3.10+, standard library only). Use a new output directory on every run; its parent must already exist:

```sh
python3 -B tools/synthetic_pilot.py run --output experiments/artifacts/rc002-demo
python3 -B tools/synthetic_pilot.py verify experiments/artifacts/rc002-demo
```

The [rehearsal guide](experiments/offline-rehearsal.md) explains the five conditions, subject/evaluator views, review packet, integrity checks, errors, and limits. RC-001 human calibration, seed refinement and public-source System Cards can proceed in parallel. The broader [execution path](START_HERE.md) remains research guidance; the offline exception does not make it an accepted protocol.

## Ways to contribute

Community members participate as co-researchers. Useful contributions include exact-source [Evidence Cards](research/evidence-card-template.md), abstract [Incident Seeds](community/incident-seed-template.zh-CN.md), system-native [System Cards](systems/system-card-template.md), [case review](case-lab/README.md), and governance critique. No raw-chat contribution is required.

Consent is per contribution, not a ladder: read [consent modes](community/consent-levels.md) and [participation principles](community/participation-principles.zh-CN.md). Restricted consent-record stewardship must be settled before sensitive collection.

## Public repository and privacy

Public visibility allows inspection; it does not authorize raw private conversations, identifying consent records, credentials, restricted system details or private review material in this repository. The CLI runs bundled invented adult material only. The checker reads Git's public working set and does not recursively inspect ignored local experiment records.

Public licenses remain an [open decision](governance/licensing-decision.md). No formal release or accepted result publication is implied by this source branch.

## Repository map

[Charter](CHARTER.md), [research questions](RESEARCH_QUESTIONS.md), [status](STATUS.md), [assumptions](ASSUMPTION_REGISTER.md), [terminology](docs/terminology.md), [language policy](docs/language-policy.md), [source research](research/README.md), [systems](systems/README.md), [cases](case-lab/README.md), [community](community/participation-principles.zh-CN.md), [governance](governance/public-private-boundary.md), [decisions](decisions/README.md), and [vision history](docs/vision/README.md).

## Authority and checks

Follow STATUS, CHARTER, ASSUMPTION_REGISTER, accepted decisions, research/governance/case materials, then non-normative vision history. Run from the repository root:

```sh
python3 -B tools/check_repo.py
python3 -B -m unittest discover -s tests -v
```

Checks validate public-file structure, links, bilingual declarations and paired changes, selected case markers, and isolated execution/evidence regressions. They do not establish semantic translation equivalence, reviewer agreement, memory necessity, long-term retention or system quality.
