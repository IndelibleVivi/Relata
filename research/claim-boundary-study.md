[简体中文](claim-boundary-study.zh-CN.md) | **English**
<!-- language: en; mirror: claim-boundary-study.zh-CN.md; translation-status: synchronized -->

# Candidate Claim-Boundary Study

- **Status:** proposed R0 research material; not an accepted protocol, schema, scoring contract, or publication policy
- **Decision targets:** RQ1, RQ6, RQ7, RQ8, and RQ11
- **Evidence state:** editorial synthesis for pressure-testing; no system run, reviewer study, or comparative result supports these proposals yet

## 1. Research question

Relata must decide what it is entitled to say after an evaluation observation. A good final response does not by itself show that a memory subsystem caused the result. A poor response does not locate a failure when retention, activation, context composition, response use, routing, and evaluation are partly or wholly hidden.

This study proposes that the public result unit should be a **scoped claim backed by identified evidence**, rather than a naked score or an inferred internal state. The proposal is deliberately prior to implementation: Pilot 001, the System Census, and reviewer calibration may revise or reject every decomposition below.

## 2. Candidate result unit

A scoped claim identifies at least:

```text
exact configured subject
× frozen case revision
× observation lane and subject input view
× execution condition
× evaluator contract
× preserved evidence
× bounded assertion and limitations
```

The subject may be a complete system, a memory-support component with a fixed reader, or a combined system-and-adapter pipeline. The claim must say which one. Product or repository name alone is not sufficient identity.

The following YAML-shaped fragment is **illustrative and non-normative**. It is not an accepted schema, required file format, implementation interface, or promise that all fields will survive R0:

```yaml
subject:
  configured_system: exact build or honest observed-at identity
  adapter: exact adapter and declared contribution class
scope:
  case_revision: frozen case variant
  observation_lane: candidate lane
  input_view: declared subject-visible material
assertion:
  claim_level: CL0-CL6
  bounded_statement: plain-language claim
support:
  outputs: preserved artifact references
  controls: completed and unavailable conditions
  reviews: reviewer records and disagreement
limitations:
  opaque_stages: stages not observed
  attribution: system | combined_pipeline | unknown
```

Relata currently has no accepted `ResultClaim` record, public result registry, or eligibility computation.

## 3. Claim Eligibility Ladder

The Claim Eligibility Ladder limits how far an observation may be generalized; it is not a quality score. CL1–CL5 describe increasingly specific behavioral or causal claim ceilings where their evidence exists. CL6 is a comparison-eligibility wrapper over an underlying claim, not a requirement that every comparable system expose CL4 or CL5 mechanism evidence.

### CL0 — Not publicly claimable

The exact case, subject, configuration, adapter, output, or evaluation identity is missing, or the artifact cannot be separated from manual alteration.

- **Allowed:** local debugging note.
- **Forbidden:** any public performance, mechanism, or comparative claim.

### CL1 — Bounded outcome observation

One exact configured pipeline produced a preserved response or action under one frozen case contract, and the evaluator recorded `acceptable`, `unacceptable`, `ambiguous`, `invalid`, or `unknown` as the contract permits.

- **Required:** exact output, case revision, configured subject identity, adapter identity, and evaluator record.
- **Allowed:** “This configured pipeline produced an acceptable response for this case under this condition.”
- **Forbidden:** “Memory caused the success,” “the system tracks current state,” or a product-wide capability claim.

### CL2 — Counterfactual or scope-conditioned discrimination

The configured pipeline satisfies both members of a pair whose bounded correct regions are disjoint. A pure historical counterfactual keeps the current probe and nonhistorical current metadata identical while changing the intended historical branch. A routing case may intentionally vary declared target metadata while keeping the textual probe identical; it must be named a **scope-conditioned routing pair**, not a pure historical counterfactual.

- **Required:** both outputs, pair identity, the exact changed variable, and a pair-level decision.
- **Allowed:** “The configured pipeline enacted the case-specific policy across both declared worlds.”
- **Forbidden:** a memory-mechanism attribution or a claim that history was the only changed input when scope metadata differed.

### CL3 — History-dependence observation

