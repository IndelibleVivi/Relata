# Decision Records

Use decision records for claims that change project authority, protocol, public boundaries, or implementation direction.

Suggested form:

```text
ADR-0003-<decision-title>.md
```

Each record includes:

- status: proposed, accepted, superseded, rejected, corrected;
- context and evidence;
- decision;
- alternatives;
- architecture/community impact;
- consequences;
- review or reversal gate.

Vision documents do not become authority without an accepted decision record.

## Decision index

- [`ADR-0001`](ADR-0001-research-first-bootstrap.md) — begin as a research program and case lab;
- [`ADR-0002`](ADR-0002-vision-doc-is-non-normative.md) — preserve Target Architecture Draft 0.1 as non-normative history;
- [`ADR-0003`](ADR-0003-mixed-domain-memory-ecology.md) — retain a longitudinal mixed-domain memory ecology for the Case Lab; its overall deployment-domain restriction is superseded by ADR-0006.
- [`ADR-0004`](ADR-0004-r0-bilingual-documentation.md) — use Chinese-first bilingual documentation with stable paired authority during R0.
- [`ADR-0005`](ADR-0005-offline-pilot-tooling.md) — permit the narrow bundled offline synthetic rehearsal without accepting a research protocol.
- [`ADR-0006`](ADR-0006-frontier-memory-research-lab.md) — expand Relata into a frontier memory research lab, including general and intimate uses, architecture criticism and independent synthesis.
- [`ADR-0007`](ADR-0007-local-memory-apparatus.md) — corrected scope: withdraw the implementation-authority interpretation, distinguish the independent Tilia goal, and retain the already-written early experiment as engineering evidence.
- [`ADR-0008`](ADR-0008-three-core-research-functions.md) ([中文](ADR-0008-three-core-research-functions.zh-CN.md)) — make Relata's own benchmark research, system collection and incubation for future memory systems core functions; retain open collection naming and separate Tilia product source.
- [`ADR-0009`](ADR-0009-exploratory-research-boundary.md) ([中文](ADR-0009-exploratory-research-boundary.zh-CN.md)) — **accepted 2026-10-23**: separate bounded exploration from benchmark promotion; activate only the fixed RC-005 → pinned Mem0 packet, with all other execution/publication/deployment scopes separate.
- [`ADR-0010`](ADR-0010-bounded-provider-compatibility-checks.md) ([中文](ADR-0010-bounded-provider-compatibility-checks.zh-CN.md)) — **accepted**: permit one finite, operator-owned provider compatibility smoke over public original synthetic text; observations are kept private and only cover parsing, response forms, usage/identity visibility, vector dimension, finite values and batch order. This is independent of the separately accepted ADR-0009 RC-005 native packet.
