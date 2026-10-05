# Hindsight：在途派生写入的源码边界核查

**状态：bounded public-source research draft；SOURCE-OBSERVED / INFERRED 分列；无上游运行、无 accepted Evidence Card。**

研究日期：2026-10-05。固定对象：[vectorize-io/hindsight commit 9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55](https://github.com/vectorize-io/hindsight/tree/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55)。范围限定为默认 SQL/PostgreSQL facts → observations consolidation 与显式 fact edit / document delete 的交错。

## 中文摘要

源码存在实质性保护：派生写入前在同一事务内重查来源存活并取得 `FOR SHARE`；observation actions 和来源 consolidation 标记共用事务；更正、删除在变更前后清理受影响 observations，并把幸存来源重新排入待归纳状态。这些是反对“只要异步就一定会写回已删来源”的正面证据。

仍需区分**来源还存在**与**派生时读取的来源内容仍有效**。本轮检查的普通 CREATE / UPDATE 写路径按 ID 校验存活，没有把派生时的 source text / revision 与提交时的当前值比较；多来源过滤也不会重新生成已准备的文本。这构成具体待验证时序，不是已经复现的 race bug。独立于本文的[并发研究工作表](correction-race-challenge.md)可检验一般机制；不得把其中作者构造的反例标作 Hindsight 运行结果。

## English summary

This bounded static audit pins one public commit and follows the default SQL observation path. Source liveness is rechecked under `FOR SHARE` inside the transaction that applies observation actions and consolidation stamps. Correction and deletion sweep dependent observations and requeue surviving facts. These guards materially constrain delete/write interleavings. The inspected ordinary write path does not compare the source revision or text used for derivation with its current value, and filtering surviving IDs does not regenerate prepared text. Same-ID corrections and partial-source removal therefore merit discriminating schedules. No upstream execution, model call, database experiment, or demonstrated race is reported.

## 取证方式与覆盖

- 重新读取 public exact-commit 文件；没有沿用二级综合中的行号来猜代码。GitHub blob HTML 的 `refInfo.currentOid` 与固定 commit 一致；从 `rawLines` 还原源码行号。大文件 `memory_engine.py` 由该 commit 的 GitHub contents API 返回 blob 标识，再经 Git blob API 取得内容。
- 网页工具的 raw 文本展示规范化空白，行号与真实文件不同；本文链接均使用取得的原始文件行号。直接访问 raw 域名的 Python/curl 遇 TLS EOF / SSL 错误，已通过 GitHub blob/API 取得所需公开内容，没有绕过身份验证或访问私有对象。
- 实际逐段检查：`consolidator.py` 的候选来源、scope 调度、LLM/embedding 前后、普通 CREATE/UPDATE/DELETE、dedup folds、事务提交与取消检查；`memory_engine.py` 的 document delete、fact edit/invalidate、清理委派和 enqueue；`memories/pg/writes.py` 的失效清理与 edit；`memories/pg/reads.py` 的待归纳选择与标记；`retain/fact_storage.py` 清理委派；`worker/poller.py` claim/retry。
- 这不是全仓审计。未检查所有 database wrapper、schema migration/trigger、隔离级别配置、替代 store、托管产品、所有写入口或 mental-model refresh 完整路径。以下推断不外推至这些对象。
- 研究入口：[既有 Hindsight study](../systems/source-studies/hindsight.md)、[更正传播综合](correction-propagation-study.md)。前者的证据状态未被本文提升；后者原本是二级综合，本文新增的是有界源码复核。

## 从选择到写入的实际路径

| 阶段 | SOURCE-OBSERVED | 能说明的边界 |
|---|---|---|
| 来源选择 | 读 `find_unconsolidated`，把 ID、text、tags、时间拷入 Python 字典；调用结束后释放该连接。[A1] | 派生使用取得时的内容；不是跨整个 LLM 阶段持有来源行锁。 |
| 派生 | 每条来源 recall 相关 observations；合并候选后调用 LLM，预备 actions、embedding 与可选 dedup。[A2] | 归纳与准备发生于最终写事务之前，存在可插入更正的阶段边界。 |
| 提交 | `conn.transaction()` 包住 DELETE、UPDATE、CREATE 和 `mark_consolidated`。[A3] | 同一响应的写入与标记共享提交/回滚边界；事务本身不重算派生文本。 |
| 写前重查 | `_filter_live_source_memories` 对 bank 内候选 ID `SELECT ... FOR SHARE`，返回仍存在的子集。[A4] | 默认 SQL 路径在检查后至事务结束保护这些行；外部 store 分支只有查询，本研究不评价其并发模型。 |
| 普通 CREATE | 重查后若来源全部消失则跳过；否则保留 prepared text，用存活 ID 子集写 observation。[A5] | 全部删除与部分删除具有不同分支；“来源数组干净”不等于“文本重新据剩余来源生成”。 |
| 普通 UPDATE | 新贡献来源重查；合并 recall 时已有的 source IDs；按 observation ID 更新。影响行数为零就跳过 history。[A6] | 不会用普通 SQL UPDATE 重建已经消失的目标行；当前目标仍在时，此语句没有 text/revision CAS 条件。 |

## 保护强度：哪些能成立，哪些不能扩大

1. **行锁有真实事务寿命。** [A3]、[A4]、[A5] 使用同一 `conn`，锁不止于 preflight。PostgreSQL 文档说明 `FOR SHARE` 阻止同一行的并发 UPDATE/DELETE，锁保持至事务结束。[P1] 因此若派生事务先锁住来源，来源更正/删除要等待；若删除先提交，后来的 liveness query 不能把已删 ID 当作存活。这是 SQL 条件下的推断，尚无本项目数据库观察。
2. **显式 document delete 前后各 sweep。** 删除事务取得 bank `FOR NO KEY UPDATE`，收集来源 ID，先清理、删除 document，再清理；第二遍用于捕捉中间提交的派生行。[A7] Bank 锁不能自动解释为所有 consolidation 都取得同一互斥锁。
3. **fact edit / invalidate 也在变更前后 sweep。** edit 的 store 写入重置 consolidation 并更新 text/embedding；invalidate 移离 live；均在事务中清理。[A8] 这保护变更时已可见的受影响 observation，但不能独自证明事务以后完成的旧派生文本已被重新验证。
4. **幸存来源重建路径确实存在。** sweep 按 source ID overlap 查 observations，按 ID 顺序锁相关事实、observations、幸存 co-sources，删除 observations/history，令幸存 world/experience 的 `consolidated_at = NULL`。[A9] 默认待归纳查询会选择未归纳且未失败的来源。[A10] 自动发起后续 consolidation 受配置及成功 enqueue 条件约束；归空不是已经重建完成。[A7]、[A8]
5. **CAS 不是全无，但范围窄。** dedup fold 用 probe 时的 observation text 作为 SQL `WHERE ... text = ...` 条件，避免覆盖已改写的 fold 目标；普通 UPDATE 的条件不同。[A11]、[A6] 不能把 dedup 的目标保护推广成所有 source revision 的保护。
6. **取消与调度保护另有对象。** `_gather_or_cancel` 取消并等待同批失败的 sibling tasks；scope locks 属于该 dispatch；operation alive 在批次后检查。worker retry 排除 `cancelled` 状态。[A12] 这些限制重试/并发重叠；已读范围未建立“任意来源 edit/delete 自动取消所有在途派生任务”的契约。

## 区分性时序：提议，未运行

设同一 bank/scope 有来源 F，旧内容为“项目日期是周五”；另有未撤回来源 G 记录“主题青瓷”。角色与材料均可使用公开合成输入。以下是执行设计，不授权 provider 或数据库运行。

| 步骤 | 操作与所需观察 |
|---|---|
| T0 | 记录 F/G 的 ID、text、consolidation 字段及已有 observations；派生 worker 取得 F 旧内容。 |
| T1 | 在 LLM/embedding 完成或 prepared action 已确定、最终写事务尚未开始处暂停；记录确切候选文本与 source IDs。不得用“任务正在运行”替代屏障。 |
| T2 | 用显式 edit 把同一 F ID 改为“周二”；等待该事务和两次 sweep 提交，核对 F 当前值、相关派生行及待归纳标记。 |
| T3 | 恢复旧任务；观察是拒绝、重新派生、跳过、写入旧文本，还是随后由其他任务修复。记录最终 SQL action、来源 ID、实际文本及标记变化。 |
| T4 | 单独观察新一轮 consolidation 是否选择 F，以及 observation 当前值；再检查 G 邻域。任务 completed 不能替代内容和来源核对。 |

对应的关键反证：若在 T2 后的最终写路径确认比较了派生时来源版本并拒绝旧 action，应否定“仅有 liveness guard”的路径假设；若旧 action 未发出 CREATE/UPDATE，不能把没有 stale write 归功于并发保护。

另保留四个相邻对照，避免把不同问题混成一项：

- **全部来源删除先提交：** T2 删除 F，action 只引用 F；预期 inspected guard 的跳过分支是正面控制。[A5]
- **派生先取锁：** 在事务内取得 `FOR SHARE` 后暂停，让 edit/delete 请求进入；记录等待与提交顺序，确认保护的寿命。锁等待属于推断，仍需实际测量。[A3]、[A4]、[P1]
- **部分来源撤回：** prepared CREATE 引用 F/G，T2 仅删除 F；核对最终文本是否仍携带仅由 F 支持的断言，以及 source IDs 是否只剩 G。ID 过滤与语义依据分开判读。[A5]
- **UPDATE 目标被清理：** prepared UPDATE 指向 T2 已删除的 observation；记录零影响行分支与 history 行数，和 CREATE 分开观察。[A6]

只有在真实路径、配置和屏障成立时，这些时序才可能区分机制；无可控屏障应记 `UNVERIFIED`。替身决定 action 可以用于将来获授权的局部工程试验，但不能代表真实 LLM、真实数据库或端到端系统表现。

## 当前结论与未决范围

- **SOURCE-OBSERVED：** 事务内 liveness/锁、原子 actions+stamps、变更前后 sweep、幸存来源归空、特定 dedup CAS、取消/重试保护都存在。
- **INFERRED：** 在所读普通写路径，存活检查未比较 source text/revision；同 ID 改文与部分来源丢失，不能仅凭 liveness 被排除为 stale-content 候选。这是需要区分的覆盖缺口，不是系统漏洞定性。
- **UNVERIFIED：** 实际隔离级别和 wrapper 行为、所有清理入口的交错闭包、是否有未读 trigger/机制补足保护、重建任务在竞争下最终是否再次选到来源、语义旧值是否真写入/召回、修复延迟、所有 mental-model/history/read paths。
- 本文没有执行上游、安装依赖、调用 LLM/embedding/provider、产生新 case result、接受 ADR 或发布 capability claim。

## 固定源码证据

下列路径均相对于同一固定 commit；行号为原始源码行号。普通写分支与 dedup 分支分别定位，避免用局部保护替代整条链的证据。

[A1]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L1224-L1261
[A2]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L2205-L2456
[A3]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L2459-L2545
[A4]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L730-L788
[A5]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L3312-L3408
[A6]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L2639-L2794
[A7]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L10175-L10349
[A8]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L12010-L12220
[A9]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memories/pg/writes.py#L240-L332
[A10]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memories/pg/reads.py#L359-L480
[A11]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L390-L533
[A12]: https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L68-L101
[P1]: https://www.postgresql.org/docs/18/explicit-locking.html#LOCKING-ROWS

补充精确位置：

- [选择连接范围 L1521–1529](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L1521-L1529)。
- [批次后取消检查 L1741–1744](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L1741-L1744)、[scope locks L1860–1895](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py#L1860-L1895)。
- [worker claim 事务 L679–716](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/worker/poller.py#L679-L716)、[retry cancellation guard L1006–1030](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/worker/poller.py#L1006-L1030)。
- [清理 engine 委派 L16403–16417](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L16403-L16417)、[fact_storage 委派 L146–182](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/retain/fact_storage.py#L146-L182)。
- [SQL edit 字段与标记 L543–607](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memories/pg/writes.py#L543-L607)、[consolidation enqueue L22184–22243](https://github.com/vectorize-io/hindsight/blob/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L22184-L22243)。
