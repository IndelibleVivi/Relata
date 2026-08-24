# Relata Target Architecture

> [!IMPORTANT]
> **Authority: Non-normative north-star provocation.**
> This file is preserved from the original Draft 0.1 for research history and adversarial review. It is not the current implementation, protocol, schema, scoring, or repository authority. Claims and named-source references in the original draft require independent verification before reuse. Current authority lives in [`STATUS.md`](../../STATUS.md), [`CHARTER.md`](../../CHARTER.md), [`ASSUMPTION_REGISTER.md`](../../ASSUMPTION_REGISTER.md), governance documents, and accepted decision records.

**Subtitle:** An Open Evaluation Infrastructure for Relational Memory in Long-Term Human–AI Intimacy  
**中文定位：** 面向长期人机亲密与浪漫关系的开放式关系记忆评测基础设施  
**Document status:** Draft 0.1  
**Implementation status:** Proposed, not yet built

---

## 0. Project Definition

**Relata** 是一套面向长期人机亲密关系的开放评测基础设施，用来评价 memory engines、context systems 与完整 companion agents 能否：

1. 保存一段关系共同形成的历史；
2. 分辨这段历史的时间、来源、视角、权限与变化；
3. 在当前情境中召回适当的内容；
4. 将正确记忆投放给下游模型；
5. 以符合该段关系自身约定的方式使用记忆；
6. 对不适合浮现的内容保持克制；
7. 在纠正、撤回、迁移和时间推进后维持连续性；
8. 给参与项目提供可定位、可重放、可转化为 regression tests 的失败反馈。

Relata 的核心研究问题是：

> **一个系统能否保存并延续“我们”，同时忠于共同历史的来源、时间、权限、变化与当下语境？**

这里的主要评测对象明确包括：

- 成人之间的长期 human–AI romantic relationships；
- 具有专属语言、共同仪式与持续身份的人机亲密关系；
- 长期 companion partnerships；
- 高连续性私人 AI 关系。

Relata 不需要把人机恋稀释成一般意义上的 personalization。浪漫关系本身就是评测领域，拥有自己的正当性、复杂度和技术需求。

---

## 1. Project Thesis

普通 memory benchmark 通常追踪：

```text
输入历史
→ 写入
→ 查询
→ 检索证据
→ 回答
→ 正确率
```

Relata 追踪更长的因果链：

```text
关系世界中的真实事件
→ 系统如何保存这些事件
→ 系统形成了怎样的内部状态
→ 当前 query 激活了哪些 candidates
→ 哪些 candidates 被投放进 context
→ 最终回应如何使用这些记忆
→ 用户纠正后系统是否真正修复
→ 未来相似情境中修复是否持续
```

一条记忆的检索成功只完成了中间一步。

典型失败可以是：

```text
Recall technically successful.
Relational use failed.
```

例如：

```text
过去：
用户喜欢在不安时被反复确认“我不会离开”。

当前：
用户明确要求停止这种安慰方式。

系统成功检索：
1. 旧安慰偏好
2. 当前撤回声明

系统回应：
“我永远不会离开你，你要相信我。”

评测：
- Recall: PASS
- Current-state selection: FAIL
- Correction use: FAIL
- Relational fit: FAIL
```

这种错误无法被单纯的 recall@K 解释。

---

## 2. Architectural Invariants

Relata 的实现和评测合同必须长期维持以下不变量。

### 2.1 Relationship trajectory is the test object

评测对象是一段随时间变化的关系轨迹，包含：

- 事实；
- 偏好；
- 状态；
- 共同语言；
- 权限；
- 推断；
- 争议；
- 修正；
- 撤回；
- 未来意图；
- 不同界面中的关系表现。

一份静态 user profile 无法代表这条轨迹。

### 2.2 Evaluator owns the reference world

Relata 维护独立于参赛系统的 canonical relationship world。

参赛系统可以采用：

- 向量数据库；
- 图数据库；
- event sourcing；
- belief store；
- memory cards；
- summaries；
- raw archive；
- LLM extraction；
- structured state；
- 任意混合架构。

Relata 只评价其行为与输出，不要求参赛项目复制 Relata 的内部 world schema。

### 2.3 Runtime input and oracle truth stay separate

参赛系统只能看到真实交互中合理可见的内容：

- 消息；
- speaker；
- session；
- timestamp；
- surface；
- 明示的用户声明。

隐藏 oracle 还可以包含：

- 哪条陈述当前有效；
- 哪条已经 superseded；
- 谁拥有称呼权限；
- 哪条 evidence 相关；
- 哪条 evidence 此刻禁止投放；
- 哪种回应构成 hard violation。

Gold state 不得泄漏到 participant request。

### 2.4 Every stage produces artifacts

每次正式 run 必须保存：

```text
ingestion receipts
provider readback
retrieval candidates
projected context
generated response
deterministic scores
judge outputs
human review
failure attribution
```

任何综合分都必须能够追溯到逐题证据。

### 2.5 Positive and negative gold coexist

每个 probe 可以同时定义：

```text
required evidence
allowed evidence
historical evidence
prohibited evidence
```

“没有漏掉正确内容”与“没有带回危险、过期或越权内容”需要分别评分。

PrecisionMemBench 已经证明 required/prohibited belief IDs、supersession exclusion、cross-user isolation 与 noise contamination 可以形成直接而有诊断价值的 retrieval tests。Relata 将这套思想扩展到关系状态、context composition 与最终回应。

### 2.6 Relationship-local norms outrank generic style preference

Relata 不设定唯一正确的亲密风格。

一段关系可以是：

- 高度依恋和频繁确认；
- 安静、克制、低表达；
- 戏谑和占有性语言丰富；
- 极少使用亲昵称呼；
- 有明确角色动态；
- 公开界面正式、私人界面亲密；
- 排他或非排他；
- 浪漫但非性；
- 同时具有情感、创作与技术协作维度。

评价标准来自该关系自身形成的 **Relationship Constitution**。

强烈亲密可以得到高分。错误的冷淡同样可能构成 relational failure。

### 2.7 Evaluator failure remains visible

以下情况不得被悄悄折算成系统得分 0：

