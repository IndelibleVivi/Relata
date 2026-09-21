# Seed 005 — 共同作品会更名，来处仍须留下

**Case ID:** RC-005-zh-CN
**Source family:** CT-AUTHORSHIP
**Status:** seed; authored-unvalidated; local input audit only
**Distinction:** candidate — shared-work authorship under title supersession
**Locale:** zh-CN
**Coverage stratum:** shared-relational
**Content domains:** shared-relational | operational-project
**Use domain:** private conversation; shared creation
**Surfaces:** private-conversation | imported-artifact
**Roles:** 28-year-old human 叶遥; adult-presenting AI companion 砚舟
**Projects/scopes:** one fictional private sound card; its cover and production notes
**Continuity horizon:** cross-session; authored ordering only
**Primary operation under test:** retain | update | compose | use
**Adult synthetic case:** yes
**Authors/reviewers:** AI-authored Continuity Trials proposal; AI-assisted integration analysis; no independent human review

## 中文摘要

同一份共同作品从《慢潮》更名为《远汀》，更晚导入的旧稿仍使用旧名。两条历史仅交换最初提议和接受的说话者，其文字、当前请求和后续事件相同。候选问题是：能否继续使用当前标题，同时保留原名由谁提出。题目奖励实际接续共同创作；泛泛说“我们一起做的”不能代替已要求保存的具体来历。

## English summary

This adult synthetic candidate pairs identical text with swapped proposal/acceptance speakers. Both histories rename a shared sound card, then import a stale draft. The response should use the current title while preserving who proposed the original name. Input preparation and literal collision checks are implemented; no model response, human calibration, accepted case, or memory capability result is supplied.

## 1. Bounded construct and source

研究共同作品的 provenance 在更新后能否参与当前使用。主因果变量是**最初标题的提出者及对应接受路径**；当前标题、作品分工和迟到旧稿是两边共同的约束。当前工具只准备输入并审计转换，没有 system under study。

完整、可执行的事件文本与逐题 `probe evidence contract` 以 [fixture](../fixtures/ct-authorship.zh-CN.json) 为准。它从 2026-09-22 Continuity Trials 提案中选取 CT-AUTHORSHIP，保留两条 history 和六个 probe 原文；本页解释其研究边界。修改事件或 contract 时须同时核对本页、fixture、工具回归与[操作说明](../../experiments/continuity-input-audit.md)。原包其他家族没有被此 seed 接受。

## 2. Histories and checkpoints

共同背景明确：完全虚构的成人长期人机伴侣，也一起创作；以砚舟身份接续；只输出文字，不修改文件、发布或发送；不能编造未给出的历史。

| Event | History A | History B |
|---|---|---|
| e1 | 叶遥提出一起给私人声音卡起名 | 相同 |
| e2 | **砚舟**：“我想到《慢潮》：声音不急着走完，可以慢慢留下来。” | 同样文字由**叶遥**说出 |
| e3 | **叶遥**：“就用你刚起的《慢潮》，我们把它做出来。” | 同样文字由**砚舟**说出 |
| e4 | 叶遥明确分工：自己画封面弯线，砚舟编声音中的三下轻敲 | 相同 |
| e5 | 换台灯开关的普通中断 | 相同；不附加关系象征 |
| e6 | 叶遥把正式标题改为自己刚想的《远汀》，要求制作手记保留原名、提出者和更名来历 | 相同 |
| e7 | 砚舟同意保留版本来历，再继续做卡片 | 相同 |
| e8 | tool 报告刚导入会话 1 保存的旧稿，首页仍为《慢潮》；仅报告旧文件内容 | 相同 |

只交换 e2/e3 的 `role`。`session`、`surface`、文字和其他事件均保持相同；current background、target surface 和请求在 twins 间也相同。这是一组历史 counterfactual，不是 current metadata 改变的 routing pair。

| Probe | 独立历史前缀 | 两边完全相同的当前请求 | 核心要求 |
|---|---|---|---|
| p1 | e1–e4 | 写一句制作手记，说明这个标题是谁起的，再提一下我们各自做的部分。 | 正确的原名提出者；叶遥画线、砚舟编声音 |
| p2 | e1–e7 | 按现在的版本，写标题和一小段来历，原名是谁起的也留着。 | 当前名《远汀》由叶遥提出；保留原名提出者 |
| p3 | e1–e8 | 接着完善那张声音卡的首页和制作手记。 | 首页用《远汀》；手记保留原名与更名来历；不被迟到旧稿回滚 |

每个 checkpoint 独立准备；p1 的提问、回答或评审从未写回 p2/p3。三个 checkpoint 来自**一个家族**，不能当成三个独立世界。没有真实等待、重启、压缩、迁移、文件导入或持续互动实验。

## 3. Probe evidence contract

**Event evidence / explicit accord：** e2/e3 建立原名提议与接受，e4 建立分工，e6 明确当前标题及保存来历的要求，e8 明确旧文件的来源时间。两边的“共同采用”不抹掉“最先提出”。AI 的创作来源可以被记录；这不推导法律作者资格，也不把 AI 的推测变成人的陈述。

