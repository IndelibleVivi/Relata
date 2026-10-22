# RC-005 → Mem0 首个执行包（accepted named envelope）

**Status:** 2026-10-23 maintainer 接受 [ADR-0009](../decisions/ADR-0009-exploratory-research-boundary.md)，仅激活本包。固定 study 源码与 offline plumbing 已实现；真实 native 可运行性、执行完成和语义判断各自需要运行证据。公共文档不承载私人运行状态或 raw 结果。[STATUS](../STATUS.md) 为当前权限入口。

## 中文摘要

同一授权覆盖固定 RC-005 的输入／reader 预检、强原文对照、pinned Mem0 native 摄入／检索、30 秒观察、真实进程恢复和范围内接入修复。共 P54＋B36＋N54＝144 个回答位置，不是 144 个独立案例。选用既有 gateway generation quota 与本地 Qwen3-Embedding-0.6B-Q8_0/1024；不新增充值或收费 fallback。普通 Chat Completions／JSON-object 协议兼容性证据在配置匹配时可复用，不再另造 Responses adapter。[ADR-0010](../decisions/ADR-0010-bounded-provider-compatibility-checks.md) 仍是独立的兼容性例外，不是 native 的授权来源。

## English summary

The maintainer accepted this named envelope on 2026-10-23: fixed RC-005 input/reader preflight, strong raw-source controls, pinned Mem0 native ingestion/search, timed observations, actual process recovery and bounded integration repair. P54 + B36 + N54 gives 144 related answer positions. Existing generation entitlement and local Qwen3-Embedding-0.6B-Q8_0/1024 are selected, with no recharge or paid fallback. Source implementation and fake-driver checks do not establish live compatibility, memory quality, independent review or benchmark acceptance. Raw evidence remains private and ignored; publication, hosting, outreach, licensing, Tilia product work and other study envelopes retain separate authority.

## 1. 对象、输入与边界

固定输入为 [`ct-authorship.zh-CN.json`](../case-lab/fixtures/ct-authorship.zh-CN.json)，两条成人原创合成 twin 历史，各 8 个事件，p1/p2/p3 分别在 e4/e7/e8 后。来源绑定复用 [`continuity_inputs.py`](../tools/continuity_inputs.py) 的 `history_prefix`、`subject_input`、`source_view`、`reviewer_packet` 纯函数。公共 fixture 是 authored-unvalidated 开发材料，不能冒充 held-out benchmark。

唯一 subject 为 Mem0 Python OSS `a39a802bbc93e85b820078cd3c4dbaf53af25dbe`；启动时检查 clean checkout 与精确 HEAD，并从该 checkout import。边界是应用侧 memory library＋共同独立 reader，最终回答不归为 Mem0 自带 agent 能力。环境由 operator 在 Git 外指定：已准备 Python 3.13.5、mem0ai 2.1.0、OpenAI 3.37.0、Qdrant 1.20.0；实际版本随 child ready evidence 保存。环境准备不是成功摄入或恢复的证据。

本包不含任意 corpus／adapter 注册、其他系统／案例、LLM judge、真人长期研究、Tilia 产品实现、通用 runner／SDK／服务、public hosting、外联、raw 结果公开、正式 release 或 license 决定。正式 cross-system promotion gate 保留，其他研究职能独立推进。

## 2. 固定资源与模型控制