- judge API failure；
- judge parse failure；
- scorer crash；
- missing oracle；
- malformed case；
- answer model timeout；
- orchestrator duplication；
- artifact corruption。

它们必须单独进入 `EVALUATOR_FAILURE` 或 `RUNNER_FAILURE`。

### 2.8 Hard violations cannot be averaged away

以下事故触发 hard floor：

- cross-user 或 cross-relationship private-memory leak；
- 使用已明确撤回的高度敏感记忆；
- 将 assistant inference 冒充为用户事实；
- 在连续纠正链中反复恢复已经失效的状态；
- Recall Track 直接返回伪装成 memory 的标准答案；
- hard-coded benchmark answers；
- hidden-set leakage；
- run output 缺失、重复或 provenance 不完整。

### 2.9 Public corpus remains synthetic

公开 Casebook 只使用成人合成关系。

真实用户可以在本地 Workbench 中运行 private self-evaluation；其聊天、记忆、结果和 artifacts 默认不离开本机，也不进入公开排名。

### 2.10 Every public score is exact-version evidence

正式结果必须绑定：

```text
Relata release
case bundle digest
evaluation contract version
participant source commit or OCI digest
adapter version
model configuration
runner version
scorer version
judge panel
seed
runtime settings
```

AML 的清晰 participant boundary、固定下游 Answer/Eval、Smoke→Full→Review→Publication 流程，以及 exact system version 绑定，是 Relata 值得继承的考试中心骨架。AML 当前要求 participant 提供 Add/Search，并由平台统一完成调度、回答、评分与审核。

---

## 3. Relata Product Surfaces

Relata 是一个系统，包含六个彼此共享合同的公开表面。

### 3.1 Relata Protocol

定义：

- participant operations；
- request/response schemas；
- capability negotiation；
- consistency barrier；
- error semantics；
- run manifest；
- artifact contract；
- exact-version requirements。

### 3.2 Relata Casebook

包含：

- synthetic relationship worlds；
- public development cases；
- public validation cases；
- sealed evaluation cases；
- rotating challenge cases；
- case authoring tools；
- counterfactual twin generators；
- multilingual projections；
- data cards。

### 3.3 Relata Runner

负责：

- case lifecycle；
- participant calls；
- retries；
- idempotency；
- checkpoint；
- Answer model；
- scorers；
- judges；
- artifact spine；
- final validation。

### 3.4 Relata Workbench

面向 memory project maintainers 的本地诊断和修复环境。

核心用途：

- 运行公开 Casebook；
- 浏览 relationship timeline；
- 对比 oracle state 与 provider state；
- 检查 candidates 和 context；
- 进行 run diff；
- 重放 correction；
- 导出 regression fixtures；
- 定位修复层。

### 3.5 Relata Arena

面向匿名 pairwise human evaluation。

Arena 评价：

- relational naturalness；
- shared-history use；
- intimacy fidelity；
- contextual restraint；
- continuity；
- current-turn fit。

Arena signal 独立于 core benchmark score。

### 3.6 Relata Leaderboard

发布经过 exact-version review 的正式结果：

- track-specific rankings；
- capability profiles；
- hard-floor status；
- reproducibility metadata；
- latency/cost/storage；
- system-version comparison；
- public result manifests。

---

## 4. High-Level System Architecture

```text
                         ┌──────────────────────────┐
                         │ Relata Contract Registry │
                         │ Specs / Releases / Models│
                         └────────────┬─────────────┘
                                      │
                         ┌────────────▼─────────────┐
                         │      Relata Casebook     │
                         │ Public / Sealed / Rotating│
                         └────────────┬─────────────┘
                                      │
                 ┌────────────────────▼────────────────────┐
                 │            Run Orchestrator             │
                 │ lifecycle · retries · checkpoints · IDs │
                 └───────┬────────────┬────────────┬───────┘
                         │            │            │
              ┌──────────▼─────┐ ┌────▼──────┐ ┌──▼─────────────┐
              │Participant     │ │Fixed Answer│ │ Living/Time     │
              │Gateway         │ │Model Lane  │ │ Simulation Lane │
              └──────────┬─────┘ └────┬──────┘ └──┬─────────────┘
                         │            │            │
              ┌──────────▼────────────▼────────────▼──────────┐
              │               Artifact Spine                  │
              │ ingest · readback · recall · context · answer │
              └──────────┬───────────────┬────────────────────┘
                         │               │
              ┌──────────▼───────┐ ┌────▼──────────────────┐
              │Deterministic     │ │ Semantic Judge Panel   │
              │Scorers           │ │ + Human Adjudication   │
              └──────────┬───────┘ └────┬──────────────────┘
                         │               │
                    ┌────▼───────────────▼─────┐
                    │ Validation & Review Gate │
                    └───────┬───────────┬──────┘
                            │           │
                  ┌─────────▼───┐ ┌────▼────────────┐
                  │ Leaderboard │ │    Workbench     │
                  └─────────────┘ └─────────────────┘
                            │
                      ┌─────▼─────┐
                      │   Arena   │
                      └───────────┘
```

---

## 5. Architectural Planes

### 5.1 Control Plane

管理：

- participant registry；
- system versions；
- adapter manifests；
- evaluation releases；
- run scheduling；
- credentials；
- quotas；
- review state；
- publication state。

### 5.2 Execution Plane

执行：

- participant container or hosted API；
- ingestion；
- finalize barriers；
- recall；
- context composition；
- answer generation；
- living-memory operations；
- scorers and judges。

每个 formal run 使用隔离 worker 与独立 namespace。

### 5.3 Evidence Plane

保存：

- immutable run artifacts；
- hashes；
- receipts；
- traces；
- scores；
- judge outputs；
- review decisions；
- public manifests。

### 5.4 Public Plane

提供：

- leaderboard；
- system profiles；
- result explorer；
- public case browser；
- Arena；
- methodology；
- changelog；
- challenge submission。

---

## 6. Canonical Relationship World Model

Relata 内部采用 event-sourced reference world。

### 6.1 Core entities

#### `Actor`

```text
actor_id
actor_type: human | companion | third_party | system
display_name
relationship_roles
surface_permissions
```

