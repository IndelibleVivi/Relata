**简体中文** | [English](claim-boundary-study.md)
<!-- language: zh-CN; mirror: claim-boundary-study.md; translation-status: synchronized -->

# Candidate Claim-Boundary Study

- **Status：** proposed R0 research material；不是 accepted protocol、schema、scoring contract 或 publication policy
- **Decision targets：** RQ1、RQ6、RQ7、RQ8 与 RQ11
- **Evidence state：** 用于 pressure-test 的 editorial synthesis；目前没有 system run、reviewer study 或 comparative result 支撑这些 proposals

## 1. Research question

Relata 必须先决定：一次 evaluation observation 结束后，项目究竟有资格说什么。Final response 正确，不等于 memory subsystem 导致了成功；response 错误，也不能在 retention、activation、context composition、response use、routing 与 evaluation 部分或完全不可见时，自动定位 failure。

本 study 提议：public result unit 应是**由已识别 evidence 支撑的 scoped claim**，而不是裸 score 或被推测出来的 internal state。这项 proposal 有意停留在 implementation 之前：Pilot 001、System Census 与 reviewer calibration 都可能修改或否定下面的任何 decomposition。

## 2. Candidate result unit

一条 scoped claim 至少识别：

```text
exact configured subject
× frozen case revision
× observation lane and subject input view
× execution condition
× evaluator contract
× preserved evidence
× bounded assertion and limitations
```

Subject 可以是 complete system、配合 fixed reader 的 memory-support component，或 system-and-adapter combined pipeline；claim 必须明确是哪一种。只有 product 或 repository 名称，不足以构成 identity。

下面的 YAML-shaped fragment **只用于示意，且 non-normative**。它不是 accepted schema、required file format、implementation interface，也不保证其中所有 fields 会在 R0 后保留：

```yaml
subject:
  configured_system: exact build or honest observed-at identity
  adapter: exact adapter and declared contribution class
scope:
  case_revision: frozen case variant
  observation_lane: candidate lane
  input_view: declared subject-visible material
assertion:
  claim_level: CL0-CL6
  bounded_statement: plain-language claim
support:
  outputs: preserved artifact references
  controls: completed and unavailable conditions
  reviews: reviewer records and disagreement
limitations:
  opaque_stages: stages not observed
  attribution: system | combined_pipeline | unknown
```

Relata 当前没有 accepted `ResultClaim` record、public result registry 或 eligibility computation。

## 3. Claim Eligibility Ladder

Claim Eligibility Ladder 限制一次 observation 可以被推广到多远；它不是 quality score。CL1–CL5 在相应 evidence 存在时，描述逐步更具体的 behavioral / causal claim ceilings。CL6 是套在 underlying claim 外的 comparison-eligibility wrapper，不要求每个可比较 system 都 expose CL4 或 CL5 mechanism evidence。

### CL0 — 不可形成 public claim

Exact case、subject、configuration、adapter、output 或 evaluation identity 缺失，或 artifact 无法与手工修改区分。

- **Allowed：** local debugging note。
- **Forbidden：** 任何 public performance、mechanism 或 comparative claim。

### CL1 — Bounded outcome observation

一个 exact configured pipeline 在一份 frozen case contract 下产生并保存了 response 或 action；evaluator 按 contract 记录 `acceptable`、`unacceptable`、`ambiguous`、`invalid` 或 `unknown`。

- **Required：** exact output、case revision、configured subject identity、adapter identity 与 evaluator record。
- **Allowed：** “这个 configured pipeline 在该 condition 下，为这张 case 产生了 acceptable response。”
- **Forbidden：** “Memory 导致了成功”“该 system 能追踪 current state”，或 product-wide capability claim。

### CL2 — Counterfactual 或 scope-conditioned discrimination

Configured pipeline 同时满足 pair 两侧互不重叠的 bounded correct regions。Pure historical counterfactual 保持 current probe 与 nonhistorical current metadata 一致，只改变 intended historical branch。Routing case 可以有意改变 declared target metadata，同时保持 textual probe 一致；此时必须叫 **scope-conditioned routing pair**，不能称作 pure historical counterfactual。

- **Required：** 两侧 outputs、pair identity、exact changed variable 与 pair-level decision。
- **Allowed：** “Configured pipeline 在两个 declared worlds 中执行了 case-specific policy。”
- **Forbidden：** memory-mechanism attribution；或在 scope metadata 已变化时声称 history 是唯一 changed input。

### CL3 — History-dependence observation

Current-turn-only 与（如 feasible）no-memory conditions 不能可靠解决 pair；history-bearing condition 可以；reference context 同时证明 response contract 可完成。

