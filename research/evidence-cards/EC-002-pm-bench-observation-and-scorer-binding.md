# Evidence Card: PM-Bench observation and scorer binding

**Card ID:** EC-002
**Status:** accepted
**Author(s):** Relata maintainer research pass (AI-assisted)
**Reviewer(s):** maintainer source-fidelity and adversarial review against pinned public bytes on 2026-08-24
**Relata questions / consumers:** RQ6, RQ8; Distinction D-006; Assumptions 14 and 20

## 中文摘要

EC-002 锁定 PM-Bench paper v1、official repo commit、scenario、scorer 与 64 份 released primary logs。Accepted transfer 是 scorer-contract boundary：最终 action success 不总能绑定到 required observation、agent intended task version 或 declared `step_id`；diagnostic label 因此可能超出 logged evidence。Fresh replay 同时确认 released corpus 中 row order 与 declared `step_id` 一致，reordering defect 对 released headline results 的 observed impact 为零。本 card 不否定 PM-Bench tables，也不采用其 architecture、scenario、metric 或 runtime。

## English summary

EC-002 pins PM-Bench's paper, repository commit, scenario, scorer, and 64 released primary logs. Its accepted transfer is a scorer-contract limit: final action success is not always bound to required observation, intended task version, or declared `step_id`, so diagnostic labels can outrun logged evidence. Fresh replay also found no row-order impact in the released corpus. The card neither invalidates PM-Bench's headline tables nor adopts its architecture, scenario, metrics, or runtime.

## 1. Decision target

This card asks one bounded question: **does PM-Bench's released scorer and log contract bind a successful or failed action to the observation and step identity needed for causal and diagnostic claims?**

The answer can change which artifacts Relata would need before attributing a result to memory, state observation, update handling, or action use. The card is not a general review of prospective memory and does not decide that Relata should adopt PM-Bench's scenario, interface, metrics, or runtime. It would become irrelevant only if Relata permanently abandoned action-timed intentions, observation-sensitive cases, and replayable evaluation artifacts.

## 2. Exact object

