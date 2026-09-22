[简体中文](README.zh-CN.md) | **English**
<!-- language: en; mirror: README.zh-CN.md; translation-status: synchronized -->

# Relata System Census

The System Census studies how actual memory and agent systems work, what their architectural choices enable or constrain, and how they sustain continuity. It supports independent comparative research as well as future system-under-study boundary choices. General agent use and adult long-term intimacy are both in scope; start with the [agent-memory inquiry](../research/agent-memory-inquiry.md).

A census object may be a memory engine, context compiler, complete companion agent, local personal stack, manually curated archive, agent framework, or mixed architecture. A system need not expose discrete memories, retrieval candidates, or a write/search API to be represented.

The [ten source studies](source-studies/README.md) cover Mem0, current Letta, Graphiti, lmc-5, Tideline Memory, Aelios, Hindsight, OpenViking, LangMem and A-MEM at pinned public commits. The [architecture atlas](architecture-atlas/README.md) provides three source-linked views per project, with standalone SVGs and an offline interactive reader. They include conditional architecture comparisons and two isolated offline observations. They remain source-study drafts, separate from reviewed or accepted System Cards.

## Classification

- `N` — system-native and observed or contributor-confirmed;
- `E` — adapter-emulated outside the native boundary;
- `O` — opaque at the selected boundary;
- `U` — unsupported by the represented system/version;
- `?` — unknown or not checked;
- `—` — not applicable to this architecture.

`O`, `U`, and `?` are different findings. None means “inferior.”

## Census workflow

1. **Basis and scope:** choose public-source research, an authorized contributor description, or a clearly separated combination. Pin the repository/version and distinguish public implementation, hosted service and historical source. For contributor material, identify disclosure authority and forbidden details.
2. **System-native description:** map components, retained or reconstructed material, update and activation behavior, surfaces, and outputs in the system’s own vocabulary.
3. **Evidence and limits:** distinguish public source, contributor-reviewed description, reproduced probe, inference, and unknown behavior.
4. **Review:** public-source cards receive source-fidelity review with the inspected paths and unresolved claims visible; maintainer endorsement is not required or implied. Contributor-derived material additionally requires the authorized contributor to correct its description and approve public-safe fields.
5. **Boundary pressure:** compare cards in an Architecture Pressure Map only after individual cards are reviewed.
6. **Research transfer:** record which proposed Relata boundary measures the system, an adapter, an opaque composite, or a capability outside scope.

The census does not require production access, credentials, raw chats, or private configuration. A contributor-described system need not publish source code. Restricted cards stay outside the public repository; their public summaries require contributor approval. Independent analysis of already-public sources does not require a system owner's permission, and must not imply insider knowledge or endorsement.

Write conditional architectural judgments: what a mechanism makes possible, the costs or constraints it introduces, who supplies missing integration, and the evidence for each statement. Separate source inspection from runtime observation; the classification above is not a performance grade. Source essays can remain clearly labeled drafts while System Card review is pending.

Every first-round System Card should also ask:

- How are ordinary personal history and operational/project history represented, if at all?
- How are multiple projects, roles, people, surfaces, accounts, and instances isolated or connected?
- How does the system decide whether personal, relational, or operational material belongs in the current context?
- What happens under full-history or full-search exposure, and which native boundaries make that comparison meaningful or distorting?

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
- multi-project isolation and cross-domain context contamination;
- artifact/source authority and decision supersession;
- role/surface routing and full-history behavior.

These are pressure questions, not required capabilities or scoring dimensions.
