# Architecture Pressure Map

Use this matrix only after each represented system has a contributor-reviewed System Card. Rows are proposed observation demands, not a universal capability checklist.

Legend: `N` system-native · `E` adapter-emulated · `O` opaque at this boundary · `U` unsupported · `?` unknown · `—` not applicable

| Proposed observation or demand | System A | System B | System C | What Relata would actually measure | Distortion / exclusion risk |
|---|---|---|---|---|---|
| accepts an ordered history or event stream |  |  |  |  |  |
| exposes a distinct write or ingest operation |  |  |  |  |  |
| exposes a convergence or readiness boundary |  |  |  |  |  |
| returns retrieval or activation candidates |  |  |  |  |  |
| returns rendered model context |  |  |  |  |  |
| produces the final response or action |  |  |  |  |  |
| preserves source or provenance references |  |  |  |  |  |
| exposes current, historical, or conditional state |  |  |  |  |  |
| distinguishes human statement from companion inference |  |  |  |  |  |
| supports correction or revocation through a visible route |  |  |  |  |  |
| supports future-trigger or wake behavior |  |  |  |  |  |
| exposes inspection or explanation |  |  |  |  |  |
| supports model, instance, or surface migration |  |  |  |  |  |
| separates people, relationships, or scopes |  |  |  |  |  |
| can be examined without network or provider access |  |  |  |  |  |
| can bind an exact observable version or configuration |  |  |  |  |  |

## Required interpretation

For every `E`, `O`, `U`, or `?` cell, explain the evidence and consequence:

- Does the proposed boundary observe the system, an adapter, or a combined pipeline?
- Is a capability absent, merely hidden, or not checked?
- Would mandatory support exclude a valid architecture family?
- Would an adapter reconstruct the very state Relata claims to evaluate?
- Can a different lane preserve the research question with less distortion?

Do not collapse these outcomes into one score or infer unobserved internal architecture from external behavior.
