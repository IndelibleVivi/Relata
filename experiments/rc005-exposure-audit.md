# RC-005 P0：离线 native exposure 审计与配对输入准备

**Status:** fixed-study offline consumer；只核对已保存记录并准备待执行输入。不是 subject／provider 执行、历史结果修订、语义 scorer 或已完成配对研究。本说明不包含任何真实运行统计；精确运行证据与解释留在 private operator 记录。

[`rc005_exposure.py`](rc005_exposure.py) 只接受[既有 RC-005 执行包](rc005-native-execution-packet.md)的固定 144-position plan，审计其中 54 个 native 回答位置。来源仍是固定 [`ct-authorship.zh-CN.json`](../case-lab/fixtures/ct-authorship.zh-CN.json)，不是任意 corpus。已有 `rc005_native.py` 的执行条件、reader 参数和历史结果保持原样。

## 目的与可解释范围

原 native reader 包装从每条 search entry 提取 `memory`（无此键时才回退 `text`）、`metadata`、`score`，并加入 `role=memory` 与 `surface=native-search` 标记。它会丢掉其他顶层原生字段；缺失的 metadata／score 会变成历史包装中的 null。现在该原表达式提纯为 [`historical_native_history`](rc005_native.py)，字段顺序、默认值及 `dump` 序列化保持一致，原运行路径仍只调用这一历史投影。

P0 将“原生结果存在什么”“实际 reader 请求暴露什么”和“模型是否理解、使用了什么”分开。字段可见性不认证其内容：`attributed_to` 或正文中有关归属的文字仍是受测系统的输出，不能补成作者真值，也不能仅凭出现就判断 reader 已正确采用。`created_at`／`updated_at` 等原生值不自动代表源事件时间；scope 字段也不证明隔离实际有效。全部语义状态保持 `unreviewed`。

## 三个固定待执行臂

| 臂 | `history` 形式 | 保留与限度 |
|---|---|---|
| `legacy` | 历史 `role/surface/text/metadata/score` 列表 | 与已发 reader body 的重建序列化逐字一致；保留历史丢字段及 missing→null 行为 |
| `full-native` | 每项为 `{"native_entry": ORIGINAL_ENTRY}` | 原 entry 按原序完整嵌套；保留 JSON 类型、null、空值、缺失键及全部原生字段，不将 native role 提升为 API chat role |
| `format-only` | 每项为 `{"historical_fields": HISTORICAL_ITEM}` | 仅将 legacy 已有字段与值放入一层结构；不增加原生信息，用于区分信息增加与包装格式变化 |

三臂保持同一 common context、current、reader model 和原 body 参数，仅替换允许的 history。`full-native` 保留的是返回的每个 entry，不把 result envelope 的非 entry 字段擅自补为 reader 证据；完整原始 result 仍保存在 private 映射中。API turns 始终为固定 system／user；原生 role、工具表面或 attributed_to 只能出现在数据层，不伪造成 tool-call 或 chat turn。

这些是**准备好的请求**，没有新 response 或执行 receipt。即使 legacy 对应历史真实回答，本工具也不会把那个回答复制成新三臂配对的结果。后续 provider 配对必须遵循单独具名的执行包与资源范围；本工具不发请求、不改 output limit、不选择模型、不重 ingest 或 search，也不自动激活新条件。归属与其他新增字段的拆分消融仍可另行设计，本版本只准备这三个固定臂。

## 运行前提与命令

由 operator 明确选择历史 run、只读 ledger 和独立 derived output。工具不会读取 runtime config、环境凭据、wallet、其他 run 或 continuity。这里只展示占位路径；真实路径和输出都保留在 ignored local artifacts。

```bash
# 只输出绑定后的审计 JSON；不创建 prepared output。
python3 -B experiments/rc005_exposure.py audit \
  --run experiments/artifacts/rc005-native/HISTORICAL_RUN \
  --ledger /PRIVATE/STUDY_LEDGER.jsonl

# 核对全部绑定后，一次准备 audit、pending requests 与 private 映射。
python3 -B experiments/rc005_exposure.py prepare \
  --run experiments/artifacts/rc005-native/HISTORICAL_RUN \
  --ledger /PRIVATE/STUDY_LEDGER.jsonl \
  --out experiments/artifacts/rc005-exposure/P0_PREPARATION

# 重新读取同一来源，验证已有准备包等价；不覆盖输出。
python3 -B experiments/rc005_exposure.py check \
  --run experiments/artifacts/rc005-native/HISTORICAL_RUN \
  --ledger /PRIVATE/STUDY_LEDGER.jsonl \
  --out experiments/artifacts/rc005-exposure/P0_PREPARATION
```