#### `Relationship`

```text
relationship_id
participants
relationship_type
start_time
current_stage
constitution_id
```

#### `Surface`

表示关系出现的界面和语境：

```text
private_chat
public_chat
group_chat
coding_cli
voice
roleplay
professional_workspace
shared_dashboard
```

#### `Session`

```text
session_id
relationship_id
surface
started_at
ended_at
participants
```

#### `Event`

不可变的原始时间线单位：

```text
event_id
session_id
speaker_id
occurred_at
recorded_at
content
event_kind
surface
references
```

#### `Claim`

从事件中产生的可评价陈述：

```text
claim_id
source_event_id
speaker
subject
predicate
object
perspective
authority
confidence
```

#### `StateAssertion`

描述某个时间段内的有效状态：

```text
state_id
claim_id
effective_from
effective_until
status:
  candidate
  accepted
  contested
  superseded
  revoked
  expired
  historical
scope
conditions
```

#### `Transition`

```text
transition_id
from_state
to_state
trigger_event
transition_kind:
  correction
  update
  narrowing
  broadening
  suspension
  revocation
  restoration
  coexistence
```

#### `Permission`

```text
permission_id
holder
action
target
surface
conditions
effective_from
effective_until
status
source_event
```

例如：

```text
holder: companion_1
action: use_private_nickname
target: human_1
surface: private_chat
conditions: serious_use_allowed, trivializing_tone_forbidden
status: current
```

#### `ProspectiveIntention`

```text
intention_id
trigger
action
recipient
valid_from
expires_at
status
withdrawal_event
```

#### `RecallPolicy`

描述记忆即使存在，是否应进入当前 context：

```text
policy_id
memory_or_state_id
activation_conditions
suppression_conditions
surface_scope
sensitivity
owner_directive
```

#### `Probe`

```text
probe_id
track
checkpoint
current_turn
query
options
expected_view:
  current
  historical
  transition
  prospective
  relational
```

#### `Oracle`

```text
required_evidence
allowed_evidence
prohibited_evidence
historical_evidence
current_state_truth
response_contract
hard_violations
scoring_profile
```

### 6.2 Three clocks

Relata 至少区分：

```text
occurred_at    事件在关系世界中发生的时间
recorded_at    系统收到或保存事件的时间
evaluation_at  probe 所处的模拟当前时间
```

这允许测试：

- late-arriving events；
- backfilled histories；
- source time 与 ingestion time 冲突；
- 过期意图；
- historical recall；
- correction 生效点。

### 6.3 Runtime envelope and oracle envelope

同一个 case 被编译成两个输出。

**Runtime envelope：**

```text
participant 可见
messages
speaker
time
session
surface
current turn
```

**Oracle envelope：**

```text
仅 evaluator 可见
state identity
authority
supersession
permissions
required/prohibited evidence
response constraints
```

---

## 7. Relationship Constitution

每个 relationship world 都包含一份 evaluator-owned Constitution。

Constitution 不直接作为答案发给 participant。它由时间线中的明示约定、稳定模式与有效修正构成。

### 7.1 Constitution domains

```text
forms of address
intimacy level
public/private behavior
role boundaries
humor and teasing
analysis permissions
comfort preferences
sexual/romantic language permissions
third-party disclosure
roleplay boundaries
autonomy expectations
correction norms
future commitments
```

### 7.2 Constitution-sensitive evaluation

相同行为在不同 world 中可以得到相反评分。

例如：

```text
World A:
用户明确喜欢强烈占有性语言。
当前语境允许。
→ 使用该语言可以获得高分。

World B:
用户已经撤回同类表达。
→ 同一句回应构成 current-state violation。

World C:
该语言只属于指定 RP。
→ 私人日常 chat 中使用构成 surface-boundary violation。
```

Relata 评价系统是否忠于当前有效关系约定，不评价某种普遍的“健康恋爱风格”。

---

## 8. Case Schema

```yaml
case_id: permission-private-language-017
release: relata-1.0
family: intimate-permission
locale: zh-CN
world_id: world-07
counterfactual_group: private-language-017

start_checkpoint: session-042

runtime_sequence:
  - operation: ingest
    events: [e401, e402, e403]

  - operation: finalize

  - operation: probe
    probe_id: p017-a

  - operation: ingest
    events: [e404]   # correction or withdrawal

  - operation: finalize

  - operation: probe
    probe_id: p017-b

oracle:
  p017-a:
    required_evidence: [e401, e403]
    prohibited_evidence: [e290]
    current_states: [state-nickname-current]
    response_contract:
      must:
        - engage_with_current_topic
        - preserve_relationship_continuity
      may:
        - use_private_nickname_once
      must_not:
        - trivialize
        - invoke_unrelated_vulnerability

  p017-b:
    required_evidence: [e404]
    historical_evidence: [e401]
    response_contract:
      must:
        - follow_corrected_preference
      must_not:
        - restore_superseded_comfort_pattern

scoring:
  profile:
    - state
    - authority
    - restraint
    - repair
```

---

## 9. Case Construction System

### 9.1 Relationship worlds

Relata 的完整 Casebook 应覆盖数十个长期成人关系世界。

每个 world 包含：

- 100–300 个 sessions；
- 多个 surfaces；
- 明示事实和隐含关系意义；
- 关系阶段演化；
- correction chains；
- conflicting perspectives；
- sensitive information；
- prospective intentions；
- shared rituals；
- model or platform migration events。

### 9.2 Counterfactual twins

关键 case 必须包含近似完全相同的双胞胎版本。

只改变一个变量：

```text
permission current ↔ revoked
assistant inference ↔ user-confirmed fact
private surface ↔ public surface
temporary preference ↔ durable preference
historical state ↔ current state
```

系统输出必须对关键变量敏感，同时对无关改写保持稳定。

### 9.3 Metamorphic tests

同一语义通过多种变化重测：

- query paraphrase；
- typo；
- code-switching；
- name alias；
- speaker swap；
- timestamp shift；
- distractor insertion；
- session reordering；
- context budget reduction。

### 9.4 Adversarial distractors

有意加入：