- **Evidence object A — paper:** Liu and Gabriel, *PM-Bench: Evaluating Prospective Memory in LLM Agents*, [`arXiv:2607.12385v1`](https://arxiv.org/abs/2607.12385v1), submitted 2026-07-14; downloaded PDF SHA-256 `ca391936e787ee6597e0ef4bb078913b54cd5ef4151e673f6bb928db39ad67a1`
- **Evidence object B — released source and artifacts:** official [`genglinliu/PMBench`](https://github.com/genglinliu/PMBench) repository at commit [`e1093c470c8981daf522d4ef047a7c3a71e077d7`](https://github.com/genglinliu/PMBench/commit/e1093c470c8981daf522d4ef047a7c3a71e077d7)
- **Pinned implementation hashes:** `sim/pm_bench.py` SHA-256 `d8ec27d8dcf4679d7a789c52fc305286df460844d47e9f116b81f2400ac254d8`; `data/synthetic_week_v9.json` SHA-256 `94a45937da1363be19ccfdc2c188d132f23093041e30abd3ec22d64d70da8f24`
- **Object types:** paper, repository, synthetic scenario, scorer, released trajectories, and aggregate report
- **Access date:** 2026-08-24
- **Identity verified by:** arXiv version metadata and PDF digest; GitHub repository/commit API; fresh full clone; local `git rev-parse`, recursive tree inventory, clean-worktree check, and file digests
- **Related but separately versioned objects:** the current arXiv metadata notes publication at COLM 2026, and the official COLM accepted-papers page lists the work; neither surface supplied a separately pinned proceedings manuscript during this review
- **Explicitly excluded objects:** model-provider requests and responses outside the released logs, API credentials, private author records, unreported experiments, the browser human-evaluation UI as an evaluated system, and any later repository or paper revision

The arXiv paper is licensed CC BY 4.0. The inspected repository has no top-level license or per-file license map. Relata therefore links to and analyzes the repository but does not copy its code, data, or logs.

### Source fitness and conflicts

The paper and official repository are primary evidence for PM-Bench's stated construct, implementation, released scenario, and released results. The authors also designed the benchmark and interpret its results, so these objects are not independent validation of construct validity, causal attribution, or generalization. A local deterministic audit was used as a hypothesis and reproduction aid, not as authority; every accepted finding below was re-pinned to the official objects, re-executed against a fresh clean checkout, and narrowed where the released data could not answer the semantic question.

## 3. Coverage and execution

- **Paper coverage:** abstract; Sections 3–5; Appendices A.1–A.6; Tables 1–3 and 7; the query-then-act contract, validator claims, metric definitions, replay descriptions, and qualitative examples.
- **Repository coverage:** inventoried all 172 tracked files and both commits; read the complete README; close-read scenario validation, required-channel classification, query accounting, per-day scoring, update handling, log grouping, report construction, and run-mode metadata; inspected the released scenario, aggregate report, and all 64 primary trajectory identities.
- **Runtime or reproduction performed:** ran the official scenario validator; executed paired scorer-function fixtures for zero/one required-channel query, updated/non-updated late action, and chronological/reversed rows with unchanged declared IDs; rescored all 64 primary logs; independently aligned rows by `(day, step_id)`; traced all `update_violation` increments; reconstructed required-channel query windows; rebuilt the official comparison report; and compared a fresh generated audit byte-for-byte with the checked local research artifact.
- **Environment:** macOS arm64, Python 3.13.3 and Git; standard library only for the audit; no model, API, API key, network call during execution, or Relata runtime dependency.
- **Hosted/private/manual stages not observed:** the original live model-provider calls, provider-side model identity or configuration beyond released metadata, author review of individual logs, and the generation decisions preceding the released deterministic week.
- **Material not read or not verified:** unreleased failures or excluded runs; behavior on another scenario seed, task mixture, or model sample; scientific validity outside the released synthetic week; independent human annotation; later paper/repository objects; whether a separately versioned COLM manuscript differs from arXiv v1.

The full released scenario passed the official validator with seven days, 80 steps, 83 task definitions, and no warnings or errors. The paper's 81 scored tasks are compatible with two canceled intentions. The corpus contains an exact 8-model by 8-setup grid: 48 live runs and 16 majority/unanimous replay-derived runs.

## 4. Source-stated construct

- **SOURCE-CLAIMED SC-01:** PM-Bench evaluates prospective memory: maintaining intentions, executing them at a future time or event, reacting to changes, and monitoring latent environment state while another activity continues. Evidence: paper abstract and Sections 1 and 3.
- **SOURCE-CLAIMED SC-02:** each step follows a query-then-act protocol. An agent may issue zero or more state-channel queries and must then choose one ongoing action plus a subset of visible prospective-task handles. Evidence: Appendix A.1.
- **SOURCE-CLAIMED SC-03:** a validator and perfect-play audit establish that every non-canceled task is solvable on time; the paper says this permits misses to be attributed to model behavior rather than an impossible benchmark artifact. Evidence: Section 3.3 and Appendix A.3. This rules out one named scenario impossibility, not every scorer, logging, runtime, or construct confound.
- **SOURCE-CLAIMED SC-04:** Set-F1 over the chosen and due sets is the primary metric. Diagnostics include hit, late, miss, false alarm, wrong content, `update_violation`, dependency violation, exact-set match, query counts, and proactive-required hit. Evidence: Section 4.1 and Appendix A.4.
- **SOURCE-CLAIMED SC-05:** `update_violation` means acting on a stale task version after cancellation, override, or rescheduling changes what is valid. Evidence: Appendix A.4.
- **SOURCE-CLAIMED SC-06:** six configurations are live model runs; majority and unanimous voting are replay ablations over the union-query traces rather than fresh model executions. Evidence: Appendix A.5 and official README.

## 5. Actual observable boundary

The benchmark runtime supplies a fixed seven-day synthetic world. At each step, the system under study receives visible narrative, an ongoing-choice menu, anonymous prospective-task handles, and the opportunity to query named hidden channels. The runtime resolves query responses and maps selected handles back to canonical task IDs before writing one action row.

The released scorer observes scenario state plus log-row fields including `day`, `step_id`, selected task IDs, and aggregate query counts. It does **not** observe an agent's internal memory, belief, reason, or the task version the agent intended to select.

Three binding boundaries matter:

1. **Observation binding:** the scorer records query counts separately, but proactive and channel hit buckets are assigned from task classification plus action outcome. A hit is not conditioned on a required-channel query.
2. **Version binding:** the scorer applies a selected canonical task ID to its current mutable task state. A released selection contains no target/version field, so a late selection after an update cannot reveal whether the agent intended the current or retired version.
3. **Step binding:** `score_log` groups rows by declared day and preserves file order; `score_day` consumes `actions[step_idx]`. It checks row count but does not realign or reject rows by declared `step_id`.

The public log contract therefore makes the final chosen set observable but does not always bind that action to the observation, task-version intention, or declared step identity needed for a stronger diagnostic interpretation.

## 6. Sample and lifecycle trace

A hidden-channel event task follows this observable path:

```text
scenario defines an active task and a hidden-channel cue
→ runtime exposes visible narrative, task handles, and optional query_state
→ agent may query the channel, then emits a choose action
→ runtime logs day, step_id, canonical task_ids, and query counts
→ scorer replays current scenario state and consumes the row by within-day position
→ selected due task contributes TP / hit and its task category contributes a proactive/channel hit
→ aggregate report combines the run with the other model/setup cells
```

If the action is correct without a required-channel query, the task still contributes the same hit and Set-F1 values; only query accounting differs. The trace establishes an action outcome. It does not establish that the agent observed the hidden cue, used a particular memory, or selected a particular task version.

## 7. Public, private, and manual seam

- **Public code, data, and contracts:** paper, scenario, generator and validator code, scorer, prompts and agent scaffolds, 64 primary logs, score reports, aggregate report builder, and frontend source.
- **Hosted or private orchestration:** model-provider execution and provider-side configuration are not independently replayed here; only released code, logs, and metadata were inspected.
- **Hidden cases or reference evidence:** none in the inspected release; the scored synthetic week and scorer are public. This is not a sealed-evaluation design.
- **Manual review or intervention:** paper describes generation and validation but the release does not expose a case-by-case human review record. No manual judgment participates in the deterministic scorer path inspected here.
- **Missing failure evidence:** excluded, aborted, or unreleased live runs; model-provider errors beyond released metadata; alternative scenario seeds; and action-intention/version fields that would disambiguate update semantics.

## 8. Architecture assumptions

- Prospective behavior can be represented as selecting discrete task handles at fixed synthetic steps.
- A query-then-act runtime with named state channels is a meaningful observation boundary for every evaluated agent scaffold.
- The scenario's current mutable task state is sufficient scoring authority even when a selected action does not name the intended task version.
- A task-category hit is useful as a monitoring diagnostic even when it is not query-provenance evidence.
- The ordered JSONL file is trusted to preserve step identity; declared `step_id` is descriptive rather than enforced by the scorer.
- A single deterministic week can support the reported finite comparison, while generalization across weeks remains open.
- Anonymous handles, a bounded task menu, and the prompt-specified action schema do not erase a system's native planning or memory behavior.
- Heartbeats, ledgers, subagents, union queries, and replay voting are comparable interventions despite changing the evidence and control path.
- Replay-derived decision rules may share queried evidence with a live trace and still be compared as decision ablations; their runtime metadata must not be treated as fresh agent inference time.

These are properties of PM-Bench's evaluation architecture, not requirements for Relata.

## 9. Claim ledger

| ID | Claim | Label | Exact evidence location | Limitation / counter-evidence | Relata consumer |
|---|---|---|---|---|---|
| C-01 | PM-Bench defines a public query-then-act prospective-memory benchmark over one deterministic synthetic week. | SOURCE-CLAIMED | paper abstract, Sections 3–4, Appendix A.1; pinned README 1–27 | construct validity and transfer to relational memory were not established | D-006 |
| C-02 | The pinned release contains the scenario, scorer, report path, and an exact 8-by-8 grid of 64 primary trajectories: 48 live and 16 replay-derived. | REPRODUCED | complete tree; run metadata inventory; Appendix A.5 | completeness is limited to the released grid; excluded or failed runs are unknown | RQ8 |
| C-03 | Paired correct actions with zero versus one required-channel query receive the same hit, Set-F1 contribution, proactive-required hit, and channel hit; only query counts differ. | REPRODUCED | `sim/pm_bench.py` 2206–2255, 2446–2449, 2522–2581; paired exact-source fixture | this narrows metric meaning; Appendix A.4 defines a task category and does not explicitly claim query provenance | RQ6, RQ8 |
| C-04 | Across the 64 released logs, 1,062 proactive-required tasks complete as hit/late; 381 have no required-channel query from reconstructed cue/due opportunity through completion. | REPRODUCED | full-corpus rescore and query-window reconstruction | finite log fact, not proof that the agent lacked all relevant information; 317 are clock and 64 non-clock cases | RQ6 |
| C-05 | The paper defines `update_violation` in stale-version terms, while the scorer increments it whenever an updated task is selected outside the exact due set, including an accepted late action on current mutable state. | CONTRADICTED | Appendix A.4; `sim/pm_bench.py` 2517–2518; update/no-update paired fixture | the scorer-level taxonomy conflicts; the fixture does not establish released agent intention | RQ6, RQ8, D-006 |
| C-06 | The 64 logs contain 541 `update_violation` increments; 27 co-occur with accepted-late completion of the scorer's current mutable state. The semantic count of current-version intent is bounded from 0 to 27. | REPRODUCED | revision-locked trace of every scorer increment and released action schema | rows name task IDs but no task version or intended target; semantic intention is not reconstructable | RQ6, RQ8 |
| C-07 | The scorer consumes within-day actions positionally without realigning or rejecting declared `step_id`; reversing two fixture rows while preserving their IDs changes the score. | REPRODUCED | `sim/pm_bench.py` 2350–2367 and 2586–2589; chronological/reversed paired fixture | scorer-function fixtures are not full validator-clean scenarios | RQ8, Assumption 20 |
| C-08 | All 64 released logs have exactly one valid row per scenario step in correct within-day order; identity alignment changes zero released scores. | REPRODUCED | full `(day, step_id)` inventory and independent alignment/rescore | no released-result impact found does not make future malformed logs safe | RQ8, Assumption 20 |
| C-09 | The official README points to `runs/March_ALL_results_v9`, but the pinned tree and report builder use `runs/all_results_v9`; the published rebuild command is not executable as written. | CONTRADICTED | pinned README 25, 128–134; complete tree; report-builder path | rebuilt report content matches after the single path substitution | RQ8 |
| C-10 | The abstract attributes 65.1% to “the best method, a GPT-5.4 agent”; Table 2 makes 65.1% the across-model optional-heartbeat macro, while Table 3 gives GPT-5.4 optional heartbeat as 79.1%. | CONTRADICTED | paper abstract; Tables 2–3 | statistical-object wording mismatch, not evidence that the released aggregates or table values are wrong | RQ8 |
| C-11 | All 16 replay-derived records report zero duration, which is replay bookkeeping rather than fresh model inference time. | REPRODUCED | run metadata modes and durations; Appendix A.5 | no runtime comparison is supported between these rows and the 48 live runs | RQ8 |
| C-12 | The official scenario validator passes, but scenario solvability alone cannot exclude scorer semantics, action-observation ambiguity, step-binding assumptions, or generalization limits. | REPRODUCED / INFERRED | official validation; Appendix A.3; C-03–C-08 | does not negate the perfect-play result or show an impossible task | RQ6, RQ8 |
| C-13 | The inspected source repository supplies no reuse license. | REPRODUCED | complete 172-file inventory at `e1093c…` | rights-documentation finding, not a conclusion about ownership | governance/licensing |

## 10. What the evidence supports

- PM-Bench provides an unusually inspectable finite chain from public scenario and agent action logs to deterministic results.
- A correct action, a recorded observation, the use of that observation, and a diagnostic label are distinct evidence objects. The released scorer does not collapse them reliably into one causal fact.
- `update_violation` has a concrete implementation/taxonomy mismatch: the exact counter increment is reproducible, while the agent's intended task version remains unobservable.
- Declared step identity and physical row order are different integrity properties. PM-Bench's scorer trusts row order, but all 64 released primary logs satisfy the stronger identity/order condition and show no resulting score change.
- Exact source, scenario, scorer, run mode, row identity, and observation fields are material parts of a reproducible evaluation claim.
- Prospective intention, update, and false-wake cases deserve a place in Relata's research agenda, but PM-Bench does not determine their relational meaning or Relata's interface.

## 11. What it does not support

- that PM-Bench's headline Set-F1 tables are wrong;
- that any released score changed because of row-order handling;
- that all 381 completions without a required-channel query were guesses or memory failures;
- that any particular one of the 27 accepted-late update co-occurrences expressed current-version or retired-version intent;
- that scenario solvability proves every miss was caused only by model memory rather than scaffold, prompt, runtime, observation, logging, or action-use behavior;
- that the eight scaffolds isolate a universal prospective-memory capability;
- that one week estimates behavior across seeds, schedules, task mixtures, systems, or real relationships;
- that PM-Bench code, data, logs, or interface may be copied into Relata under a stated repository license;
- that Relata should build a runner, service, scoreboard, or PM-Bench-compatible adapter during R0.

## 12. Transfer to Relata

| Relata area | Preserve | Adapt | Reject / defer | Reason |
|---|---|---|---|---|
| Construct | prospective intention is distinct from retrospective recall; cancellation, rescheduling, expiry, and false wake matter | separate state availability, observation, retained intention, action eligibility, and actual action | PM-Bench hit rate as a relational-memory construct | the scorer exposes useful distinctions but not relational authority, consent, or appropriateness |
| System-under-study boundary | make observation and action surfaces explicit | classify push, proactive query, system-native context, adapter reconstruction, and opaque observation separately | task-handle menu plus named channel API as Relata's canonical boundary | the interface is architecture-specific and may alter native agent behavior |
| Lifecycle | trace state change through observable evidence to action and score | bind a selected action to current rule/version where a diagnostic depends on it | inferring agent intent from canonical object ID alone | update semantics require more than mutable current-state replay |
| Artifacts | pin exact source, scenario/case, scorer or review contract, run mode, and result identity | validate row identity/order or make the scorer align by declared identity; record observation evidence separately | symbolic version labels or trusted file order as public proof | C-07/C-08 separate latent integrity risk from actual released impact |
| Evaluation | use paired fixtures and finite released-corpus audits; keep diagnostic meaning narrower than its name | add observation/no-observation, current/retired version, and reordered-row controls before causal attribution | composite score as proof of mechanism or intent | deterministic scoring is reproducible only for what its inputs and rules actually bind |
| Governance | publish limits and source rights status with transferred findings | require claim-specific evidence review before a metric name becomes a public conclusion | importing unlicensed implementation or treating public visibility as reuse permission | source analysis does not grant code/data rights |

## 13. Generated research actions

- **Candidate distinction:** state available to a system versus state observed, retained, made action-eligible, and correctly acted upon.
- **Candidate counterfactual:** hold final action constant while varying whether the required evidence was available, observed, or supplied in reference context; separately hold current state constant while changing the retired version.
- **Candidate baseline or control:** exact `(case, probe, observation, action, contract-version)` binding; reject or explicitly align mismatched identities before scoring.
- **Candidate architecture pressure test:** classify whether a system receives state by native push, proactive query, adapter-generated query, rendered context, or an opaque complete-agent path, and record which boundary can expose observation evidence without demanding a universal architecture.
- **Assumption or ADR affected:** Assumption 14 remains a working hypothesis but now requires semantic counterexample tests for deterministic diagnostics. Assumption 20 now includes observation, task-version, step-identity, and run-mode binding where the claim depends on them. No implementation ADR or runner is justified.

## 14. Review decision

- **Pinned identity is adequate:** yes
- **Coverage statement is honest:** yes
- **Claim labels match evidence:** yes
- **Counter-evidence or limits are visible:** yes
- **Concrete Relata consumer exists:** yes
- **Decision:** accept for narrow use
- **Review notes:** EC-002 is accepted only for PM-Bench's public query/action/scoring boundary, the reproduced meaning limits of proactive and update diagnostics, the source-level step-identity risk with zero impact found across the 64 released primary logs, exact release contradictions, and the resulting Relata evidence-binding requirements. Acceptance does not invalidate PM-Bench's headline Set-F1 table, label individual model failures, validate the benchmark construct, generalize beyond the released week, or authorize adoption of its interface, scorer, data, code, or infrastructure.
- **Replacement card if superseded:** none