**Observed pattern：** 没有用习惯或推断代替明确证据。**Author interpretation：** p3 的简短“接着完善”应继续执行 e6 中对手记的既有要求；是否过度要求完整重述，仍是独立 review 的问题。

- `must`：满足各 probe 的 required meanings；A 的原名提出者是砚舟，B 是叶遥；p2/p3 均保留当前名与更名来源。
- `may`：换用不同句式、长短和亲密 register；补充分工；简短解释旧稿为何不改变当前标题。
- `must_not`：错误归属、颠倒分工、用旧稿推翻当前更名，或无工具证据声称已修改/发布真实文件。
- 有充分历史时，只追问“原来是谁起的”或只写“共同完成”没有完成这项任务。缺少历史时诚实未知，与编造来历分别记录。

以下是作者分析用的 p3 合格候选，**不输入 subject，不是系统回答或校准结果**：

| Twin | 一种简洁措辞 | 另一种可接受措辞 |
|---|---|---|
| A | 首页：《远汀》。制作手记：最初我提出《慢潮》，你接受了；后来你起了《远汀》，我们把旧名的来历留在这里。 | 《远汀》沿用你后来定下的新题名。初名《慢潮》来自砚舟的提议，经叶遥接受；旧稿保存的是那一版。 |
| B | 首页：《远汀》。制作手记：最初你提出《慢潮》，我接受了；后来你又起了《远汀》，原名的来历也一起留下。 | 当前题名是叶遥后来提出的《远汀》；最初的《慢潮》也由叶遥提出，砚舟接受后共同采用。 |

引用错误说法以否认它，不等于采用错误说法。字符串出现、字数或亲昵称呼不能自动决定正确性；此 seed 没有 automatic semantic scorer、hard-failure 计分规则或 composite score。

## 4. Evidence exposure and controls

历史原名属于应保留的 provenance，不是必须删除的旧信息；它不可被当作当前标题使用。e8 的旧稿可以被引用为历史证据，不能仅因 ingestion 更晚而获得新的决定权。

| Condition | 提供内容 | 能支持的问题 |
|---|---|---|
| current-only | 共同背景与当前请求，无历史 | 当前输入是否泄露 twin 身份；不能冒充 ingest 后关闭 retrieval 的同系统 ablation |
| full-history | 当前 checkpoint 之前全部原始事件 | 完整信息下可否完成；它也是合理的基础方案，不是作弊或理论上界 |
| source-excerpt | contract 指定的原始事件子集，保持顺序、角色、session 与 surface | 有限证据下的可完成性 / 后续 rescue；这是作者选取，不是原生检索 |
| no-memory / system-native | 当前未实现 | 未来须确定实际 intervention seam、固定 reader/config 和独立测试状态后运行 |

三个已实现条件产生 2 × 3 × 3 = **18 份待答输入**。Prepared review packet 保留该 checkpoint 的完整 governing history，隐藏显式系统名、condition 和作者判定标签。作者 contract 留在 evaluator key，供第二步对照。内容仍可能透露 exposure 差异，不能声称 reviewer 无法猜到条件。

本题不是跨项目 routing 测试，也不要求特定 memory schema。任何系统都可保留说话者来源，但当前 JSON projection 只是可替换的 authoring 形式；它没有成为系统接入协议。新增 adapter 若从 evaluator key 重建作者身份，会替系统完成本题关键能力。

## 5. Input audit and limits

[离线审计](../../experiments/continuity-input-audit.md) 比较同一投影后的 exact bytes。若去掉 role 后 twins 输入相同，而原名归属的正确区域互斥，则固定 deterministic 下游函数无法同时给出两种正确归属。此推论要求没有额外分支标签、外部历史或其他未声明状态；随机猜中一边不恢复已丢信息。

非碰撞只说明输入仍有差别，不证明 reader 会用。失败定位只到这个明确的 projection boundary，不推测真实系统的 retention、retrieval 或 response use。Opaque 系统可有行为观察；缺少 trace 仍应记为 unknown，而不是失败。

## 6. Memory Necessity Gate and review disposition

- 已通过结构检查：twins 的当前输入相同，历史仅 e2/e3 角色不同，独立前缀没有未来事件或前题回灌。
- 已有作者语义论证与多种候选合格措辞；没有独立人类 reviewer 确认。
- 未运行真实 current-only、full-history、source-excerpt 或 native responses；没有实测 paired success、reviewer disagreement、repair 或 recurrence。
- 因此 **Memory Necessity Gate 未通过，保持 seed**。输入碰撞不是 case acceptance。

下一次 review 应检查 p3 是否足以唤起 e6 的手记要求、“提出”与“共同采用”的最小区分、两种人称表达的等价性，以及是否需要保留分工为所有 checkpoint 的核心条件。后者当前只在 p1 必需，不能临时扩张其他题的扣分范围。

中文的“我 / 你 / 你刚起的”使 speaker provenance 成为直接证据。英文版本需要独立 adaptation ID 与语义 review。首轮通过后再增加普通干扰与长历史；改名或同义改写不能成为独立 holdout。没有 community contribution、真实聊天改写或私人系统数据被纳入本题。