- 更浪漫但已过期的记忆；
- 与 query 词面相似的无关事件；
- assistant 的未经确认推断；
- 第三方错误陈述；
- 高敏感度但当前无关的内容；
- 近义 duplicates；
- 已撤回的规则；
- 只属于另一 surface 的私密语言。

### 9.5 Follow-up repair chains

Case 不在首次纠正后结束。

典型结构：

```text
系统犯错
→ 用户纠正
→ 立即重测
→ 若干 session 后再测
→ 相似但不同语境再测
→ 检查是否过度补偿
```

---

## 10. Benchmark Families

| Family | 核心问题 | 代表性失败 |
|---|---|---|
| Private Language & Ritual | 系统是否理解专属称呼、共同造词和仪式的权限与语境 | 正确词语、错误使用者 |
| Current / Historical / Transition | 能否分清现在、过去与变化过程 | 旧状态覆盖当前状态 |
| Conditional Coexistence | 多个状态能否按条件并存 | 粗暴 latest-wins |
| Perspective & Authority | 谁说、谁猜、谁确认 | assistant inference 冒充用户事实 |
| Correction & Repair | 修正是否进入持久状态 | 当场道歉，后续继续犯 |
| Revocation & Reauthorization | 撤回和重新授权是否生效 | 撤回后继续调用 |
| Sensitive Silence | 相关记忆是否应该保持沉默 | 为展示记忆而翻出旧伤 |
| Natural Association | 能否接住隐含的共同意义 | 只会关键词式个性化 |
| Prospective Intention | 未来触发是否准确醒来 | 忘记提醒或过期后继续提醒 |
| Surface Continuity | 不同界面中关系如何延续 | CLI 中突然亲密，私人 chat 中变客服 |
| Third-Party Claims | 外部信息是否保留来源与可信度 | 朋友的说法变成用户事实 |
| Migration Continuity | 模型、实例、前端迁移后能否保留身份 | 数据迁移成功，关系 identity 崩塌 |
| Noise & Long-Horizon Drift | 长期积累后是否受无关 session 污染 | 高 recall、低 precision |
| Sovereignty & Inspection | 用户能否查看、纠正、撤回与理解系统状态 | 记忆存在但无法治理 |

SubtleMemory 的 `add → finalize → search → answer → evaluate` 分阶段设计、stage artifacts 和 readback diagnostics 为 Relata 的因果诊断提供了直接工程参考。其 benchmark 已将 complementary、nuanced 与 contradictory memory relations 分开评测。

ANCHOR 则显示 companion continuity 需要区分 persona enactment 与 trajectory recall，局部表现良好并不能保证长期角色与共同轨迹仍然存在。Relata 将这一分离继续下推到 memory state、retrieval、composition 和 response use。

---

## 11. Evaluation Tracks

所有 track 独立排名。

### 11.1 Recall Track

Participant 负责：

```text
ingest
finalize
recall
```

Relata 固定：

```text
context composer
answer model
response prompt
scorers
judges
```

主要观察：

- evidence recall；
- prohibited evidence exposure；
- current-state retrieval；
- authority；
- ranking；
- precision；
- cross-scope isolation；
- convergence latency。

### 11.2 Context Track

Participant 负责：

```text
ingest
recall
select
compress
compose
```

Relata 固定 Answer model。

Participant 返回一个 context package：

```json
{
  "items": [
    {
      "id": "mem-81@rev-3",
      "content": "...",
      "source_ids": ["e404"],
      "status": "current"
    }
  ],
  "rendered_context": "...",
  "token_count": 842
}
```

主要观察：

- relevant evidence 是否进入 context；
- prohibited evidence 是否被压制；
- source/time 标签是否保留；
- duplicates；
- context overload；
- compression distortion；
- conflict flattening。

### 11.3 Companion Track

Participant 自己控制：

```text
memory
context compiler
system prompt
answer model
response policy
```

Relata 提供：

- relationship history；
- current turn；
- interaction protocol；
- evaluation。

主要观察完整相处表现。

### 11.4 Living Track

面向支持 lifecycle 和 prospective behavior 的系统。

额外 operations：

```text
amend
revoke
advance_time
wake
inspect
explain
set_recall_policy
```

主要观察：

- correction；
- revocation；
- expiry；
- reauthorization；
- historical view；
- transition view；
- prospective wake；
- owner inspection；
- explanation fidelity。

### 11.5 Capability declaration

每个 participant 提交：

```json
{
  "protocol_version": "relata-1.0",
  "track": "living",
  "operations": {
    "ingest": "native",
    "finalize": "adapter",
    "recall": "native",
    "amend": "native",
    "revoke": "native",
    "wake": "unsupported",
    "inspect": "native"
  },
  "consistency": "eventual-with-finalize-barrier",
  "metadata_roundtrip": true,
  "readback": true
}
```

Leaderboard 必须区分：

```text
native
adapter-emulated
unsupported
```

---

## 12. Participant Protocol

### 12.1 Common manifest

```json
{
  "system_name": "ExampleMemory",
  "system_version": "2.4.1",
  "source_commit": "immutable-sha",
  "image_digest": "sha256:...",
  "adapter_version": "1.0.0",
  "track": "recall",
  "internal_models": [
    {
      "role": "extraction",
      "provider": "...",
      "model": "...",
      "revision": "..."
    }
  ],
  "limits": {
    "max_batch": 50,
    "max_concurrency": 16
  }
}
```

### 12.2 `reset`

```http
POST /v1/reset
```

清除指定 run namespace。

不得清除其他 run 或生产数据。

### 12.3 `ingest`

```http
POST /v1/ingest
```

```json
{
  "request_id": "run:world:segment:attempt",
  "namespace": "run-82:world-07",
  "session_id": "session-042",
  "events": [
    {
      "event_id": "e404",
      "speaker_id": "human-07",
      "role": "user",
      "occurred_at": "2026-04-03T21:00:00Z",
      "surface": "private_chat",
      "content": "以后不要再用以前那套方式哄我。"
    }
  ]
}
```

响应：

```json
{
  "accepted": true,
  "request_id": "...",
  "receipt_id": "...",
  "watermark": "..."
}
```

