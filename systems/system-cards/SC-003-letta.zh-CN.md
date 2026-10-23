[English](SC-003-letta.md) | **简体中文**
<!-- language: zh-CN; mirror: SC-003-letta.md; translation-status: synchronized -->

# System Card：Letta（当前 OSS local backend）

**Card ID：** SC-003\
**Status：** source-reviewed\
**Basis：** public-source\
**Visibility：** public\
**Contribution ID：** not applicable（公开源码分析）\
**Contributor attribution：** 不适用；这是 Relata 独立源码分析，不代表维护方声明或背书\
**Source analyst / contributor authority：** Relata 源码分析者；仅对照既有固定版本 source study 与 atlas 做忠实性核对\
**Exact version or observation date：** `letta-ai/letta-code` commit `f5c5bbce6e9394b30c626909315c2b3acc665672`（`package.json` 0.32.17）；source study 日期 2026-09-22；card fidelity review 日期 2026-10-23（对照既有 studies/atlas）

> 这不是产品评分卡。先按系统自己的术语描述，再翻译成 Relata 的拟议边界。

## 中文摘要

当前 Letta 的 local backend 是一个 stateful agent harness：conversation 的原始消息记录与压缩事件、Git 管理的可修改 MemFS，以及供后续调用使用的编译后 system prompt。模型可通过 `memory` 工具改写文件并按路径 commit，每个 turn 检测 Git revision 变化并把新编译结果作为 system 消息追加。本地检索是 FTS-lite，没有向量索引；记忆内容的演化变成普通文件与 Git 操作，但 Git 可追溯不等于事实归属或遗忘保证。本 card 绑定固定公开 commit 的静态源码，不代表运行或语义效果。

## English summary

The current Letta local backend is a stateful agent harness built from three persistent objects: a conversation’s raw message record and compaction events, a Git-managed, editable MemFS, and a compiled system prompt used by later calls. The model can rewrite files through the `memory` tool and commit by path; each turn compares the compiled version with the current Git revision and appends the new memory update as a system message. Local search is FTS-lite, with no vector index. Memory content evolution becomes ordinary file and Git operations, but Git traceability is not fact attribution or a forgetting guarantee. This card binds a pinned public commit’s static source and claims no runtime or semantic outcome.

## 1. 系统身份与范围

- 主要用途与关系/agent 角色：通过改写 memory、skills、prompts 与 mods 跨调用保留身份与经验的 stateful agent harness；不是独立 memory service。
- local / hosted / mixed：当前 OSS 有 local 与 Cloud 两个 backend。本 card 覆盖 local backend；Cloud 是另一边界，其托管数据库、检索、删除保证与线上可用性不在此确认。
- 包含组件：conversation 消息持久化（`conversation.json`、`messages.jsonl`，带 `parentId` 与时间戳）；`memory` 工具（`create`、`str_replace`、`insert`、`delete`、`rename`、`update_description`）；带 agent author 与 reason 的 Git commit；本地 system-prompt compiler；FTS-lite transcript 检索；turn 末压缩。
- 明确排除：已 retired 的 `letta-ai/letta` archive 与 V1 API server、旧 MemGPT 工具与数据库层次、channels、多用户授权、shared memory、permission confinement、Cloud backend 及全部迁移/恢复路径。
- 当前成熟度：固定 commit 上的当前 OSS 源码快照。
- 可用证据：公开源码（静态检查）。

## 2. System-native map

```text
turn input -> message {id, role, timestamp, agent_id, conversation_id}
  -> 持久化 conversation.json + messages.jsonl（parentId 链）
  -> 模型可调用 memory(create/str_replace/insert/delete/rename/update_description)
       -> 检查工作区、改文件、以 agent author 与 reason 做 git commit
  -> 编译 committed Markdown：persona -> <self>，system 文件 -> <memory>，external 目录只列树
  -> 每个 turn：比对已编译 revision 与当前 Git revision；变化时生成 memory update
  -> stream adapter 把 update 作为 system 消息追加（保留原始 system prompt）

长 conversation -> compaction：模型摘要 + 保留尾部；transcript 追加 compaction 事件
本地 recall -> agent/conversation + 日期 + hidden 过滤，FTS-lite 匹配（无本地向量索引）
```

