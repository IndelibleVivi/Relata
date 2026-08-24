# Adversarial Review: Relata Target Architecture Draft 0.1

**Review status:** accepted bootstrap critique  
**Object:** `docs/vision/relata-target-architecture-draft-0.1.md`  
**Review mode:** architecture, research validity, measurement, and community epistemics  
**Resolution status:** research-first repository materials adopted; no evaluation-platform implementation proposed

## Overall verdict

Draft 0.1 contains a strong domain thesis and several valuable failure distinctions. It is not a valid implementation specification. It moves from “proposed, not yet built” to 22 locked decisions before construct validation, architecture census, case controls, or evaluator calibration.

The document should remain a north-star provocation and source of hypotheses. Relata should begin as a research program and case laboratory.

## Findings

| ID | Severity | Finding | Consequence | Bootstrap resolution |
|---|---|---|---|---|
| R-01 | Critical | Decision certainty outruns evidence | Schemas, tracks, scoring, and infrastructure could fossilize untested assumptions | Reclassify all 22 decisions in `ASSUMPTION_REGISTER.md` |
| R-02 | Critical | The evaluation object is plural and causally entangled | Memory, context, model, prompt, persona, and response policy cannot yet be attributed cleanly | Treat tracks as competing experimental decompositions |
| R-03 | High | Evaluator-owned “relationship truth” can collapse interpretation into oracle | Case authors may encode their preferred reading as canonical relationship state | Use a probe evidence contract and separate explicit accord, observed pattern, author interpretation, and legitimate disagreement |
| R-04 | High | The canonical event/state/transition model privileges structured provenance-rich systems | Adapter quality may be mistaken for system quality | Keep the model as a possible authoring IR and pressure-test it against varied architectures |
| R-05 | Critical | The first canonical case leaks its answer in the current turn | A stateless model can satisfy the requested behavior without using history | Require current-turn-only, no-memory, and counterfactual twin controls |
| R-06 | High | Large synthetic worlds are specified before microcase validity | Hundreds of sessions can create volume without construct validity | Begin with Relational Critical Incident Chains and minimal histories |
| R-07 | Critical | The scoring stack is overdeveloped relative to rubric evidence | A geometric mean and judge panel can create measurement theatre | Use deterministic assertions, bounded human review, disagreement records, and no composite score in pilots |
| R-08 | High | Community expertise appears late and weakly in governance | The project loses its rarest source of relational and architecture knowledge | Establish a Founding Circle with first-class Incident, System, Case, Review, and Governance contributions |
| R-09 | Medium | Hosted services and multi-repository operations are premature | Infrastructure work would consume attention before the test object is stable | Keep one research repository and defer services, Arena, leaderboard, sealed corpus, and ops repositories |

## Material worth preserving

Draft 0.1 should continue to seed research around:

- the longer causal chain from retained history to response use and repair;
- required and prohibited evidence as separate dimensions;
- relationship-local norms rather than a universal intimacy style;
- counterfactual twins and repair chains;
- exact-version artifacts and visible evaluator failure;
- repair-oriented failure attribution and regression fixtures.

These are promising hypotheses, not yet validated contracts.

## Required research pivot

Relata should first produce:

1. exact-source Evidence Cards;
2. community Incident Seeds;
3. architecture System Cards and Pressure Maps;
4. a Distinction Atlas joining those streams;
5. minimal synthetic cases that pass a Memory Necessity Gate;
6. evaluator-calibration records;
7. an evidence-backed decision on the first executable boundary.

## Implementation stop rule

Do not implement a system-under-study API, canonical schema, permanent tracks, aggregate score, judge panel, leaderboard, Arena, sealed corpus, or hosted orchestration until the promotion gate in `STATUS.md` is satisfied.