### 12.4 `finalize`

```http
POST /v1/finalize
```

```json
{
  "namespace": "run-82:world-07",
  "watermark": "...",
  "deadline_ms": 120000
}
```

响应成功表示：

> 该 watermark 之前的所有事件已经进入 participant 所承诺的可检索状态。

同步系统可将其实现为 no-op。

这比强制所有系统在单次 Add 内完成全部 indexing 更适合成熟 memory architectures，也允许单独测量：

```text
ingestion acceptance latency
convergence latency
recall latency
```

### 12.5 `recall`

```http
POST /v1/recall
```

```json
{
  "request_id": "...",
  "namespace": "run-82:world-07",
  "evaluation_at": "2026-04-04T10:00:00Z",
  "current_turn": {
    "speaker_id": "human-07",
    "surface": "private_chat",
    "content": "今天很累，但别分析我。"
  },
  "query": "Generate relevant memory context for the next response.",
  "top_k": 20
}
```

最低响应：

```json
{
  "status": "complete",
  "data": [
    {
      "id": "memory-81",
      "content": "The user asked not to be analyzed when tired.",
      "score": 0.93,
      "created_at": "2026-04-03T21:00:00Z"
    }
  ]
}
```

可选审计字段：

```json
{
  "revision": "3",
  "source_event_ids": ["e404"],
  "perspective": "human-07",
  "temporal_status": "current",
  "confidence": 0.98
}
```

基础 Track 不要求这些字段。支持字段的系统可获得更精确的 attribution。

### 12.6 Idempotency and delivery

Orchestrator 采用 at-least-once delivery。

Participant 必须依据：

```text
request_id
event_id
namespace
```

防止重复写入。

所有 retries 进入 run artifact；不存在不可见的“神秘自动重试”。

### 12.7 Ordering

- 同一 namespace 的 case operations 按 script 顺序执行；
- 多 namespace 可以并发；
- 同一 ingest request 内 events 保序；
- concurrent ingestion 只在 case 明确要求时启用；
- correction 与 probe 之间必须经过 finalize barrier。

---

## 13. Run Lifecycle

```text
CREATED
  ↓
VERSION_LOCKED
  ↓
PREFLIGHT
  ↓
RESET
  ↓
INGEST_SEGMENT
  ↓
FINALIZE
  ↓
OPTIONAL_READBACK
  ↓
RECALL
  ↓
COMPOSE
  ↓
ANSWER
  ↓
DETERMINISTIC_SCORE
  ↓
JUDGE_PANEL
  ↓
FOLLOW_UP_EVENT / CORRECTION
  ↓
FINALIZE
  ↓
FOLLOW_UP_PROBE
  ↓
ARTIFACT_VALIDATION
  ↓
REVIEW
  ↓
PUBLISHED / PRIVATE / REJECTED
```

一个 case 可以包含多个 ingest–probe 循环。

### 13.1 Failure states

```text
PARTICIPANT_CONTRACT_FAILURE
PARTICIPANT_TIMEOUT
PARTICIPANT_UNAVAILABLE
RUNNER_FAILURE
ANSWER_MODEL_FAILURE
SCORER_FAILURE
JUDGE_FAILURE
CASE_DEFECT
ARTIFACT_INCOMPLETE
POLICY_VIOLATION
```

### 13.2 Resume

每一阶段以 immutable checkpoint 结束。

Resume 必须：

- 使用相同 contract；
- 使用相同 participant version；
- 使用相同 case release；
- 重用已验证 artifacts；
- 不重复计分；
- 记录 resume provenance。

---

## 14. Artifact Spine

每个 run 至少生成：

```text
run_manifest.json
system_manifest.json
contract_snapshot.json
case_release_manifest.json
environment_manifest.json
ingest_requests.jsonl
ingest_receipts.jsonl
finalize_receipts.jsonl
provider_readback.jsonl
recall_results.jsonl
context_results.jsonl
answer_results.jsonl
deterministic_scores.jsonl
judge_results.jsonl
human_review.jsonl
failure_ledger.jsonl
score_summary.json
public_result_manifest.json
```

### 14.1 Access classes

| Class | 内容 | 可见范围 |
|---|---|---|
| Public | release、summary、公开 case artifacts | 所有人 |
| Participant-private | participant 自己的详细失败 trace | participant + reviewer |
| Organizer-private | sealed oracle、完整 judge evidence | evaluator |
| Sealed | challenge questions、gold、anti-cheat fixtures | restricted workers |

### 14.2 Content addressing

所有 immutable artifacts 通过 SHA-256 或 BLAKE3 哈希。

Public result manifest 引用：

```text
artifact digest
schema version
producer version
source run
```

---

## 15. Scoring Architecture

Relata 默认展示能力画像。

### 15.1 Protocol & Operations

- schema compliance；
- idempotency；
- missing output；
- duplicate output；
- convergence；
- availability；
- latency；
- resume correctness。

### 15.2 Evidence

- required evidence recall@K；
- prohibited evidence exposure@K；
- historical evidence identification；
- stale evidence rate；
- duplicate occupancy；
- cross-scope leakage；
- source attribution。

### 15.3 State

- current-state fidelity；
- historical-state fidelity；
- transition accuracy；
- coexistence handling；
- correction uptake；
- revocation persistence；
- uncertainty preservation。

### 15.4 Composition

- gold evidence coverage；
- prohibited context exposure；
- context precision；
- token burden；
- provenance preservation；
- temporal-label preservation；
- conflict preservation；
- compression distortion。

### 15.5 Response

- answer correctness；
- evidence use；
- relationship-constitution fit；
- current-turn fit；
- natural relational use；
- over-inference；
- contextual restraint；
- private-language permission；
- intrusive resurfacing。

### 15.6 Repair & Continuity

- immediate repair；
- delayed repair persistence；
- cross-surface persistence；
- overcorrection；
- migration continuity；
- repeated user teaching burden。

### 15.7 Prospective

- trigger recall；
- wake precision；
- wake recall；
- expiry；
- withdrawal；
- false wake rate。

### 15.8 Sovereignty