本地 MemFS 强制为 v1（`system/*.md` 是 core）；非本地且存在根 `MEMORY.md` 才为 v2。v1/v2 是当前 MemFS 格式差异，不是 retired V1 API 的年代划分。

## 3. 持续性材料

保留内容：原始消息（role、时间戳、provider/model metadata、`parentId`）、compaction 事件、以 core/deferred/skills 分层的可编辑 Markdown memory 文件，以及派生 Git commit。agent 身份绑定 MemFS；conversation 绑定一段活动上下文，同一个 agent 的新 conversation 可复用同一份 memory。系统保留 transcript 与可编辑文件，而不是单一向量库。persona 文件与任意 memory 文件可表达内容边界，因此 personal-lived、shared-relational、operational/project 与 companion/system 材料都能写入，但结构不强制文件属于哪个域。

## 4. 变更与修复

- `memory` 工具按路径改文件并 commit，要求非空 reason 与 agent author。`memory delete` 删除目标文件或目录并 commit；`rename` 移动路径。该工具路径没有到 transcript、既存摘要、其他 memory 文件中的复述或 Git history 的级联。
- 完整编译会从新 content 中排除已删除文件；常规 turn 在 raw system hash 相同、MemFS revision 变化时则保留旧 content，更新 core/revision 并追加 memory update。同一 conversation 的旧文字因此未必退出输入，完整重编译与追加覆盖指示应分开；两者都不等于全系统遗忘。
- Cloud 同步可出现 dirty、conflict 或 push_failed；非快进时尝试 rebase 后 push，失败状态会返回。
- 可静默失败之处：若模型把“同事喜欢咖啡”概括成“用户喜欢咖啡”，Git 会忠实记录错误概括；除非正文自觉保留引用，结构不会纠正归属。

## 5. 唤起与使用

本地编译器用 `git ls-tree HEAD` 与 `git show HEAD:path` 读取 committed Markdown；每个 turn 比对已编译版本与当前 Git revision，revision 改变时生成新的 memory update，由 stream adapter 作为 system 消息追加。这不是编辑磁盘后当前推理立即重写，也不能单凭代码断言模型遵循了新规则。长 conversation 的 compaction 保留模型摘要加尾部，并追加 compaction 事件，而不是直接删除早期记录。本地 recall 匹配无法区分“系统没有记忆”“词汇不匹配”“scope 错误”“模型没搜索”或“原本没写入”。

## 6. 来源、权威与视角

Git revision、diff、commit reason、文件正文、conversation/message ID 与时间戳提供较强的操作级可检查性；role 区分 user、assistant、toolResult，并携带 provider/model metadata；搜索结果可回到 conversation 与 message。这些是消息与操作来源，不是事实级来源。MemFS frontmatter 主要为 `description`/`read_only`/`limit` 或 `name`/`description`，没有强制事实级 source、speaker、valid-time 或支持证据 ID。因此 Git 会忠实记录模型的概括，包括错误归属，除非正文本身引用了来源。

## 7. 时间

消息携带 `timestamp`，compaction 事件按时间顺序追加。memory 层没有显式区分事件时间与记录时间；时间主要以消息顺序与 commit history 进入。历史材料留在 transcript 与 Git history，但结构本身不把旧材料明确当作非当前指引。

## 8. Surfaces、模型与身份

`agent` 与 `conversation` 是技术 scope，本身不等于家庭、客户、项目或亲密关系 scope。消息携带 provider/model metadata，Cloud 同步跨机器且有其时序。文件结构与 prompt 可表达内容边界，但本研究未证明其能确定性阻止跨域泛化。多个项目、角色、人与 surface 仅在 harness 把它们映射到 agent/conversation 的范围内被隔离。

## 9. 前瞻行为

所检查路径未建立本地的未来触发、提醒或唤醒行为。scheduler 与 reminder 不在本 card 的 review 边界内，因此前瞻行为标为 unknown 而不作断言。

## 10. Contributor control 与用户主权

记忆演化是普通文件与 Git 操作，便于人与 agent 检查、修订与迁移。原始经验与压缩后的工作上下文分离，摘要遗漏后可再查。但删除应拆分为纠错、撤回可用性与数据清除；没有证据显示存在全系统语义级撤回闭包。Cloud 状态在技术与制度上仍不透明。

