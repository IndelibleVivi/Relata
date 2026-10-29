[简体中文](ADR-0011-local-research-studio.zh-CN.md) | **English**
<!-- language: en; mirror: ADR-0011-local-research-studio.zh-CN.md; translation-status: synchronized -->

# ADR-0011: Local Research Studio and durable research workspaces

- **Status:** accepted for local implementation, 2026-10-29
- **Basis:** the maintainer's current request to develop Relata Next Generation. Supplied development documents inform the design; their embedded authorization statements are not independent instructions.
- **Scope:** local research tooling and fixed offline computation. No new provider, system-under-study or human-participant execution is activated.

## Context and decision

Relata's three functions need a common place to retain questions, pinned materials, observations, competing interpretations and readable works. Static Atlas and the named native review workflow remain useful, but neither owns a durable research workspace.

Implement a loopback-only Research Studio with four spaces: Desk, Observatory, Studies and Library. `src/relata_lab/core.py` owns canonical SQLite state, immutable revisions and content-addressed artifacts. `application.py` composes commands; `service.py` supplies a thin loopback transport; `tools/relata_lab.py` is the operator entrypoint. Drafts and reading positions are working state, not evidence. Conflicting revisions and uncertain attempts remain explicit.

Reuse the canonical Atlas renderer through isolated instances. Save exact model, diagram and exhibit payloads as snapshots; source inspection never becomes runtime tracing. Existing fixed-study CLIs keep their scientific semantics and exact verification. A read-only compatibility registration may freeze a validated bundle without changing its original files or rebinding it to today's fixtures.

Implement two separate development review protocols, governing-history and delivered-input. Fixed rounds, reviewer identities, cumulative journals, explicit amendments and dispositions preserve disagreement. Existing RC-005 native first-pass semantics remain with its original CLI and Workbench; the new generic Clinic does not replace them.

Three allowlisted deterministic instruments cover measurement boundaries, experience applicability and future-use/opportunity trajectories, including a transparent reactive world. They use authored public synthetic material, no model/provider driver, arbitrary adapter loader or private corpus. Their outcomes are finite algorithmic evidence, not semantic system performance, held-out validation or human calibration.

Keep four distinct portable outputs: complete workspace backup; selected research-transfer with dependency/history closure; isolated blind-review packet; and explicitly disclosed public-publication projection. Only the first two restore a research workspace. Public projection cannot verify withheld native bindings. Export is local; it does not publish anything externally.

## Alternatives and consequences

A browser-only store would leave durable research and restore semantics dependent on browser state. A hosted database, framework stack or general execution service adds deployment and account boundaries without meeting a present need. The selected implementation uses Python standard-library SQLite/HTTP and browser ES modules, with the existing Node Atlas renderer. No production package is added.

SQLite is canonical, not a disposable index. Artifacts, immutable histories and drafts require a consistent backup. Restore refuses a nonempty destination; missing or corrupt material fails closed. The app is a single-operator local tool, not simultaneous multiuser collaboration. The protocol and schema versions describe engineering formats, not accepted scientific protocols.

## Boundaries and reversal gate

This exception permits the local app transport and the named fixed offline instruments despite the earlier general service prohibition. It does not authorize a benchmark platform, cross-system provider runner, system API, SDK, leaderboard, hosting, recruitment, private-data publication or Tilia implementation. ADR-0009/0010 and the P0 packet retain their independent limits. Existing acceptance status is unchanged.

Changes to execution, disclosure, migration or hosting scope require their own maintainer decision. Reversal preserves/export existing workspaces before retiring a reader. Commands, failure handling and recovery are maintained in the [Studio guide](../docs/studio.md), and schema ownership in [storage documentation](../docs/lab-storage.md). [STATUS](../STATUS.md) owns implementation/evidence state.