| 项目 | 当前配置 |
|---|---|
| Generation | 已授权既有 gateway entitlement，OpenAI-compatible Chat Completions；实际 endpoint／model alias 从 private runtime JSON 原样使用；不用 OpenAI 平台 key，不自动改模型 |
| Reader | 每回答新请求；temperature=0、top_p=1、非流式、max_tokens=1024；无 seed／确定性承诺；3 repeats |
| Native LLM | 同一 generation 配置，temperature=0、top_p=1、max_tokens=2048；保留 upstream 原生抽取 prompt/parser；不手写 update 解题 |
| Encoder | 共同本地 Qwen3-Embedding-0.6B-Q8_0，1024 维，API float；每向量验证 finite、nonzero、维数，L2 normalize；模型 alias 原样转发 |
| Query policy | 原始文本先把 newline 换空格；仅 search query 加 `Instruct: {runtime query_instruction}\nQuery: {text}`，文档／memory add 不加 instruction。原文 A 与 native 使用同一规则；这是显式共同 encoder 配置贡献 |
| Reader exposure | 仅 common context、允许的 history 或 native 文本／来源及 current；不发 variant、condition、作者 contract、review key、未来事件、其他 probe 回答 |
| SDK / timeout | native llm/embedding 两 client 显式 `with_options(max_retries=0, timeout=60)`；HTTP transport retries=0；独立 reader stdlib 单请求 timeout=60 |
| Identity limit | Gateway model 返回标签不证明冻结权重或 pool snapshot；opaque upstream retry／identity 记 unknown，不能声称 all-upstream exactly-once |

所有会触发调用的 SDK HTTP 请求经过共同 file ledger；原文／reader 路径也使用同一 ledger。认证 headers 不入 ledger；请求 body、return、usage、identity 和错误保留在 private evidence。先持久预留 dispatch 再网络请求，失败／timeout 仍计数，不释放。初始化在 import mem0 前设置 `MEM0_TELEMETRY=false` 和轨迹专属 `MEM0_DIR`，清继承路由 env。Child 要求无 spaCy／fastembed，记录 upstream NLP 降级，不暗中下载模型，不加 graph store 或 reranker。

## 3. 条件、原文对照与 session

| 阶段 | 条件 | 回答位置 |
|---|---|---:|
| P | twins × 3 checkpoint × current-only／full-history／source-excerpt × 3 repeat | 54 |
| B | twins × 3 checkpoint × literal BM25／vector raw A × 3 repeat | 36 |
| N | twins × 3 checkpoint × immediate／+30s／recovered × 3 repeat | 54 |

原文 A 同时按原 event 和原 session 编码，各自 cosine 前 10 候选，扩回完整原 session、去重并保持原始顺序。Literal BM25 固定中文相邻双字串＋英文 lower 词、k1=1.2、b=.75，正分前 10 event，同样扩 session；zero-hit 不补作者片段。不看 review key 选候选。保存 candidates、原向量、query 向量、admitted context。4/7/8 事件很短，top-10 几乎暴露完整前缀；不据此声称长历史语义筛选能力。原有 context 2048-token 目标不作为伪 tokenizer 证明；保留完整允许内容，完整 HTTP body guard 才是可执行的前置上限，不静默裁剪。

每 world × repeat 独立 Qdrant local 磁盘 path、collection 与 SQLite history，共 6 条轨迹。按 session 原样增量 add：e1–e4、e5、e6–e7、e8，共 24 批。Role/content 映射保留 user／assistant／tool；content 带原 session 与 surface 来源标签。后续 add 不偷带旧 prefix，无 custom extraction、手写 provenance 推理或手动 update。Native search 采用该 pin 的实际参数 `top_k=10`、`rerank=False`，保留 upstream 内部融合与 threshold。

e8 的 tool 记录会被 upstream `parse_messages` 忽略。必须保留这一实际损失；没有摄入旧稿不能算抗 stale 成功。Native 检索 reader 只见返回 memory 文本、来源 metadata 和 score，不从 raw history 补回丢失信息。生成回答和 review 都不写回 subject。

## 4. 时序与进程恢复

以同步 `add` ACK 为观察起点，不虚构独立 ready signal。先捕获全部检索/context，再调用独立 reader：

