# Relata Research Foundation: Start Here

This is the operational path from the non-normative Target Architecture Draft 0.1 to evidence-backed research and cases.

## Foundation now present

- [Charter](CHARTER.md), [research questions](RESEARCH_QUESTIONS.md), and [assumption register](ASSUMPTION_REGISTER.md)
- [adversarial architecture review](docs/reviews/target-architecture-draft-0.1-adversarial-review.md)
- [source/evidence workflow](research/README.md) and Evidence Card template
- community co-research, consent, attribution, and withdrawal materials
- System Census and Architecture Pressure Map templates
- Distinction Atlas, case method, Pilot 001, and a manual pilot plan
- repository structure and Markdown-link checker

First run:

```bash
python3 tools/check_repo.py
```

## Work item 1 — Evidence Card 001 accepted

- [x] Separate and identify the pinned AML GitHub source, pinned Hugging Face result snapshot, and dated mutable hosted observations.
- [x] Confirm that no prior local AML audit artifact existed; import no inherited AML conclusion.
- [x] Separate source claims, reproduced observations, inferences, contradictions, and unverified boundaries in [`EC-001`](research/evidence-cards/EC-001-agent-memory-leaderboard.md).
- [x] Link the accepted transfer to RQ1/RQ6/RQ7, Assumptions 5/20, and System Census pressure questions.
- [x] Reconcile an adversarial source-fidelity review before accepting the card for narrow use.

**Exit reached 2026-08-24:** one accepted Evidence Card supporting bounded Relata questions without endorsing AML scores, validity, architecture, hosted execution, or governance.

## Work item 2 — Run the first System Census

- [ ] Confirm restricted consent-record storage before collecting community contributions.
- [ ] Invite a small, varied Founding Circle privately; the source repo is public, but do not collect sensitive community material through public issues or pull requests.
- [ ] Let each contributor choose Incident Seed, System Card, case review, source review, or governance work without a skill hierarchy.
- [ ] Complete three contributor-reviewed System Cards using each system’s native vocabulary and boundary.
- [ ] Produce one Architecture Pressure Map that distinguishes native, adapter-emulated, opaque, unsupported, unknown, and not-applicable behavior.
- [ ] List every proposed observation boundary that would privilege or erase a represented architecture.

**Exit:** three materially different systems and one explicit protocol-bias record. No ranking follows.

## Work item 3 — Run Pilot 001

- [ ] Freeze one revision of `case-lab/cases/pilot-001-current-state-without-erasure.md`.
- [ ] Produce current-turn-only, no-memory, full-minimal-history, reference-context, and system-native outputs for both twins.
- [ ] Keep the current turn byte-identical and the answer-model configuration fixed within each comparison.
- [ ] Blind-review outputs with at least two disclosed reviewer perspectives.
- [ ] Record deterministic assertions, bounded semantic judgment, legitimate disagreement, evaluator ambiguity, and observability limits separately.
- [ ] Decide whether semantic equivalents of the revoked phrase are inside this pilot’s formal failure boundary.
- [ ] Accept, revise, split, or reject the case; do not produce a composite score.

**Exit:** a reviewed decision on whether Pilot 001 demonstrates memory necessity and counterfactual discriminability.

## Work item 4 — Evidence Card 002 accepted

- [x] Re-pin PM-Bench's official paper revision, repository commit, scorer, released scenario, and released primary-log boundary.
- [x] Treat the locally verified scorer-contract audit as a candidate evidence package, not Relata authority.
- [x] Trace observation provenance, `step_id` identity, scorer consumption, diagnostic meaning, and released-result impact separately.
- [x] Separate source-level possibility, released-corpus prevalence, causal interpretation, and no-observed-impact findings.
- [x] Complete source-fidelity and adversarial review before accepting the narrow transfer to RQ6 and RQ8.

**Exit reached 2026-08-24:** one accepted decision-targeted card about observation and scorer binding, not a general PM-Bench summary or a new benchmark run. The accepted transfer records zero released step-order impact and does not invalidate PM-Bench's headline tables.

## After the current open items

Update `STATUS.md`, the Distinction Atlas, and the relevant assumption or decision records. Only then assess whether the working promotion gate has enough evidence for an implementation-boundary ADR.

## Explicitly deferred

- canonical event-sourced world schema;
- permanent Recall / Context / Companion / Living tracks;
- system-under-study API;
- benchmark runner and SDKs;
- composite scoring and model-judge panel;
- Arena and Leaderboard;
- sealed benchmark repository;
- services and hosted orchestration;
- FastAPI, Temporal, Kubernetes, S3, or multi-repository operations;
- 100–300-session synthetic worlds.

These items may return only through evidence-backed decisions that name architecture and governance consequences.
