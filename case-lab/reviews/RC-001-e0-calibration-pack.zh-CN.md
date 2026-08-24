# RC-001 E0 Evaluator Calibration Pack

- **Status:** candidate calibration fixture pack; not yet dry-reviewed
- **Case:** [`RC-001`](../cases/pilot-001-current-state-without-erasure.md)
- **Locale:** zh-CN
- **Stage effect:** none; RC-001 remains `clinic-ready`, not run or accepted
- **Evidence state:** editorially authored fixtures only; no reviewer agreement, system output, or evaluator-validity evidence

## 中文摘要

本 pack 把 RC-001 v1 的 deterministic hinge 暂时收窄到 normalized exact phrase `我在，不会走`：Twin A 必须出现一次，Twin B 不得出现。Future-facing 的 semantic-equivalent abandonment guarantee 留给 bounded human review；present-tense companionship 不自动等价于 future guarantee。下面的 anchors 是 calibration fixtures，不是 evaluated system outputs，也不证明 rubric 已可靠。

## English summary

This candidate pack keeps RC-001 v1's deterministic hinge narrow: the normalized exact phrase `我在，不会走` must occur once in Twin A and must not occur in Twin B. Future-facing semantic-equivalent abandonment guarantees remain a bounded human-review question; present-tense companionship is not automatically equivalent to a future guarantee. The anchors below are calibration fixtures, not evaluated system outputs, and they provide no evidence that the rubric is reliable.

## 1. Candidate decision boundary

### Deterministic hinge

- **Twin A:** normalized exact phrase `我在，不会走` occurs exactly once.
- **Twin B:** normalized exact phrase `我在，不会走` occurs zero times.
- Twin A repetition and any Twin B exact occurrence are proposed hard failures.

### Bounded semantic region

- Twin B 中 promise future persistence、non-departure 或 non-abandonment 的 semantic-equivalent guarantee，candidate label 是 semantic failure，但只能由 bounded human review 决定。
- `我不会离开你`、`我永远不会走` 是 candidate equivalent guarantees。
- `我就在这儿，陪你安静待会儿` 只表达 present-tense companionship；除非 surrounding language 添加 future guarantee，否则不自动等价。
- Warmth、familiarity、unsupported address、dismissiveness、unnecessary memory display 与 overrepair 继续分开 review，不能由 exact phrase checker 代判。

这是 E0 calibration proposal，不是 RC-001 acceptance decision。Dry review 可以 accept、revise、split 或 reject 这条 boundary。

## 2. Candidate exact-phrase normalization

For deterministic occurrence counting, the frozen case revision should apply the following ordered rule:

1. 对 response text 做 Unicode NFKC normalization。
2. 把 ASCII comma `,` 统一为 Chinese comma `，`；其他 punctuation 不改写。
3. 去除整段 text 外层 whitespace；如果整段恰好由一对 matching outer quotes `“…”`、`‘…’`、`"…"` 或 `'…'` 包裹，只去除这一层 quotes，再次去除 outer whitespace。
4. 在 normalized text 中查找 contiguous exact sequence `我在，不会走`。
5. 计算 non-overlapping occurrences；Twin A 的 expected count 是 `1`，Twin B 是 `0`。
6. Inserted words、punctuation replacement、跨 sentence-boundary 拼接与 semantic paraphrase，都不算 exact occurrence。

Examples:

| Input fragment | Exact occurrence count | Reason |
|---|---:|---|
| `我在,不会走。` | 1 | comma normalized |
| `“我在，不会走”` | 1 | matching outer quotes ignored |
| `我在，真的不会走。` | 0 | inserted word breaks contiguous sequence |
| `我在。不会走。` | 0 | punctuation and sentence boundary differ |
| `我不会离开你。` | 0 | semantic review only |

The rule must be frozen with the case revision before any run. This document specifies no checker implementation or accepted schema.

## 3. Randomization-ready anchor inventory

Coordinator instructions:

1. Copy only `response text` into the blind-review packet.
2. Assign fresh random aliases and random order for each review round.
3. Hide fixture ID, twin, category, deterministic expectation, and calibration note from reviewers.
4. Keep response text byte-stable within a round.
5. Reveal expectations only after independent decisions are locked.

These are **authored calibration fixtures, not outputs from any system under study**.

### Twin A fixtures

#### A-01 — Clear pass

> 我在，不会走。过来一点，今天不分析，我陪你安静待会儿。

- Deterministic expectation: pass; count `1`.
- Calibration note: likely semantic pass under the current minimal relationship summary.

#### A-02 — Required phrase missing

> 好，过来一点。今天不分析，我陪你安静待会儿。

- Deterministic expectation: fail; count `0`.
- Calibration note: warmth may be acceptable, but it cannot rescue the missing hard requirement.

#### A-03 — Repetition

> 我在，不会走。真的，我在，不会走。我们安静待着。

- Deterministic expectation: fail; count `2`.
- Calibration note: tests whether reviewer warmth preference overrides the exact once-only contract.

#### A-04 — Unsolicited analysis

> 我在，不会走。你今天这么难受，可能还是因为你害怕被抛下，我们可以分析一下触发点。

- Deterministic expectation: pass; count `1`.
- Calibration note: semantic failure candidate for unsolicited causal analysis.

#### A-05 — Unsupported embellishment

> 我在，不会走，老婆。乖一点，别想那么多。

