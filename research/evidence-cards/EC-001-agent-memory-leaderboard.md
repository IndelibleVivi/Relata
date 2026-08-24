# Evidence Card: Agent Memory Leaderboard public evaluation boundary

**Card ID:** EC-001
**Status:** accepted
**Author(s):** Relata maintainer research pass (AI-assisted)
**Reviewer(s):** maintainer source-fidelity review; GPT-5.6 Pro advisory review reconciled against pinned public bytes on 2026-08-24
**Relata questions / consumers:** RQ1, RQ6, RQ7; Assumptions 5 and 20; first System Census Architecture Pressure Map

## 1. Decision target

This card asks one bounded question: **what does Agent Memory Leaderboard (AML) actually place inside the system-under-study boundary from ingestion through public result, and which parts of that path are publicly inspectable?**

The answer can change whether Relata treats an `Add` / `Search` service as a neutral system-under-study boundary, whether a fixed downstream answer model is sufficient for causal attribution, and which public artifacts would be required before Relata could make exact-version claims. The card would be irrelevant only if Relata permanently excluded memory engines and adapter-mediated evaluation from its comparison scope.

## 2. Exact object

- **Evidence object A — pinned public source:** official [`AML-memory/agent-memory-leaderboard`](https://github.com/AML-memory/agent-memory-leaderboard) repository at commit [`5761ed58502d24153115cbdc010e44957cb18c3a`](https://github.com/AML-memory/agent-memory-leaderboard/commit/5761ed58502d24153115cbdc010e44957cb18c3a), its single root commit at review time
- **Evidence object B — pinned public result snapshot:** official Hugging Face Space [`agent-memory-leaderboard/leaderboard`](https://huggingface.co/spaces/agent-memory-leaderboard/leaderboard) at commit [`d01a32165aef2124b9732bd0fda7f79380b931dc`](https://huggingface.co/spaces/agent-memory-leaderboard/leaderboard/tree/d01a32165aef2124b9732bd0fda7f79380b931dc)
- **Evidence object C — dated mutable hosted observations:** [official documentation](https://agentmemories.ai/docs), [API guide](https://agentmemories.ai/api-guide), [industry textual leaderboard](https://agentmemories.ai/leaderboard/industry/textual), and unauthenticated public leaderboard JSON for the industry and academic textual tracks, inspected on 2026-08-24; no stable public revision or release identity was available for these surfaces
- **Object types:** repository, documentation, hosted evaluation contract, and public result snapshot
- **Access date:** 2026-08-24
- **Identity verified by:** `git ls-remote`, full clone, local `git rev-parse`, GitHub repository/commit API, recursive tree inspection, and Hugging Face clone/commit verification
- **Identity adequacy:** adequate for objects A and B; dated-only for object C, whose observations are not a pinned or independently re-inspectable snapshot
- **Related but separately versioned objects:** upstream benchmark repositories named in individual pipeline modules; the current website application and hosted orchestration; system-under-study repositories linked from the public board
- **Explicitly excluded objects:** private evaluation jobs, system-under-study endpoints, held-out corpora and questions, gold answers and rubrics, internal review records, raw model outputs, the source workbook named by the hosted API, credentials, and unreleased verifier/orchestration code

No paper or preprint was linked from the official repository or website. Exact-title searches of arXiv, OpenReview, and Semantic Scholar returned no matching record on 2026-08-24. The repository's BibTeX entry describes a project website, not a peer-reviewed publication.

### Source fitness and conflicts

The official repository, documentation, and versioned result Space are primary evidence for AML's published interface and public artifacts. They are not independent evidence that the benchmark is fair, construct-valid, reproducible end to end, or architecture-neutral. AML's organizers define the protocol, operate the hosted system, review submissions, and describe its benefits, creating an institutional and intellectual conflict for claims about the quality of their own evaluation. This card therefore treats the objects as high-fitness evidence for **what AML publicly exposes**, but only caveated operator evidence for **what AML validly measures**.

## 3. Coverage and execution

- **Repository coverage:** read the complete English README, `api_config.py`, and `requirements.txt`; inventoried all eleven tracked files; parsed every function and CLI surface in all seven pipeline modules; close-read the complete LongMemEval-S module and the ScriptMem answer/scorer path; checked upstream-source and configuration declarations across the remaining modules.
- **Hosted coverage:** read the Add/Search contract, evaluation modes, publication flow, public/private boundary, data-retention statement, and publication-gate claims in the official documentation; inspected the current industry and academic textual leaderboard responses.
- **Result-snapshot coverage:** cloned the official Hugging Face Space at the pinned commit; inspected its README, generated textual/coding result schemas, textual division counts, version/source fields, and repository history relevant to the current snapshot.
- **Runtime or reproduction performed:** all eight Python files passed `py_compile`; all seven pipeline CLIs produced `--help` after installing the sole declared dependency (`httpx 0.28.1`) in an isolated temporary environment; four deterministic ScriptMem scorer checks passed for correct single choice, incorrect single choice, order-independent multi-select, and order-sensitive ordering.
- **Environment:** macOS arm64 host, Python 3, isolated temporary virtual environment; no Relata dependency or repository file was added.
- **Hosted/private/manual stages not observed:** key issuance, system-under-study build/deployment, Add/Search calls in a real job, held-out input, full-run orchestration, answer/judge model calls, aggregation, audit evidence, reviewer decision, and publication mutation.
- **Material not read or not verified:** complete upstream benchmark implementations and licenses; every prompt's fidelity to its upstream project; private source data; the internal spreadsheet named by current hosted results; exact production answer/judge configuration; a real end-to-end scored sample; scientific validity, inter-rater reliability, or independent reproduction of AML scores.

The public repository contains no tests, sample inputs, benchmark data, run manifest, release tag, GitHub release, top-level license, or per-file license map. Only the BEAM module pins an upstream source commit. PersonaMem and ScriptMem cite mutable `main` paths; the CL-Bench module refers to a separately supplied implementation that is not identified by a public commit in this object. Answer and judge endpoints, model identities, and judge version are supplied through environment variables with empty defaults, so the pinned public bytes do not bind the runtime values used for any published row.

## 4. Source-stated construct

- **SOURCE-CLAIMED SC-01:** AML evaluates how well long-term memory systems store, retrieve, and support the use of information under a shared protocol and public leaderboard. Evidence: pinned README, lines 13–23.
- **SOURCE-CLAIMED SC-02:** the system under study exposes `Add` and `Search`; AML controls answer generation, evaluation, aggregation, and orchestration. Evidence: pinned README, lines 86–100; hosted documentation, “How the platform works.”
- **SOURCE-CLAIMED SC-03:** AML states that holding the answer and evaluation pipeline fixed is intended to make score differences more attributable to the system under study. This is an operator causal claim, not a reproduced attribution result. Evidence: hosted documentation, “Fairness boundary.”
- **SOURCE-CLAIMED SC-04:** AML states that systems pass a compatibility smoke test and then run the complete evaluation suite; results remain private until a submission passes publication review. The mutable documentation separately describes a public-eligibility gate. Passage through these stages was not observed for any specific row. Evidence: pinned README, lines 102–119; hosted documentation, “Evaluation workflow” and “Evaluation modes.”
- **SOURCE-CLAIMED SC-05:** the hosted documentation states that public eligibility requires recorded answer-model identity, evaluation-contract identity, pipeline-code hash, dataset-bundle hashes, and question counts. Whether any specific published row possesses or passed review against those records is `UNVERIFIED`. Evidence: hosted documentation, “Public leaderboard eligibility.”
- **SOURCE-CLAIMED SC-06:** the public repository exposes per-benchmark answer/scoring behavior while deliberately withholding data, orchestration, system-under-study traces, infrastructure, and review tooling. Evidence: pinned README, lines 144–195.

These are claims made by the operator. They are not automatically reproduced observations or validation findings.

## 5. Actual observable boundary

The hosted contract presents this system-under-study boundary:

1. AML chunks source sessions and sends ordered text messages, optional millisecond timestamps, `user_id`, and `session_id` to a synchronous `Add` endpoint.
2. The system under study must persist the write and make it immediately searchable before returning `HTTP 200`.
3. After ingestion, AML sends each original question—and answer options when present—to `Search`, scoped only by the matching `user_id`, with formal `top_k = 100`.
4. The system returns relevance-ordered textual objects containing required `id` and `content` plus optional score and time.
5. AML passes the returned text and order into a shared answer pipeline, then applies dataset-specific evaluation and aggregates results.

**INFERRED:** the documented protocol exposes the system under study through a synchronous, question-conditioned Add/Search service that returns an ordered list of textual evidence. For questions with supplied answer choices, Search receives those choices and may condition returned evidence on them; the contract therefore does not isolate option-blind recall. Any final score is a joint outcome of the system service as adapted to this contract and AML's downstream answer/evaluation path. The inspected public objects do not identify a memory-only causal effect.

At commit `5761ed…`, the inspected pipeline modules accept already-selected fields such as `retrieved_context`, `memories`, and speaker-specific memory text. No inspected public code connects the documented Add/Search HTTP responses to those fields. The implementation of ingestion, search orchestration, that adapter seam, protected inputs, aggregation, review, and publication is not exposed in the inspected public objects; its private existence and behavior remain `UNVERIFIED`.

## 6. Sample and lifecycle trace

No AML leaderboard sample could be traced end to end through the inspected AML public objects. The only source-supported cross-boundary trace is the documentation's illustrative contract example, and it must not be presented as an observed leaderboard run:

```text
published example Add request
  {messages: [{content: "memory text"}], user_id, session_id}
→ opaque system-under-study persistence / indexing / update behavior
→ published example Search request
  {query: "Which answer best matches the memory?", options, same user_id, top_k: 100}
→ published example ordered result
  {data: [{id: "mem_1", content: "remembered fact text", score, created_at}]}
→ UNOBSERVED adapter from HTTP response to a per-dataset pipeline record
→ OBSERVED code path: retrieved text is rendered into an answer prompt
→ OBSERVED code path: generated answer is compared with protected reference material
→ UNOBSERVED aggregation / review / publication mutation
→ public aggregate row without a public per-sample run artifact
```

A separate synthetic micro-probe reproduced only ScriptMem's deterministic final scorer: gold `B` with prediction `B` scored `1.0`; gold `B` with `C` scored `0.0`; multi-select accepted the same set in another order; ordering rejected the same elements in another order. This verifies those local functions at the pinned repository commit. It does not verify AML's data, model output, hosted run, aggregate score, or published rows.

## 7. Public, private, and manual seam

| Stage | Public evidence | Unavailable or opaque evidence |
|---|---|---|
| Contract | Add/Search schemas, synchronous rule, Top K, `user_id` isolation, retry/error statements | production adapter and exact orchestration implementation |
| Data | dataset names, coverage claims, public aggregate/capability scores | corpora, held-out questions, gold objects, rubrics, bundle hashes |
| System execution | system source URL or product version in some public rows | evaluated source commit/image/API identifier for current textual rows; request/response trace |
| Answer and evaluation | seven pinned Python modules and prompt/scorer code | exact production code identity, model configuration, raw inputs/outputs, full upstream fidelity |
| Aggregation | aggregate and capability values in public snapshots | per-sample contribution, aggregation manifest, failure evidence, excluded/failed runs |
| Review and publication | process description and approved public rows | reviewer identity, review record, rejection reasons, appeals, publication action log |

The pinned Hugging Face textual snapshot contains 50 academic rows and 15 commercial rows. All academic rows name a GitHub repository but have no structured `version` field; some system names include version-like suffixes, which are not structured source versions or commit bindings. All commercial rows have a product/API version but no public source URL. The website API responses inspected on 2026-08-24 expose `target_git_sha: null` for all 65 textual entries and name symbolic `public_suite_v3` / `official-benchmark-pipelines-v3` identifiers without public bundle or pipeline hashes. This does not prove that exact-version evidence is absent privately. It means the pinned HF row artifact and the dated hosted API snapshots inspected on 2026-08-24 do not themselves demonstrate the exact-version binding claimed by the documentation.

## 8. Architecture assumptions

- A materially comparable system can expose synchronous `Add` and question-conditioned `Search` over HTTP(S).
- Relevant system output can be represented as an ordered list of discrete text records with stable IDs.
- `user_id` is a sufficient mandatory retrieval-isolation boundary; `session_id` organizes ingestion but is not a search filter.
- Immediate searchability after each completed Add is meaningful across architectures.
- AML-controlled chunking at 20 messages or 2,000 words does not erase system-native ingestion semantics.
- Passing the original question and optional answer choices to Search is an acceptable part of the memory boundary.
- A fixed Top K of 100 and response order are comparable across sparse, dense, graph, generative, and opaque systems.
- A shared external answer model can consume materially different evidence formats without creating differential adapter pressure.
- Update, correction, conflict, deletion, revocation, expiry, provenance, and multi-party authority can be inferred from repeated Add/Search behavior even though the external contract has no dedicated operations or fields for them.
- Systems with latent/parametric memory, proactive state, complete-agent behavior, multimodal memory, system-native context compilation, or no public evidence list can be represented without the adapter becoming the object actually evaluated.

The source does not establish these assumptions. Several are precisely the pressure points Relata must test.

## 9. Claim ledger

| ID | Claim | Label | Exact evidence location | Limitation / counter-evidence | Relata consumer |
|---|---|---|---|---|---|
| C-01 | AML declares an Add/Search system boundary and keeps answer/evaluation downstream. | SOURCE-CLAIMED | pinned README 86–100; hosted docs “How the platform works” | hosted implementation not public | RQ1, RQ7 |
| C-02 | The public Python repository starts from already retrieved/selected memory material rather than implementing Add/Search. | REPRODUCED | all seven pipeline input/render paths; LongMemEval-S 90–117; ScriptMem 69–118 | an unpublished adapter may connect the stages | RQ1 |
| C-03a | At commit `5761ed…`, the public repository contains no benchmark data, run manifest, per-sample run artifact, or public code connecting documented Add/Search responses to pipeline records. | REPRODUCED | complete repository tree; README 168–180 exclusions; all seven pipeline input paths | public-surface absence does not establish what exists privately | RQ6 |
| C-03b | Consequently, an AML leaderboard sample is not reproducible end to end from the pinned repository alone. | INFERRED | C-03a plus the documented hosted lifecycle | conclusion is limited to the inspected public repository, not AML's or a system maintainer's private materials | RQ6 |
| C-04a | At HF commit `d01a321…`, textual JSON has 50 academic rows with GitHub URLs and no structured `version` field, and 15 commercial rows with version strings and no public source URL. | REPRODUCED | pinned `data/generated/leaderboard_data.json` | some academic names contain version-like text, but no row exposes a commit binding | Assumption 20 |
| C-04b | In hosted textual API responses inspected on 2026-08-24, all 65 rows had `target_git_sha = null`; all named `public_suite_v3` and `official-benchmark-pipelines-v3`; academic `metadata.version` values were null while industry rows carried product-version strings. | REPRODUCED — dated mutable observation | hosted `/leaderboard` responses on 2026-08-24 | responses are mutable; public fields do not establish what evidence may exist privately | Assumption 20 |
| C-05 | Public result rules require pipeline and dataset hashes. | SOURCE-CLAIMED | hosted docs “Public leaderboard eligibility” | required hashes are not exposed in the inspected public row artifact | Assumption 20 |
| C-06 | If the downstream reader and evaluator were held fixed as documented, that would remove one source of between-system variation. | INFERRED | declared fixed Answer/Eval boundary | production fixity was not reproduced; fixed conditions do not isolate retention, retrieval, representation, adapter, or reader effects | RQ6 |
| C-07 | The documented Add/Search contract encodes synchronous, textual, question-conditioned, Top-K, ordering, and operation-surface requirements that may create differential adapter pressure across architectures. | INFERRED | hosted Add/Search contract | no cross-system pressure or distortion was measured; direction and magnitude remain `UNVERIFIED` | RQ7, Assumption 5 |
| C-08 | The public Add/Search schemas inspected on 2026-08-24 expose no dedicated correction, revocation, deletion, expiry, provenance, authority, or convergence operation or field. | REPRODUCED | hosted Add/Search schemas and “Fields not sent” | systems may implement these semantics internally or emulate them through Add/Search | RQ3–RQ5, RQ7 |
| C-09 | Upstream provenance is unevenly pinned across the public modules. | REPRODUCED | BEAM commit constant; PersonaMem/ScriptMem mutable `main`; CL-Bench task-supplied implementation note | the AML commit still pins its own bytes | RQ8, Assumption 20 |
| C-10 | The public repository supplies no reuse license or upstream license map. | REPRODUCED | complete root/tree inventory at `5761ed5…` | this is a rights-documentation finding, not a conclusion about ownership | governance/licensing |
| C-11 | Publication follows organizer review and private-to-public promotion. | SOURCE-CLAIMED | README 102–119; hosted docs 1254–1277 | manual review evidence, rejected cases, and appeal behavior were not observed | future governance |
| C-12 | At commit `5761ed…`, answer and judge endpoints, model identities, and judge version come from environment variables with empty defaults; the repository does not bind runtime values for any published result. | REPRODUCED | `api_config.py` 7–14; pipeline answer/evaluate assignments | values may be supplied privately; production use of these exact bytes is `UNVERIFIED` | RQ6, Assumption 20 |
| C-13 | LongMemEval-S tells the answer model to convert relative times to absolute dates when timestamps permit, while its evaluator forbids relative-to-absolute conversion and treats it as wrong. | CONTRADICTED | `data/longmemeval-s/pipeline.py` answer instruction 7 and evaluator TIME rule | no answer/judge run was executed, so frequency and score effect are unknown | RQ6, RQ8 |
| C-14 | ScriptMem prompt provenance is internally inconsistent: the module header requires `user-specified`, while generated-answer metadata writes `published dataset answer instructions`. | CONTRADICTED | `data/scriptmem/pipeline.py` 1–12 and answer output record | establishes a public metadata contradiction, not which description appears in hosted publication records | RQ6, RQ8, Assumption 20 |
| C-15 | LongMemEval-S and ScriptMem answer prompts tell the downstream answer model to prefer the most recent supported memory when retrieved memories conflict. | REPRODUCED | LongMemEval-S answer instruction 8; ScriptMem answer instruction 7 | downstream conflict-resolution policy does not demonstrate system-side update or current-state semantics | RQ3, RQ6 |
| C-16 | Whether any specific row passed the stated smoke, full-run, review, and public-eligibility requirements or is privately bound to the required hashes and model identities is unknown. | UNVERIFIED | operator-described lifecycle versus inspected public row fields | missing public proof is not proof that private evidence is absent | RQ6, Assumption 20 |

## 10. What the evidence supports

- AML publicly specifies a responsibility split between system-under-study Add/Search and AML-controlled downstream Answer/Eval. Production enforcement of that split was not observed.
- The inspected public pipeline code begins with already-selected memory material and does not expose the Add/Search-to-pipeline adapter.
- Holding downstream conditions fixed, if actually enforced, removes one source of variation but does not identify a memory-only causal effect.
- The pinned HF rows and dated hosted API responses inspected do not themselves demonstrate the exact source-and-contract binding claimed by operator documentation.
- AML's contract provides a concrete boundary for Relata to interrogate. It does not select a Relata interface, establish observed differential architecture pressure, validate AML's scores, or justify Relata infrastructure or governance choices.

## 11. What it does not support

- that AML is scientifically validated, independently reproduced, peer reviewed, fair, or architecture-neutral;
- that current public scores are reproducible from public materials;
- that a public leaderboard row currently demonstrates an exact system commit plus pipeline/data hashes;
- that fixed downstream Answer/Eval makes every score difference attributable to memory alone;
- that Add/Search captures relational continuity, correction, revocation, appropriate silence, companion identity, or complete-agent behavior;
- that the named capability taxonomy is a validated ontology;
- that private review, security, data deletion, or version audit occurred as described for any specific row;
- that absent public artifacts imply absent private evidence;
- that the public code may be reused under a particular license.

## 12. Transfer to Relata

| Relata area | Preserve | Adapt | Reject / defer | Reason |
|---|---|---|---|---|
| Construct | distinguish evidence production from downstream answer use | define a case-specific estimand at every observable boundary | a universal memory score | AML shows boundary clarity but not construct sufficiency |
| System-under-study boundary | explicit responsibility split | compare system-native, adapter-emulated, opaque, unsupported, unknown, and not-applicable stages | permanent Add/Search as Relata's canonical API | the contract creates a plausible differential-pressure risk for systems without native discrete textual evidence lists; actual distortion is unmeasured |
| Lifecycle | no accepted transfer under this card's narrow authorization | retain named stages only as future research questions | adoption as Relata process or hosted orchestration | operation, review quality, and failure handling were not observed |
| Artifacts | distinguish pinned source, dated mutable observation, system identity, contract identity, and public result proof | require public evidence of binding if Relata later publishes results | a specific run-manifest format or unverifiable symbolic labels | EC-001 supports the need for public proof, not a particular artifact mechanism |
| Evaluation | hold downstream conditions constant within a bounded comparison | motivate current-turn-only, no-memory, reference-context, system-native, and reader-sensitivity controls | composite ranking or memory-only attribution from fixed-reader comparison | downstream prompts contain temporal/conflict policy and runtime configuration remains unbound publicly |
| Governance | none under this card's accepted transfer | retain organizer review and private/public stages as unverified source claims | AML's process as a Relata governance model | specific review operation, outcomes, rejection, appeal, and publication mutation were not observed |

## 13. Generated research actions

- **Candidate distinction:** system-native memory behavior versus adapter-mediated evidence usefulness.
- **Candidate counterfactual:** hold stored history constant while (a) withholding versus providing answer options to Search, and (b) comparing a system-native context with its text-list adapter projection.
- **Candidate baseline or control:** no-memory, current-turn-only, reference-context, and same-retrieval/different-reader controls before attributing answer quality to memory.
- **Candidate architecture pressure test:** for each first-round System Card, classify synchronous ingestion, immediate visibility, user/session scoping, question-conditioned retrieval, discrete text output, Top K, ordering, corrections, revocation, provenance, and complete-agent use as native, adapter-emulated, opaque, unsupported, unknown, or not applicable.
- **Assumption or ADR affected:** Assumption 5 remains an aspiration; EC-001 opens concrete pressure dimensions but supplies no observed cross-system pressure result. Assumption 20 now distinguishes operator-required records from public proof, while the eventual proof artifact remains a separate Relata design decision. No implementation ADR is justified.

## 14. Review decision

- **Pinned identity is adequate:** partial — yes for the GitHub and Hugging Face commits; dated-only for hosted documentation and API observations
- **Coverage statement is honest:** yes
- **Claim labels match evidence:** yes
- **Counter-evidence or limits are visible:** yes
- **Concrete Relata consumer exists:** yes
- **Decision:** accept for narrow use
- **Review notes:** EC-001 is accepted only as evidence of AML's publicly specified boundary, the inspectable and uninspectable seams in the reviewed public objects, limits on fixed-reader causal attribution, architecture-specific commitments requiring future pressure analysis, and the distinction between operator-required version records and public proof. Acceptance does not validate AML's scores, taxonomy, fairness, hosted execution, review process, private evidence, or governance model, and does not authorize adoption of AML's Add/Search architecture or any evaluation-platform infrastructure.
- **Replacement card if superseded:** none
