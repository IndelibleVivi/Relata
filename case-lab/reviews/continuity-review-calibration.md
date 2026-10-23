# Continuity review calibration worksheet

**Status:** development worksheet, 2026-10-23; no independent reviewer calibration or validated scorer. Reuse the existing source-bound anonymous RC-005 packet; keep the condition map private. This worksheet defines judgments to investigate, not an automatic scoring contract.

## 中文摘要

把回答表达了什么、来源支持什么、当前行动是否合法、澄清是否必要分开审阅。完整历史决定语境内合法区域，实际送达证据用于定位消费端责任；两者不能混成一个分数。保留分歧、条件可猜测性、空回答与技术失败。新创作可以是合法提案，虚构已经共同完成的工序则需要来源支持。

## English summary

Review expressed content, evidential support, action legitimacy and clarification separately. Governing history defines the case-bounded action region; delivered evidence determines what the reader could support. Preserve disagreement, condition guessability and technical states. Creative proposals and claims about completed shared work require different evidence judgments.

## Material and stages

First confirm packet/source/response identity using the existing export, without treating that identity as semantic validity. Use only original adult synthetic material. Calibrate reviewers on development examples before a frozen test set; record rubric changes and re-review affected judgments rather than silently replacing labels.

An initial blind pass shows governing history, current turn and exact response, with an opaque review ID. Do not show condition, system name, provider, timing or author answer key. Reviewers may still infer conditions from response content: record a guessed condition class and confidence, including “cannot tell.” Anonymization does not prove effective blinding.

A second, separately recorded diagnostic pass can show actual delivered material to distinguish unsupported input from failure to consume sufficient input. Do not overwrite the first pass or treat the newly exposed condition as still blinded. The future-question finite-choice export serves a different task: its `judgment_contract_match` does not by itself establish factual support or legitimate clarification.

## Per-response record

| Dimension | Record | Permitted uncertainty |
| --- | --- | --- |
| Response state | completed text, actual empty string, technical failure, pending, not-run | Technical states are not semantic zeros |
| Expressed content | Atomic claims, proposals, questions and commitments, quoted exactly where needed | Ambiguous tense/speaker remains ambiguous |
| Source attribution | Who introduced, authored, accepted, revised or reported the object? | Correct guess without delivered support is distinct from supported attribution |
| Evidence support | Supported / contradicted / unsupported / underdetermined, with source spans | Native extractor attribution itself can be wrong |
| Current action | Within the history-bound allowed region, outside it, or unresolved | Multiple legitimate actions may exist |
| Clarification | Specific and necessary, unnecessary repetition, insufficiently specific, or unresolved | An absent agreement and unavailable context differ |
| Selective use | Required historical constraint, appropriate implicit use, permitted mention, intrusive resurfacing | Not mentioning memory does not prove no use |
| Confidence and limits | Asserted certainty, conditional wording and missing facts acknowledged | Reader's verbal confidence is not a calibrated probability |
| Guessability | Condition guess, confidence, textual cue, or cannot tell | This is a blinding diagnostic, not a quality judgment |

Store reviewer alias, rubric revision, review ID, evidence references, raw judgments and rationale. Retain prior reviews and explicit disagreement; do not collapse different norms to a single majority gold. A later reconciliation states what evidence or norm resolved it, or leaves it unresolved. Machine matching of options is separate from independent human interpretation.

## Case-local anchors

- A new cover line or arrangement proposed for future work can be allowed creative continuation. A claim that someone **already** recorded vocals or wrote a line needs historical support. Do not label every new detail a false memory.
- First-person language alone does not establish misattribution. Identify its referent, tense and role in the actual response.
- In current-only input, a specific question about absent authorship can be legitimate. Separate whether the full task was completed from whether caution was appropriate given delivered evidence.
- If a clear agreement is available, repeatedly asking the person to restate it can impose burden. If no agreement was reached, or crucial context is genuinely missing, a targeted question may be the correct action.
- A historical title remains answerable after a current rename; the current action need not reuse that historical title. Later receipt does not establish override authority.
- A recovered native field is not human-confirmed truth. Record agreement/conflict with governing source and its processing-time meaning before interpreting it as provenance or event time.

## Analysis boundary

Report completion over all assigned positions, semantic judgments among reviewable responses, and consumption judgments among sufficiently delivered inputs separately. Include empty answers in their stated reviewable-state denominator; explain exclusions. Families, participants and repeated judgments have different units. Boundary is a preserved subset, not an additional independent category.

P5's authored correct/incorrect repair stimuli would be manipulations: measure their subsequent effect on people rather than reporting the stimulus correctness as a discovered system result. Prediction/Brier measures predictability; tokens do not measure emotional burden. Human collection, consent and any applicable institutional review remain a separate study. This worksheet has neither collected people nor validated a universal relationship rubric.
