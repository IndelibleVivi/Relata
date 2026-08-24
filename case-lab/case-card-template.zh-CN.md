**简体中文** | [English](case-card-template.md)
<!-- language: zh-CN; mirror: case-card-template.md; translation-status: synchronized -->

# Case Card：<Title>

**Case ID:** RC-000
**Status:** seed | clinic | pilot | accepted | rejected | superseded
**Distinction:** D-
**Locale:**
**Coverage stratum:** personal-lived | shared-relational | operational-project | companion-system | mixed-domain
**Content domains:** personal-lived | shared-relational | operational-project | companion-system | mixed
**Use domain:** private conversation | group conversation | coding | research | planning | roleplay | other
**Surfaces:**
**Roles:**
**Projects/scopes:**
**Continuity horizon:** same session | cross-session | delayed | migration | prospective
**Primary operation under test:** retain | update | retrieve | route | suppress | compose | use | repair | migrate | wake
**Adult synthetic case:** yes
**Authors/reviewers:**

## 1. Bounded construct

写出本 case 要测试的一个 behavior distinction。

## 2. Causal claim

哪个 historical variable 应改变 correct response、retrieval 或 context region？

## 3. Minimal common history

只列建立 case 所必需的 events。

## 4. Counterfactual twins

每个 twin 只改变一个 critical variable；irrelevant wording、current turn、model settings 与 review contract 保持稳定。

## 5. Current probe

Current turn 不应直接泄露 historical answer。

## 6. Probe evidence contract

### Event evidence

Synthetic timeline 中客观发生了什么？

### Explicit accord

哪些内容被 explicit accepted、corrected、revoked 或 scoped？

### Observed pattern

哪些 repeated behavior 存在，但没有 explicit agreement？

### Author interpretation

Case author 推断了什么？列出 alternatives 与 confidence。

### Probe expectation

为这个 bounded probe 定义 `must`、`may` 与 `must_not`。

### Hard prohibition

只有 explicit、high-confidence case evidence 支持时才使用。

## 7. Evidence classes

- required；
- allowed；
- historical；
- prohibited from retrieval、context 或 response use。

## 8. Memory Necessity Gate

- [ ] Current turn 本身不能可靠解决所有 twins。
- [ ] 移除 history 会改变 correct behavior region。
- [ ] Twins 只在 intended critical variable 上不同。
- [ ] No-memory system 应在 twins 上表现相同。
- [ ] Reference-context baseline 能完成 task，证明 response contract feasible。

## 9. Controls

- current-turn-only；
- no-memory；
- 在 feasible 时 full-history/full-search；
- bounded minimal history 或 reference-context；
- system-native；
- optional architecture-specific ablation。

## 10. Routing and isolation claim

这个 memory 应进入哪个 domain、project、surface、person、instance 或 role？哪些 neighboring scopes 必须隔离？若 routing 不属于本 case，说明原因。

## 11. Significance discipline

Case 是否让 ordinary information 保持 ordinary，还是 author 发明了不必要的 romantic、symbolic 或 relational meaning？写明任何 significance claim 与 evidence。

## 12. Observable stages

指定 required outputs：evidence、rendered context、final response、repair behavior 或其他 artifacts。

## 13. Evaluation and review

分开 deterministic assertions、bounded semantic judgments 与 legitimate disagreement。Bootstrap 期间不定义 composite score。

## 14. Expected failure layers

Ingestion、state、authority、retrieval、composition、response use、repair、migration、evaluator 或 unknown。

## 15. Architecture assumptions

列出任何可能偏爱某个 system family 的 requirement。

## 16. Ambiguity and alternative readings

说明 reasonable reviewer 为什么可能 disagree。

## 17. Cultural and linguistic notes

记录 register、code-switching、private language 或 culturally specific interpretation。

## 18. Privacy and provenance

声明 case 是 fully invented，还是 synthetically derived from consented Incident Seeds。不要包含 raw private excerpts。

## 19. Acceptance decision

根据 review evidence 选择 accept、revise、split 或 reject。