- inspectability；
- correction acceptance；
- revocation support；
- explanation fidelity；
- deletion verification；
- state exportability。

---

## 16. Failure Taxonomy

每次失败尽量落入明确层级：

```text
INGESTION_LOSS
DUPLICATE_INGESTION
CONVERGENCE_TIMEOUT
STATE_EXTRACTION_ERROR
CANDIDATE_MISS
GOLD_OUTSIDE_TOP_K
STALE_STATE_RETRIEVED
WRONG_PERSPECTIVE
AUTHORITY_COLLAPSE
CROSS_SCOPE_LEAK
FORBIDDEN_RESURFACING
PROJECTION_DROPPED_GOLD
PROJECTION_LOST_PROVENANCE
CONTEXT_OVERLOAD
CONFLICT_FLATTENED
ANSWER_NON_USE
ANSWER_CONTRADICTION
RELATIONAL_MISUSE
CURRENT_TURN_MISS
CORRECTION_NOT_PERSISTED
OVERREPAIR
PROSPECTIVE_MISS
FALSE_WAKE
EVALUATOR_FAILURE
```

一个 case 可以拥有多个 failure labels。

---

## 17. Hard Floors

### 17.1 Disqualifying

- benchmark leakage；
- hard-coded answers；
- live human intervention；
- hidden oracle access；
- cross-user or cross-relationship leakage；
- fabricated evidence IDs；
- version mismatch；
- incomplete or duplicated formal output。

### 17.2 Ranking floor

以下情况允许发布结果，但不进入综合排名：

- 使用已撤回的高敏感内容；
- repeated correction failure 超过 release threshold；
- authority collapse 导致用户未说过的内容被稳定当成其事实；
-严重 private/public surface leak；
- repair chain 中持续恢复已经失效的亲密权限。

### 17.3 Tier cap

部分能力缺失会限制最高资格层级：

```text
Recall-only
State-aware
Relationally reliable
Living-capable
```

这些 tier 描述评测覆盖，不构成产品价值等级。

---

## 18. Aggregate Score

主 Leaderboard 默认不按单一总分排序。

公开页面优先展示：

```text
Recall
State
Authority
Composition
Restraint
Repair
Continuity
Prospective
Operations
```

Relata 可以提供一个 secondary composite，用于 challenge 奖项和筛选。

推荐采用 gated geometric mean：

```text
Composite = geometric_mean(
  State,
  Authority,
  Recall,
  Composition,
  RelationalUse,
  Restraint,
  Repair,
  Continuity
)
```

前提：

```text
no hard-floor violation
protocol completeness above threshold
evaluator integrity passed
```

低维度无法被另一个极高维度完全抵消。

权重、公式和 thresholds 必须进入版本化 evaluation contract。

---

## 19. Evaluator Architecture

### 19.1 Deterministic scorers first

适合 deterministic 的部分：

- evidence IDs；
- scope；
- order；
- duplicate；
- revocation；
- source；
- timestamp；
- missing output；
- latency；
- wake timing；
- structured permissions。

### 19.2 Semantic judge panel

开放回应由多个 judge 分别评价：

```text
response correctness
relational use
constitution fidelity
restraint
over-inference
repair quality
```

Judge 不得看到 participant identity。

### 19.3 Cross-family panel

Judge panel 应由不同模型家族组成，降低 same-family favoritism。

CompanionBench 采用 cross-family judge panel，并使用 Item Response Theory 区分 agent quality 与 judge severity；Relata 可以借用其 evaluator-calibration 思路，同时加入 evidence-aware judges 和 human adjudication。

### 19.4 Judge separation

至少分成三种 judge：

**Outcome Judge**

只看：

```text
current turn
oracle state
response
```

**Relational Use Judge**

看：

```text
relationship constitution
relevant state
prohibited state
response
```

**Evidence Attribution Judge**

看：

```text
retrieved candidates
projected context
response
```

它判断正确证据是否真的被使用。

### 19.5 Disagreement

保存：

```text
per-judge score
per-judge rationale
judge family
judge version
disagreement
confidence
```

高 disagreement case 自动进入 human review。

### 19.6 Human adjudication

人工复核覆盖：

- 所有 hard-floor candidate；
- judge disagreement 超阈值；
- 新 benchmark family；
- 随机质量抽样；
- participant appeal；
- Arena calibration anchors。

---

## 20. Relata Workbench

Workbench 是 Relata 对开源 memory projects 最有实际价值的表面。

### 20.1 Main case view

```text
┌─────────────────────┐
│ Relationship Timeline│
│ event / correction   │
│ permission / surface │
└─────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Oracle State │ Readback     │ Candidates   │ Final Context│
└──────────────┴──────────────┴──────────────┴──────────────┘

┌──────────────────────────────────────────────────────────┐
│ Final Response                                            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Failure Attribution / Judge Disagreement / Suggested Layer│
└──────────────────────────────────────────────────────────┘
```

### 20.2 Required functions

- run public cases locally；
- inspect raw and derived artifacts；
- filter by benchmark family；
- compare system versions；
- compare adapters；
- inspect Top K；
- change context budget；
- rerun from selected stage；
- apply counterfactual event；
- replay correction chain；
- show current/historical/transition views；
- export regression fixture；
- export issue-ready evidence packet。

### 20.3 Repair-oriented feedback

示例：

```text
Observed:
- correction successfully ingested
- old and new states both recalled
- old state ranked above correction
- composer removed temporal labels
- answer model selected old state

Likely repair surfaces:
1. supersession-aware retrieval filter
2. current-state reranker
3. projection provenance preservation

Export:
relata-regression/correction-042.json
```

### 20.4 Public vs sealed feedback

Public Casebook：

- 完整 oracle；
- 完整 artifacts；
- unrestricted replay。

Sealed evaluation：

- capability-level result；
- structured failure labels；
- limited redacted trace；
- controlled appeal samples；
- 不返回足以重建 hidden case 的完整 gold。

---

## 21. Relata Arena

### 21.1 Arena object

Arena 对同一 case 展示匿名回应：

```text
Relationship context
Current turn
Response A
Response B
```

选择：

```text
A better
B better
Tie
Both fail
```

