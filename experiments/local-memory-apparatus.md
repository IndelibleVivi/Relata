# Local Memory Apparatus — 工程实验记录

**Status:** very early engineering experiment，2026-09-26；已实现并局部检查，范围纠正后保留；没有 accepted architecture 或 capability result。
**Scope correction:** [ADR-0007](../decisions/ADR-0007-local-memory-apparatus.md) 已撤回把长期 goal 当作实现授权的解释；本记录保留实际工程证据，不提供后续实现权限。
**System:** 独立本地 repository `relata-memory`（历史工作名）；Python 标准库与 SQLite。不是正式 Tilia。
**Code revision:** `99f673f95770215b186e7d2530122ad50b04a42b`，该 repo 的首次本地 commit。
**Publication:** 源码尚未公开发布、无 remote、未选择公共 license；本文不是公共代码已可独立复现的结果包。

## 中文摘要

本实验将[候选 B](../research/own-memory-architecture.md)的部分状态责任推进成明确操作的本地装置，走通输入、持久化、修订、派生状态、字面检索、context 消费与恢复。操作与内容均为人工编写的 synthetic development material，consumer 为脚本。所记录代码通过 110 项工程测试与一套 38 个 CLI 步骤、21 项断言的 demo；每个 CLI 步骤都是新进程。它验证构造场景中的 revision、scope、失效、输入暴露和恢复机制，不能测自动抽取、语义回答质量、长期连续性或架构比较收益；现有 Case Lab 状态不变。未来独立装置以 Tilia 为名，需要向量语义检索；现有实验未实现这项能力，保留它不表示设计已被接受。

## English summary

This very early local experiment implements selected responsibilities of candidate B with explicit operations, literal search, a persistent store and a scripted consumer. The recorded code passed 110 engineering tests and a 38-step subprocess demo with 21 assertions. Checks cover constructed revision, scope, invalidation, input-exposure and recovery scenarios. They do not establish automatic extraction quality, semantic response quality, longitudinal continuity, comparative benefit or Case Lab acceptance. The code is retained after correcting an implementation-scope misinterpretation; it is locally committed but not publicly published. It is not formal Tilia and lacks the vector-based semantic retrieval required for that independent goal.

## 问题与实现边界

装置闭合「输入与来源/scope → 持久保存 → 检索/context → 实际脚本消费 → 局部修订 → 重启后继续使用」，同时提供检查、导出恢复与三个独立对照读者。使用本地可信 caller、显式操作、单个 SQLite store。Scope 过滤不等于身份认证；作者与接受字段是输入声明，不是装置证明的社会事实。

原始材料和 revisions 属于 canonical state；view 是明确声明输入依赖的派生内容；packet 是选中正文、来源状态和 revision 的快照。派生发布与 context 保存各自使用受保护事务，消费前重新读取当前状态。两张实现图及可编辑 Mermaid 源图位于该 repo 的 `docs/architecture.md`、`docs/figures/`；它们与 Relata 中的 proposed 设计图、十项目 source atlas 分开维护。

## 命令与实际观察

验收环境为 Python 3.13.3 / SQLite 3.53.4。在独立实现的 checkout 内执行：

```bash
python3 -B -m unittest discover -s tests -v
python3 -B demo/run_demo.py --out local/accepted-demo-20260926
```

最终相关代码编辑后，完整 suite 两次通过，均为 **110 tests / OK**。单独 demo 返回 **38 CLI steps / 21 invariant checks / OK**，生成 `summary.json`、逐步 JSON、原始输入日志、活动数据库、导出和恢复库。再次运行必须选择全新的 `--out`；工具不覆盖既有演示。生成物保持本地且不进 Git。协调者另以 CLI 重放了 13 个输入／文件／恢复反例，均通过；这组本地复查不增加科学样本数。

| 边界 | 本次实际检查 | 结论的范围 |
|---|---|---|
| canonical mutation | 迟到旧 revision 拒绝；失败事务回滚；交错写入；局部修改保留同 scope 与另一 scope 邻居 | 构造的事务与版本场景；没有模拟断电或全类存储故障 |
| 派生发布 | job 状态在写事务内复核；同 job 不重复发布；不能跨 scope 覆盖；多层失效；metadata-only acceptance 使旧 job/view 失效 | 显式输入和依赖；不证明派生内容忠于原文 |
| context 与消费 | 组装/持久化共同提交；拒绝擦除前选出的旧内容重新入库；拒绝过期 packet 和重算 digest 后伪造的 provenance/standing | 本地一致性；不是对数据库所有者的安全认证 |
| 历史依赖与清除 | republish 更换输入后仍找到含旧来源的库内 packet；清空指定正文与受影响派生 payload；保留无关原始邻居 | 采用历史依赖的保守并集，可能额外失效或清空已换源的当前 view；外部副本不受影响 |
| 真实重启 | 提交、修改和再次读取分别由新 CLI 进程执行，重启后使用修订内容 | 实际进程边界；不是长时段连续性或 companion identity 实验 |
| export/restore | 单读取快照；拒绝覆盖 DB/已有输出；恢复竞态不覆盖新出现的文件；拒绝错误 current 指针、scope、引用及缺失 packet 索引；有效逻辑状态往返一致 | 当前 schema 的结构与引用检查；不证明所有语义一致性 |
| 原始输入与回执 | 保留被拒旧稿、接受依据、reopen、view 手工输入及 context 条件；输出/日志在提交后失败时报告已提交状态 | 日志与 SQLite 是两个文件，不声称原子提交；未进行多进程原始日志压力测试 |
| 选择与预算 | 中文子串查询、确定性排序、截断、UTF-8 字节计量 | 只计算选中正文；不包含 metadata、格式与 current request，不是 token/context 总预算 |

## 独立对照看到什么

- `current-only` 只接收显式 current request，完全不读取历史。当前请求本身是否足够回答，需具体语义实验判断。
- `raw-history` 从独立 JSONL 读取已记录的 memory 输入，包括被拒的写入／发布；按输入顺序暴露完整 input 对象。整库管理命令不属于这份历史。Scope 过滤、是否额外带 outcome/exposure 诊断均显式标注。
- `file-search` 对同一 JSONL 的 `content` / `payload` 正文字段作字面检索与正文预算截断；不搜索 `basis`、`note` 或其他 metadata，不能叫完整日志的全文检索。未截断原始历史仍是独立对照。

手工提供的 view payload 同样进入原始日志，不能让结构化路径独享额外人工输入。以上只展示不同 exposure，不比较语义正确率，也不把更短输入视为更优架构。

## 与研究问题的连接

该实验主要连接 [test map](../research/memory-design-test-map.md) 的 X2（进程重启）、X3（revision）、X5（scope）、X7（局部修改与邻域保留）、X9（派生失效）和 X10（可检查的使用）。这些是机械部分，不能自动证明完整语义版本。X1 历史必要性、X4 语义归属、X6 回应适当性、X8 prospective memory 与长期效用仍需各自的研究。

此次实现使三类设计问题变得具体：正文 revision 不足以代表接受状态；当前依赖不足以定位历史副本；恢复时丢失引用关系会改变后续清除行为。这些是自有实现的工程反例，不是关于所有 memory 架构的普适结论。

人工写入操作不等于自动抽取成功，脚本展示材料不等于 agent 正确使用。原始日志、export、已输出 packet 都是独立副本，数据库内清除不召回它们。没有模型/provider 执行、私人材料导入、上游系统比较、既有 Case Card 升级、完整文章、正式 release 或部署。
