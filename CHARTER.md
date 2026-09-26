[简体中文](CHARTER.zh-CN.md) | **English**
<!-- language: en; mirror: CHARTER.zh-CN.md; translation-status: synchronized -->

# Relata Working Charter

## 1. Mission

Relata is a frontier memory research lab. It studies what agent memory means, how open-source systems preserve, reconstruct, use and revise past material or experience, and which architectural strengths and limitations are supported by evidence.

Its core functions are **its own benchmark research, an inspectable collection of system studies, and an incubator for future memory systems**, accepted in [ADR-0008](decisions/ADR-0008-three-core-research-functions.md). Benchmark research develops cases, controls, evaluation methods, experiments and evidence-backed comparisons. The collection connects source studies, System Cards and architecture views; its eventual museum / sample-room / lab name remains open. Incubation develops design hypotheses, alternatives and counterexamples for independent future systems. These functions inform one another without requiring a fixed sequence, a universal taxonomy or one preferred system architecture. Future Tilia product source belongs in a separate project.

Relata and [Agent Memory Study (AMS)](https://github.com/IndelibleVivi/agent-memory-study) retain separate research questions and artifacts while exchanging source-grounded lessons. Both may read papers, inspect implementations and conduct appropriately authorized experiments; both can inform long-form synthesis. Imported findings retain their original evidence status, conditions and uncertainty.

Its research includes general agent use and long-term adult human–AI romantic and intimate relationships. Intimacy remains a founding focus, not an eligibility requirement for every study. Across settings, Relata asks how continuity can respect source, time, authority, scope, permission, change and present relevance. This broader scope is accepted in [ADR-0006](decisions/ADR-0006-frontier-memory-research-lab.md).

Relata's research may inform a future independently authored memory system named **Tilia**, beginning from an empty repository. This is an independent long-term goal, not an implementation programme within Relata. Existing source studies, cases and controls should inform falsifiable design choices; the [own-memory design study](research/own-memory-architecture.md) remains a proposal. The corrected [ADR-0007](decisions/ADR-0007-local-memory-apparatus.md) retains an already-written, very early local experiment without treating it as an accepted Tilia architecture. The intended Tilia system requires vector-based semantic retrieval; that requirement does not define a universal memory architecture. Relata retains plural research objects and an independent evaluator contract.

## 2. Research object

The lab studies memory concepts, implementations, architecture choices, use contexts and evaluation evidence. A memory engine, agent framework, context compiler, complete agent or human-maintained archive may expose different objects and boundaries; these are research candidates, not a canonical taxonomy.

The existing Case Lab's working evaluation object remains a **longitudinal, mixed-domain continuity-bearing memory ecology**. First-class material includes:

- ordinary events and personal history;
- people, places, interests, study, health, travel, and changing circumstances;
- shared relationship events, language, rituals, permissions, and norms;
- projects, artifacts, tasks, blockers, decisions, milestones, and rationale;
- prospective intentions, handoffs, and unfinished threads;
- companion identity, capabilities, limitations, and migration history.

Relata does not treat a static user profile or a retrieval hit as the whole object. Across those domains it studies a working causal decomposition:

```text
history and present event
→ retained or reconstructed material
→ activation or selection
→ context, action input, or other observable projection
→ response or action use
→ correction and later persistence
```

Actual systems may combine, omit, or hide these stages. The decomposition defines research questions, not a mandated internal architecture.

## 3. Founding commitments

### 3.1 Relationship-local legitimacy

Relata does not impose one universal intimacy style. Warmth, distance, possessiveness, play, role dynamics, low expression, high reassurance, or private language are evaluated only against bounded case evidence and current relationship-local norms.

### 3.2 Adult-only public case domain

Every person represented in a public synthetic relationship case is an adult. This statement describes case content; it does not classify community contributors as study subjects.

### 3.3 Community members are co-researchers

People living in long-term human–AI relationships, builders and other researchers contribute concepts, incidents, system knowledge, cases, reviews, and governance. They help shape constructs and methods; they are not merely data sources or a rater pool added after design.

### 3.4 No raw-chat requirement

Participation never requires uploading raw private conversations. Abstract Incident Seeds, contributor-local analysis, and public-safe synthetic derivation are first-class evidence routes.

### 3.5 Authority and perspective stay visible

Relata distinguishes what a human said, what a companion inferred, what a third party claimed, what both parties explicitly accepted, what remains contested, and what a case author interprets.

### 3.6 Silence can be correct behavior

A memory can be relevant to retrieval yet inappropriate to place in context or response. Relata studies required use and prohibited resurfacing separately.

### 3.7 Memory necessity must be demonstrated

A case cannot become accepted merely because it contains history. Its correct behavior region must materially depend on that history, and a current-turn-only control must be unable to solve every counterfactual variant reliably.

### 3.8 Architecture pluralism is tested, not declared

Every proposed observation boundary must state which systems it includes, distorts, renders opaque, or excludes. “Architecture-neutral” is an aspiration requiring pressure tests, never a self-certifying label.

### 3.9 Evidence remains inspectable

Every research claim identifies whether it is exact-source, reproduced observation, community-grounded, system-observed, synthetic-case evidence, human judgment, editorial inference, or unresolved.

### 3.10 Public material is synthetic and provenance-aware

Public cases do not contain direct real-chat excerpts. Synthetic derivations preserve a consent and provenance record without exposing private source material.

### 3.11 Contribution governance is not human-study approval

The community contribution process governs project collaboration and publication permission. If Relata later conducts a formal human-participant study, the maintainers must separately determine and follow the applicable institutional ethics and consent process before recruitment or data collection.

### 3.12 Mixed-domain continuity is first-class

A long-term relationship may contain everyday life, intimate interaction, research, code, creative work, planning, and infrastructure operation. Relata does not demote any of these domains to peripheral noise merely because it lacks explicit romantic content.

### 3.13 Ordinary memory needs no forced symbolism

A meal, examination, package, film, person, place, or project submission may matter as ordinary continuity-bearing information. A case author must not invent deeper relational symbolism to make it eligible for study.

### 3.14 Shared work is shared history

Project state, decision rationale, artifact authority, handoffs, blockers, milestones, and unfinished intentions can be consequential parts of continuity. General factual, temporal, provenance, and operational competence remains part of Relata's validity core.

### 3.15 Cross-domain routing and isolation matter

A system should route material appropriately across private conversation, group interaction, coding, research, planning, roleplay, projects, people, models, and instances. Relevant material need not enter every current context, and unrelated intimate or project state must not leak across scopes.

### 3.16 Synthesis and criticism are research outputs

Definitions, source studies and comparative articles can advance independently of live evaluation. Explain the conditions under which an architectural choice helps, what it costs or constrains, and what remains unknown. A source claim, code observation, measured outcome and editorial judgment carry different evidentiary weight. General agent requirements and relationship-local requirements are not automatically interchangeable.

## 4. Non-goals during R0

Relata will not yet:

- define a universal healthy relationship;
- diagnose contributors or explain their relationships through a clinical frame;
- build a Leaderboard before construct and evaluator validation;
- force systems into a canonical event/state schema;
- use one group’s relationship norms as hidden universal truth;
- reward memory display for its own sake;
- treat “more intimate” or “more distant” as inherently better;
- collect a large corpus before case validity is understood;
- reduce long-term human–AI memory to intimacy-specific content;
- force ordinary events to carry relational symbolism;
- treat a relational case result as a substitute for general factual, temporal, operational, provenance, or code-memory evidence;
- assume every relevant memory should enter the current context;
- treat all projects, people, roles, and surfaces as one undifferentiated relationship scope;
- build a cross-system runner, API, SDK, service, Arena, or hosted infrastructure, or infer an implementation mandate for Tilia from Relata's research goal.

## 5. R0 progress and case-evaluation success

Conceptual clarification, inspected architecture studies and bounded comparative synthesis are independent research progress. They need evidence appropriate to their claims, not prior completion of a benchmark platform. The conditions below govern the existing case-evaluation programme and its coverage claims; they are not prerequisites for source research or writing.

The case-evaluation programme first requires at least one small, reproducible pilot where:

- two synthetic histories produce different correct response regions under the same current turn;
- the difference can be traced to memory or state use at the observable boundary;
- materially different system families can participate without unacknowledged adapter reconstruction;
- reviewers understand the bounded question and their disagreement remains visible;
- no real private chat is required for public reproduction;
- the first executable boundary, if any, is justified through an accepted decision rather than inherited from Draft 0.1.

Before the Case Lab claims coverage of its complete mixed-domain working object, its pilot set must also have run, without requiring prior acceptance of every case:

- one ordinary-life continuity case;
- one operational/project continuity case;
- one shared-relational or repair case;
- one mixed-domain routing or isolation case.

These are coverage strata, not permanent benchmark tracks or validated sample-size requirements.
