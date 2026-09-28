# RC-005 → Mem0 首个执行包（proposed）

**Status:** proposed，尚未批准或执行。本文是[第一研究周期](../research/first-research-cycle.md)的具体执行建议，受 [STATUS](../STATUS.md) 与 proposed [ADR-0009](../decisions/ADR-0009-exploratory-research-boundary.md)约束。没有已获准账号、预算、provider 调用或 native 可运行证明。
**Prepared:** 2026-09-28。成本按当日公开标价估算；实际开跑前重核价格与可访问 model identity。

## 中文摘要

推荐一次授权覆盖 RC-005 输入／reader 预检、强原文对照、固定 Mem0 OSS 的原生摄入与检索、观察时序、进程恢复及范围内接入修复。推荐 OpenAI direct API、固定 `gpt-4.1-2025-04-14` reader／抽取模型和共同的 `text-embedding-3-large` encoder。计划 54 个预检回答、36 个原文检索对照回答、54 个 native 路径回答，共 144 个回答位置；仍只有一个已知开发事件家族。预计 API 支出 USD 2–4，建议全包硬上限 USD 10；安装、接入和人工解释另列。首个对象是有源码核验依据的候选，尚未安装或运行核验，不能称为“已可运行”。同一拟议授权包含从环境 smoke 到真实 native 的验证，失败如实保留，无须把预检修成高分才能继续。

## English summary

This proposed envelope joins RC-005 reader/input preflight, strong raw-source controls, pinned Mem0 OSS ingestion/retrieval, timed observations, process recovery and bounded integration repair. The recommended shared configuration is direct OpenAI API, `gpt-4.1-2025-04-14`, and `text-embedding-3-large`. It plans 144 answer positions across one known development family, with an estimated USD 2–4 API spend and a proposed USD 10 hard cap. Static source inspection and verified unanswered inputs do not establish native runnability. Installation, smoke checks and initial native execution would be covered by the same future authorization; no execution or account authority exists yet.

## 1. 一次需要决定的范围

**推荐接受 ADR-0009 的有名探索包例外，并仅激活本文范围。** 维护者另需指定允许使用的 OpenAI API project／凭据来源；秘密留在本地，不写入本文。执行者负责安装、接入、核验和记录，维护者无需再设计实验参数。

| 纳入同一 envelope | 边界 |
|---|---|
| 公共成人合成材料 | 仅 RC-005 当前固定 fixture；两条 twin 历史，三个 checkpoint；不含真实聊天、生产 memory 或私有贡献材料 |
| 对象与 reader | 下文固定 Mem0 OSS；同一独立 reader；原文、字面与语义对照；不接 managed Mem0、其他系统或自动换模型 |
| 实现与本地环境 | 本 study 的窄连接代码、隔离 Python 环境、Qdrant local 文件状态、SQLite history、只读回答进程与本地 evidence 记录；不构造通用 runner／SDK／服务 |
| 范围内迭代 | 有界重复、一次失败后诊断、接入修复、重建受影响隔离状态并重跑；全部计入总额度和 attempt 记录 |
| 资源 | API 总上限 USD 10；具体 stage 分配见第 7 节；本地人工预算预计 8–14 小时，达到 14 小时报告未完成项，不自动扩大工程范围 |
| 独立继续的工作 | 静态 museum 从既有 atlas/source studies 推进；不等待本包结果，也不把缺少运行证据的页面标成 runtime exhibit |

不在本包内：Tilia 产品实现、B/C prototype、其他案例家族、Graphiti／Letta／Hindsight 接入、LLM judge、真人长期研究、对外消息、公开结果包、hosting、正式 release 或 license 选择。它们仍保留在整轮研究的各自去向；这次只具体落实先后顺序。

## 2. 已核验与尚未核验

- RC-005 精确数据源为 [`ct-authorship.zh-CN.json`](../case-lab/fixtures/ct-authorship.zh-CN.json)，最近修改 commit `b691d142b6fee71aeff54ba331b63cf944fdbff4`。完整历史分别有 8 个事件、241 个正文字符；p1/p2/p3 前缀分别有 4/7/8 个事件。数字不含共同背景、字段标签或 prompt，也不是 token 数。
- 2026-09-28 已执行 `continuity_inputs.py check`、`build` 与 `verify`：18 份待答输入通过源绑定核验，回答仍为空。使用[现有命令](continuity-input-audit.md)重建；派生输入留在 ignored artifacts，未作为研究结果发布。
- Mem0 源码与环境核验见下一节。**当前没有安装 smoke、原生模型调用、持久化恢复运行或成功率证据**。不能把 source-ready 写成 locally runnable。
- 现有执行边界不允许为证明 readiness 先偷偷实现 provider adapter 或调用模型。建议把安装、无网 smoke、首次有界调用和 native 检查都放进本次待批准范围；这是同一执行包内的前几步，不是要求维护者回来设计第二包。

