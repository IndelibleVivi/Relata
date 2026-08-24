# Evidence Card: <Exact source or object>

**Card ID:** EC-000  
**Status:** draft | reviewed | accepted | rejected | superseded  
**Author(s):**  
**Reviewer(s):**  
**Relata questions / consumers:** RQ- / D- / RC- / assumption / ADR

## 中文摘要

用简洁中文说明 exact object、version/boundary、accepted findings、关键 limits，以及本 card 明确不支持什么。

## English summary

Summarize the exact object, version and boundary, accepted findings, material limits, and what the card explicitly does not support.

## 1. Decision target

What Relata question, distinction, case, assumption, or decision could this object change? What would make the card irrelevant?

## 2. Exact object

- Public locator:
- Object type: paper | repository | dataset | specification | documentation | hosted system | other
- Exact version, commit, release, DOI, or date:
- Access date:
- Identity verified by:
- Related but separately versioned objects:
- Explicitly excluded objects:

## 3. Coverage and execution

- Files, sections, pages, samples, or routes read:
- Runtime or reproduction performed:
- Environment or configuration:
- Hosted/private/manual stages not observed:
- Material not read or not verified:

## 4. Source-stated construct

What does the exact object claim to evaluate, enable, or demonstrate? Label these statements `SOURCE-CLAIMED` and cite exact locations.

## 5. Actual observable boundary

What input does the system under study receive? What operation, context, response, action, or artifact is visible? What remains fixed, hidden, hosted, or reconstructed by an adapter?

## 6. Sample and lifecycle trace

Trace one concrete sample or case through ingestion or exposure, memory/state behavior, answer or action use, scoring or review, and result publication. Do not invent missing stages.

```text
observed input
→ observed or opaque system stage
→ returned material / action / response
→ scorer or reviewer
→ result artifact
```

## 7. Public, private, and manual seam

- Public code, data, and contracts:
- Hosted or private orchestration:
- Hidden cases or reference evidence:
- Manual review or intervention:
- Missing failure evidence:

## 8. Architecture assumptions

List assumptions about retained objects, update semantics, activation, context, state, identity, timing, system interfaces, and adapter capabilities. Mark architecture-specific conclusions.

## 9. Claim ledger

| ID | Claim | Label | Exact evidence location | Limitation / counter-evidence | Relata consumer |
|---|---|---|---|---|---|
| C-01 |  | SOURCE-CLAIMED / REPRODUCED / INFERRED / CONTRADICTED / UNVERIFIED |  |  |  |

## 10. What the evidence supports

State only conclusions supported by the exact object and declared coverage.

## 11. What it does not support

State non-reproduced claims, absent data, inaccessible behavior, unsupported generalization, and interpretive limits.

## 12. Transfer to Relata

| Relata area | Preserve | Adapt | Reject / defer | Reason |
|---|---|---|---|---|
| Construct |  |  |  |  |
| System-under-study boundary |  |  |  |  |
| Lifecycle |  |  |  |  |
| Artifacts |  |  |  |  |
| Evaluation |  |  |  |  |
| Governance |  |  |  |  |

## 13. Generated research actions

- Candidate distinction:
- Candidate counterfactual:
- Candidate baseline or control:
- Candidate architecture pressure test:
- Assumption or ADR affected:

## 14. Review decision

- Pinned identity is adequate: yes | no
- Coverage statement is honest: yes | no
- Claim labels match evidence: yes | no
- Counter-evidence or limits are visible: yes | no
- Concrete Relata consumer exists: yes | no
- Decision: accept | revise | reject
- Review notes:
- Replacement card if superseded:
