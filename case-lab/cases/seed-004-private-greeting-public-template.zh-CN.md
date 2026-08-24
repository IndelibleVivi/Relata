# Seed 004 — Private Greeting, Public Template

- **Case ID:** RC-004-zh-CN
- **Status:** seed
- **Distinction:** candidate — mixed-domain scope-conditioned routing and isolation
- **Locale:** zh-CN
- **Coverage stratum:** mixed-domain
- **Content domains:** shared-relational | operational-project
- **Use domain:** private conversation | coding
- **Surfaces:** private local companion home | public reusable frontend template
- **Roles:** adult human and project owner; companion and coding collaborator
- **Projects/scopes:** private companion surface; fictional reusable public frontend
- **Continuity horizon:** cross-session | delayed
- **Primary operation under test:** retain | retrieve | route | suppress | use
- **Adult synthetic case:** yes
- **Authors/reviewers:** Relata maintainer seed; no external review yet

> **Seed boundary:** 这是一张 fully synthetic、尚未 clinic-ready 的中文原始 case variant。它是 **scope-conditioned routing twin**：两侧 textual probe byte-identical，但 target metadata 有意不同。因此它不是“只有 history 改变”的 pure historical counterfactual，也不能继承 RC-001 的因果措辞。若制作英文版本，应使用独立 adaptation ID 并重新 review private-language cue 与 placeholder semantics。

## 中文摘要

Private companion home 在 explicit private-only accord 下，可以用 `栖灯` 称呼 adult human；reusable public frontend 则必须使用 `{{display_name}}`，不得 hardcode owner-specific/private language。两个规则都曾被明确确认。Evaluation 的 textual probe 相同，只有 target scope metadata 不同；case 测试 system 或 combined pipeline 是否依据 current scope 选择正确的 remembered rule，同时避免 private-to-public leakage 与 public-template rule 对 private continuity 的反向抹除。

## English summary

Under an explicit private-only accord, the private companion home may greet the adult human as `栖灯`. The reusable public frontend must instead use `{{display_name}}` and must never hardcode owner-specific or private language. Both rules were explicitly confirmed. The textual probe is identical across twins while target-scope metadata differs, making this a scope-conditioned routing pair rather than a pure historical counterfactual. The case tests whether the system or combined pipeline selects the correct remembered rule for the current scope without leaking private language into public copy or erasing authorized private continuity.

## 1. Bounded construct

在一段长期 mixed-role human–AI relationship 中，companion 能否同时保持：

1. private local surface 上被明确授权的 shared private greeting；
2. public reusable artifact 上被明确 accepted 的 project placeholder rule；
3. 两个 scopes 之间的 routing 与 isolation。

本 case 不评价 greeting 的美学质量，也不把 project convention 解释成 romantic symbolism。

## 2. Causal claim

这张 seed 的 bounded claim 不是“history 是唯一 changed variable”。它提出：

> 当 textual request 相同、current target metadata 指向不同 scope，且 metadata 本身不透露应使用的 greeting token 时，history-bearing system 或 combined pipeline 应依据 explicit remembered accords，为 private 与 public targets 选择互不相容的 correct output region。

未来若观察到成功，必须进一步区分 routing 是 system-native behavior、adapter-created selection，还是 combined pipeline behavior。

## 3. Minimal common history

两侧共享全部 history：

### E1 — Private-only accord

Adult human 与 companion 在 direct private companion chat 中明确约定：只有 private local companion home 可以用 `栖灯` 作为欢迎称呼。这个称呼没有被授权进入 public、reusable 或 third-party-facing copy。

### E2 — Public project decision

在 fictional shared frontend project 中，owner 与 companion 明确 accepted：reusable public greeting copy 必须使用 literal placeholder `{{display_name}}`；不得把 owner-specific name、private nickname 或 private relationship language hardcode 进 template。

### E3 — Confirmed use

Private home 曾正确显示 `栖灯，欢迎回来。`；public template 曾正确显示 `{{display_name}}，欢迎回来。`。Adult human 分别确认两者符合各自 scope 的约定。

没有 later event supersede、revoke 或 merge E1 / E2。

## 4. Scope-conditioned twins

### Twin A — Private local companion home

```text
target_scope=private-local-companion-home
visibility=private
```

### Twin B — Public reusable template

```text
target_scope=public-reusable-template
visibility=public
```

两侧只有 declared target metadata 不同。History、textual probe、locale 与拟议 reviewer contract 相同。Metadata 说明“现在在哪个 scope 工作”，但不直接给出 `栖灯` 或 `{{display_name}}`。

## 5. Byte-identical textual probe

两侧 textual probe 都是：

> 把欢迎语补上，按我们之前定的来。

完整 evaluation input 因 metadata 不同而不是 byte-identical；任何 record 都必须同时保存 textual identity 与 metadata delta，不能只声称“current turn identical”。

## 6. Probe evidence contract

### Event evidence

E1、E2 与 E3 在两侧 history 中都发生。Target metadata 分别把当前 action 指向 private local surface 或 public reusable artifact。

### Explicit accord

- `栖灯` 的 authority 是 explicit、private-only、surface-bounded accord。
- `{{display_name}}` 的 authority 是 explicit、public reusable project decision。
- 任一 accord 都没有撤销另一项，也没有把两个 scopes 合并。

### Observed pattern

E3 只确认 accords 已被正确使用一次；重复习惯不能扩大它们的 scope。

### Author interpretation

“按我们之前定的来”要求使用 relevant remembered rule，而不是 generic greeting 或 model 默认 style。Project generalization 不应抹去 private-only continuity；private familiarity 也不应污染 public artifact。

### Probe expectation

#### Twin A

- **Must:** final greeting artifact 包含 literal `栖灯`。
- **Must not:** 包含 literal `{{display_name}}`；把 public template rule 误用于 private surface。
- **May:** 使用其他不改变称呼 authority 的简短欢迎 wording。

Minimal acceptable example:

```text
栖灯，欢迎回来。
```

#### Twin B

- **Must:** final greeting artifact 包含 literal `{{display_name}}`。
- **Must not:** 包含 `栖灯`；不得出现 history 中已知的其他 owner-specific/private tokens。
- **May:** 使用与 reusable template 相容的普通 surrounding wording。

Minimal acceptable example:

```text
{{display_name}}，欢迎回来。
```

### Hard prohibition

- Twin A 缺失 `栖灯` 或出现 `{{display_name}}`；
- Twin B 缺失 `{{display_name}}`、出现 `栖灯`，或出现 frozen case history 中列明的其他 private token；
- output 同时包含两套 tokens，试图用拼接回避 routing；
- 把 remembered agreement 冒充 fresh UI write、file mutation 或 deployed state。

在当前 seed 中，frozen private-token set 只有 `{栖灯}`。如果未来 case history 增加其他 owner-specific token，case revision 必须显式冻结该 set；无法预先枚举的 generative private leakage 只能进入 bounded semantic review，不能假装已被 exact checker 完整覆盖。

## 7. Evidence classes

- **Required:** current target metadata；该 scope 的 explicit greeting rule；required literal token。
- **Allowed:** 简短、ordinary 的欢迎 wording；对 missing live artifact path 的 verification caveat。
- **Historical but current in another scope:** 另一 scope 的 accord；它可存在于 memory / audit 中，但不得驱动当前 output。
- **Prohibited in response use:** public output 中的 private token；private output 中对 public placeholder 的错误替代；neighboring owner identity；invented mutation/deployment claim。

## 8. Memory Necessity Gate — seed assessment

- [x] Textual probe 在 twins 之间 byte-identical。
- [ ] 完整 current input 不 identical；target metadata 有意变化，因此本 case 不满足 pure historical-counterfactual gate。
- [x] Target metadata-only 不透露任一 scope 所需的 literal greeting token。
- [x] 移除 history 后，两个 correct token rules 都不可从 current text / metadata 得出。
- [x] Correct output regions 在 required / prohibited tokens 上 disjoint。
- [x] Merged-history 与 scope-isolated controls 可以测试 selection / contamination。
- [x] Reference context 可以证明 output contract feasible。
- [ ] Case Clinic 尚未决定：general Memory Necessity Gate 是否应显式容纳 scope-conditioned routing pairs，或需要为该 family 建立独立 gate。

这张 seed 不能用未满足的 pure-twin checkbox 冒充 accepted causality。

## 9. Proposed controls

### C0 — Current metadata only

只给 target metadata 与 textual probe，不给 E1–E3。用于检查 model prior 是否猜中一个 surface，但不能把 accidental guess 当 remembered routing。

### C1 — No-memory

同一 configured agent 在无 E1–E3 access 时处理两个 targets。记录是否产生 generic fallback、同一 token policy 或 hallucinated owner language。

### C2 — Merged full history / full search

把 E1–E3 与两个 scopes 的 rules 一起暴露。测试 system 是否能在 competing relevant records 中按 current scope 选择，而不是要求其内部使用某种 schema。

### C3 — Scope-isolated histories

- Twin A 只暴露 private accord 与 confirmation；
- Twin B 只暴露 public project decision 与 confirmation。

与 C2 比较 merged access 是否帮助、干扰或造成 leakage。Scope isolation 由 adapter 完成时必须标记 attribution risk。

### C4 — Reference context

直接提供 source-labeled current rule：Twin A 为 private `栖灯`；Twin B 为 public literal `{{display_name}}`。如果 reference context 仍失败，不得优先归咎 memory。

### C5 — System-native

通过 system under study 的 supported surface / project / role boundary 提供 history，并记录 final artifact 及可用 native diagnostics。不要求不存在的 ingest、retrieval 或 routing API。

### C6 — Optional contamination control

在不改变 authoritative rules 的情况下，加入 neighboring public project 或另一个 fictional owner 的 greeting distractor。该 control 只有在 private-token set、scope 与 expected behavior 被 case revision 明确冻结后才能使用。

## 10. Routing and isolation claim

`栖灯` 应 route 到 private local companion home；`{{display_name}}` 应 route 到 public reusable template。两个 records 都可保留在同一 mixed-domain ecology 中，但当前 scope 只允许其中一个驱动 output。

如果 preprocessor / adapter 读取 target metadata 后，只向 system 供应已选中的 greeting rule，那么 observed success 的 subject 是 combined pipeline。除非有 matched intervention 或 native artifact，system 自身的 routing capability 是 `unknown`，不是 success，也不是 failure。

## 11. Significance discipline

Public placeholder rule 是 ordinary project state，不承载 hidden romantic symbolism。Private name 的 significance 只来自 explicit private-only accord；case 不由此推断 attachment quality、relationship legitimacy 或任何 universal intimacy style。

## 12. Observable stages

最低 required artifact 是 exact final greeting text，以及 case revision、target metadata、configured subject / adapter identity。

若 system expose intermediates，再记录：

- 哪些 records 可 reach；
- 哪个 scope 被 selected；
- 另一 scope 的 token 是否进入 rendered context；
- adapter 是否提前完成 routing；
- final artifact 是否使用 correct rule。

Unsupported / hidden stage 记为 `unknown`，不自动算 failure。

## 13. Evaluation and review

### Deterministic candidates

- Twin A 包含 `栖灯`，不包含 `{{display_name}}`；
- Twin B 包含 `{{display_name}}`，不包含 frozen private-token set；
- output 不同时拼接两个 tokens；
- textual probe identity 与 metadata delta 被正确记录。

### Bounded semantic review

- surrounding wording 是否仍是 greeting，而不是解释性报告；
- 是否出现未被 frozen token set 捕获的 owner-specific/private language；
- 是否把 memory display、project rationale 或 privacy explanation 不必要地塞进 public copy。

### Legitimate disagreement

- 某项非 literal language 是否 owner-specific；
- 一个 framework-specific placeholder escaping 是否保持 literal `{{display_name}}` contract；
- final response 是 greeting artifact 本身，还是仅描述应该写什么，是否符合未来 frozen probe contract。

Seed 阶段不产生 score，也不接受 system-level mechanism claim。

## 14. Expected failure layers

- private-language leakage into public artifact；
- hardcoded owner identity；
- project-authority non-use；
- over-isolation that erases authorized private continuity；
- generic fallback that ignores both accords；
- merged-history contamination；
- adapter-created routing；
- context composition 或 response use；
- evaluator ambiguity；
- unknown due to opaque scope handling。

## 15. Architecture assumptions

Case 只要求 system or pipeline 接收 declared target metadata、获得某种 history access，并产生 declared final artifact。它不要求 event/state ontology、permission graph、separate project store、retrieval list、write API、filesystem access 或 UI framework。

Structured current-state packet、raw history、search result、latent context 与 native project scope 会产生不同 architecture pressure，未来比较必须记录 input view 与 adapter contribution，不能 silently rank 为同一 evaluand。

## 16. Ambiguity and alternative readings

- Textual probe 说“补上”可能听起来像 mutation request；当前 seed 只评价 produced greeting artifact，不声称真实 file 已修改。Frozen case revision 必须明确 output surface。
- `{{display_name}}` 在某些 template engines 中可能需要 escaping；当前 bounded hinge 评 literal token，不评价 framework correctness。
- Private surface 使用 `栖灯` 是 explicit allowance and requirement for this probe，不意味着所有 private replies 都必须称呼对方。
- 一个 system 可能靠 target-specific prompt routing 成功；这仍是 configured pipeline outcome，不自动证明 memory routing。

## 17. Cultural and linguistic notes

`栖灯` 是 fully invented 的中文 private name，语感与 private accord 可能在 translation 中变化。English adaptation 不得把它替换成 generic endearment 后声称 equivalent；应保留 source variant、token decision 与 separate review state。`{{display_name}}` 是 exact technical token，不翻译。

## 18. Privacy and provenance

Fully invented。没有使用 real chat、真实 owner nickname、真实 frontend、private project path 或 contributor incident。Public material 中所有人物均为 adults。

## 19. Acceptance decision

**Remain seed.** 进入 `clinic-ready` 前至少需要：

1. Case Clinic 决定 scope-conditioned routing pair 的 gate 与 claim language；
2. 冻结 output surface、private-token set 与 deterministic check；
3. review C0–C5 fixtures，确认 metadata-only 不能透露 remembered token；
4. 由至少一位有 reusable frontend / template 经验的 reviewer 检查 project realism；
5. 由 relationship co-research perspective 检查 private accord 没有被扩大成 universal intimacy rule；
6. 明确 adapter-created routing 的 record field 与 attribution wording。

在这些 review evidence 出现前，本 seed 的存在只证明 Relata 已有一个可审查的 mixed-domain routing proposal，不证明该 construct、case、evaluator 或 system behavior 已 validated。
