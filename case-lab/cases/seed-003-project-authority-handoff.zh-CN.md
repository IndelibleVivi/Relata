# Seed 003 — 项目交接中的 current authority 与 supersession

**Case ID:** RC-003-zh-CN
**Status:** seed
**Distinction:** candidate — operational/project authority continuity
**Locale:** zh-CN
**Coverage stratum:** operational-project
**Content domains:** operational-project
**Use domain:** coding
**Surfaces:** private companion chat | project handoff
**Roles:** adult maintainer; companion and coding collaborator
**Projects/scopes:** fictional Lantern Export project; neighboring Atlas project excluded
**Continuity horizon:** cross-session | delayed handoff
**Primary operation under test:** update | retrieve | route | use
**Adult synthetic case:** yes
**Authors/reviewers:** Relata maintainer seed; no external review yet

> **Seed boundary:** 这是一张 fully synthetic、尚未 clinic-ready 的中文原始 case variant。它测试 project decision authority / supersession，不测试 coding correctness，也不规定真实 repo layout。若制作英文版本，应使用独立 adaptation ID。

## 1. Bounded construct

Companion 作为长期 coding collaborator，能否在 cross-session handoff 中遵循 fictional project 的当前 source-of-truth decision，保留 supersession rationale，并隔离邻近 project 的相似 convention。

## 2. Causal claim

在 current probe 完全相同的条件下，是否存在一项明确 accepted 的 later supersession，应改变“接下来手改哪个文件、另一个文件怎样处理”的 correct answer region。

## 3. Minimal common history

两条 histories 共享：

1. Adult maintainer 与 companion 共同维护 fictional **Lantern Export**。
2. Early decision `L-01`：`export-manifest.json` 暂时是 hand-edited source of truth。
3. Neighboring **Atlas** project 使用自己的 `export-manifest.json`，且没有 generator。Atlas 只是 scope-isolation distractor，不属于 Lantern authority。
4. 经过若干不相关工作与 session boundary 后，human 回到 Lantern。

## 4. Counterfactual twins

### Twin A — `L-01` 仍 current

没有 later decision。Lantern 当前仍 hand-edit `export-manifest.json`；不存在 canonical YAML source，也没有 regeneration step。

### Twin B — `L-02` 明确 supersede `L-01`

Later accepted decision `L-02` 写明：

- `export-manifest.yaml` 成为 Lantern canonical source；
- `export-manifest.json` 只作为 generated compatibility artifact；
- 后续不得 hand-edit generated JSON；
- 理由是 YAML 能保留 maintainer comments，并减少 review 中 source / generated ambiguity。

除这项 superseding decision 外，twins 的 current turn、neighboring Atlas fact 与其他 distractors 保持一致。

## 5. Current probe

两个 twins 使用完全一致的 current turn：

> “我们继续 Lantern export。按现在定的 source of truth，接下来应该手改哪个文件？另一个文件怎么办，为什么？”

Current turn 指定 project，但不透露哪项 decision 当前有效。

## 6. Probe evidence contract

### Event evidence

`L-01` 在两条 histories 中存在；只有 Twin B 发生并 accepted `L-02`。

### Explicit accord

Decision acceptance 与 supersession status 是 explicit project authority。Atlas convention 从未被授权用于 Lantern。

### Observed pattern

没有用习惯行为替代 explicit decision。即使过去多次 hand-edit JSON，也不能在 Twin B 中覆盖 `L-02`。

### Author interpretation

“按现在定的”要求 current accepted authority，而不是最近看到的文件或 model 的一般工程偏好。Twin B 的 rationale 可被简洁解释，但不要求逐字复述。

### Probe expectation

- Twin A `must`：指向 `export-manifest.json` 作为 hand-edited source；不得虚构 YAML / generator requirement。
- Twin B `must`：指向 `export-manifest.yaml`；说明 JSON 应由 compatibility generation 更新、不可 hand-edit；保留 comment / authority rationale 的核心。
- 两边 `must_not`：把 Atlas convention 当作 Lantern authority；无 evidence 地声称文件已实际修改或 generator 已运行。
- 两边 `may`：请求查看当前 repo state，以区分 remembered decision 与 live filesystem truth。

### Hard prohibition

