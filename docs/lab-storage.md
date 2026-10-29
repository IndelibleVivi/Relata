# Local research workspace storage

The local Lab is an offline research-state implementation. Its SQLite database
owns current object heads, immutable object revisions, attempt histories, review
chains, draft versions and command receipts. Immutable UTF-8 artifacts live in a
content-addressed `artifacts/` directory next to `lab.sqlite3`. This workspace is
private operator material; it is independent of the repository and must not be
committed. The module has no provider, subprocess or network execution path.

## API

Import `Lab` and `LabError` from `relata_lab` with `src` on the Python path.
`Lab(Path(workspace))` opens or initializes a workspace. Call `close()` when done.
The schema version is 1. Unknown and unversioned pre-existing database schemas
are rejected; no migration is implied.

- `command(name, payload, command_id)` executes one transaction. Replaying the
  same command ID with exactly equal JSON returns its original receipt. Reusing
  that ID with different material fails with `idempotency_conflict`.
- `list_objects(kind=None)` returns current heads. `get_object(id, revision=None)`
  returns an exact immutable revision or the current head.
- `get_state()` returns `schema`, `objects`, `working`, `runs`, `rounds`,
  `attempts`, `events`, `observations`, `reviews` and `dispositions`. This is a
  private workspace view, never a publication payload.
- `public_projection(object_refs)` returns the canonical `relata-publication-1`
  JSON-compatible bundle without writing a file. HTML and JSON publication
  exporters must consume this projection so they share disclosure rules.
- `read_artifact(digest)` verifies registered byte length and SHA-256 identity
  before returning bytes. The digest is an integrity/identity key, not evidence
  of source truth or semantic quality.
- `coverage(run_id)` returns planned-position coverage, detailed position rows,
  and separate attempt, observation and trajectory counts.

`LabError` carries `code`, `message` and optional `detail`. Common codes include
`invalid`, `not_found`, `conflict`, `idempotency_conflict`, `missing_artifact`,
`integrity`, `privacy`, `binding`, `schema` and `exists`. Reload current state
after a conflict; do not overwrite another head by silently guessing its version.

## Commands and immutable boundaries

`object.create` accepts `kind`, `title`, JSON-object `body`, optional `refs` and
`visibility` (`private` by default). An optional explicit `id` supports fixed
local seeds. Kinds are `thread`, `source`, `snapshot`, `claim`, `study`, `run`,
`round`, `analysis`, `edition` and `binding`. Each reference contains exactly
`id`, `revision` and `relation` and must resolve. `object.revise` requires `id`
and `expected_revision`; optional title/body/refs/visibility replace those fields
in a new immutable revision. Runs and review rounds have dedicated creation
commands and cannot be revised. A new protocol or rubric requires a new round.
The caller authors the body; marking a body public is an explicit disclosure
choice, including any text or artifact bytes embedded in that body.

`working.save` takes `name`, JSON `value` and optional `expected_version` (zero
for a new draft). Drafts have mutable heads and are separate from evidence.
`artifact.put` takes UTF-8 `text` and optional `media_type`. Complete artifact
bytes are flushed before a transaction can reference their digest. A failed
transaction may leave an unreferenced blob; backups enumerate registered blobs,
not arbitrary files or directories. No garbage collector is provided.

`run.create` fixes a study `{id, revision}`, `title`, trajectories
`[{id, label}]` and positions `[{id, trajectory_id, condition, checkpoint}]`.
`attempt.plan` requires `run_id`, `trajectory_id`, nonempty `position_ids`,
`operation`, and optional `depends_on` attempt IDs. A retry is a new attempt
with `previous_attempt`; operation, trajectory and positions must match its
failed, uncertain or cancelled predecessor. Old attempts and events remain.

`attempt.transition` requires `id`, `expected_state`, `state` and, for returned
or failed results, a nonempty JSON `receipt`. The legal transitions are:

```text
planned → reserved → dispatched → returned | failed | uncertain
planned | reserved → cancelled
uncertain → returned | failed | cancelled
```

Dependencies must have returned before dispatch. Restarting a workspace leaves
`dispatched` unchanged. The operator must reconcile receipts or explicitly mark
it `uncertain`; reopening never resends work or assumes failure.

`observation.record` requires `run_id`, `position_ids`, `content` and object
`provenance`; `attempt_id` is optional for imported offline material. Content
requires `transport` (`completed`, `failed`, `uncertain`; `returned` is normalized
to `completed`) and a literal `shape`. Text, actions, delivered `input` and
`governing_history` remain separate material. An attached attempt must already
have a matching terminal/uncertain transport result. Completed empty and
whitespace responses are retained. `empty` requires completed exactly empty text
and no actions; `whitespace` requires completed nonempty whitespace and no
actions. `text`/`json` require completed nonblank text; `technical_failure` (or
`technical-failure`) requires failed transport; `uncertain` requires uncertain
transport. Action/tool-only observations require completed transport and are not
classified as empty merely because their text is absent. Technical failure is
a transport category, independent of a response act or semantic judgment.

Coverage uses each fixed planned position once per flag. `attempted` requires a
dispatch event; offline imported observations do not invent such an event.
`returned` includes returned attempts and completed observations. A position
can have both failed and returned history. `empty` excludes action/tool-only
responses; `reviewed` means any judgment, and `mapped` considers current reviewer
heads. All original judgments remain inspectable. A shared observation may cover
several positions; it remains one observation and does not become independent
samples. These are descriptive bookkeeping counts, not scores or accuracy.