## 11. 已知成功与失败

SOURCE-OBSERVED（静态、固定版本）：三个持久对象与清晰编译步骤；模型与人可编辑且带 reason 的 memory；revision 触发的追加 update 或完整重编译；原始 transcript 与压缩上下文分离；FTS-lite 本地检索（明确不是向量/hybrid）。竞争解释是：它是一套可编程 context management，“学习”可指未来提示改变；这不贬低工程价值，但不能替代行为改善的证据。UNVERIFIED：线上性能、召回率、跨进程一致性、长期关系效果、托管删除保证与全局权限安全。

## 12. 候选 Relata 边界上的可观察性

图例：`N` native · `E` adapter-emulated · `O` opaque · `U` unsupported · `?` unknown · `—` not applicable（定义见 [`systems/README.zh-CN.md`](../README.zh-CN.md)）。

| 候选观察 | 类别 | 证据 | 失真说明 |
|---|---:|---|---|
| ordered history exposure | N | source study，“一条写入、保留、使用与修订路径”（messages.jsonl） | 按 conversation 排序加 `parentId` |
| distinct ingest/write output | N | source study，“一条写入、保留、使用与修订路径”（memory 工具） | 文件编辑加 Git commit |
| retrieval/activation material | N | source study，“可检查性、来源与控制”（FTS-lite recall） | 关键词/短语匹配，无本地向量 |
| rendered model context | N | source study，“一条写入、保留、使用与修订路径”（编译 prompt） | 原始 system prompt 一并保留 |
| final response or action | N | source study，“结论与对象边界”（stateful harness） | 模型/provider 在外部，但 harness 运行它 |
| correction/revocation route | N | source study，“修改、删除及派生影响”（`memory delete`） | 无到 transcript 或 Git history 的级联 |
| inspection/explanation route | N | source study，“可检查性、来源与控制” | Git diff/reason 与 message ID |
| time advance or future wake | ? | source study，“覆盖与未验证” | scheduler 未 review；不作断言 |
| full-history or full-search exposure | N | source study，“一条写入、保留、使用与修订路径”（transcript） | transcript 可检索；有 compaction 边界 |
| multi-project isolation | O | source study，“可检查性、来源与控制” | agent/conversation scope，非 project scope |
| artifact/source authority | O | source study，“可检查性、来源与控制” | 消息来源不是事实权威 |
| role/surface routing | O | source study，“可检查性、来源与控制” | 无自动 role/surface 路由 |
| cross-domain context contamination | O | source study，“可检查性、来源与控制” | 结构不阻止跨域泛化 |

## 13. 候选 Relata probes

本 card 可对 D-005（identity continuity across migration）与 D-002（authority without narrative theft）施加压力：source study 提议归属与时效双重修订 probe（A 说 B 喜欢咖啡、A 以前喝咖啡现在不喝；后续项目聊天只提给 B 带咖啡）与删除残留 probe（合成偏好写入 core、external reference 与摘要，再在三种条件下撤回未来使用）。保留系统的 lane 是本地 compile 加 Git 边界：观察原始 role/time、memory diff、编译 context、检索调用与回答，并把 Cloud 行为单列。

## 14. 保密与发布限制

仅公开源码。不得读取或发布私人 memory、Cloud 内部或凭据，不得暗示 Letta 背书，也不得把本地结论扩展到 Cloud 或 retired archive。

## 15. 来源 / contributor review

- 系统描述对既定用途足够准确：yes
- review 依据与检查的源码路径：对照核查 [`systems/source-studies/letta.md`](../source-studies/letta.md) 及其固定 commit 证据索引；图模型 [`letta.json`](../architecture-atlas/models/letta.json)
- Public-safe contributor-derived fields approved：not applicable（仅公开源码）
- 保留的分歧或未知：local 与 Cloud 边界；reflection 生命周期未完整阅读；前瞻行为不作断言；全部运行与语义效果 UNVERIFIED
- Review date：2026-10-23
- Reviewer / contributor confirmation route：Relata source-fidelity review；无 contributor 确认适用
- Review 限制：本轮 2026-10-23 仅核对既有 source studies 与 atlas models 的一致性；未重读全部 upstream 链接、重跑离线核对或执行系统。此前 2026-10-14 review 来源未能建立，不予追认。
