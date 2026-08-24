# Relata 从这里开始：Research Foundation 执行路径

这条路径负责把 non-normative 的 Target Architecture Draft 0.1，推进成有 source provenance、architecture pressure、community authority 与 case evidence 的 Relata。

## 当前已经存在的正式基础

- [Charter](CHARTER.md)、[research questions](RESEARCH_QUESTIONS.md) 与 [assumption register](ASSUMPTION_REGISTER.md)
- [原 architecture 的 adversarial review](docs/reviews/target-architecture-draft-0.1-adversarial-review.md)
- [source / evidence workflow](research/README.md) 与 Evidence Card template
- community co-research、consent、attribution 与 withdrawal 材料
- System Census 与 Architecture Pressure Map templates
- Distinction Atlas、case method、Pilot 001 与 manual pilot plan
- repository structure / Markdown link checker

先运行：

```bash
python3 tools/check_repo.py
```

## 第一项：Evidence Card 001 已 accepted

- [x] 分开锁定 AML 的 pinned GitHub source、pinned Hugging Face result snapshot 与 dated mutable hosted observations。
- [x] 确认本地没有可复用的既有 AML audit artifact，因此没有迁入悬空结论。
- [x] 在 [`EC-001`](research/evidence-cards/EC-001-agent-memory-leaderboard.md) 中分开 source claim、reproduced observation、inference、contradiction 与 unverified boundary。
- [x] 把 accepted transfer 连到 RQ1/RQ6/RQ7、Assumptions 5/20 与 System Census pressure questions。
- [x] 完成 adversarial source-fidelity review 并逐条对回 pinned bytes 后，才 narrow-accept 该 card。

**已于 2026-08-24 达成：** 一张支撑 bounded Relata questions 的 accepted Evidence Card；但不为 AML 的 score、validity、architecture、hosted execution 或 governance 背书。

## 第二项：做第一轮 System Census

- [ ] 收集 community contribution 前，先确认 identifying consent records 的 restricted storage 与 steward。
- [ ] 只做小范围、私下 Founding Circle 邀请；source repo 已公开，但不要通过 public issue / PR 收 sensitive community material。
- [ ] 每个人可以自由选择 Incident Seed、System Card、case review、source review 或 governance，不设技能等级。
- [ ] 用系统自己的 vocabulary 与 boundary，完成三张 contributor-reviewed System Cards。
- [ ] 做一张 Architecture Pressure Map，分清 native、adapter-emulated、opaque、unsupported、unknown 与 not applicable。
- [ ] 单独列出每个拟议 observation boundary 会偏爱或抹掉哪类 architecture。

**完成标志：** 三种 materially different systems + 一份明确的 protocol-bias record；不产生排名。

## 第三项：执行 Pilot 001

- [ ] freeze `case-lab/cases/pilot-001-current-state-without-erasure.md` 的一个 revision。
- [ ] 为 twins 分别生成 current-turn-only、no-memory、full-minimal-history、reference-context 与 system-native outputs。
- [ ] current turn 保持 byte-identical；每组比较内部固定 answer-model config。
- [ ] 至少由两种已披露 perspective 的 reviewers 做 blind review。
- [ ] 分开记录 deterministic assertion、bounded semantic judgment、legitimate disagreement、evaluator ambiguity 与 observability limits。
- [ ] 决定“撤回短语的 semantic equivalent”是否属于本 pilot 的 formal failure boundary。
- [ ] 最终 accept、revise、split 或 reject；不生成 composite score。

**完成标志：** 对 Pilot 001 是否真正证明 memory necessity 与 counterfactual discriminability，得到有 review evidence 的决定。

## 第四项：完成 Evidence Card 002

- [ ] 重新锁定 PM-Bench 的 official paper revision、repo commit、scorer、released scenario 与 primary-log boundary。
- [ ] 把本地已验证的 scorer-contract audit 只当 candidate evidence package，不当 Relata authority。
- [ ] 分开追踪 observation provenance、`step_id` identity、scorer consumption、diagnostic meaning 与 released-result impact。
- [ ] 分清 source-level possibility、released-corpus prevalence、causal interpretation 与 no-observed-impact finding。
- [ ] 任何结论转入 RQ6 / RQ8 前完成 source-faithful review。

**完成标志：** 一张针对 observation / scorer binding 的 decision-targeted card；不是泛泛的 PM-Bench summary，也不是新建 benchmark run。

## 当前开放事项完成以后

更新 `STATUS.md`、Distinction Atlas 以及受影响的 assumption / decision records。然后才判断 working promotion gate 是否足以支持第一份 implementation-boundary ADR。

## 明确延后

- canonical event-sourced world schema；
- 永久固定的 Recall / Context / Companion / Living tracks；
- system-under-study API；
- benchmark runner 与 SDK；
- composite score 与 model-judge panel；
- Arena 与 Leaderboard；
- sealed benchmark repo；
- services 与 hosted orchestration；
- FastAPI、Temporal、Kubernetes、S3 或 multi-repo operations；
- 100–300 session synthetic worlds。

这些东西以后可以回来，但必须由 evidence-backed decision 明确说明 architecture 与 governance consequences。
