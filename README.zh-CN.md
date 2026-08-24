**简体中文** | [English](README.md)
<!-- language: zh-CN; mirror: README.md; translation-status: synchronized -->

# Relata

> 中文贡献者可以直接从本页与 [中文执行路径](START_HERE.zh-CN.md) 开始；R0 的主要工作与社区参与语言是中文。[English entrypoint](README.md) 与中文 authority 同步维护。

**Relata** 是一个开放、由社区活经验参与塑造的研究计划与案例实验室，用于研究成人长期人机关系中的记忆与连续性。

它的核心问题是：

> 一个系统能否延续这个人、这段关系，以及双方共同形成的生活与工作世界，同时忠于历史的来源、时间、权威、范围、权限、变化与当下相关性？

成人长期人机亲密与浪漫关系继续是 Relata 的 primary deployment domain，但这不意味着 memory content 只能是显式的亲密、浪漫或关系治理材料。Relata 研究：什么被 retained，什么被 activated，什么进入 model / action layer，它怎样被使用，不适合当下的记忆是否保持沉默，以及 correction 能否在不抹去这个人、这段关系或共同工作的前提下持续生效。

## 记忆生态

Relata 当前的 working evaluation object 是 **longitudinal, mixed-domain continuity-bearing memory ecology**，即长期人机关系中的混合领域连续性记忆生态：

- **Personal / lived world：** 普通事件、人物与地点、兴趣与习惯、健康、学习、旅行、媒体与日常生活。
- **Shared relational world：** 共同经历、私密语言与 ritual、关系变化、interpretation、correction、permission 与 boundary。
- **Operational / project world：** 项目状态、决策与理由、任务、blocker、milestone、artifact、evidence、handoff 与 future intention。
- **Companion / system continuity：** companion identity、model/provider/instance 变化、migration history、capability、limitation 与 interaction pattern。

一项内容不需要具有显式的浪漫或象征意义，才属于 Relata。普通生活事件和共同项目历史都是一等 continuity-bearing material。

Relata 保留 general memory evaluation 的有效核心，包括 factual recall、temporal reasoning、provenance、noise resistance、scope isolation 与 full-history/full-search comparison。它额外追问的是：异质 memory 怎样跨越长期的 roles、surfaces、projects 与关系变化，被正确 routing、governed、used、repaired 与 carried forward。

## 当前阶段

Relata 处于 **R0 — Research Foundation**。`R0` 是阶段名，不是项目名。

| Area | 当前状态 |
|---|---|
| Charter 与 research questions | working authority |
| Draft 0.1 assumptions | 已重新分类为 decisions、hypotheses、aspirations、deferred items 或 rejected items |
| Source research | 两张 accepted Evidence Cards；AML 与 PM-Bench findings 只在各自 narrow authorization 内迁入，没有采用其 architecture 或 score |
| Community participation | co-research 与 consent materials 已存在；尚未开放 intimate-material collection |
| System Census | templates 已存在；尚无 reviewed System Card |
| Distinction Atlas | 六条 seed hypotheses 与 mixed-domain incident families；尚无 supported distinction |
| Case coverage | 五个 proposed coverage strata；一张 clinic-ready pilot 与两张未经 review 的中文 case seeds；尚未运行，也没有 balanced pilot set |
| Pilot 001 | clinic-ready 的 shared-relational/current-state-use case；尚未运行，也不能代表完整 scope |
| Software | 只有 repository checker |

Relata 当前**不声称**拥有 canonical ontology、system protocol、scoring contract、benchmark release、runner、Leaderboard、Arena、SDK、service、hosted infrastructure 或 accepted implementation architecture。

## 为什么暂时不建平台

原 architecture draft 在 Relata 尚未建立 construct validity、architecture coverage、case causality、reviewer calibration 或 contributor-governance path 之前，就指定了一套成熟 evaluation platform。现在直接构建，会把开放研究问题过早固化成 accidental interfaces 与 scores。

因此，保存在 [`docs/vision/`](docs/vision/README.md) 下的 [Target Architecture Draft 0.1](docs/vision/relata-target-architecture-draft-0.1.md) 是 **non-normative north-star draft**。[Adversarial review](docs/reviews/target-architecture-draft-0.1-adversarial-review.md)、[foundation integration review](docs/reviews/research-foundation-integration-review.md) 与 [assumption register](ASSUMPTION_REGISTER.zh-CN.md) 记录了哪些内容保留、改写、defer 或 reject。

## 已经开始的研究

第一批 exact-source targets 已完成：

- [`EC-001`](research/evidence-cards/EC-001-agent-memory-leaderboard.md) 锁定 Agent Memory Leaderboard 的 public evaluation boundary，只接受 responsibility seam、fixed-reader causal limit、architecture-specific interface commitment 与 version-binding public proof findings。
- [`EC-002`](research/evidence-cards/EC-002-pm-bench-observation-and-scorer-binding.md) 锁定 PM-Bench paper、scorer、scenario 与 64 份 released primary logs，分开 action success、observation provenance、current-version intent 与 step identity，并记录 released logs 没有 step-order score impact。

