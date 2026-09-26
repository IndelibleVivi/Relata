# Relata Repository Contract

## Project identity

- The project name is **Relata**. `R0` and `Research Foundation` are phase labels only.
- Relata is a frontier memory research lab with three core functions under ADR-0008: its own benchmark research, an inspectable collection of system studies, and incubation for future memory systems. The collection's museum / sample-room / lab name remains open. The existing case programme is benchmark research in progress, not an accepted benchmark platform.

## Authority

Read current authority in this order:

1. `STATUS.md`
2. `CHARTER.md`
3. `ASSUMPTION_REGISTER.md`
4. accepted records in `decisions/`
5. research, governance, system-census, and case-lab materials
6. `docs/vision/`

The body of `docs/vision/relata-target-architecture-draft-0.1.md` is preserved historical material. It is not implementation authority.

## Current scope

Work may advance definitions, public-source architecture research, comparative synthesis and articles, project questions, source Evidence Cards, community contribution methods, System Cards, Architecture Pressure Maps, distinctions, synthetic cases, pilot records, decision records, and repository checks. Source research and writing do not wait for the cross-system implementation promotion gate.

Keep all three core functions visible in project direction and reading paths. Existing cases, source studies, architecture views and candidate designs support them with distinct evidence status; they are not permanent benchmark tracks or a universal ontology. Use relevant existing AMS work with its provenance and limits for Relata's own questions, and investigate concrete gaps as needed. Both projects can inform long-form writing; do not turn Relata into a duplicate reading room or require a predetermined article thesis. Incubation does not make Relata the source repository for future Tilia product code or promote a preferred design into the evaluator's contract.

Under ADR-0006, general agent memory and adult long-term human–AI intimacy are independent research contexts; intimacy remains a founding focus, not an eligibility filter for every study. The existing Case Lab's working evaluation object is a longitudinal mixed-domain memory ecology spanning personal/lived, shared-relational, operational/project, and companion/system continuity. Do not require ordinary events or shared work to carry explicit romantic symbolism. Treat coverage strata as case-portfolio labels, not permanent tracks or an ontology for the whole lab.

The research may inform a future independently authored memory system named **Tilia**. This is a long-term goal, not an implementation task within Relata. `research/own-memory-architecture.md` and `research/memory-design-test-map.md` remain proposed design/validation studies, not an accepted Tilia architecture or universal ontology. The corrected ADR-0007 withdraws the earlier implementation-authority interpretation. Already-written `relata-memory` code remains a very early separate local experiment; `experiments/local-memory-apparatus.md` owns its engineering evidence and limits. Retention does not authorize further implementation, physical renaming or migration. Tilia's intended design requires vector-based semantic retrieval; the experiment's literal search does not supply it, and encoder/model choices remain open. Its schema must not become the evaluator’s answer format. Source studies, articles and the existing Case Lab retain independent value.

The proposed design figures in `research/figures/own-memory-*.mmd` are editable Mermaid sources; their `.svg` counterparts are derived presentation. Keep the design text, diagram semantics and exports aligned, and inspect actual rendered figures after edits. These candidate figures are separate from the ten upstream source models in the architecture atlas.

Public-source system studies do not require maintainer endorsement. Follow the source-review route in `systems/README.md`; private contributor descriptions retain their disclosure and consent requirements. Separate public code, hosted products, historical versions, source claims, observed behavior and editorial judgment. Linking AMS or another research project does not import accepted evidence or authorize cross-repository edits.

The ten bounded drafts in `systems/source-studies/` are source research, not accepted System Cards or live system results. Their two `observations/` scripts consume exact, clean public lmc-5/Graphiti checkouts and public synthetic inputs only; commands and evidence limits live in that directory's README. They are source-study diagnostics, not a general runner or an extension to model/provider execution.

The architecture atlas is a research-document renderer, not system-under-study execution. `systems/architecture-atlas/models/*.json` owns the source-grounded nodes, relations, boundaries, state notes and pinned evidence; `guide-layouts.cjs` selects existing relations for the introductory path, while `build.cjs` and `render-*.cjs` own presentation generation. Edit models or viewer sources, then regenerate `diagrams/<project>/*.{svg,mmd}` and `index.html` with `node systems/architecture-atlas/build.cjs`. Do not hand-edit generated figures or keep parallel topology copies in reports. Run `node systems/architecture-atlas/build.cjs --check` after changes, and visually inspect affected diagrams and reader interactions. `observed` in models means static source inspection, never verified runtime behavior.

Do not add a benchmark runner, system-under-study API, Leaderboard, Arena, SDK, services, hosted infrastructure, sealed corpus, or canonical system ontology unless a later accepted implementation-boundary decision explicitly authorizes it and changes `STATUS.md`. ADR-0008 accepts research functions, not that implementation boundary.

The narrow engineering exception in `decisions/ADR-0005-offline-pilot-tooling.md` permits `tools/synthetic_pilot.py` and its bundled scripted subject to rehearse public synthetic inputs, controls, evidence binding and blind-packet export. It does not authorize a model/provider adapter, arbitrary corpus, stable cross-system interface or performance claim. Do not treat scripted outputs as completed case studies or reviewer calibration.

Under ADR-0001’s case-validity tooling scope, `tools/continuity_inputs.py` may prepare and verify inputs and audit literal projections for the bundled `RC-005-zh-CN` candidate. It executes no subject. Exact histories and candidate probe contracts live in `case-lab/fixtures/ct-authorship.zh-CN.json`; the Case Card explains their meaning. Update affected case documentation and regression checks when that source changes. Prepared inputs are ignored local derived artifacts, not authored source or accepted case results. This does not extend ADR-0005 to model/provider adapters.

Use `system under study` for a technical system. Reserve `community contributor`, `co-researcher`, and `reviewer` for people. Use `probe evidence contract` for case-bounded reference evidence; do not imply that a case author owns total relationship truth.

Cases and system work must distinguish deployment domain, memory content domain, use domain, coverage stratum, and system boundary where they matter. Preserve valid general-memory controls, mixed-domain routing, scope isolation, and full-history/full-search comparison without mandating one architecture.

## Research and privacy boundaries

- Public case material is synthetic and represents adults only.
- Raw private conversations, identifying consent records, credentials, private system details, and restricted review notes do not belong in this repository.
- A named source or claim in the vision draft is unverified until an Evidence Card pins and checks the exact object.
- Architecture absence, hidden observability, and adapter reconstruction are different findings; do not collapse them into one failure label.
- Community contribution governance is not a substitute for any institutional ethics review required by a future formal human-participant study.
- Ignore rules are also a checker's reading boundary; do not recursively scan local experiment records or follow public symlinks into them.

## Documentation and verification

Update the authoritative surface whose truth changed. Keep stage, evidence, and publication status explicit: template, seed, clinic-ready, reviewed, accepted, implemented, released, and live are not interchangeable.

Run:

```bash
python3 -B tools/check_repo.py
python3 -B -m unittest discover -s tests -v
```

The offline rehearsal commands and limits are in `experiments/offline-rehearsal.md`. Review the complete diff before any commit. The public `origin` remote is current project state; publication of private material, external outreach, formal releases, and deployment still require their own authority.