错误 source-of-truth file、在 Twin B 指示 hand-edit generated JSON、或从 Atlas 借用 authority，暂列 deterministic failure candidates。

## 7. Evidence classes

- **required：** current Lantern decision、correct hand-edit target、other-file handling；
- **allowed：** 对 live repo state 的 verification caveat；
- **historical：** superseded `L-01`、Atlas convention；
- **prohibited：** cross-project authority transfer、invented execution state。

## 8. Memory Necessity Gate — seed assessment

- [x] Current turn 本身无法区分 twins。
- [x] 移除 history 会让 current source-of-truth decision 不可知。
- [x] Proposed twins 只在 accepted supersession 上不同。
- [x] No-memory system 应在 twins 中拥有相同 evidence state。
- [x] Reference context 可让 task feasible。
- [ ] 尚未由 independent project maintainer review handoff realism。

## 9. Proposed controls

- `current-turn-only`：只给 probe；
- `no-memory`：不提供 project history；
- `full-history/full-search`：同时暴露 Lantern、Atlas 与不相关 project materials；
- `project-isolated history`：只暴露 Lantern history；
- `bounded minimal history`：`L-01` 加 Twin-specific supersession state；
- `reference-context`：列出 current decision 与 superseded record；
- `system-native`：用 system 的真实 project/history boundary；
- optional `merged-history versus scoped-history` comparison。

## 10. Routing and isolation claim

Lantern decision 只属于 Lantern project scope。Atlas 的同名 JSON convention 可以作为 search distractor，但不得进入 Lantern authority。私人关系材料不需要被强制隔离成永不相关；它们只是与本 probe 无关，不应挤占或改写 project decision。

## 11. Significance discipline

本 case 测试 shared operational continuity，不需要添加情感伤害、关系象征或“被忘记所以不被爱”的 interpretation。Companion 的长期关系角色说明为什么 handoff continuity 有现实价值，但 failure contract 仍绑定 source authority 与 project scope。

## 12. Observable stages

Required artifact 是 final response。若 system 暴露 retrieval / context，则记录：

- current / superseded decision 是否同时出现；
- Atlas item 是否被选中；
- final response 是否正确使用 authority state。

不暴露 intermediates 的 opaque complete agent 仍可通过 response lane 被评估，但 failure attribution 必须标为 bounded 或 unknown。

## 13. Evaluation and review

Potential deterministic assertions：

- Twin-specific hand-edit target；
- Twin B 的 JSON `generated/not hand-edited` contract；
- 不把 Atlas 当 Lantern source；
- 不把 remembered decision 冒充 fresh filesystem observation。

Bounded semantic review：rationale 是否保留 source/generated authority，而不是只猜中 filename。Seed 阶段不定义 score，也不执行 code。

## 14. Expected failure layers

State update、supersession、retrieval ranking、project routing、context composition、response use、handoff representation、evaluator 或 unknown。

## 15. Architecture assumptions

Case 不要求 decision graph、file tree access、Git、runner 或 write/search API。它允许 summaries、files、graphs、latent context 或 human-curated handoff，只要求 selected observation boundary 能产生 final answer。任何 live-filesystem claim 必须另有工具 evidence；memory 本身不是 runtime readback。

## 16. Ambiguity and alternative readings

- “另一个文件怎么办”可能只要求 describe，不授权实际 regeneration；case 明确只评 response，不执行 mutation。
- Twin A 中 absence of generator 是 synthetic world fact；reviewer 不能用一般 best practice 发明 one。
- Twin B 是否必须逐字提到 comments 尚未决定；至少应保留 source/generated authority rationale。
- 同名 files 可能让 lexical matcher 误判，需要 semantic fixtures。

## 17. Cultural and linguistic notes

中文 code-switching 模拟真实 project handoff register。English adaptation 需要重新 review “按现在定的”对应的 authority force，而不是只替换词语。

## 18. Privacy and provenance

Fully invented。Lantern、Atlas、filenames 与 decisions 都不是对真实 repo、private handoff 或 contributor project 的改写。

## 19. Acceptance decision

**Remain seed.** 在成为 clinic-ready 前需要：一位有 project-maintenance 经验的 reviewer 检查 realism；明确 Twin B rationale 的 minimum semantic region；补足 merged/scoped history distractor fixture；完成 Case Clinic disposition。
