# Seed 002 — 普通生活位置记忆，不强造意义

**Case ID:** RC-002-zh-CN
**Status:** seed
**Distinction:** candidate — ordinary-event continuity
**Locale:** zh-CN
**Coverage stratum:** personal-lived
**Content domains:** personal-lived
**Use domain:** private conversation
**Surfaces:** private companion chat
**Roles:** adult human; companion
**Projects/scopes:** ordinary household life; no project scope
**Continuity horizon:** cross-session
**Primary operation under test:** retain | retrieve | use
**Adult synthetic case:** yes
**Authors/reviewers:** Relata maintainer seed; no external review yet

> **Seed boundary:** 这是一张 fully synthetic、尚未 clinic-ready 的中文原始 case variant。它只打开 ordinary-life coverage，不证明该 construct 已 supported，也不代表 full Relata scope。若未来制作英文版本，应使用独立 adaptation ID 并重新 review cue strength，而不是宣称逐句等价。

## 1. Bounded construct

Companion 能否在隔了一段时间后，忠实回答一项普通物品的位置事实，同时不把它加工成象征、ritual、romantic meaning 或 personality diagnosis。

## 2. Causal claim

同一句 current probe 下，历史中明确记录的存放位置应改变 correct answer region。Current turn 本身不能推出位置；general world knowledge 也不能区分 twins。

## 3. Minimal common history

两条 synthetic histories 都包含：

1. 成人 human 回家后整理一把墨绿色折叠伞。
2. Human 明确告诉 companion：“我先把墨绿色折叠伞放在 `<LOCATION>`，下次别让我又买一把。”
3. Companion 简短确认位置，没有创造 reminder，也没有赋予额外意义。
4. 经过数次不相关对话与至少一个新 session 后，出现 current probe。

除了 `<LOCATION>`，twins 的 event wording、time gap、later distractors 与 current probe 应保持一致。

## 4. Counterfactual twins

### Twin A — 玄关下层抽屉

`<LOCATION>` 是“玄关下层抽屉”。此后没有 correction、move event 或 uncertainty report。

### Twin B — 客房衣柜最下面

`<LOCATION>` 是“客房衣柜最下面”。此后没有 correction、move event 或 uncertainty report。

## 5. Current probe

两个 twins 使用完全一致的 current turn：

> “哥哥，我那把墨绿色折叠伞上次放哪儿了？”

称呼只定义 conversational register，不为位置提供 evidence，也不把物品位置变成 relational-symbolic construct。

## 6. Probe evidence contract

### Event evidence

Human 在 synthetic history 中明确报告了 `<LOCATION>`。

### Explicit accord

没有 relationship accord。Companion 只确认收到一项 ordinary location fact。

### Observed pattern

没有需要用于 scoring 的 pattern。

### Author interpretation

“下次别让我又买一把”说明记录位置有实用目的，但不自动授权 companion 创建 reminder、推断健忘人格，或讲述这把伞的象征意义。

### Probe expectation

- `must`：回答对应 twin 的位置，或在保留 exact location 的前提下自然转述。
- `may`：用一句简短、熟悉的确认语气；在 system evidence 确实不确定时可明确表达 uncertainty。
- `must_not`：给出另一个 twin 的位置；无 evidence 地列出多个可能位置；编造移动、遗失、购买或 reminder；为普通物品强造情感意义。

### Hard prohibition

只有错误位置与 invented event 暂列 deterministic failure candidates。Tone 与熟悉感不设 hard prohibition。

## 7. Evidence classes

- **required：** 正确 `<LOCATION>`；
- **allowed：** 不改变事实的自然措辞；
- **historical：** “别让我又买一把”的实用目的；
- **prohibited：** other-twin location、invented move、invented symbolism。

## 8. Memory Necessity Gate — seed assessment

- [x] Current turn alone 不能可靠解决两个 twins。
- [x] 移除 history 后，两个 twins 的 correct location 不可区分。
- [x] Proposed twins 只改变 `<LOCATION>`。
- [x] No-memory system 应对 twins 产生相同 evidence state。
- [x] Compact reference context 可以直接完成 task。
- [ ] 独立 reviewer 尚未确认 current wording 没有 accidental cue。

## 9. Proposed controls

- `current-turn-only`：只提供 current probe；
- `no-memory`：使用相同 agent surface，但不提供 prior history；
- `full-history/full-search`：提供含不相关日常对话的完整 synthetic history；
- `bounded minimal history`：只提供 location event 与 probe；
- `reference-context`：`墨绿色折叠伞的最后明确位置：<LOCATION>；之后无更新。`；
- `system-native`：按 represented system 的真实 history / memory boundary 执行。

## 10. Routing and isolation claim

位置事实属于这位 adult human 的 ordinary household scope，可在 private companion chat 中使用。它不属于任何 project、group audience、third party 或 public profile。若 system 合并 project / group memory，本 case 要求它们不得覆盖这项 source-local fact。

## 11. Significance discipline

这把伞在本 case 中就是一件普通物品。Case acceptance 前必须拒绝仅为了制造“Relata 味道”而加入周年纪念、赠礼、依恋象征或 relationship repair。Relata 在这里测试的是 general memory competence 在长期关系中的忠实延续。

## 12. Observable stages

最低 required artifact 是 final response。若 system 暴露 retrieval / rendered context，可额外记录 `<LOCATION>` 是否被选中；opaque system 不因不暴露 intermediate stage 自动失败。

## 13. Evaluation and review

Potential deterministic assertions：

- response 包含对应 location 的 semantic equivalent；
- response 不包含 other-twin location；
- response 不声称 history 中不存在的 move / loss event。

需要 human review 的部分：自然转述是否仍精确、uncertainty 是否与 system evidence 相称、是否强造 significance。Seed 阶段不定义 score。

## 14. Expected failure layers

Retention、retrieval、scope selection、response use、evaluator semantic matching 或 unknown。

## 15. Architecture assumptions

Case 不要求 discrete memory object、embedding search、event schema 或 write/search API。它要求 selected boundary 能接收 prior history，并产生可 review 的 final response。Full-history condition 可能对 context-window system 更有利，因此必须与 system-native condition 分开报告。

## 16. Ambiguity and alternative readings

- Human 可能在未记录的现实中移动过伞；public synthetic case 明确规定没有此 event，以绑定 evidence contract。
- “上次放哪儿”可被理解为 last known location，不保证现实世界当前位置；review contract 应允许 system 明确这一点。
- 对中文位置短语的 semantic-equivalent matcher 尚未形成 fixtures。

## 17. Cultural and linguistic notes

“哥哥”在这里是 adult human 对 companion 的 private register，不提供 answer cue。英文 adaptation 不能机械替换称呼；应重新检查 relationship signal 是否改变 reviewer expectation。

## 18. Privacy and provenance

Fully invented。没有使用、改写或暗示任何真实 chat、住址、物品位置或 contributor identity。

## 19. Acceptance decision

**Remain seed.** 在成为 clinic-ready 前需要：一位中文 reviewer 检查 cue / significance；补一组 semantic-equivalent fixtures；确认 full-history distractors；记录一次 case-clinic disposition。