`--ledger` 必须显式提供，始终只读。本工具不构造 `Ledger`、`Study`、`Child` 或 HTTP client。路径不得含 `..` 或 symlink，固定记录也不能通过 symlink 指向其他位置。只读取所需的具名文件，不递归扫描原 run。Output 必须与历史 run 分离，不能是原 run、其子目录或祖先，也不能包含源 ledger；输出已有无关文件时拒绝混放。

## 绑定检查与失败状态

准备输入前，工具逐项核对：

1. `plan.json` 与当前固定 `cells()` 的完整 144 个位置一致，coverage 无缺项、重复、越界或 cell metadata 改写；native 位置必须闭合为 complete 或有明确错误证据的 technical-failure。
2. Ledger 中唯一 binding 的 output、完整 fixture 与 upstream pin 匹配；`effective-config.json` 与已绑定配置相同。Fixture 在运行后被改动会拒绝，不能把新历史配给旧回答。
3. 每份成功 capture 与对应已完成 search operation 的原始 result 一致。若历史 RPC 没有 operation echo，单独标 `unavailable-historical-protocol`，不把它写成已核验的 echo；其固定 operation record、capture 及实际 search embedding query 仍须一致。
4. 历史投影与保存的 admitted context 相同；运行时 governing record 与当前 fixture、实际 answer operation 相同。
5. 原 reader dispatch 的 messages 与 context 完全相符，参数与原 study 一致；必须有唯一成功 return 绑定实际保存的回答。Native search 的每个 embedding attempt 都须符合完整固定 query／model／float payload，terminal return 不得歧义，且至少有一次成功、维度／finite／nonzero／batch index 合法的 encoder return。多次 attempts 保留，不默默挑一个看起来合适的不同 payload；失败或缺返回的正确请求不能借另一条错误 query 的成功响应完成绑定。

缺少绑定或任一项不一致就停止，不写新的 preparation，也不修写原 run。这里证明的是记录之间的一致性，不是签名 attestation、独立目击或所有文件未被协调改写的证明。

Technical-failure 单列在 native 54 位置分母中，不生成三臂输入或配对回答，也不计成语义零分。失败 capture、coverage 错误以及无 answer/context/reader dispatch 必须相符；同 variant／probe 还需有成功位置的 run-bound governing record。错误同时存在回答或 context 时先拒绝，要求 operator 明确处置。Pending／uncertain 不能被静默升级为完成。

## 输出、重复运行与解释

独立 output 只包含三个具名文件：

- `audit.json`：native 位置、成功／技术失败与准备请求分母；每个字段路径的 missing／null／empty／nonempty、JSON type 与三臂 dropped／exposed／missing 计数。已知 audit-interest 字段即使全缺失仍列出，同时纳入全部实际返回字段及嵌套路径；它不是通用 schema validator。空字符串、空 list／object 为 empty；0 和 false 是有类型的 nonempty 值。
- `paired-inputs.json`：每个成功 native capture 的三臂 body，状态为 `prepared-not-dispatched`。只把每项 `request` 作为未来请求 body；pair／arm／request ID 是本地编排标签，不进入模型输入。该包不是盲评 packet，也不包含语义判断、作者 key 或历史回答。
- `author-governing-map.private.json`：pair 与原 cell 对应、作者 probe evidence contract、governing record、原 capture/search、context、reader attempts/return 和 run binding。该文件含 evaluator-side 信息及本地运行细节，只供 operator 私有留存，不发送给 reader，也不和输入包一起交给 reviewer。

Output 以 exclusive create 写入，绝不覆盖既有不同内容。重复 `prepare` 在当前来源与全部已存在输出逐字一致时复用；`check` 要求完整已存在输出。任何内容变化、来源篡改或冲突文件都拒绝覆盖；若先前写入中断，只能在已有文件全部等价时补齐缺失文件。原历史 artifacts 始终只读。

字段丢失审计只能说明这份历史包装的 exposure 边界；不能直接说明 Mem0 是否保存了正确的共同创作来历，也不能证明 full-native 会提高回答质量。新的 provider 配对尚未由这个工具执行。后续如取得真实三臂输出，仍需分别记录实际请求、返回、技术失败、usage、语义评审与替代解释，不能让本次准备状态替代 receipt。

## 离线验证

```bash
python3 -B -m unittest discover -s tests -p 'test_rc005_exposure.py' -v
python3 -B tools/check_repo.py
python3 -B -m unittest discover -s tests -v
```

测试使用公开原创 synthetic records，覆盖原投影序列化、原生类型／顺序／missing-null 保留、格式控制不增信息、绑定变更拒绝、symlink／路径越界、零 HTTP／零 subject、技术失败分母以及不可变重复准备。它们不证明真实 run 已通过该审计，也不验证新的 reader 配对效果。