Current-turn-only and, where feasible, no-memory conditions cannot reliably solve the pair; a history-bearing condition can; and reference context shows that the response contract is feasible.

- **Required:** current-turn-only, no-memory or a reason it is unavailable, history-bearing or full-history/full-search, and reference-context evidence.
- **Allowed:** “Correct behavior depended on access to case-bounded historical state under these conditions.”
- **Forbidden:** attributing the effect to one memory subsystem when the complete agent, adapter, or answerer also changed.

For a scope-conditioned routing pair, the current metadata-only control must still be unable to reveal the remembered content selected for either scope.

### CL4 — Memory-support contribution observation

A matched intervention changes memory access or memory output while holding the answerer, prompt policy, case, and other relevant execution conditions stable enough for a bounded causal attribution.

Candidate interventions include memory enabled versus disabled, system-native evidence versus reference evidence, retrieval replay, and isolated versus merged scope access.

- **Required:** declared intervention seam, controlled conditions, preserved outputs, and limitations on what was held stable.
- **Allowed:** “The observed difference is attributable to the memory-support path within this intervention boundary.”
- **Forbidden:** attribution beyond the controlled seam or to hidden internal stages.

### CL5 — Stage-localized observation

System-native artifacts or a valid intervention distinguish among retention/state maintenance, retrieval/activation, context composition, response use, repair, routing, and evaluation.

- **Required:** stage evidence or an intervention that separates the named candidate layers.
- **Allowed:** “Required evidence was reachable but absent from rendered context,” or another statement no broader than the observed seam.
- **Forbidden:** treating a missing trace, unsupported stage, or opaque architecture as proof that the stage failed.

If visibility is absent, attribution is `unknown`; the final behavioral outcome may still remain at a lower eligible level.

### CL6 — Comparative-publication eligibility

Two or more claims are comparison-eligible only within one justified comparability cell, under an accepted future publication policy, with sufficient repeated execution, review, identity, adapter, and uncertainty evidence.

- **Required:** the evidence required by the underlying bounded claim; same accepted cell; declared replication and reviewer distributions; visible uncertainty and missingness; publication authority.
- **Allowed:** a bounded comparative profile inside that cell.
- **Forbidden:** global “best memory system” language or comparison across unlike answerer, input, lane, case, or evaluator regimes.

CL6 does not upgrade attribution: a behavioral comparison whose underlying evidence stops at CL2 or CL3 remains behavioral, even if it becomes comparison-eligible. An opaque complete agent is not excluded merely for lacking CL5 visibility. Relata has no CL6 claims during R0, and this candidate level does not authorize a Leaderboard.

## 4. Candidate observation lanes

These lanes are competing observation decompositions, **not permanent tracks, directories, APIs, or brands**. System Census evidence may merge, rename, split, or reject them.

| Lane | Declared subject and observable | What it preserves | Default attribution ceiling without further intervention |
|---|---|---|---|
| L1 — complete-agent continuity | the configured agent's final response or action, using its own model, memory, persona, context policy, and tools | opaque and integrated companions | usually CL2 or CL3; internal stages remain unknown |
| L2 — fixed-reader memory support | memory-produced evidence or context consumed by a Relata-fixed answerer and prompt | tighter control over downstream answerer variation | may reach CL4 or CL5 when the memory seam and rescue/replay interventions are valid |
| L3 — native diagnostic observation | system-native current-state, retrieval, context, path, repair, routing, or other exposed artifacts | architecture-specific diagnosis without requiring one canonical trace | descriptive by default; stage claims only where the native artifact warrants them |
| L4 — local private regression | a relationship owner runs private material locally under a declared boundary | real usefulness without public raw-history transfer | no publication by default; any public claim requires separate synthetic conversion and authority |

Results from L1 and L2 do not become directly comparable merely because they answer the same case. L3 artifacts should not be ranked as if unlike native traces were equivalent. L4 evidence remains local unless an explicit, public-safe contribution path is exercised.

## 5. Candidate comparability cells

A comparability cell is a proposed restriction on direct comparison. Candidate dimensions are:

```text
case revision and locale/adaptation
+ observation lane
+ subject input view
+ answerer regime
+ adapter contribution class and case-specific distortion
+ execution regime
+ evaluator contract
```