- **Required：** current-turn-only、no-memory 或其 unavailable 理由、history-bearing 或 full-history/full-search，以及 reference-context evidence。
- **Allowed：** “在这些 conditions 下，正确行为依赖于访问 case-bounded historical state。”
- **Forbidden：** complete agent、adapter 或 answerer 也发生变化时，把 effect 归因到某一个 memory subsystem。

对于 scope-conditioned routing pair，current metadata-only control 仍必须无法透露任一 scope 应选中的 remembered content。

### CL4 — Memory-support contribution observation

一项 matched intervention 改变 memory access 或 memory output，同时把 answerer、prompt policy、case 与其他相关 execution conditions 控制到足以支持 bounded causal attribution。

Candidate interventions 包括：memory enabled versus disabled、system-native evidence versus reference evidence、retrieval replay，以及 isolated versus merged scope access。

- **Required：** declared intervention seam、controlled conditions、preserved outputs，以及哪些因素保持稳定的 limitations。
- **Allowed：** “Observed difference 可归因于该 intervention boundary 内的 memory-support path。”
- **Forbidden：** 越过 controlled seam，或向 hidden internal stages 继续归因。

### CL5 — Stage-localized observation

System-native artifacts 或 valid intervention 能区分 retention/state maintenance、retrieval/activation、context composition、response use、repair、routing 与 evaluation。

- **Required：** stage evidence，或能够分开 named candidate layers 的 intervention。
- **Allowed：** “Required evidence 可 reach，但没有进入 rendered context”，或不超过 observed seam 的其他 statement。
- **Forbidden：** 把 missing trace、unsupported stage 或 opaque architecture 当作该 stage 已失败的证据。

Visibility 缺失时，attribution 是 `unknown`；final behavioral outcome 仍可停留在较低 eligible level。

### CL6 — Comparative-publication eligibility

两条或更多 claims 只有在一个 justified comparability cell 内、受到未来 accepted publication policy 约束，并具有足够的 repeated execution、review、identity、adapter 与 uncertainty evidence 时，才 eligible for comparison。

- **Required：** underlying bounded claim 本身需要的 evidence；相同 accepted cell；declared replication 与 reviewer distributions；可见的 uncertainty / missingness；publication authority。
- **Allowed：** 该 cell 内的 bounded comparative profile。
- **Forbidden：** global “best memory system” language，或跨 answerer、input、lane、case、evaluator regimes 比较。

CL6 不升级 attribution：underlying evidence 只到 CL2 或 CL3 的 behavioral comparison，即使 eligible for comparison，也仍然只是 behavioral。Opaque complete agent 不会仅因缺少 CL5 visibility 被排除。Relata 在 R0 没有 CL6 claims；这个 candidate level 不授权 Leaderboard。

## 4. Candidate observation lanes

这些 lanes 是彼此竞争的 observation decompositions，**不是永久 tracks、directories、APIs 或 brands**。System Census evidence 可以 merge、rename、split 或 reject 它们。

| Lane | Declared subject 与 observable | 保留什么 | 没有进一步 intervention 时的 default attribution ceiling |
|---|---|---|---|
| L1 — complete-agent continuity | configured agent 使用自身 model、memory、persona、context policy 与 tools 产生的 final response / action | opaque 与 integrated companions | 通常是 CL2 或 CL3；internal stages 仍为 unknown |
| L2 — fixed-reader memory support | memory-produced evidence / context，由 Relata-fixed answerer 与 prompt 消费 | 更严格控制 downstream answerer variation | memory seam 与 rescue/replay intervention valid 时，可能达到 CL4 或 CL5 |
| L3 — native diagnostic observation | system-native current-state、retrieval、context、path、repair、routing 或其他 exposed artifacts | 不强迫统一 trace 的 architecture-specific diagnosis | 默认 descriptive；只有 native artifact 足以支撑时才形成 stage claim |
| L4 — local private regression | relationship owner 在 declared boundary 下本地运行 private material | 在不 public-transfer raw history 的前提下保留真实 usefulness | 默认不 publication；任何 public claim 都需要另行完成 synthetic conversion 与 authority |

L1 与 L2 即使回答同一 case，也不会因此直接 comparable。L3 artifacts 不能被当成 equivalent native traces 排名。L4 evidence 保持 local，除非一条 explicit、public-safe contribution path 已实际走通。

## 5. Candidate comparability cells

Comparability cell 是对 direct comparison 的 proposed restriction。Candidate dimensions 是：

```text
case revision and locale/adaptation
+ observation lane
+ subject input view
+ answerer regime
+ adapter contribution class and case-specific distortion
+ execution regime
+ evaluator contract
```

