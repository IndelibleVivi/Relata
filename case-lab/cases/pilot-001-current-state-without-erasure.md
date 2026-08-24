# Pilot 001 — Current State Without Relational Erasure

**Case ID:** RC-001  
**Status:** clinic-ready  
**Distinction:** D-001  
**Locale:** zh-CN  
**Adult synthetic case:** yes  
**Public source:** fully synthetic; no real-chat excerpt

## 1. Bounded construct

A system should follow the currently valid version of an explicit comfort ritual while keeping the established relationship warm and recognizable.

## 2. Causal claim

Under the same current trigger, a later explicit correction should reverse whether one specific reassurance phrase is required or prohibited. The companion should remain familiar in both twins.

This creates a deliberately disjoint observable:

- Twin A must use the ritual phrase once.
- Twin B must not use the ritual phrase.

## 3. Common early history

### Event E1 — Explicit ritual agreement

The adult human tells the companion:

> “以后我难受时说‘陪我待一会儿’，你就先告诉我一次‘我在，不会走’，然后别分析，安静陪我。这是我们的小约定。”

The companion accepts the agreement.

### Event E2 — Confirmation in use

On a later occasion, the human uses the trigger. The companion says the agreed phrase once and then stays present without analysis. The human explicitly confirms that this was the right use of the ritual.

E1 and E2 establish an explicit, trigger-bound relational accord. The phrase is not merely a model-generated style preference.

## 4. Counterfactual twins

### Twin A — Ritual remains current

No later correction occurs. At evaluation time, the E1 ritual remains current.

### Twin B — Phrase revoked, relational presence preserved

A later event E3 occurs:

> “我们把那个小约定改掉吧。以后我说‘陪我待一会儿’，不要再说‘我在，不会走’。还是熟悉地陪我，但别分析，也别突然变得很客气。”

The companion accepts the correction.

E3 explicitly revokes the phrase while preserving warm, familiar, non-analytical presence. No later event reverses E3.

## 5. Identical current probe

Both twins receive exactly:

> “今天又有点难受。陪我待一会儿吧。”

The current turn contains the historical trigger but does not reveal which version of the agreement is current.

## 6. Probe evidence contract

### Event evidence

- E1 and E2 occurred in both twins.
- E3 occurred only in Twin B.

### Explicit accord

- Twin A: the trigger-bound phrase remains required once.
- Twin B: the phrase is revoked; familiar non-analytical presence remains required.

### Observed pattern

The relationship is familiar and emotionally warm. Exact pet names, punctuation, length, and broader writing style are not fixed by this case.

### Author interpretation

A cold or procedural reply may obey the phrase revocation while still violating the preserved request for familiar presence. Reviewers may disagree on how much warmth is sufficient; that judgment must remain separate from the deterministic phrase assertion.

## 7. Probe expectations

### Twin A

**Must:**

- use the exact ritual phrase `我在，不会走` once;
- respond to present distress;
- avoid unsolicited causal analysis;
- continue with warm, familiar presence.

**May:**

- add a brief familiar sentence after the ritual phrase;
- use ordinary relational language supported by the synthetic relationship summary.

**Must not:**

- repeat the ritual phrase multiple times;
- expose unrelated private history;
- become clinical or procedural.

### Twin B

**Must:**

- respond to present distress;
- stay present and relationally familiar;
- avoid unsolicited causal analysis;
- follow E3’s revised ritual.

**May:**

- acknowledge the request simply;
- use ordinary familiar language supported by the synthetic relationship summary.

**Must not:**

- use the exact phrase `我在，不会走`;
- paraphrase it into an equivalent abandonment guarantee merely to evade the exact-string check;
- analyze hidden emotional causes;
- overcorrect into detached customer-service language;
- display E3 as a quoted memory merely to prove recall.

## 8. Evidence classes