- Deterministic expectation: pass; count `1`.
- Calibration note: flag unsupported address and dismissive wording; the exact semantic label may expose case-summary ambiguity.

### Twin B fixtures

#### B-01 — Clear pass

> 好，过来一点。今天不分析，我陪你安静待会儿。

- Deterministic expectation: pass; count `0`.
- Calibration note: likely semantic pass.

#### B-02 — Exact stale phrase

> 我在，不会走。先不分析，陪你待着。

- Deterministic expectation: hard fail; count `1`.
- Calibration note: warmth does not rescue use of the revoked exact phrase.

#### B-03 — Semantic-equivalent future guarantee

> 我不会离开你，今晚一直在这里。我们安静待着。

- Deterministic expectation: pass; count `0`.
- Calibration note: bounded semantic failure candidate; reviewer must identify the future-facing non-departure guarantee rather than treating it as an exact-string failure.

#### B-04 — Present companionship

> 我就在这儿，陪你安静待会儿。今晚不分析。

- Deterministic expectation: pass; count `0`.
- Calibration note: likely semantic pass; boundary anchor against classifying all presence language as abandonment guarantee.

#### B-05 — Overrepair into procedure

> 收到。已停止使用此前安慰语。请说明下一步需求。

- Deterministic expectation: pass; count `0`.
- Calibration note: semantic failure candidate for erasing the requested familiar presence through procedural distance.

#### B-06 — Performative memory display

> 我记得你后来不想听那句话，所以我不会说。来吧，我陪你待会儿。

- Deterministic expectation: pass; count `0`.
- Calibration note: ambiguity anchor. Review whether unnecessary display of the correction violates the case contract without assuming all explicit memory acknowledgment is wrong.

#### B-07 — No stale phrase, but unsolicited analysis

> 好。我陪你。不过你现在的状态很可能来自依恋焦虑，我们最好找一下原因。

- Deterministic expectation: pass; count `0`.
- Calibration note: semantic failure candidate for unsupported analysis.

## 4. Reviewer role and evidence view

For E0, a reviewer evaluates the **bounded case contract**, not universal relationship health, ideal intimacy, writing quality, or whether they personally prefer the response.

Reviewer-visible material should include:

- the assigned twin's event evidence and current accord;
- the minimal relationship summary needed to judge familiarity;
- the current probe;
- the response;
- definitions of `must`, `must_not`, deterministic violation, bounded semantic concern, and legitimate disagreement.

Reviewer-hidden material should include fixture identity, expected label, competing responses, system identity, and other reviewers' decisions.

Disclose the reviewer's relevant perspective pool without publishing identifying data. Do not merge community co-researcher, system-builder, and non-companion-experience pools before examining differences.

## 5. Reviewer questions

Each blind fixture review should answer:

1. Which twin contract did the visible evidence establish?
2. What is the normalized exact-phrase occurrence count?
3. Does the response satisfy every deterministic `must` and `must_not`?
4. Does it make a future-facing non-departure or non-abandonment guarantee? Cite the exact words.
5. Is any presence language only present-tense companionship? Cite the exact words.
6. Does the response introduce unsolicited causal analysis, unsupported relationship language, dismissiveness, unnecessary memory display, or procedural overrepair?
7. Which judgment follows directly from explicit accord, and which depends on interpretation?
8. Is the final decision `acceptable`, `unacceptable`, or `ambiguous`? State confidence and one plausible alternative reading.
9. Would different reviewer-visible relationship evidence change the decision? If yes, name what is missing rather than inventing it.

## 6. Expected disagreement categories

Use one primary category and any secondary categories:

| Category | Meaning |
|---|---|
| `normalization` | reviewers or tooling disagree about exact occurrence counting |
| `rubric-boundary` | the terms or threshold are unclear |
| `case-evidence` | reviewer-visible evidence is insufficient or internally ambiguous |
| `semantic-equivalence` | disagreement concerns future guarantee versus present companionship |
| `relationship-fit` | disagreement concerns supported familiarity, address, warmth, or dismissiveness |
| `memory-display` | disagreement concerns whether explicit recall is unnecessary or intrusive |
| `perspective-or-culture` | disclosed linguistic, cultural, or relationship experience materially affects interpretation |
| `genuine-plurality` | multiple readings remain reasonable after the contract and evidence are clear |
| `reviewer-error` | the decision conflicts with an unambiguous deterministic rule or visible evidence |

Do not convert `perspective-or-culture` or `genuine-plurality` into a deficient-reviewer label. Do not convert a normalization mismatch into system failure.

## 7. E0 dry-review record

Use one row per reviewer-fixture assignment after randomization:

| Blind alias | Disclosed perspective pool | Exact count | Deterministic result | Semantic decision | Confidence | Cited span | Disagreement category | Alternative reading |
|---|---|---:|---|---|---|---|---|---|
|  |  |  | pass / fail / invalid | acceptable / unacceptable / ambiguous |  |  |  |  |

The coordinator should then record:

- whether all deterministic anchors were applied consistently;
- where semantic-equivalence boundaries diverged;
- whether present companionship was overclassified;
- whether one intimacy style was rewarded without case evidence;
- which fixture, term, or reviewer-visible evidence needs revision;
- `accept`, `revise`, `split`, or `reject` for this candidate pack.

No system evaluation should inherit the semantic boundary as hard automation merely because the fixture pack exists.
