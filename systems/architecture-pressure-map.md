[简体中文](architecture-pressure-map.zh-CN.md) | **English**
<!-- language: en; mirror: architecture-pressure-map.zh-CN.md; translation-status: synchronized -->

# Architecture Pressure Map

**Status:** first census pressure map; public-source synthesis of ten bounded studies; no runtime, capability, or ranking result.
**Basis:** static source studies at pinned commits, plus two isolated offline source-branch checks. `N` here means source-observed at the pinned version, never verified runtime behavior.
**Companion cards:** [`SC-001` Mem0](system-cards/SC-001-mem0.md) · [`SC-002` Graphiti](system-cards/SC-002-graphiti.md) · [`SC-003` Letta](system-cards/SC-003-letta.md)

This map records where ten architectures sit on the pressure dimensions opened by [`EC-001`](../research/evidence-cards/EC-001-agent-memory-leaderboard.md) and the [System Census workflow](README.md#census-workflow). Rows are proposed observation demands, not a universal capability checklist and not a scoring rubric. Read it together with the [System Card template](system-card-template.md) legend and the [source studies](source-studies/README.md).

Legend: `N` system-native and source-observed at the pinned version · `E` adapter-emulated outside the native boundary · `O` opaque at this boundary · `U` unsupported by the represented version · `?` unknown or not checked · `—` not applicable.

**Fidelity review:** 2026-10-23, against the existing source studies and atlas models only; no new full upstream reading or system execution. Earlier review provenance was not established.

## Represented systems and evidence binding

| Key | System | Source study | Pinned version | Evidence class | Reviewed card |
|---|---|---|---|---|---|
| MEM | Mem0 Python OSS | [mem0.md](source-studies/mem0.md) | `a39a802` | static source | [SC-001](system-cards/SC-001-mem0.md) |
| LET | Letta local backend | [letta.md](source-studies/letta.md) | `f5c5bbc` | static source | [SC-003](system-cards/SC-003-letta.md) |
| GRA | Graphiti | [graphiti.md](source-studies/graphiti.md) | `16cdf70` | static source + offline branch check | [SC-002](system-cards/SC-002-graphiti.md) |
| LMC | lmc-5 upstream | [lmc-5.md](source-studies/lmc-5.md) | `fb3e72c` | static source + offline branch check | none |
| TID | Tideline Memory | [tideline-memory.md](source-studies/tideline-memory.md) | `76490fe` | static source | none |
| AEL | Aelios | [aelios.md](source-studies/aelios.md) | `9e65c80` | static source | none |
| HIN | Hindsight | [hindsight.md](source-studies/hindsight.md) | `9c7f6c6` | static source | none |
| OVI | OpenViking | [openviking.md](source-studies/openviking.md) | `bbf2e37` | static source | none |
| LAN | LangMem | [langmem.md](source-studies/langmem.md) | `9d033b4` | static source | none |
| AMEM | A-MEM paper implementation | [a-mem.md](source-studies/a-mem.md) | `0c8039f` | static source | none |

The three reviewed cards are the deep dives; the matrix below still covers all ten studies so the comparison is not restricted to carded systems. Every cell is a static source observation about the represented version, not a measured outcome.

## Pressure matrix

| Proposed observation or demand | MEM | LET | GRA | LMC | TID | AEL | HIN | OVI | LAN | AMEM |
|---|---|---|---|---|---|---|---|---|---|---|
| accepts an ordered history or event stream | N | N | N | N | N | N | N | N | N | N |
| exposes a distinct write or ingest operation | N | N | N | N | N | N | N | N | N | N |
| exposes entry-specific completion signals | O | N | N | O | O | O | O | O | O | O |
| returns retrieval or activation candidates | N | N | N | N | N | N | N | N | N | N |
| returns rendered model context | E | N | E | N | N | N | E | N | E | N |
| produces the final response or action | U | N | E | E | E | E | N | U | E | N |
| preserves source or provenance references | O | N | N | O | O | N | N | N | O | U |
| exposes current, historical, or conditional state | O | N | N | N | N | N | N | N | O | O |
| distinguishes human statement from companion inference | O | O | O | O | O | O | O | O | U | U |
| supports correction or revocation through a visible route | N | N | N | N | O | N | N | N | N | U |
| supports prospective-intention trigger or wake behavior | U | ? | U | O | O | O | O | O | O | U |
| exposes inspection or explanation | N | N | N | N | N | N | N | N | N | N |
| supports model, instance, or surface migration | ? | N | ? | O | ? | O | ? | N | ? | ? |
| exposes technical partition or scope keys | N | N | N | O | U | N | N | N | N | U |
| establishes project isolation beyond caller scope mapping | O | O | O | O | U | O | O | O | O | U |
| preserves artifact and source authority | O | O | O | O | O | O | O | O | U | U |
| exposes revision, version, or supersession mechanisms | O | N | N | N | N | N | N | N | U | U |
| routes by role or surface | O | O | O | O | O | N | O | N | O | U |
| exposes retained-source or historical-material lookup | O | N | N | N | N | N | N | N | O | O |
| avoids cross-domain context contamination | O | O | O | O | O | O | O | O | O | U |
| permits static source inspection without provider calls | N | N | N | N | N | N | N | N | N | N |
| can bind an exact observable version or configuration | N | N | N | N | N | N | N | N | N | N |

## Required interpretation

For every `E`, `O`, `U`, or `?` cell, the evidence and consequence follow. Cells not listed are `N`: the mechanism is visible in the pinned source. `O` and `U` are different findings; neither means "inferior". A "boundary" here observes the system, an application-supplied adapter, an opaque composite, or a capability outside scope, and each cell names which.

**Row 3, entry-specific completion signals.** `N` for LET's file/Git commit and GRA's awaited write, within those inspected entry points; neither proves later semantic use. `O` for MEM (returned ADD/history is not per-fact persistence or searchability proof), LMC (current-state/vector channels can lag supersession), TID (amendment commit precedes best-effort derived updates), AEL (human input is awaited but assistant output is recorded later), HIN (async operation ID means submitted), OVI (snapshot completed can conceal reindex errors), and AMEM (metadata/index updates diverge). LAN is `O`: hot tools and the async store manager await their specific Store operations, but local reflection queues are not durable, remote futures acknowledge submission, and sync mutation completion has an unverified source-level concern. See the respective source-study write/update sections and LangMem's “延迟与回执”; no system-wide durable-readiness guarantee is inferred.

**Row 5, rendered model context.** `N` where the represented system itself produces the model-facing context: LET compiles a system prompt (source study, "一条写入、保留、使用与修订路径"); LMC SessionStart restores a start context (source study, "一条生命周期及接线责任"); TID injects identity/tiered context (source study, "判断与原生生命周期"); AEL appends a temporary patch to the current user turn (source study, "写入、保留、选择、使用"); OVI returns an `AssembleResult` (source study, "状态与全生命周期"); AMEM's harness builds the prompt (source study, "选择、context 与回答"). `E` where assembly lives in caller or example code: MEM has no `chat` and the caller assembles (source study, "检索与交接"); GRA's example concatenates `edge.fact` (source study, "时间、冲突与来源"); HIN's LiteLLM callback is one optional integration (source study, "写入、后台归纳、读取与使用"); LAN's prompt callback is a guide example (source study, "对象、生命周期与使用").

**Row 6, final response or action.** `N` where the boundary includes generation: LET runs the agent (source study, "结论与对象边界"); HIN `reflect` synthesizes an answer (source study, "写入、后台归纳、读取与使用"); AMEM's harness answers (source study, "选择、context 与回答"). `E` where generation is external: GRA/TID/AEL/LAN use an application or model outside the memory layer (GRA "时间、冲突与来源"; TID "判断与原生生命周期"; AEL "写入、保留、选择、使用"; LAN "运行与存储边界"); LMC injects context but the main agent generates (source study, "一条生命周期及接线责任"). `U` where no generation route exists: MEM has no `chat` (source study, "检索与交接"); OVI returns context and final use is unknown (source study, "边界与模型").

**Row 7, provenance.** `N`: LET keeps message IDs, roles, timestamps and Git commits (source study, "可检查性、来源与控制"); GRA keeps episode UUIDs and bi-temporal edges (source study, "时间、冲突与来源"); AEL keeps source messages and `authored_by` (source study, "修订、curation 与遗忘"); HIN keeps `source_memory_ids` and document IDs (source study, "状态与写入权"); OVI keeps version/source/freshness metadata (source study, "权威分层"). `O`: provenance exists but is weak or model-produced: MEM `attributed_to` is LLM output (source study, "来源、角色、时间与派生影响"); LMC curated `source` is a path/trace without forced speaker or subject (source study, "证据、纠正、scope 与连续性边界"); TID `source_links` are optional and unverified (source study, "判断与原生生命周期"); LAN has no version ledger (source study, "更正、删除与模型权威"). `U`: AMEM does not fill structural provenance (source study, "输入、笔记与 state ownership").

**Row 8, current/historical/conditional state.** `N` where the system exposes supersession or version state: LET Git history (source study, "修改、删除及派生影响"); GRA `valid_at`/`invalid_at` (source study, "时间、冲突与来源"); LMC current/review/superseded (source study, "证据、纠正、scope 与连续性边界"); TID amendments and effective text (source study, "判断与原生生命周期"); AEL versions and `includeHistory` (source study, "修订、curation 与遗忘"); HIN invalidation archive and model history (source study, "更正、删除与派生状态"); OVI version and archive/live (source study, "状态与全生命周期"). `O`: MEM keeps `created_at` and history but no current-vs-historical query semantics (source study, "来源、角色、时间与派生影响"); LAN exposes current key only while its versioned-history docstring is unsupported by the write path (source study, "文案与实现需区分的地方"); AMEM rewrites context without revision history (source study, "更正、删除、保留与 relational use").

**Row 9, human statement versus companion inference.** No carded system cleanly separates these, which is the pressure D-002 names. `O` where a partial cue exists but not an authority model: MEM role-based extraction and LLM `attributed_to` (source study, "来源、角色、时间与派生影响"); LET roles and Git author but no per-fact source (source study, "可检查性、来源与控制"); GRA episode source links with a caller-side risk of mistaking agent write-back for human approval (source study, "时间、冲突与来源"); LMC "user said/assistant replied" atoms but curated schema lacks forced speaker (source study, "证据、纠正、scope 与连续性边界"); TID USER/ASSISTANT markers and `entities_role` (source study, "判断与原生生命周期"); AEL `authored_by` with a judge, but `authored_by` is not authentication (source study, "修订、curation 与遗忘"); HIN caller-provided source context, bank display name is not narrator (source study, "写入、后台归纳、读取与使用"); OVI self/peer separation by rule, not consent (source study, "有条件优势与限制"). `U`: LAN lets the model decide authority (source study, "更正、删除与模型权威"); AMEM has only a speaker string (source study, "更正、删除、保留与 relational use"). This row is a finding about the observation boundary, not a defect label.

**Row 10, correction or revocation route.** `N` where a visible route exists, with the recorded caveat: MEM update/delete (source study, "更新与删除"); LET `memory delete` (source study, "修改、删除及派生影响"); GRA `remove_episode` (source study, "Scope、更新与撤回"); LMC supersede and patrol (source study, "一条完整生命周期及接线责任"); AEL upsert/supersede/archive/delete (source study, "修订、curation 与遗忘"); HIN invalidate/edit/delete (source study, "更正、删除与派生状态"); OVI content write and rm (source study, "状态与全生命周期"); LAN update/delete tool (source study, "更正、删除与模型权威"). `O`: TID has a visible correction route but no delete/forget tool in the listed MCP tools (source study, "判断与原生生命周期"). `U`: AMEM has no correction or delete API (source study, "更正、删除、保留与 relational use").

**Row 11, prospective-intention trigger or wake behavior.** `O` marks adjacent maintenance or context-supply mechanisms, not an established intention-execution contract: TID injects open threads and runs DREAM maintenance; LAN schedules reflectors, with remote `after_seconds`; LMC has cron/sweep; AEL has Dream and associative trigger vectors; HIN refreshes mental models; OVI schedules resource refresh/session commit. Their source studies do not establish valid-intention triggering and withdrawal/expiry handling across those paths. `U`: MEM has visibility expiry, GRA validity-time fields, and AMEM no wake route in the represented boundary. `?`: LET schedulers were not reviewed. Text about future plans may still be stored; storage is distinct from wake execution.

**Row 13, migration.** `N`: LET files and Git are migratable and Cloud syncs across machines (source study, "修改、删除及派生影响"); OVI has a snapshot/restore reindex path (source study, "恢复与回执的具体落差"). `O` where a reference pattern or provider binding exists but execution is unproven: LMC Forge/Swap are deployment references (source study, "证据、纠正、scope 与连续性边界"); AEL is Cloudflare-bound with provider routing (source study, "精确对象与版本选择"). `?` where migration was not investigated: MEM, GRA, TID, HIN, LAN, AMEM.

**Row 14, technical partition keys, and Row 15, project isolation.** Row 14 `N` identifies source-visible keys: MEM scope IDs, LET agent/conversation, GRA group_id, AEL write/read namespaces, HIN bank/scoped SQL, OVI account/user/peer, and LAN namespace templates (see their source-study scope sections). LMC is `O`: thread labels do not constrain fact_key or cross-session search. TID and AMEM are `U` for native multi-scope keys in the represented boundaries. Row 15 is `O` for the eight systems with technical scope or caller/deployment mapping: keys do not establish an independent project-authorization guarantee; TID and AMEM remain `U`. HIN tags/untagged visibility need explicit handling. AEL's legacy orphan-vector fallback concerns liveness/grounding, not evidence of cross-namespace leakage.

**Row 16, artifact and source authority.** Almost every system preserves references without an authority model, so most cells are `O`: MEM LLM `attributed_to`; LET Git author without fact attribution; GRA source links without truth guarantee; LMC evidence-presence gate that does not verify existence (source study, "证据、纠正、scope 与连续性边界"); TID optional `source_links`; AEL `authored_by` without authentication; HIN source IDs with best-effort grounding; OVI version/source metadata (see row 7 citations). `U`: LAN and AMEM (see row 7). This is the sharpest shared gap and the reason D-002 and the "artifact and source authority" incident family stay open.

**Row 17, revision/version/supersession mechanisms.** `N`: LET, GRA, LMC, TID, AEL, HIN and OVI expose source-visible version, amendment or invalidation mechanisms (row 8 sources). This does not establish accepted decision authority or correct semantic supersession. `O`: MEM explicit updates and history do not persist the prompt's revision lineage. `U`: LAN's represented write path only replaces the current key; AMEM rewrites context without revision history.

**Row 18, role or surface routing.** `N` describes only the technical source-visible routing in AEL gateway identity/read namespaces and OVI URI/actor-peer scope (their source-study lifecycle sections), not audience consent. `O`: MEM, LET, GRA, LMC, TID, HIN and LAN depend on caller mapping or lack an inspected role/surface route. LAN's hot/background split changes update timing; it is not role/surface routing. `U`: AMEM in the represented boundary.

**Row 19, retained-source or historical-material lookup.** `N` records lookup routes, not complete original-history coverage: LET transcript search; GRA episode lookup with optional raw-content retention; LMC raw search; TID MCP search over rewritten/truncated narratives, contexts and amendments; AEL original windows under its default seven-day raw-message retention; HIN documents/chunks; OVI archive messages.jsonl (their source-study retention/search sections). `O`: MEM's history/recent buffer lacks a full-search contract; LAN separates checkpointer and Store; AMEM's corpus index can lag. A strong full-history/full-search control must separately establish allowed-source completeness, retention and actual exposure; no such control is certified here.

**Row 20, cross-domain contamination.** `O` for all systems that rely on caller-supplied scope: MEM, LET, GRA, LMC, TID, AEL, HIN, OVI, LAN (see rows 14/15 citations; for HIN also untagged-default visibility in source study, "Bank、scope 与模型边界"). `U`: AMEM has no multi-domain isolation. No represented system natively routes personal, relational and operational material in its own vocabulary, so this row is a shared pressure rather than a differentiator.

**Row 21, static inspection without provider calls.** All ten are `N` for static source inspection, as their pinned studies demonstrate. A different question is model-free execution: only LMC and GRA have the recorded isolated offline branch checks, with synthetic inputs and doubles as documented in source-studies/README.md. Complete native operation without providers has not been established for the ten systems; missing runs or database dependencies do not prove impossibility. Row 22 binds exact source commits, not installed or live configurations.

## Protocol-bias record

This matrix is itself a protocol that can privilege or erase architectures. The explicit biases Relata must carry forward:

- Requiring "retrieval or activation candidates" privileges vector/graph services over file-first or Git-first systems, where the analogous event is a file read or a diff, not a ranked candidate list.
- Requiring a "rendered model context" privileges harness-gateways (LET, AEL) over libraries (LAN) and services (MEM), and would force an adapter that reconstructs the very assembly Relata claims to observe.
- Requiring "final response or action" inside the boundary privileges complete agents over memory layers and would exclude valid services.
- Treating a returned material object as evidence risks measuring an adapter rather than the system; MEM, GRA, HIN and LAN assembly is caller or example code.
- Mandatory cross-domain routing or mandatory multi-project keys would exclude single-scope designs (TID, AMEM) and file/Git designs (LET) that legitimately leave scoping to the harness.
- A full-history or full-search comparison requires retained raw history and penalizes systems that store only derived state; it must be run as a labelled control, not as a native-capability test.
- Static source observation cannot establish runtime behavior. Every `N` in this map means "present in the pinned source", never "observed working", and the two offline checks are isolated source-branch checks, not end-to-end results.

Consequence for Relata: name, per row and per system, whether a boundary observes the system, an adapter, an opaque composite, or nothing, and keep excluded or adapter-distorted systems visible. Do not collapse these outcomes into one score, and do not infer unobserved internal architecture from external behavior.

## Limits

All ten studies are source-study drafts without independent human review; classifications are editorial judgments over pinned source, and the two offline checks cover only specific source branches. Nothing here establishes performance, capability, safety, retention or relationship quality, and nothing here selects a benchmark interface or a preferred architecture.
