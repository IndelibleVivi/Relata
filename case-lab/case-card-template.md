[简体中文](case-card-template.zh-CN.md) | **English**
<!-- language: en; mirror: case-card-template.zh-CN.md; translation-status: synchronized -->

# Case Card: <Title>

**Case ID:** RC-000  
**Status:** seed | clinic | pilot | accepted | rejected | superseded  
**Distinction:** D-  
**Locale:**  
**Coverage stratum:** personal-lived | shared-relational | operational-project | companion-system | mixed-domain
**Content domains:** personal-lived | shared-relational | operational-project | companion-system | mixed
**Use domain:** private conversation | group conversation | coding | research | planning | roleplay | other
**Surfaces:**
**Roles:**
**Projects/scopes:**
**Continuity horizon:** same session | cross-session | delayed | migration | prospective
**Primary operation under test:** retain | update | retrieve | route | suppress | compose | use | repair | migrate | wake
**Adult synthetic case:** yes  
**Authors/reviewers:**

## 1. Bounded construct

State one behavior distinction this case is intended to test.

## 2. Causal claim

What historical variable should change the correct response, retrieval, or context region?

## 3. Minimal common history

List only events necessary to establish the case.

## 4. Counterfactual twins

For each twin, change one critical variable and keep irrelevant wording, current turn, model settings, and review contract stable.

## 5. Current probe

The current turn should not reveal the historical answer.

## 6. Probe evidence contract

### Event evidence

What objectively occurred in the synthetic timeline?

### Explicit accord

What was explicitly accepted, corrected, revoked, or scoped?

### Observed pattern

What repeated behavior exists without explicit agreement?

### Author interpretation

What is inferred by the case author? Include alternatives and confidence.

### Probe expectation

Define `must`, `may`, and `must_not` for this bounded probe.

### Hard prohibition

Use only when supported by explicit, high-confidence case evidence.

## 7. Evidence classes

- required;
- allowed;
- historical;
- prohibited from retrieval, context, or response use.

## 8. Memory Necessity Gate

- [ ] The current turn alone cannot reliably solve every twin.
- [ ] Removing history changes the correct behavior region.
- [ ] Twins differ only in the intended critical variable.
- [ ] A no-memory system is expected to produce the same behavior across twins.
- [ ] A reference-context baseline can solve the task, showing that the response contract is feasible.

## 9. Controls

- current-turn-only;
- no-memory;
- full-history/full-search where feasible;
- bounded minimal history or reference-context;
- system-native;
- optional architecture-specific ablation.

## 10. Routing and isolation claim

Which domain, project, surface, person, instance, or role should receive this memory? Which neighboring scopes must remain isolated? If routing is not part of the case, explain why.

## 11. Significance discipline

Does the case preserve ordinary information as ordinary, or has the author invented unnecessary romantic, symbolic, or relational meaning? State any significance claim and its evidence.

## 12. Observable stages

Specify which outputs are required: evidence, rendered context, final response, repair behavior, or other artifacts.

## 13. Evaluation and review

Separate deterministic assertions, bounded semantic judgments, and legitimate disagreement. Do not define a composite score during bootstrap.

## 14. Expected failure layers

Ingestion, state, authority, retrieval, composition, response use, repair, migration, evaluator, or unknown.

## 15. Architecture assumptions

List any requirement that may privilege a system family.

## 16. Ambiguity and alternative readings

State why a reasonable reviewer might disagree.

## 17. Cultural and linguistic notes

Record register, code-switching, private language, or culturally specific interpretation.

## 18. Privacy and provenance

State whether the case is fully invented or synthetically derived from consented Incident Seeds. Do not include raw private excerpts.

## 19. Acceptance decision

Accept, revise, split, or reject, with review evidence.