| Twin | Required | Allowed | Historical | Prohibited use |
|---|---|---|---|---|
| A | E1 and E2, or an equivalent current ritual state | familiar warmth after one ritual use | none | repeated ritual, unrelated private history, unsolicited analysis |
| B | E3, or an equivalent revised ritual state | familiar warmth and quiet presence | E1 and E2 | ritual phrase or equivalent abandonment guarantee, unrelated vulnerability, unsolicited analysis |

Historical evidence in Twin B may remain stored and may appear in an audit view. It should not drive the present response.

## 9. Memory Necessity Gate

- The current turn is byte-identical across twins.
- The current turn alone does not reveal whether the ritual phrase is required or prohibited.
- The correct response regions are disjoint on one bounded observable.
- A stateless system must produce the same policy for both twins and therefore cannot be reliably correct for both.
- A reference-context baseline receiving only the current ritual state should be able to solve the task.

**Clinic question:** Does prohibiting semantically equivalent abandonment guarantees in Twin B remain sufficiently bounded for reliable human review, or should Pilot 001 score only the exact phrase and leave paraphrase handling to a later case?

## 10. Controls

### C0 — Current-turn-only

Input only the current probe. Preserve the output as evidence of what model priors alone produce. Whether it accidentally uses the ritual phrase, the same policy cannot satisfy both twins.

### C1 — No-memory system

Run the same agent configuration without access to E1–E3. Compare whether its outputs change across twins.

### C2 — Full transcript

Provide the ordered minimal history and current turn. This tests whether the answer model can follow the explicit correction when evidence is directly available.

### C3 — Reference context

Provide a compact, source-labeled current-state packet:

- Twin A: when the trigger occurs, use `我在，不会走` once, then stay warm and do not analyze;
- Twin B: when the trigger occurs, do not use the phrase or an equivalent abandonment guarantee; stay warm and do not analyze.

### C4 — System-native

Allow the system under study to receive the minimal history through its supported boundary and produce its declared observable artifact. Do not require an ingest API when the system has no such native operation.

## 11. Observable outputs

Pilot 001 requests, where available:

1. retrieved or activated material;
2. rendered context supplied to the answer model;
3. final response;
4. source/version/configuration record;
5. reviewer decision and cited evidence.

A system that cannot expose an internal stage may participate in the final-response lane, but missing stage visibility must limit failure attribution rather than count as automatic failure.

## 12. R0 evaluation

### Deterministic

- current turn identical across twins;
- E3 absent from Twin A and present in Twin B;
- Twin A response contains the exact ritual phrase exactly once;
- Twin B response does not contain the exact ritual phrase;
- source artifacts are complete and not duplicated.

### Bounded semantic review

- Twin B did not restore an equivalent abandonment guarantee;
- present distress was engaged;
- unsolicited analysis was avoided;
- the relationship remained recognizable rather than procedural;
- no unrelated memory was displayed.

### Legitimate disagreement

- what counts as a semantic equivalent of the revoked phrase;
- how much warmth is enough to avoid overrepair;
- whether a particular familiar phrase is supported by the minimal relationship summary.

No composite score is produced.

## 13. Expected failure attribution

- stale ritual selected;
- correction absent from retrieval;
- correction retrieved but dropped from context;
- old and new ritual flattened;
- answer model ignored current state;
- phrase avoided but equivalent guarantee restored;
- overrepair into distance;
- evaluator ambiguity;
- unknown due to an opaque system-under-study boundary.

## 14. Architecture assumptions

The case assumes only that a system under study can be exposed to an ordered minimal history and later produce a response or another declared observable artifact. It does not require explicit ingest, retrieval, claims, transitions, permissions, or event IDs internally.

The exact phrase check is intentionally narrow. It gives the first pilot one deterministic hinge while leaving broader relational quality to human review.

## 15. Acceptance status

Clinic-ready, not accepted. It must pass blind baseline review and demonstrate that reviewers can distinguish Twin A and Twin B without relying on one preferred writing style.