两张 card 都不验证 source benchmark，也不为 Relata 选择 interface。[`ADR-0003`](decisions/ADR-0003-mixed-domain-memory-ecology.zh-CN.md) 使 mixed-domain scope correction 成为 authority，同时明确 coverage strata 不是 implementation tracks。

接下来三项可执行工作是：

1. Review 并 refine 新增的 ordinary-life 与 operational/project seeds；然后设计第一张 mixed-domain routing/isolation seed，且不把任何 seed 冒充 clinic-ready。
2. 完成三张 materially different、contributor-reviewed System Cards 与一张 Architecture Pressure Map；在收集 sensitive contributions 前选择 restricted consent-record stewardship。
3. 运行 Pilot 001 controls 与 blind Case Clinic review，同时构建 full-scope claim 所需的第一批 ordinary-life、operational/project 与 mixed-domain routing cases。

这些任务可从 [中文执行路径](START_HERE.zh-CN.md) 进入；[English execution path](START_HERE.md) 与之同步。

## 参与方式

社区成员以 co-researchers 身份参与，不是在设计完成后才加入的普通 subjects。贡献路径包括：

- 一张 exact-source [Evidence Card](research/evidence-card-template.md)；
- 一份无需 raw chat 的抽象 [Incident Seed](community/incident-seed-template.zh-CN.md)；
- 一张使用 system-native vocabulary 的 [System Card](systems/system-card-template.zh-CN.md)；
- [Case Lab](case-lab/README.zh-CN.md) 中的 synthetic case 或 case review；
- terminology、privacy、consent、attribution、withdrawal 或 governance review。

Consent 按每份 contribution 单独选择，不构成 participation ladder。收集材料前请阅读 [中文 consent modes](community/consent-levels.zh-CN.md)、[中文 participation principles](community/participation-principles.zh-CN.md) 与 [R0 language policy](docs/language-policy.zh-CN.md)。

## Public repo 与 privacy

Public source repository 是 [IndelibleVivi/Relata](https://github.com/IndelibleVivi/Relata)。公开可见是为了让 research、cases、methods 与 code 可 inspect；它不授权发布 raw private conversations、identifying consent records、credentials、restricted system details 或 private review material。Public-safe source 与 documentation feedback 可以走普通 GitHub contribution；sensitive community material 需要另行约定 restricted route。

Relata 还没有选择 public licenses。Repo 可见不等于授予 reuse rights；参见 [open licensing decision](governance/licensing-decision.md)。

## Repository map

- [`CHARTER.zh-CN.md`](CHARTER.zh-CN.md) — mission、scope、commitments、non-goals 与 R0 success condition
- [`RESEARCH_QUESTIONS.zh-CN.md`](RESEARCH_QUESTIONS.zh-CN.md) — open questions 与 required evidence
- [`ASSUMPTION_REGISTER.zh-CN.md`](ASSUMPTION_REGISTER.zh-CN.md) — Draft 0.1 claims 的 current disposition
- [`STATUS.zh-CN.md`](STATUS.zh-CN.md) — 当前 evidence 与 promotion state
- [`research/`](research/README.md) — source/evidence workflow
- [`systems/`](systems/README.zh-CN.md) — architecture census
- [`case-lab/`](case-lab/README.zh-CN.md) — distinctions、case method 与 Pilot 001
- [`community/`](community/participation-principles.zh-CN.md) — co-research 与 consent materials
- [`governance/`](governance/public-private-boundary.md) — privacy、attribution、withdrawal 与 publication boundaries
- [`decisions/`](decisions/README.md) — accepted 与 proposed decisions
- [`docs/terminology.zh-CN.md`](docs/terminology.zh-CN.md) — current research terms
- [`docs/language-policy.zh-CN.md`](docs/language-policy.zh-CN.md) — R0 双语 authority 与 drift rules
- [`docs/vision/`](docs/vision/README.md) — non-normative historical vision

## Authority 与检查

文档冲突时，依次遵循：

1. `STATUS.md` / `STATUS.zh-CN.md`
2. `CHARTER.md` / `CHARTER.zh-CN.md`
3. `ASSUMPTION_REGISTER.md` / `ASSUMPTION_REGISTER.zh-CN.md`
4. `decisions/` 下的 accepted records
5. research 与 governance materials
6. case-lab materials
7. vision documents

在 repo root 运行：

```bash
python3 tools/check_repo.py
```

Checker 验证 required research surfaces、禁止的 premature project shells、Draft 0.1 authority banner、assumption-register coverage、Case Card metadata、Pilot controls、required bilingual pairs、reciprocal links 与 local Markdown links。它不会假装自动验证中英语义等价。