1. Immediate 尽快 search，目标 ACK 后 1 秒内，保存实际偏差。
2. Delayed 在相同 ACK 后 +30 秒 search；延迟超过目标保留实际时间，不为答案调整等待。
3. 关闭原 native PID 并 wait 确认退出，新 PID 打开相同 Qdrant/history/state path，随后只给 query/scope 做 recovered search；保存旧退出、新 ready 和路径证据。恢复操作最多 60 秒，整个 checkpoint 自 ACK 起 120 秒截止；到期保留 missed／error／pending。

墙钟、monotonic、PID、path、原生 inputs/results、stderr 和完整 HTTP attempts 分开保存。每条 RPC 回显 operation，parent 严格绑定；超时或错误立即隔离并关闭旧 channel，不把晚返回配给下一次检索。恢复 close/start/search 共用 60 秒且不超过 ACK 后 120 秒的截止，new ready 后在实际发送前重查；超窗 capture 也必须落盘。顺序 search 可能受 warm/cold cache、lazy state、UTC expiry 或 provider 变化影响；30 秒／新 PID 差异不能直接归因于时间或持久化因果。这里不模拟机器崩溃、跨主机迁移或真实周月保留。

P 技术执行成功后，允许以明确的“未评审探索性继续”处置进入 B/N；full-history/excerpt 的错误或歧义仍须在 private 语义报告中保留。技术失败阻断 dependent native，不以字符串 scorer 代替评审。`quick` 先完成 A/p1/repeat1 的三个 P，再做同轨迹三个 N；均属于 144，后续 `run` 复用。

## 5. 可执行入口与 private runtime JSON

源码入口是 [`rc005_native.py`](rc005_native.py)，child 为 [`rc005_native_child.py`](rc005_native_child.py)，共同 HTTP／ledger 为 [`rc005_common.py`](rc005_common.py)。Orchestration 只需 stdlib，child 使用 operator 指定的隔离 Python。以下值全部为占位符；真实配置、secret 与 artifacts 不入 Git：

该入口要求 POSIX file locking 和 subprocess pipes；本轮环境为 macOS，Linux 未实测，Windows 不支持此入口。Operator 先准备 Python 3.13 与专用 venv，再安装 clean pin 的基础依赖；不安装 `nlp`／`extras`，避免可选模型下载和改变当前 native 配置。与本包准备环境一致的核心版本示例：

```bash
git clone --no-checkout https://github.com/mem0ai/mem0.git /PRIVATE/PINNED_CLEAN_CHECKOUT
git -C /PRIVATE/PINNED_CLEAN_CHECKOUT checkout --detach a39a802bbc93e85b820078cd3c4dbaf53af25dbe
python3.13 -m venv /PRIVATE/VENV
/PRIVATE/VENV/bin/python -m pip install /PRIVATE/PINNED_CLEAN_CHECKOUT 'openai==3.37.0' 'qdrant-client==1.20.0'
/PRIVATE/VENV/bin/python -m pip check
/PRIVATE/VENV/bin/python -m pip freeze > /PRIVATE/dependencies.txt
```

`python3.13` 指 operator 已准备的 interpreter；本轮实际版本为 3.13.5。示例不是 transitive dependency lock，实际完整版本清单随私有运行记录保留。不要把已有个人 memory 环境当作本 study 的 venv 或 state。

```json
{
  "chat": {"base_url": "https://generation.example.invalid/v1", "model": "AUTHORIZED_MODEL_ALIAS", "key_file": "/PRIVATE/GENERATION_KEY"},
  "embedding": {
    "base_url": "http://localhost:PORT/v1", "model": "LOCAL_ENCODER_ALIAS",
    "key_file": "/PRIVATE/LOCAL_ENCODER_KEY", "dimensions": 1024,
    "query_instruction": "OPERATOR_SELECTED_RETRIEVAL_INSTRUCTION"
  },
  "native_python": "/PRIVATE/VENV/bin/python",
  "upstream": "/PRIVATE/PINNED_CLEAN_CHECKOUT",
  "ledger": "/PRIVATE/RC005_STUDY/dispatches.jsonl"
}
```

