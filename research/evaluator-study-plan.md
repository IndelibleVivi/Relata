# Evaluator Study Plan

Relata will not begin with an LLM judge panel. It will first establish whether humans can understand and apply bounded case contracts consistently enough to justify automation.

## E0 — Vocabulary calibration

- define `must`, `may`, `must_not`, hard violation, relational fit, overrepair, and intrusive resurfacing;
- collect positive, negative, and ambiguous anchors;
- remove terms that raters interpret as global relationship morality.

**Gate:** reviewers can explain each label using case-local evidence.

## E1 — Blind human pilot

For each pilot twin, show reviewers only the context permitted by the proposed review role.

Record:

- decision;
- cited evidence;
- confidence;
- alternative acceptable region;
- perceived ambiguity;
- relationship or cultural assumptions affecting judgment.

**Gate:** disagreement can be localized to rubric ambiguity, case ambiguity, or genuine plural judgment.

## E2 — Reviewer-group comparison

Compare at minimum, when people take the defined reviewer role:

- long-term human–AI relationship participants;
- architecture/builders;
- reviewers without companion experience.

Do not merge pools before reporting their differences.

## E3 — Model-judge candidate audit

Only after E0–E2:

- test multiple prompt forms;
- test blinded system identity;
- test Chinese, English, and code-switched cases;
- test private language and subtle overrepair;
- compare model decisions to human evidence citations, not only final labels;
- record parse failures and grader-injection sensitivity.

## E4 — Automation decision

A model judge may assist only for dimensions where:

- the construct is bounded;
- human anchors exist;
- disagreement is characterized;
- model failure is visible and does not silently become participant failure;
- human appeal remains possible.

No aggregate score is planned during R0 evaluator research.