只有 evidence 表明会 materially change evaluand 的 dimensions，才应成为 accepted cell boundaries。把每个 configuration field 都当 boundary，会把 evidence 切碎到无法比较；忽略 material differences，则会制造 false ranking。

在 System Census 与 pilot runs 出现前：

- 这些 dimensions 是 pressure-test questions，不是 accepted partition；
- cross-cell observations 可以描述，但不能放进同一 ordered table；
- raw-history 与 structured-current-state inputs 不得被 silently equated；
- system-owned 与 fixed answerers 不得被 silently equated；
- public synthetic case 与 local private regression 不得共享一个 public result class。

## 6. Adapter Contribution Classes

Class names 描述 adapter 在一条 declared case path 中的 contribution；它们不能代替 case-specific distortion note。

| Class | Candidate meaning | Claim consequence |
|---|---|---|
| A0 — transport only | invocation、authentication、retry 或 serialization，不发生 semantic change | system-level claim 可能保留 |
| A1 — deterministic lossless normalization | reversible field rename、stable order、encoding normalization 或 wrapping | 能为该 case 证明 lossless 时，system-level claim 可能保留 |
| A2 — deterministic lossy projection | truncation、fixed chunking、field omission 或其他 non-semantic loss | 需要 separate comparison treatment 与 explicit loss report |
| A3 — semantic transformation | summarization、extraction、relevance filtering、改变 ambiguity 的 translation，或 inferred labels | claim subject 变成 system-and-semantic-adapter combined pipeline |
| A4 — state reconstruction or capability emulation | adapter 创建 system 没有 expose 的 current state、supersession、provenance、routing、correction 或其他 capability | 不得形成 underlying-system mechanism claim；仍可 observation final pipeline behavior |
| A5 — task solving | adapter 选择或写出被 evaluation 的 response / action | 不得声称 underlying memory system 执行了 tested behavior |

一个 adapter 在不同 cases 中可以属于不同 class。Deterministic operation 也可能摧毁正在测试的 capability。因此每条 result 都必须同时说明 candidate class，以及 observed 或 unresolved distortion。

## 7. `unknown` 是 evidence state

Relata 必须分开以下 findings：

- architecture 没有实现某项 capability；
- capability 存在，但其 stage hidden；
- supported boundary unknown；
- adapter reconstructs 或 emulates capability；
- combined pipeline 产生 final success 或 failure。

Missing visibility 永远不自动变成 failure。反过来，opaque stages 下的 final success 也不证明某种 memory mechanism 成功。Strongest justified claim 必须停在最后一个 observed 或 validly intervened boundary。

## 8. 对当前 research questions 的 pressure

| Research question | 本 study 引入的 pressure | Acceptance 前需要的 evidence |
|---|---|---|
| RQ1 — evaluation object | 要求每条 claim 说明 subject 是 complete agent、memory support path、native diagnostic stage，还是 combined pipeline | competing System Cards，以及多个 boundary 上的 pilot claims |
| RQ6 — causal contribution | 分开 final correctness、history dependence、memory-support contribution 与 stage localization | matched controls、rescue/replay interventions，以及 explicit unavailable conditions |
| RQ7 — cross-system boundary | 让 architecture pressure 与 adapter reconstruction 成为 claim identity 的一部分 | 三张 materially different reviewed System Cards 与一张 Architecture Pressure Map |
| RQ8 — reproducible judgment | 防止 deterministic check、bounded semantic review 与 legitimate disagreement 被压成一个 label | E0 anchors、blind human review、disagreement analysis；只有 evidence 支持时才做后续 model-judge audit |
| RQ11 — mixed-domain routing | 要求 routing/isolation case 识别 selected scope 与任何 adapter-created selection | scope-conditioned controls、isolated versus merged histories，以及 ordinary project/private cases |

## 9. Candidate decision tests

在本 study 的任何部分成为 protocol authority 前，Relata 应能回答：

1. Reviewers 是否真的用 ladder 收窄 claims，还是只重复填写 metadata？
2. Materially different systems 能否共享有用 observation boundary，而不让 adapter reconstruction 变成被测 capability？
3. 哪些 proposed cell dimensions 会 materially change outcome 或 interpretation？
4. Adapter contribution 能否在附带 case-specific distortion note 时被一致分类？
5. Pilot 001 与 mixed-domain routing case 是否会得到不同 justified claim ceilings？
6. Missing visibility 能否保持醒目，又不被误当成 failure 或被拿来为 success 开脱？

这些 tests 获得 evidence 前，本文件继续是 candidate study。它不修改 `STATUS.md` authority，不 accept executable boundary，也不授权 schemas、runners、services、Workbench、Arena 或 Leaderboard。