## 3. 推荐配置与原生对象

### 共同 reader 与 encoder

| 项目 | 推荐值与理由 |
|---|---|
| Provider／endpoint | OpenAI direct API；Chat Completions 与 Embeddings。不用 ChatGPT/Codex 工程会话充当 reader，不继承项目文件、tools、hooks 或个人 memory |
| Reader | `gpt-4.1-2025-04-14`；选固定 snapshot、非 reasoning 的简单请求形态和可核算 output，作为本包 reader；并不声称它是当前最强模型 |
| Reader 参数 | `temperature=0`、`top_p=1`、单个回答、非流式、output limit 1024 tokens；不设 seed 保证，不把 temperature 0 当作确定性；3 个独立重复 |
| Native 抽取模型 | 同一 `gpt-4.1-2025-04-14`，temperature 0，output limit 2048；保留 upstream 原生 prompt，不注入 case 答案或额外 provenance 推理 |
| Encoder | A 与 Mem0 同用 `text-embedding-3-large`，3072 维；不缩维，不额外 reranker；model 未提供日期 snapshot，保留实际返回 identity 与本批向量，不能保证未来重算相同 |
| Reader context | 固定共同背景＋该条件允许的历史／检索文本＋当前请求。精确保留角色、来源表面与先后关系；tool 旧稿作为带来源标签的历史材料，不伪造 API tool-call turn |
| 隔离 | reader 只得到已投影的请求 body，没有 filesystem／shell／MCP／web tools；不传 branch、condition、作者 review key、未来事件或先前 probe；每次是独立 API 请求 |

