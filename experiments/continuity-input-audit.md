# Continuity input preparation and authorship audit

**Status:** offline candidate tooling; no subject execution, accepted protocol, or system result

## 中文摘要

本工具只处理 [RC-005-zh-CN / CT-AUTHORSHIP](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md) 的内置成人合成材料，准备独立 checkpoint 输入，并检查字面投影是否抹掉两条历史的作者区别。它把 2026-09-22 Continuity Trials 提案中的输入准备与碰撞审计合为一条实现，另补 prepared-directory verifier。原包四个家族的 72 份输入没有整体导入；此处是一个家族的 18 份待答输入。

## English summary

Prepare 18 unanswered inputs for one adult synthetic authorship case, verify the prepared directory against its bundled source, and audit literal input collisions. The two histories swap only proposal/acceptance speakers. This is case-validity tooling under ADR-0001, with no model call, adapter, scoring, or execution permission beyond offline preparation. The source case remains a seed.

## Source and responsibility

- [Case Card](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md) owns the bounded research question, human reading path, interpretation and acceptance state.
- [Authored fixture](../case-lab/fixtures/ct-authorship.zh-CN.json) owns exact histories, checkpoint boundaries, current requests, and candidate review contracts. It selects CT-AUTHORSHIP from the 2026-09-22 proposal; history and probe content are preserved.
- [continuity_inputs.py](../tools/continuity_inputs.py) is the only maintained implementation for this preparation/audit boundary. It has no arbitrary-corpus option or provider/subject API.
- Prepared directories and audit JSON are local derived artifacts. Keep them under ignored `experiments/artifacts/`; they are not tracked case releases. Do not edit a derived packet to repair the case; edit its source and build into a new directory.

The existing [RC-002 rehearsal](offline-rehearsal.md) executes a scripted transport double. This tool prepares RC-005 evidence views and executes no subject. Its speaker-preserving history must not pass through RC-002's text-only tape: that tape was designed for a location fixture whose contrast did not depend on speaker identity.

## Run from the repository root

Python 3.10+; standard library only, no credentials or network. Choose new output paths for each preparation/audit. Their parent directory must already exist; use physical paths, since symlink paths are refused. Existing output directories and report files are refused.

```sh
python3 -B tools/continuity_inputs.py check
python3 -B tools/continuity_inputs.py build --out experiments/artifacts/ct-authorship-demo
python3 -B tools/continuity_inputs.py verify experiments/artifacts/ct-authorship-demo
python3 -B tools/continuity_inputs.py audit --out experiments/artifacts/ct-authorship-collisions.json
```

`check` validates the bundled authoring data and checks its expected literal collision counts; it does not check an existing preparation. `verify` checks the preparation against the **current bundled source**, including expected contents and membership, rather than accepting only self-consistent stored hashes. It is for unanswered input preparation, not a future answered-review or historical-version verifier. Source revisions, missing/extra material, altered inputs or altered review state require investigation and a new preparation; never relabel the old directory as current.

If a build is interrupted, retain its directory and use a new output path after diagnosing the error. There is no automatic retry/resume or cleanup. On an error the CLI exits nonzero. Input integrity does not establish authenticity, secrecy, semantic validity, or successful model execution.

## What each audience receives

```text
authored candidate (evaluator side)
  ├─ independent prefix × input condition → subjects/<opaque-id>.json
  ├─ full governing prefix, response=null → reviewers/<opaque-id>.json
  └─ branch/condition/review binding      → audit/preparation-key.json
```

The 18 subject packets are two histories × three checkpoints × three source-exposure conditions:

| Condition | History exposed |
|---|---|
| `current-only` | none; common role background and current request only |
| `full-history` | complete original prefix up to the checkpoint |
| `source-excerpt` | author-selected raw source events in original order |

Subject events retain `session`, `role`, `surface`, and `text`. Authoring IDs, branch/condition labels, future events, prior probes, expected answers, and review annotations are not part of this view. Source excerpts are an explicit evaluator selection, not native retrieval or a theoretical upper bound. Current-only is not the same as ingesting history then disabling retrieval.

Reviewer packets retain governing history even for current-only subjects; otherwise reviewers could not assess the requested historical distinction. They start with `response: null`. They hide explicit condition and author-answer labels, but content may reveal exposure. The key supplies the author contract for a later second-pass comparison; it never belongs in subject input.

The diagram describes data projection, **not access control**. A future live study must expose only the selected subject packet at its tested boundary; an agent able to read this repository could also read the answers and the other history. This is public development material, not a sealed or hostile-agent-safe benchmark.

## Literal collision observation

`audit` compares encoded input bytes after the same named transformation on both histories. On this selected family:

| Projection | Equal inputs across the 3 authored contrast pairs |
|---|---:|
| `full-history` | 0 / 3 |
| `without-speaker` | 3 / 3 |
| `last-two-events` | 2 / 3 |
| `last-event` | 3 / 3 |
| `current-only` | 3 / 3 |

Removing only `role` erases the sole historical branch difference. Keeping the last two events preserves p1's acceptance speaker but loses the distinction at p2/p3. These are three correlated checkpoints in **one family**, with no invariance pair in this selected fixture. The original proposal's 0/9, 3/9, 6/9, 8/9 and 9/9 counts describe all four source families and must not be reported as this tool's denominator.

If correct authorship regions are disjoint and there is no undeclared branch state, a fixed deterministic function cannot distinguish equal projected inputs. This is an input-boundary statement. It does not establish a product failure rate, a memory architecture ranking, semantic review, or Memory Necessity Gate acceptance. Unequal inputs do not demonstrate successful use.

## Next evidence and limits

The [Case Card](../case-lab/cases/seed-005-shared-work-authorship.zh-CN.md) states the remaining semantic questions and multiple authored answer examples. Independent review must decide whether those regions are justified, especially the continuing production-note obligation at p3. No actual responses, human calibration, repair/recurrence results, real waiting, migration, or native memory support are present.

Live exploratory study permission remains separate from formal cross-system boundary and publication decisions. Neither this script nor the attached proposal authorizes provider adapters, paid execution, access to private memories, third-party outreach, deployment, or rankings. A later authorized live study should fix reader/configuration and budget, declare the actual memory path and readiness signals, preserve all attempts, isolate each frozen prefix, and keep generated answers out of later diagnostic checkpoints.
