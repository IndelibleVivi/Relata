# Relata System Census

The System Census maps how actual memory and companion systems sustain continuity before Relata chooses a system-under-study boundary.

A census object may be a memory engine, context compiler, complete companion agent, local personal stack, manually curated archive, agent framework, or mixed architecture. A system need not expose discrete memories, retrieval candidates, or a write/search API to be represented.

## Classification

- `N` — system-native and observed or contributor-confirmed;
- `E` — adapter-emulated outside the native boundary;
- `O` — opaque at the selected boundary;
- `U` — unsupported by the represented system/version;
- `?` — unknown or not checked;
- `—` — not applicable to this architecture.

`O`, `U`, and `?` are different findings. None means “inferior.”

## Census workflow

1. **Permission and scope:** identify the contributor’s authority to describe the system, the exact version or date, visibility, and forbidden details.
2. **System-native description:** map components, retained or reconstructed material, update and activation behavior, surfaces, and outputs in the system’s own vocabulary.
3. **Evidence and limits:** distinguish public source, contributor-reviewed description, reproduced probe, inference, and unknown behavior.
4. **Contributor review:** let the authorized contributor correct the System Card and approve the public-safe fields.
5. **Boundary pressure:** compare cards in an Architecture Pressure Map only after individual cards are reviewed.
6. **Research transfer:** record which proposed Relata boundary measures the system, an adapter, an opaque composite, or a capability outside scope.

The census does not require source code, production access, credentials, raw chats, or private configuration. Restricted cards stay outside the public repository; only contributor-approved summaries may be added here.

Start from the [English](system-card-template.md) or [Chinese](system-card-template.zh-CN.md) System Card, then use the [Architecture Pressure Map](architecture-pressure-map-template.md).

## First pressure dimensions opened by source evidence

[`EC-001`](../research/evidence-cards/EC-001-agent-memory-leaderboard.md) does not choose a Relata interface. It gives the first concrete boundary to test against materially different systems. The first Architecture Pressure Map must therefore classify, rather than assume:

- synchronous ingestion and immediate search visibility;
- external chunking versus system-native episode/session boundaries;
- `user_id` and `session_id` as isolation and organization surfaces;
- whether Search sees the question and answer options;
- discrete, textual, relevance-ordered evidence with a fixed Top K;
- correction, revocation, expiry, provenance, authority, and disagreement semantics;
- final-answer generation inside or outside the system-native boundary;
- public version identity and the evidence that binds a result to that version.

These are pressure questions, not required capabilities or scoring dimensions.