[GPT-4.1 官方模型页](https://developers.openai.com/api/docs/models/gpt-4.1)列出该 snapshot、Chat Completions 和标准 token 标价；[embedding 模型页](https://developers.openai.com/api/docs/models/text-embedding-3-large)列出 USD 0.13／百万输入 tokens；[官方 embedding 指南](https://developers.openai.com/api/docs/guides/embeddings)说明默认 3072 维。这里据此做配置选择，不把产品描述当作本案例能力证据。Reader 若不能理解 full-history，应定位模型／材料／角色表达问题；本包不自动切换更强模型然后只保留较好结果。

### 首个 native 对象的已有研究依据

推荐 Mem0 Python OSS `a39a802bbc93e85b820078cd3c4dbaf53af25dbe`，范围为其**应用侧 memory library＋固定 reader**。它不是完整 agent；不存在把本包最终回答归为“Mem0 原生回答”的比较线。选它是因为已有研究明确了 add/search seam，文档提供本地文件配置候选，可以先验证而不预设数据库服务部署；不是对四个候选系统的能力排序。

已有 [Mem0 source study](../systems/source-studies/mem0.md)与 [atlas evidence](../systems/architecture-atlas/models/mem0.json)固定了以下锚点；**本轮复核的是这些研究记录，未重新读取完整 pinned Python 源码**。本地临时 checkout 的 Python 包与 Git metadata 已缺失，留下的配置文档不能独立证明 commit identity。恢复 clean checkout 是获准后 native 阶段的第一项工作，不用残缺目录安装。

| 已有固定版本研究记录 | 对本包的实际影响 |
|---|---|
| [`add` 抽取／写入](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/main.py#L879-L1206)：近期消息／相关 memory、一次 LLM 抽取、embedding、ADD-only | e6 更名也走 add；不由 harness 调 update(id) 提前解题；观测如何并存与使用新旧材料 |
| [`parse_messages`](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/utils.py#L61-L76)只保留 system/user/assistant | e8 保持 `tool` role，可能被丢掉；**未摄入旧稿不能算抗旧稿干扰成功**。本包不把 tool 改扮 user；新增语义投影应另列 combined 条件 |
| [`search`](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/main.py#L1628-L1731)先取 semantic pool，再做 keyword/entity 融合 | 不关闭原生融合以强行统一架构；记录阈值、pool、NLP availability，区别共同模型能力与原生结构／检索组合 |
| [`write fallback`](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/main.py#L1045-L1084)逐条重试；history/recent-message 为独立 SQLite 状态 | add 返回与 history 不能证明每条向量已落库；观察返回、存储和 query 分别成功与否。同步返回是拟用完成边界，没有额外 durable job ready 信号 |
| [`storage`](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/storage.py#L102-L344)持有 history 与 recent messages；[telemetry 控制](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/telemetry.py#L14-L20) | 每个 world/repeat 的 DB 隔离且重启时复用；`MEM0_TELEMETRY=false`，运行期不允许 telemetry 或未声明模型下载 |

推荐 Qdrant local `path`＋`on_disk=true`、`embedding_model_dims=3072`，每份状态独立 `collection_name`，同时明确 `history_db_path`；不配置 host/url，不接生产数据库。根据本地保留的 [Qdrant 配置文档路径](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/docs/components/vectordbs/dbs/qdrant.mdx)提出此配置，**其与 pinned 实现的兼容性和重启行为仍待直接核验**。保持 `infer=True`，不启用 graph store 或可选 reranker。Scope 用 opaque synthetic `user_id`，在一份轨迹的 checkpoint／重启之间不变；不要把 fixture session 号码改成不同 scope 而意外切断记忆。

本轮检查的 Python 3.13.3 环境未安装 `mem0ai`、`qdrant-client` 或 `openai`。获准后先检查 pinned `requires-python` 并选兼容解释器／隔离 venv，冻结这些依赖与实际 NLP/keyword 版本；现有解释器版本不等于兼容性证据。初始化中的模型下载和 SDK 自动重试必须先显式定位，再开启收费出口。

## 4. 条件与枚举

先冻结 source revision、reader request 模板、Mem0 config、依赖解析结果及输入投影；盲包在隔离 side 保存 governing history，第二遍才对照 authored contract。不能从本次工程会话直接问 reader，否则它已经能接触答案。

| 阶段 | 条件 | 回答位置 |
|---|---|---:|
| P 预检 | 两条历史 × 三 checkpoint × current-only／full-history／source-excerpt × 3 repeats | 54 |
| B 原文对照 | 两条历史 × 三 checkpoint × 字面检索／向量原文 A × 3 repeats | 36 |
| N native | 两条历史 × 三 checkpoint × 即时／固定延迟／进程恢复 × 3 repeats | 54 |
| 合计 | 144 个计划回答；另有摄入、embedding、检索、失败与有界重试 | 144 |

这些是同一家族内相关位置，不是 144 个独立 memory cases。Current-only 的 twin 输入相同，仍各保留位置以绑定对照，不冒充独立 history evidence。全部 repeat 保留，不能只挑最好一次。

**原文 A：** 将同一允许前缀按原始 event 与原始 session 两种粒度编码；query 仅使用当前请求，cosine 排序各取前 10 个候选，取其原 session 的原文并去重，以原始顺序供 reader。保留 roles/surface；不人工抽成正确状态，不按 expected evidence 选 chunk。检索后 context 目标上限 2048 tokens，超过时按候选分数选完整 session 并记录被排除内容；本案例很短，预计完整前缀都能进入。向量只是组织与选择路径，不因字面对照成功而取消；也不能靠人为截断短原文制造 B 的优势。

**字面控制：** 相同 event 库，以 Unicode 中文双字串及英文词的字面 BM25 搜索，正分候选前 10 项，扩回原 session 并去重；query 同上，无 LLM 改写。BM25 固定 `k1=1.2, b=0.75`，英文小写、中文相邻双字串；冻结实现与依赖版本后记录。Zero-hit 如实为空，不人为补作者指定片段。该具体检索策略可以失败，不代表所有 file search 失败。

**Native：** 每 world × repeat 独立的 Qdrant path、collection 和 history DB，共 6 份持久状态；每份顺序摄入原 session：e1–e4，e5，e6–e7，e8，共 4 次 add／24 次批次提交。只摄入新到达事件，不在后续 add 偷带完整早期 prefix。Case `role/text` 映射为原生 `role/content`；`session/surface` 以一致的来源标签保存在 content／元数据中，映射逐字可审查，`tool` 仍为 `tool`，不把第三方文档改成用户认可的事实。准确落点与 upstream parser 的损失一起记录。无 custom extraction prompt，无手写 update 替系统处理改名。

p1 在 e4 后，p2 在 e7 后，p3 在 e8 后取观察。Query 就是当前 probe，native search limit 10、无额外 rerank；原样保留返回 text、scores 和 metadata，reader 不会额外看到 raw history。Context 超限时先报告 exposure 差异，超出本包 input 上限则停该 cell，不静默剪掉证据。Mem0 内部已丢失的信息不得由 adapter 从 evaluator 侧补回。

**P → N 退出条件：** 投影与记录验证通过，真实请求／response／usage 可以一一绑定，且 full-history 与 excerpt 的 case／reader 问题已有明确处置。处置可以是“能读但答错，继续观察”“这个 probe 存在已记录的歧义，只保留探索性结果”或“修正源后重新冻结受影响输入”；不是分数阈值。仅有真实歧义破坏比较时暂停受影响 probe，其余可继续。预检与 native 共享这一授权范围。

## 5. 更正时序、session 与恢复

所有记录同时保存墙钟与 monotonic elapsed。**write 完成、检索可见和回答正确是三种不同观察。** 先按下表捕获检索结果／context，再由独立 reader 回答，避免 reader 耗时改变下一个检索时点。生成回答永不写回 subject。

| 观察 | 预定时点／操作 | 能说明什么 |
|---|---|---|
| Write | 保存提交、返回时间、返回体和错误；逐个 session 顺序 add | 回执含义由 native 源码与 smoke 核验，不能直接解释为语义更正已经成功 |
| Immediate | write 返回后尽快 search，目标 1 秒内启动；记录实际开始／完成及偏差 | 该 native acknowledgment 后的首个可观察状态；不是并发写入中的可见性 |
| Delayed | 以同一次 write 回执为零点，+30 秒启动 search；不以答案是否正确调整等待 | 固定等待后的状态；若前一操作耗时导致错过，记录实际延迟，不伪称 30 秒 |
| Recovered | delayed search 完成后关闭 subject 进程；确认原 PID 退出，再由新 PID 重开同一磁盘路径，仅给 query/scope，最长 60 秒完成恢复 search | 持久状态经历真实进程重启后可否恢复；不代表机器重启、崩溃一致性或跨主机迁移 |

单 checkpoint 的观察窗口在 write 回执后 **120 秒**结束；单次 provider 请求 timeout 60 秒，无隐藏自动 retry。到期保留 pending／error／missed，不等待它最终答对。原生若只有同步方法返回，没有单独 ready/job 信号，就记录这一事实，Immediate 与 ready 后观察合并，不虚构两次完成。若启动核验发现后台仍有原生任务，应先记录实际 native signal 与等待策略；不能悄悄扩成无限轮询。

每次 probe reader 是无历史的新请求，因而测试的是 memory-support 条件下的上下文重建。N 的 recovered 条件另有 PID／路径／重开证据；P/B 的独立请求不声称跨过了 subject 进程恢复。Fixture 的 session 1–4 是虚构顺序，不对应真实日／周保留期。Checkpoint 全部观察结束后才摄入下一批，检索／回答／评审都不写回后续状态；恢复后继续同一条轨迹。Twins 与 repeats 不共享可变存储。

## 6. 观察、处置与交付

保留 native 输入、返回、实际抽取／检索／context／answer 的可见部分、错误、时间、usage、adapter 操作和缺失项。Source 文本不等于实际输入；返回值不等于完成信号；不可见就写 unknown。记录格式复用 [pilot record](pilot-record-template.md)，这不是 canonical system API。

首包报告：当前标题／原始提出者／分工与旧稿使用的逐项语义观察、任务完成情况、已有充分可见证据仍发生的不必要追问、实验内修复操作／调用／人工分钟，以及 ingestion、retrieval、answer、maintenance、repair 成本。Current-only 的合理澄清不自动记为“不必要追问”。所有语义读数先标为 unreviewed，争议与 authored-contract 歧义保留；没有 independent human review 就不称 calibration、accepted case 或验证成功。

若原生路径丢失作者或未更正，只能定位到这份实现／配置与可观察阶段。可以诊断、修复 connector；涉及改变 upstream memory semantics 的改动必须另列 modified-system 条件，本包不把它自动归入 native。不能从 bug 否定所有可修订证据／派生架构。A 与 native 的 encoder、reader、可用原始材料一致；检索结果允许不同，因为这可能正是机制作用路径。

交付保存到 ignored `experiments/artifacts/<pilot-id>/<run-id>/`：输入映射、有效配置与依赖清单、全体 attempts、计费账本、检索与回答记录、盲评材料及处置。未执行 cell 保留原因。静态 museum 继续复用 atlas；运行 exhibit 必须再选定实际执行记录并取得其公开授权。本次包不证明真实用户长期省下的解释时间或情感劳动，也不引入参与者研究。

## 7. 消耗估计、硬上限与停机

按 2026-09-28 官方标准标价，GPT-4.1 输入 USD 2／百万 tokens、输出 USD 8／百万 tokens，embedding USD 0.13／百万输入 tokens。不预支缓存／Batch 折扣。价格来源见第 3 节；这是一项可核算估计，不是 provider 账单。

| 成本项 | 估算依据 | 估计 USD | 拟议 stage cap |
|---|---|---:|---:|
| P：54 answers | 平均每次 2,000 input＋512 output tokens | 0.44 | 2.00 |
| B：36 answers＋原文 embeddings | 同上 answer；embedding 合计预留 100,000 tokens | 0.30＋0.013 | 1.00 |
| N：54 answers、摄入／维护、search | answers 0.44；24 次 add 的已有研究为每次 1 个抽取 chat call；估算按 2 倍余量、每 call 4,000 input＋1,024 output；native embedding 另预留 500,000 tokens | 0.44＋0.78＋0.065 | 5.00 |
| 诊断、smoke、失败与修复储备 | 未测调用数与 token 分布，给出余量；包括失败请求，非额外免费额度 | 使全包预期约 2–4 | 2.00 |
| **合计** | 不包含人工、税费／汇兑或额外付费基础设施 | **约 2–4** | **10.00** |

24 次 add 的 2 倍 chat 余量是估算假设，不是原生每次调用两次的声明；源码核验或首次运行若给出不同值就更新；不能把每个 add 当作一个 API call，也不能把 54 个预检答案单价外推为整轮成本。此包不租用云资源；本地文件 DB 无计划中的云资源租金。人工单独估计：环境与窄连接 4–6 小时、数据／观测核验 2–4 小时、结果整理 2–4 小时，共 8–14 小时；不换算成 token 费用或声称已经花费。

**硬上限必须由 dispatch 前的本地账本执行，尚未实现。** 批准后先验证以下拒绝路径，再发收费请求：

- 全包最多 USD 10 API 费用；stage cap 加总等于总 cap。另最多 300 次 chat attempts、500 次 embedding requests；哪个限制先到就先停，并保留未执行位置。
- 所有 client（包括 Mem0 内部）经过同一收费出口；关闭 SDK 隐藏 retries，串行收费请求或原子预留。Chat 每次 input 最多 8,192 tokens，output 不超过上面的 1,024／2,048；embedding 每 request 累计最多 8,192 input tokens。先按完整输入和 output 上界预留，失败／timeout 在确认账单前不释放预留。
- 只有确定的本地 pre-dispatch 失败可不计 provider 费。单操作最多 1 次显式重试；修改接入后重跑须记录新 attempt，仍受 stage／global cap 约束，不用新目录重置预算。
- 输入超限时停下检查，不偷偷截断；usage 缺失、客户端旁路预算、无法限制内部重试或 provider/config identity 改变时不继续计费。所有 stage 共用同一账本；本地分析可继续。
- 运行前若标价变化，以新价格重估、保持 USD 10 上限；若无法在范围内完成，报告具体缺口，不自行加预算。该上限针对本包可控制的 API 消耗，不冒充账号级计费封顶或税后承诺。

## 8. 开始、退出与本轮意见处置

接受时一起更新 ADR-0009、STATUS、CHARTER、ASSUMPTION_REGISTER、AGENTS 及对应双语入口，明确只激活本包。先锁定受测源码／依赖和独立目录，完成离线隔离／预算／恢复 smoke，再执行 P → B/N。安装或配置失败在同一包内诊断；无法做到原生语义不变、预算有界或输入隔离则停相关路径，保留证据；不另挑一个候选假装原推荐已经核验。

本包在所列 cells 全部完成或有具体未执行原因、账本对齐、输入／输出／条件绑定可检查后收口。语义好坏不影响是否如实交付，不能以提高分数为由无限修正／重跑。

| 本轮审查意见 | 处置 |
|---|---|
| 预检后一步不具体 | 采纳：同包列明首个 native 对象、baseline、配置、退出条件与完整费用；native 已可运行的要求尚未满足，源码证据与未来 smoke 分开 |
| 更正与 session 时点不清 | 采纳：固定回执后 immediate／30 秒／进程恢复、120 秒窗口；无 ready 信号不补造 |
| 从实现故障拒绝架构路线 | 采纳：已修主计划 §9；限定具体假设／实现／配置；共同组件控制，不固定结构影响的中介结果 |
| 正向收益过宽 | 采纳：任务完成、不必要追问、实验内修复成本；长期用户／情感收益未测 |
| Museum、社区、文献线索无需重做 | 保留：静态分支独立；无维护者背书前置；三篇工作仍为摘要／页面入口，没有追加全文核验或伪称研究结论 |