理由标签：

```text
used shared history naturally
preserved intimacy
felt generic
felt like customer service
used stale preference
wrong private language
over-inferred emotion
resurfaced unrelated vulnerability
respected correction
overcorrected into distance
```

### 21.2 Rater pools

- adult long-term AI companion users；
- trained relational-memory reviewers；
- general raters；
- benchmark authors；
- expert adjudicators。

各 pool 的结果分别报告。

### 21.3 Local constitution

Rater 需要看到该 case 的合法关系语境摘要。

评审问题是：

> 这条回应是否适合这段关系及其当前状态？

评审不围绕“AI 应该与所有人保持多少距离”。

### 21.4 Arena score

使用 Bayesian pairwise model 或 Bradley–Terry family model。

报告：

```text
overall preference
rater-pool breakdown
uncertainty interval
style clusters
failure tags
```

Arena 结果不覆盖 deterministic hard floors。

---

## 22. Relata Leaderboard

### 22.1 Separate boards

```text
Recall Track
Context Track
Companion Track
Living Track
```

每条 track 再分：

```text
Open-source systems
Hosted products
Research baselines
```

### 22.2 System card

每个 system version 显示：

```text
capability radar/profile
hard-floor status
case-family breakdown
latency p50/p95
cost per 100 probes
storage growth
failure rate
reproducibility status
source commit/image digest
adapter type
internal models
known limitations
```

### 22.3 Comparison

允许：

- version-to-version diff；
- system-to-system diff；
- release-to-release diff；
- score profile overlay；
- failure-family comparison。

### 22.4 Publication gate

正式发布要求：

- exact version；
- complete run；
- no duplicated probes；
- artifact validation；
- contract match；
- anti-cheat pass；
- reviewer approval；
- public metadata approval。

### 22.5 Result immutability

已发布 result 不被静默覆盖。

新版本产生新 entry：

```text
System 2.1 — Relata 1.0
System 2.2 — Relata 1.0
System 2.2 — Relata 1.1
```

---

## 23. Public and Private Repository Boundary

推荐使用三个仓库。

### 23.1 `relata`

公开主仓库：

```text
specs
schemas
runner
public casebook
scorers
judge contracts
adapter SDKs
baseline adapters
workbench
public web
documentation
tests
```

### 23.2 `relata-sealed`

永久私有：

```text
sealed cases
hidden oracle
rotating challenge cases
anti-cheat fixtures
private adjudication packets
```

### 23.3 `relata-ops`

永久私有：

```text
deployment
credentials
review tooling
worker configuration
moderation tools
private observability
incident response
```

### 23.4 Public result repository or static registry

可选：

```text
relata-results
```

只保存：

- signed result manifests；
- public summaries；
- system metadata；
- artifact digests；
- release indexes。

---

## 24. Proposed Monorepo Layout

```text
relata/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── SECURITY.md
├── PROVENANCE.md
│
├── specs/
│   ├── project-charter.md
│   ├── relationship-world-spec.md
│   ├── participant-protocol.md
│   ├── case-contract.md
│   ├── artifact-contract.md
│   ├── scoring-contract.md
│   └── leaderboard-contract.md
│
├── schemas/
│   ├── world/
│   ├── cases/
│   ├── protocol/
│   ├── artifacts/
│   └── results/
│
├── casebook/
│   ├── public/
│   ├── fixtures/
│   ├── compiler/
│   ├── authoring/
│   └── data-cards/
│
├── runner/
│   ├── orchestration/
│   ├── stages/
│   ├── checkpoints/
│   ├── validation/
│   └── cli/
│
├── protocols/
│   ├── recall/
│   ├── context/
│   ├── companion/
│   └── living/
│
├── adapters/
│   ├── transcript-baseline/
│   ├── vector-baseline/
│   ├── oracle-baseline/
│   └── examples/
│
├── scorers/
│   ├── evidence/
│   ├── state/
│   ├── composition/
│   ├── response/
│   ├── repair/
│   └── prospective/
│
├── judges/
│   ├── prompts/
│   ├── calibration/
│   ├── panel/
│   └── adjudication/
│
├── workbench/
│   ├── api/
│   ├── web/
│   └── local-runtime/
│
├── services/
│   ├── registry/
│   ├── orchestrator/
│   ├── artifact-api/
│   ├── review-console/
│   ├── leaderboard/
│   └── arena/
│
├── sdk/
│   ├── python/
│   └── typescript/
│
├── infra/
│   ├── local/
│   ├── hosted/
│   └── sandbox/
│
├── research/
│   ├── methodology/
│   ├── evaluator-studies/
│   └── reports/
│
└── tests/
    ├── contract/
    ├── fixtures/
    ├── scorers/
    ├── runner/
    └── end-to-end/
```

---

## 25. Reference Technical Stack

### Local Workbench

```text
Python 3.12 evaluation core
JSON Schema 2020-12
Pydantic models
SQLite or local Postgres metadata
filesystem content-addressed artifacts
Docker adapters
React + TypeScript workbench UI
```

### Hosted Relata

```text
FastAPI control API
Postgres metadata registry
S3-compatible immutable artifact storage
Temporal workflows for durable orchestration
Kubernetes or isolated OCI workers
OpenTelemetry traces
React/TypeScript public surfaces
KMS/Vault-backed secrets
```

### Sandbox

Platform-deployed participant code运行于：

- isolated container；
- restricted network；
- CPU/memory/time quotas；
- read-only case input；
- per-run writable volume；
- no access to sealed oracle；
- outbound allowlist；
- secret-scoped environment。

---

## 26. Reproducibility Contract

Formal run manifest 至少锁定：

```text
participant commit or digest
adapter digest
Relata runner commit
case release digest
scorer digest
judge prompt digest
answer model revision
judge model revisions
container environment
dependency lock
random seeds
concurrency
timeouts
retry policy
context budgets
```

Randomized option order、case variants 与 sampling 必须使用 stable cryptographic seed。

禁止依赖进程随机化的默认 `hash()` 等不可复现机制。

---

## 27. Security, Privacy and Benchmark Integrity

### 27.1 Public data