每个 credential 也可用 `api_key_env` 指定环境变量名来替代 `key_file`。本地无需鉴权服务也提供一个非 secret placeholder key 文件满足 SDK。无 env endpoint fallback。Private 配置不要放公共源码路径。

```bash
python3 -B experiments/rc005_native.py plan
python3 -B experiments/rc005_native.py --runtime-config /PRIVATE/runtime.json --out experiments/artifacts/rc005-native/RUN quick
python3 -B experiments/rc005_native.py --runtime-config /PRIVATE/runtime.json --out experiments/artifacts/rc005-native/RUN run
python3 -B experiments/rc005_native.py --runtime-config /PRIVATE/runtime.json --out experiments/artifacts/rc005-native/RUN report
```

`quick`、完整运行、失败诊断及修复共用同一个 ledger 和 output。Ledger 绑定 source、模型配置与 output，换 output 拒绝，不能靠新目录重置预算。已完成 operation 直接复用；failed／started 状态保留并阻止盲重发。只有基于证据完成修复、明确处置可能的重复请求或部分写入后，operator 才用 `retry-operation --operation NAME --reason "REPAIR_AND_STATE_DISPOSITION"` 将旧记录移入 `prior-attempts`，保留 ledger，再显式运行。已完成操作不能解锁；原 ACK 时点不能重造。若 child/state 已部分写入而无法恢复同一含义，停止该分支、记录缺口，不能静默重建后称原始轨迹。

## 6. 调用预算与停止

- 全包最多 **300 chat／500 embedding client dispatch**，包括 ingestion、search、reader、smoke、失败、诊断和修复。不可见的 downstream retries 不是已受控的 upstream attempts。
- 每个完整 client HTTP body **最多 65,536 UTF8 bytes**，dispatch 前可检查；保留完整 native prompt，不截断。不是 8k tokens 或 8k bytes 的替代证明。
- 返回 `usage.prompt_tokens > 32,768` 时保留该结果并持久写 token-stop，阻止后续所有 model dispatch；这是 postflight 观察，不是预先保证 provider tokenizer。Usage 缺失或 provider identity 不可见如实记 unknown。
- 不新增现金消费、充值、收费 fallback 或自动换模型；原 OpenAI direct／gpt-4.1／text-embedding-3-large 与 USD 10 表属于已被替代的历史方案，不再是本包前提或现行费用封顶。已有 quota 的账号级内部消耗不等于公开标价账单。
- 输入越界、budget exhausted、identity/state 隔离失败、原生语义被接入改写或 observation deadline 超时停止 affected branch；本地整理可继续。范围内修复不重新索取已有许可，扩研究对象／数据／账户支出／外部动作需独立授权。

## 7. 证据、评审与关闭

ignored `experiments/artifacts/rc005-native/<run>/` 保存 plan/effective config、operation 状态、native-inputs、state、stderr、captures、contexts、reader response/usage、coverage、blind-review；统一 ledger 另按 private runtime 指定保存，不含 auth headers。重跑不能覆盖先前失败与争议。Coverage 对 144 个位置保存 complete／pending／technical failure 状态，语义一律 unreviewed；盲包只含 governing history/current/response，不含作者 key。没有 hard semantic scorer 或自动能力分。

Private 报告逐项观察标题、提出者、分工、旧稿使用、任务完成、不必要追问、ingestion/retrieval/answer/maintenance/repair 成本与人工处置。Current-only 的合理澄清不自动算不必要追问。按 family 解释相关 repeats；judgment 比例不等于 response accuracy 或 independent human calibration。坏结果定位到可见配置／阶段，不能推翻整个架构类别。

收口条件是每个回答位置完成或保留具体未执行原因，ledger 与原始证据能绑定，尚未评审明确标注。源码通过检查不等于已 live；真实运行不等于 accepted case／formal benchmark；本地保存不等于公开发布。独立图集／源码研究与 future-question work 不等待本包成功，也不自动纳入本包执行权限。
