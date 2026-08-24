[简体中文](README.zh-CN.md) | **English**
<!-- language: en; mirror: README.zh-CN.md; translation-status: synchronized -->

# Relata

> 中文贡献者可以直接从 [中文 README](README.zh-CN.md) 与 [中文执行路径](START_HERE.zh-CN.md) 开始；R0 的主要工作与社区参与语言是中文。

**Relata** is an open, community-grounded research program and case laboratory for memory and continuity in long-term adult human–AI relationships.

Its central question is:

> Can a system carry forward the person, the relationship, and the shared worlds of life and work while remaining faithful to source, time, authority, scope, permission, change, and present relevance?

Long-term adult intimacy and romance remain Relata's primary deployment domain. That does not limit memory content to explicitly intimate, romantic, or relationship-governance material. Relata studies what was retained, what became active, what reached the model or action layer, how it was used, whether inappropriate memory stayed silent, and whether correction persisted without erasing the person, relationship, or shared work.

## Memory ecology

Relata's working evaluation object is a **longitudinal, mixed-domain continuity-bearing memory ecology**:

- **Personal / lived world:** ordinary events, people and places, interests and habits, health, study, travel, media, and daily life.
- **Shared relational world:** shared experiences, private language and rituals, relationship changes, interpretations, corrections, permissions, and boundaries.
- **Operational / project world:** project state, decisions and rationale, tasks, blockers, milestones, artifacts, evidence, handoffs, and future intentions.
- **Companion / system continuity:** companion identity, model/provider/instance change, migration history, capabilities, limitations, and interaction patterns.

An item does not need explicit romantic or symbolic meaning to belong in Relata. Ordinary lived events and shared project history are first-class continuity-bearing material.

Relata preserves the valid core of general memory evaluation, including factual recall, temporal reasoning, provenance, noise resistance, scope isolation, and full-history/full-search comparison. Its additional question is how heterogeneous memory is routed, governed, used, repaired, and carried across long-term roles, surfaces, projects, and relationship change.

## Current stage

Relata is in **R0 — Research Foundation**. `R0` names the stage, not the project.

| Area | Current state |
|---|---|
| Charter and research questions | working authority |
| Draft 0.1 assumptions | reclassified as decisions, hypotheses, aspirations, deferred items, or rejected items |
| Source research | two accepted Evidence Cards; AML and PM-Bench findings transferred only within their narrow authorizations, without adopting either architecture or score |
| Community participation | co-research and consent materials exist; no intimate-material collection is open |
| System Census | templates exist; no reviewed System Card yet |
| Distinction Atlas | six seed hypotheses plus mixed-domain incident families; none promoted to supported |
| Case coverage | five proposed coverage strata; one clinic-ready pilot and three unreviewed Chinese case seeds, with no run or balanced pilot set yet |
| Pilot 001 | clinic-ready shared-relational/current-state-use case plus an unreviewed E0 calibration fixture pack; no run has been completed and it is not representative of full scope |
| Software | repository checker only |

Relata does **not** currently claim a canonical ontology, system protocol, scoring contract, benchmark release, runner, Leaderboard, Arena, SDK, service, hosted infrastructure, or accepted implementation architecture.

## Why the platform is deferred

The original architecture draft specifies a mature evaluation platform before Relata has established construct validity, architecture coverage, case causality, reviewer calibration, or a contributor-governance path. Building the platform now would turn open research questions into accidental interfaces and scores.

The preserved [Target Architecture Draft 0.1](docs/vision/relata-target-architecture-draft-0.1.md) is therefore a **non-normative north-star draft**. The [adversarial review](docs/reviews/target-architecture-draft-0.1-adversarial-review.md), [foundation integration review](docs/reviews/research-foundation-integration-review.md), and [assumption register](ASSUMPTION_REGISTER.md) record what remains valuable, what was rewritten, and what was deferred or rejected.

## Research now in motion