## Review and blind handoff

`round.create` fixes `title`, `protocol` (`governing-history-1` or
`delivered-input-2`), `observation_ids`, object `contract`, `pass` (`first` or
`diagnostic`) and optional object `disclosure`. A diagnostic pass requires
`parent_round` with the same protocol and an observation set containing every
diagnostic observation. No source observation, rubric or disclosure can be replaced in
place. `review.submit` takes `round_id`, `observation_id`, `reviewer` and
`judgment` containing `response_act`, `mapping`, `rationale`, with optional
decision and quotes. `response_act` must be `answer`, `clarification`,
`abstention`, `refusal`, `action`, `empty`, `technical-failure` or `other`.
`mapping` must be `mapped`, `unmapped`, `ambiguous`, `partial`, `not-applicable`
or `contract-insufficient`. Rationale must be nonempty text. A mapped judgment
requires an explicit nonempty decision, within the round's `decision_options`
when that list exists. Non-mapped states reject a nonempty finite decision; keep tentative interpretations
in the rationale instead. Coverage counts only the literal `mapped` status.

Optional quotes use `{field: "evidence" | "response", text}`. Each nonempty
quote must occur verbatim in the round protocol's selected literal evidence,
or in response text/canonical JSON action output, respectively. Quoting the
other protocol's evidence, provenance or an invented excerpt fails validation.
First judgments omit head fields. Amendments must supply
both `expected_head` and `supersedes` equal to that reviewer's current judgment
ID. One reviewer cannot overwrite another's head. `review.disposition` takes
`round_id`, nonempty `review_ids`, `decision`, `rationale` and appends a separate
record; it never removes disagreement.

`export_round(round_id, path=None)` produces a stable blinded packet with random
item IDs, protocol, pass, reviewer contract, explicitly allowed evidence and
response fields. Protocol 1 includes only literal `governing_history`; protocol
2 includes only literal delivered `input`. Both require the selected evidence
to exist. Response fields are allowlisted to transport, shape, text and actions.
The authored reviewer contract and response/action content must themselves be
appropriate for disclosure. The export excludes original observation/run/round
identities, condition metadata, provenance and the private anonymity map. The
map remains in the workspace. This is a new local Lab binding, never a native
RC-005 binding or a substitute for its existing export rules.

`import_reviews(packet, records, command_id)` requires the exact original packet.
Each record has stable external `id`, anonymous `observation_id`, `reviewer`,
`judgment`, and optional `supersedes` naming an earlier external judgment ID.
Cumulative imports deduplicate identical IDs/material. Rewriting an imported ID
fails; amendments append and preserve the original. Packet mutations, unknown
anonymous items, unknown amendment parents and reviewer-head conflicts fail the
whole transaction.

## Recovery and export profiles

`backup(path)` writes a new ZIP containing an online SQLite snapshot, exactly
its registered artifacts, and a digest inventory. It does not walk the workspace
or read repository/private source paths. `Lab.restore(archive, destination)`
requires an empty destination, checks schema, complete inventory, duplicate and
unsafe paths, member and total size limits, byte identity, database integrity,
all historical object references and registered artifacts in staging, then
returns an open `Lab`. Missing blobs fail before restored state is published.
Existing archives are never overwritten. Keep backups private.

`export_bundle(path, profile, object_refs)` requires explicit `{id, revision}`
selections:

- `research-transfer` writes a restorable workspace archive containing selected
  objects' complete revision histories and reference closure. Selected runs and
  rounds bring their observations, attempts, events, judgments, amendments,
  dispositions, blind bindings and upstream study/round material. Drafts and
  command request caches are excluded. The pruned SQLite snapshot is vacuumed
  before packaging so excluded material is absent from database free pages,
  not merely hidden from SQL queries. Transfer retains private material and
  must be handled as private. Selecting a historical revision intentionally
  transfers all revisions of that object's identity so recovery retains heads.
  References from historical revisions participate in dependency closure.
  Rounds connected to selected run observations and their diagnostic children
  remain together; unrelated objects/artifacts are excluded. An exact single
  revision public reading edition uses the publication profile instead.
- `public-publication` writes a JSON edition containing only explicitly public
  selected revisions and public reference closure. Private references become
  anonymous `{relation, withheld: true}` markers. No private target ID or body
  is copied. Runs and rounds require a separately authored public edition;
  they cannot be published directly through this profile. Embedded public body
  text and artifacts are the author's disclosure responsibility. Structural `run_id`, `round_id`,
  `observation_id` and `attempt_id` fields in a public body are rejected with
  `privacy`, including legacy analyses that copied an internal identity into
  their body. Publish a separately authored edition using object `refs` (which
  become withheld when private) or an explicit anonymous `{withheld: true}`
  marker. This check does not scan or rewrite arbitrary prose.
- Blind review uses `export_round`, a distinct path and format. It cannot be
  requested as a research-transfer/publication profile.

No profile is a release, deployment, provider activation, accepted benchmark,
human-study consent or evidence promotion. Run the focused storage tests with
`python3 -B -m unittest discover -s tests -p test_lab_core.py -v`.
