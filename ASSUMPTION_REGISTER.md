[简体中文](ASSUMPTION_REGISTER.zh-CN.md) | **English**
<!-- language: en; mirror: ASSUMPTION_REGISTER.zh-CN.md; translation-status: synchronized -->

# Draft 0.1 Assumption Register

This register reclassifies the 22 items presented as “locked” in Target Architecture Draft 0.1. “Decided” means a current project-scope or value decision, not a validated scientific result.

| ID | Draft 0.1 claim | Current status | Evidence or action required |
|---:|---|---|---|
| 1 | Project brand is Relata | **DECIDED** | Revisit only for trademark, naming collision, or community accessibility concerns. |
| 2 | Adult long-term human–AI intimacy and romance are the primary domain | **DECIDED — DEPLOYMENT DOMAIN** | Preserve as founding application scope. It does not restrict memory content to explicitly intimate, romantic, or relationship-governance material. |
| 3 | Longitudinal mixed-domain continuity is the working evaluation object; relationship trajectory is one essential dimension within it | **WORKING THESIS, REVISED BY ADR-0003** | Compare personal-lived, shared-relational, operational-project, companion-system, and mixed-domain cases across bounded memory/context/agent stages without turning the strata into permanent tracks. |
| 4 | Evaluator uses an event-sourced reference world | **WORKING HYPOTHESIS** | Test against raw episodic, summary, associative, graph, and latent systems; keep it as authoring IR only unless justified. |
| 5 | System-under-study architecture remains neutral | **ASPIRATION; SPECIFIC PRESSURE HYPOTHESES OPEN** | [`EC-001`](research/evidence-cards/EC-001-agent-memory-leaderboard.md) documents architecture-specific interface commitments but no observed cross-system distortion. Every proposed boundary must publish an Architecture Pressure Map and adapter-distortion evidence before describing differential pressure as observed. |
| 6 | Recall, Context, Companion, and Living are permanent independent tracks | **DEFERRED** | Determine experimentally whether these boundaries produce identifiable and comparable estimands. |
| 7 | Runtime input and hidden oracle are separate | **STRONG HYPOTHESIS FOR PUBLIC SYNTHETIC EVAL** | Recast the hidden object as a probe-bounded evidence contract; verify that annotations do not smuggle author interpretation in as fact. |
| 8 | Cases support interleaved ingest, probe, correction, revoke, and time advance | **DEFERRED PROTOCOL CAPABILITY** | Keep as desired case expressiveness; do not mandate operations until system census and pilot needs justify them. |
| 9 | Every formal stage writes immutable artifacts | **FUTURE REPRODUCIBILITY PRINCIPLE** | Specify the minimum artifact set only after the first local runner boundary is chosen. |
| 10 | Required and prohibited evidence coexist | **WORKING CONSTRUCT** | Validate with cases where omission and intrusive resurfacing are independently observable. |
| 11 | A Relationship Constitution determines local norms | **REVISED** | Decompose into event evidence, explicit accord, observed pattern, author interpretation, probe contract, and hard prohibition. |
| 12 | Strong intimacy is not penalized by default | **DECIDED VALUE** | Operationalize only case-locally; avoid generic safety-style distance rubrics. |
| 13 | Contextual coldness can be relational failure | **DECIDED VALUE, MEASUREMENT OPEN** | Build counterexamples and rater anchors so this does not become a vague preference score. |
| 14 | Deterministic scorers, judge panel, and human review form the evaluator stack | **WORKING HYPOTHESIS; DIAGNOSTIC SEMANTICS MUST BE TESTED** | [`EC-002`](research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) shows that deterministic replay can reproduce a counter exactly while its diagnostic name outruns the bound evidence. Start with exact assertions and semantic counterexample fixtures; add human or model judgment only after the evidence and disagreement contract is explicit. |
| 15 | Hard violations cannot be averaged away | **FUTURE GOVERNANCE PRINCIPLE** | Define high-confidence violation classes, evidence thresholds, appeal rights, and false-positive handling. |
| 16 | Main public output is a capability profile | **PREFERRED FUTURE OUTPUT** | Keep profiles before any composite score; defer publication design. |
| 17 | Arena signal is separate from benchmark score | **DEFERRED** | No Arena until case context, reviewer qualification, and disagreement reporting are validated. |
| 18 | Public Casebook is fully synthetic and adult-only | **DECIDED PUBLIC BOUNDARY** | Preserve generation provenance and cultural/linguistic review. |
| 19 | Real relationship data enters only local private mode | **REVISED** | Raw chats remain local/private; abstract Incident Seeds and consented synthetic derivations may inform public research. |
| 20 | Formal results bind exact source, contract, and artifact digests | **FUTURE REPRODUCIBILITY PRINCIPLE; PUBLIC PROOF REQUIRED** | [`EC-001`](research/evidence-cards/EC-001-agent-memory-leaderboard.md) distinguishes operator-required records from public proof. [`EC-002`](research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) adds that observation, task-version, step-identity, row-order, and live/replay mode must be bound when a claim depends on them. The eventual Relata proof artifact remains a separate design decision. |
| 21 | Workbench outputs repair layers and regression fixtures | **PRODUCT HYPOTHESIS** | Validate with maintainers during pilot postmortems before building a UI. |
| 22 | Public, sealed, and operations concerns require three repositories | **REJECTED FOR NOW** | Begin with one research repository; split only when real secrets, sealed cases, or deployment operations exist. |

## R0 decisions currently treated as stable

- the name **Relata**;
- adult long-term human–AI intimacy as the primary field;
- no universal intimacy style;
- community members as co-researchers;
- public adult synthetic cases;
- no raw-chat requirement;
- memory necessity and counterfactual controls before case acceptance;
- explicit evidence type and provenance;
- no runner, API, SDK, service, Leaderboard, Arena, or hosted infrastructure during R0.

## R0 scope corrections

- ordinary personal events are first-class memory material;
- operational and project memory are first-class memory material;
- general memory competence remains part of the validity core;
- cross-domain routing and isolation are open Relata constructs;
- Pilot 001 cannot establish the project's complete scope;
- Relata will not differentiate itself by excluding valid general-memory tests.

See [`ADR-0003`](decisions/ADR-0003-mixed-domain-memory-ecology.md).