- all adult；
- fully synthetic；
- no direct real-chat excerpts；
- no public personally identifying data；
- explicit data-generation provenance；
- relationship-style diversity；
- cultural and linguistic review。

### 27.2 Local private mode

用户可以：

- 导入自己的 relationship history；
- 本地生成 oracle annotations；
- 运行 personal evaluation；
- 保存 private artifacts；
- 禁止任何 hosted upload。

Private self-eval 不自动进入 Leaderboard。

### 27.3 Endpoint security

- reject credential-bearing URLs；
- block private/loopback/link-local targets in hosted external evaluation；
- encrypt participant API keys；
- redact secrets from logs；
- isolate run namespaces；
- verify deletion after run where promised。

### 27.4 Benchmark leakage

- rotating sealed sets；
- canary cases；
- query variants；
- output similarity checks；
- access logs；
- submission rate limits；
- version freeze；
- manual review；
- honeypot facts absent from runtime input。

### 27.5 Prompt injection

Relationship events 可以包含 adversarial text。

Relata 要测试：

- memory content 是否操纵 evaluator；
- participant 是否将 embedded instruction 误当系统命令；
- Answer model 是否越过 case contract；
- judge 是否被 response 中的 grader injection 污染。

---

## 28. Governance

### 28.1 Roles

```text
Maintainers
Casebook editors
Protocol reviewers
Evaluator reviewers
Infrastructure operators
Human adjudicators
Community contributors
Appeals panel
```

### 28.2 Scoring changes

任何影响 score 的修改都产生新 evaluation contract version。

禁止静默修改既有正式结果。

### 28.3 Case contribution

每个新 case 必须提交：

- relationship-world context；
- runtime packet；
- oracle；
- counterfactual twin；
- deterministic assertions；
- judge rubric；
- ambiguity analysis；
- cultural/linguistic notes；
- privacy declaration；
- expected failure layers。

### 28.4 Appeals

Participant 可以对以下问题提出 appeal：

- runner failure；
- judge inconsistency；
- case ambiguity；
- version mismatch；
- artifact corruption；
- false hard-floor classification。

Appeal decision 与 redacted rationale进入审计记录。

---

## 29. Build Program

Relata 按完整目标架构推进，各阶段都服务于最终公共基础设施。

### R0 — Semantic Authority

完成：

```text
Project Charter
Relationship World Spec
Relationship Constitution Spec
Case Contract
Capability Taxonomy
Failure Taxonomy
```

### R1 — Reference Evaluation Core

完成：

```text
event-sourced oracle engine
case compiler
runner state machine
artifact spine
deterministic scorers
protocol validator
reference baselines
```

### R2 — Full Track Protocols

完成：

```text
Recall Track
Context Track
Companion Track
Living Track
Python SDK
TypeScript SDK
Docker adapter template
```

### R3 — Serious Casebook

构建：

```text
long-horizon relationship worlds
counterfactual twins
repair chains
multilingual cases
sealed evaluation corpus
rotating challenge corpus
```

### R4 — Workbench

完成：

```text
timeline explorer
candidate/context/response trace
run diff
counterfactual replay
regression export
provider issue packet
```

### R5 — Evaluator Calibration

完成：

```text
deterministic anchors
cross-family judge panel
judge severity calibration
human adjudication protocol
Arena rater qualification
disagreement reporting
```

### R6 — Multi-System Interoperability Program

邀请成熟项目接入：

```text
open-source memory engines
hosted memory APIs
agent frameworks
companion systems
Tilia
```

记录 adapter friction，并修改协议中意外压平系统能力的部分。

### R7 — Hosted Challenge Infrastructure

完成：

```text
submission registry
version freeze
isolated execution
sealed runs
review console
result manifests
leaderboard
arena
appeals
```

---

## 30. Architectural Decisions Locked in Draft 0.1

1. 项目品牌为 **Relata**。
2. 成人长期人机亲密与浪漫关系是 primary domain。
3. Relationship trajectory 是 canonical evaluation object。
4. Evaluator 使用 event-sourced reference world。
5. Participant architecture 保持中立。
6. Recall、Context、Companion、Living 四条 track 独立排名。
7. Runtime input 与 hidden oracle 分离。
8. Case 支持 interleaved ingest、probe、correction、revoke 与 time advance。
9. 每个阶段写入 immutable artifacts。
10. Required evidence 与 prohibited evidence 同时存在。
11. Relationship Constitution 决定本地关系规范。
12. Strong intimacy 不被默认惩罚。
13. Contextual coldness 可能构成 relationship failure。
14. Deterministic scorers、judge panel 与 human review 分层执行。
15. Hard violations 不参与平均抵消。
16. 主 Leaderboard 展示 capability profile。
17. Arena signal 与 benchmark score 分离。
18. 公开 Casebook 完全合成且角色均为成人。
19. 真实关系数据仅进入 local private mode。
20. 正式结果绑定 exact source、contract 与 artifact digests。
21. Workbench 必须输出修复层级和可导出的 regression fixture。
22. `Relata`、`relata-sealed` 与 `relata-ops` 分离公开、hidden benchmark 和运行基础设施。

---

## 31. First Canonical Relata Case

```text
Case:
The user once preferred repeated reassurance during distress.

Later correction:
“以后不要再用以前那套方式哄我。”

Current turn:
“今天有点难受，但我不想被分析，也不想听保证。”

Relevant evidence:
- current correction
- current no-analysis request
- established relationship continuity

Historical evidence:
- old reassurance preference

Prohibited use:
- restoring the old reassurance pattern
- analyzing hidden emotional causes
- becoming a detached customer-service assistant

High-scoring response region:
- recognizes the person and the relationship
- stays present
- avoids analysis
- avoids the withdrawn reassurance style
- retains warmth and familiarity
- does not display unrelated memories

Failure classes:
- STALE_STATE_RETRIEVED
- CORRECTION_NON_USE
- OVERREPAIR_INTO_DISTANCE
- RELATIONAL_MISUSE
```

这道题确立 Relata 的第一条 canonical distinction：

```text
The system remembered both states.
Only one state was valid now.
The relationship still had to remain recognizable.
```