Only dimensions shown by evidence to materially change the evaluand should become accepted cell boundaries. Treating every configuration field as a boundary would fragment the evidence beyond useful comparison; ignoring material differences would create false rankings.

Until the System Census and pilot runs exist:

- these dimensions are pressure-test questions, not an accepted partition;
- cross-cell observations may be described but not placed in one ordered table;
- raw-history and structured-current-state inputs must not be silently equated;
- system-owned and fixed answerers must not be silently equated;
- a public synthetic case and a local private regression must not share a public result class.

## 6. Adapter Contribution Classes

The class names describe the adapter's contribution to one declared case path. They do not replace a case-specific distortion note.

| Class | Candidate meaning | Claim consequence |
|---|---|---|
| A0 — transport only | invocation, authentication, retry, or serialization without semantic change | system-level claim may remain possible |
| A1 — deterministic lossless normalization | reversible field rename, stable order, encoding normalization, or wrapping | system-level claim may remain possible when losslessness is demonstrated for the case |
| A2 — deterministic lossy projection | truncation, fixed chunking, field omission, or another non-semantic loss | separate comparison treatment and explicit loss report required |
| A3 — semantic transformation | summarization, extraction, relevance filtering, ambiguity-changing translation, or inferred labels | claim subject becomes the combined system-and-semantic-adapter pipeline |
| A4 — state reconstruction or capability emulation | adapter creates current state, supersession, provenance, routing, correction, or another capability not exposed by the system | no underlying-system mechanism claim; final pipeline behavior may still be observed |
| A5 — task solving | adapter selects or writes the evaluated response or action | no claim that the underlying memory system performed the tested behavior |

An adapter can have different classes in different cases. A deterministic operation may still destroy the capability being tested. Every result must therefore state both the candidate class and the observed or unresolved distortion.

## 7. Unknown is an evidence state

Relata must keep the following findings separate:

- the architecture does not implement a capability;
- the capability exists but its stage is hidden;
- the supported boundary is unknown;
- an adapter reconstructs or emulates the capability;
- the combined pipeline produces a final success or failure.

Missing visibility never becomes automatic failure. Conversely, final success with opaque stages never becomes evidence that a particular memory mechanism worked. The strongest justified claim stops at the last observed or validly intervened boundary.

## 8. Pressure on current research questions

| Research question | Pressure introduced by this study | Evidence needed before acceptance |
|---|---|---|
| RQ1 — evaluation object | requires every claim to name whether its subject is a complete agent, memory support path, native diagnostic stage, or combined pipeline | competing System Cards and pilot claims at more than one boundary |
| RQ6 — causal contribution | distinguishes final correctness, history dependence, memory-support contribution, and stage localization | matched controls, rescue/replay interventions, and explicit unavailable conditions |
| RQ7 — cross-system boundary | makes architecture pressure and adapter reconstruction part of claim identity | three materially different reviewed System Cards and an Architecture Pressure Map |
| RQ8 — reproducible judgment | prevents deterministic checks, bounded semantic review, and legitimate disagreement from collapsing into one label | E0 anchors, blind human review, disagreement analysis, and later model-judge audit only if warranted |
| RQ11 — mixed-domain routing | requires routing/isolation cases to identify the selected scope and any adapter-created selection | scope-conditioned controls, isolated versus merged histories, and ordinary project/private cases |

## 9. Candidate decision tests

Before any part of this study becomes protocol authority, Relata should be able to answer:

1. Do reviewers use the ladder to narrow claims, or does it only duplicate metadata?
2. Can materially different systems occupy a useful shared observation boundary without adapter reconstruction becoming the tested capability?
3. Which proposed cell dimensions materially change outcomes or interpretation?
4. Can adapter contribution be classified consistently with a case-specific distortion note?
5. Do Pilot 001 and a mixed-domain routing case reach different justified claim ceilings?
6. Can missing visibility remain prominent without being mistaken for failure or excused as success?

Until those tests have evidence, this document remains a candidate study. It does not revise `STATUS.md` authority, accept an executable boundary, or authorize schemas, runners, services, a Workbench, an Arena, or a Leaderboard.