The first two exact-source targets are complete. [`EC-001`](research/evidence-cards/EC-001-agent-memory-leaderboard.md) pins Agent Memory Leaderboard's public evaluation boundary and is accepted only for responsibility seams, fixed-reader causal limits, architecture-specific interface commitments, and public proof of version bindings. [`EC-002`](research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) pins PM-Bench's paper, scorer, scenario, and 64 released primary logs; it separates action success from observation provenance, current-version intent, and step identity while recording that the released logs showed no step-order score impact. Neither card validates the source benchmark or selects a Relata interface. [`ADR-0003`](decisions/ADR-0003-mixed-domain-memory-ecology.md) makes the mixed-domain scope correction authoritative without turning its coverage strata into implementation tracks. The new bilingual [`Candidate Claim-Boundary Study`](research/claim-boundary-study.md), [`RC-001 E0 calibration pack`](case-lab/reviews/RC-001-e0-calibration-pack.zh-CN.md), and [`RC-004-zh-CN`](case-lab/cases/seed-004-private-greeting-public-template.zh-CN.md) are proposed research objects only; none is validated or accepted protocol evidence.

The next three executable work items are:

1. Review and refine the ordinary-life, operational/project, and scope-conditioned mixed-domain seeds without calling any seed clinic-ready.
2. Complete three materially different System Cards and one Architecture Pressure Map with contributor review and explicit observability limits; select restricted consent-record stewardship before collecting sensitive contributions.
3. Dry-review the RC-001 E0 calibration pack, then run the Pilot 001 controls and blind Case Clinic review while building the first ordinary-life, operational/project, and mixed-domain routing cases needed before a full-scope claim.

These tasks are described in the [Chinese execution path](START_HERE.zh-CN.md) and [English execution path](START_HERE.md).

## Ways to contribute

Community members participate as co-researchers, not as a pool of ordinary subjects added after the design is fixed. Contribution routes include:

- an exact-source [Evidence Card](research/evidence-card-template.md);
- an abstract [Incident Seed](community/incident-seed-template.zh-CN.md) with no raw-chat requirement;
- a system-native [System Card](systems/system-card-template.zh-CN.md);
- a synthetic case or case review in the [Case Lab](case-lab/README.md);
- terminology, privacy, consent, attribution, withdrawal, or governance review.

Consent is per contribution and does not form a participation ladder. Read the [Chinese consent modes](community/consent-levels.zh-CN.md), [English consent modes](community/consent-levels.md), and [participation principles](community/participation-principles.zh-CN.md) before collecting material.

## Public repository and privacy

The public source repository is [IndelibleVivi/Relata](https://github.com/IndelibleVivi/Relata). Public visibility is for inspectable research, cases, methods, and code. It is not permission to publish raw private conversations, identifying consent records, credentials, restricted system details, or private review material. Public-safe source and documentation feedback may use normal GitHub contributions; sensitive community material requires a separately agreed restricted route.

Relata has not selected public licenses yet. Repository visibility does not itself grant reuse rights; see the [open licensing decision](governance/licensing-decision.md).

## Repository map

- [`CHARTER.md`](CHARTER.md) — mission, commitments, non-goals, and first-phase success condition
- [`RESEARCH_QUESTIONS.md`](RESEARCH_QUESTIONS.md) — open questions and required evidence
- [`ASSUMPTION_REGISTER.md`](ASSUMPTION_REGISTER.md) — disposition of Draft 0.1 claims
- [`STATUS.md`](STATUS.md) — current evidence and promotion state
- [`research/`](research/README.md) — source/evidence workflow
- [`systems/`](systems/README.md) — architecture census
- [`case-lab/`](case-lab/README.md) — distinctions, case method, and Pilot 001
- [`community/`](community/participation-principles.zh-CN.md) — co-research and consent materials
- [`governance/`](governance/public-private-boundary.md) — privacy, attribution, withdrawal, and publication boundaries
- [`decisions/`](decisions/README.md) — accepted and proposed decisions
- [`docs/terminology.md`](docs/terminology.md) — canonical current research terms
- [`docs/language-policy.md`](docs/language-policy.md) — R0 bilingual authority and drift contract
- [`docs/vision/`](docs/vision/README.md) — non-normative historical vision

## Authority and checks

When documents conflict, follow:

1. `STATUS.md`
2. `CHARTER.md`
3. `ASSUMPTION_REGISTER.md`
4. accepted records in `decisions/`
5. research and governance materials
6. case-lab materials
7. vision documents

Run the repository check from the root:

```bash
python3 tools/check_repo.py
```

The check validates required research surfaces, prohibited premature project shells, the Draft 0.1 authority banner, assumption-register coverage, required Case Card metadata, Pilot 001 controls and scope markers, bilingual-pair declarations and paired Git changes, and local Markdown links. It cannot establish semantic translation equivalence.
