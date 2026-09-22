# Relata · Memory Architecture Atlas

**研究日期：** 2026-09-22 · **状态：** source-study drafts；独立人类 review 待完成。

## 中文摘要

十个公开 memory / agent 项目，每个三幅架构图：**全景与边界、写入到使用、修订与控制**。图集让读者追踪过去保存在哪里、经谁选择而进入当前 context，以及改变一处后哪些派生状态继续保留、等待刷新或不在已读边界内。它是带源码证据的研究表达，不是完整系统审计、部署图或性能排行榜。

## English summary

Thirty architecture views compare ten pinned public-source implementations. Each project has a boundary overview, a write-to-use flow, and a revision/control view. Nodes, relations, regions and state ownership link to exact source revisions; static observation, inference and unknown boundaries remain distinct. The atlas is an offline research reader with portable SVGs and editable Mermaid topology. It introduces no upstream execution, provider integration or performance claim.

## 打开与阅读

**[离线交互 reader：index.html](index.html)**。下载或 clone 本仓库后，用浏览器直接打开这个文件。HTML 已嵌入模型、SVG、样式与脚本，图集本身无需网络、server、账号或依赖安装。访问源码、研究文档或下载 Mermaid 时会打开所选链接；相邻文件需保留仓库目录关系。GitHub 的 HTML 文件页不运行 reader，可直接从下面打开 SVG。

左侧按项目或机制搜索，上方切换三视图。点击导读或详细图的节点，或使用节点列表，查看职责、状态、相邻箭头与 evidence；相关连线会高亮。每条关系也在下方完整列出。`阅读` 使用可读字号，窄屏可横向滑动；`适宽` 与 `全图` 用于定位，`＋/−` 控制缩放。SVG 可独立下载和放大，节点链接打开其首条固定源码；完整多条证据在 reader 中展开。Mermaid 保留可编辑拓扑，自动排版可能不同。

每张图保留主路径导读和详细状态/关系。`N` 为本图节点号，`E` 为关系号：源端列出动作及目标，目标箭头重复同一 E 编号。编号供沿图定位，不是跨项目 ontology；稳定对象 ID 在 JSON 模型中。跨区长线可按两端编号追踪，不能只按空间邻近推断关系。

## 三十幅图

| 项目 / 源码研究 | 固定版本 | 全景与边界 | 写入 → 使用 | 修订与控制 |
|---|---|---|---|---|
| [Aelios](../source-studies/aelios.md) | [`9e65c80`](https://github.com/wusaki0723/Aelios/commit/9e65c802ec1c13a68d22a68c5c9d7cdce385e041) | [SVG](diagrams/aelios/overview.svg) · [Mermaid](diagrams/aelios/overview.mmd) | [SVG](diagrams/aelios/flow.svg) · [Mermaid](diagrams/aelios/flow.mmd) | [SVG](diagrams/aelios/revision.svg) · [Mermaid](diagrams/aelios/revision.mmd) |
| [Mem0](../source-studies/mem0.md) | [`a39a802`](https://github.com/mem0ai/mem0/commit/a39a802bbc93e85b820078cd3c4dbaf53af25dbe) | [SVG](diagrams/mem0/overview.svg) · [Mermaid](diagrams/mem0/overview.mmd) | [SVG](diagrams/mem0/flow.svg) · [Mermaid](diagrams/mem0/flow.mmd) | [SVG](diagrams/mem0/revision.svg) · [Mermaid](diagrams/mem0/revision.mmd) |
| [Letta Code](../source-studies/letta.md) | [`f5c5bbc`](https://github.com/letta-ai/letta-code/commit/f5c5bbce6e9394b30c626909315c2b3acc665672) | [SVG](diagrams/letta/overview.svg) · [Mermaid](diagrams/letta/overview.mmd) | [SVG](diagrams/letta/flow.svg) · [Mermaid](diagrams/letta/flow.mmd) | [SVG](diagrams/letta/revision.svg) · [Mermaid](diagrams/letta/revision.mmd) |
| [Graphiti](../source-studies/graphiti.md) | [`16cdf70`](https://github.com/getzep/graphiti/commit/16cdf7045378c8d53ae01f94e2fa60d238cb0f68) | [SVG](diagrams/graphiti/overview.svg) · [Mermaid](diagrams/graphiti/overview.mmd) | [SVG](diagrams/graphiti/flow.svg) · [Mermaid](diagrams/graphiti/flow.mmd) | [SVG](diagrams/graphiti/revision.svg) · [Mermaid](diagrams/graphiti/revision.mmd) |
| [lmc-5](../source-studies/lmc-5.md) | [`fb3e72c`](https://github.com/wuxuyun0606-collab/lmc-5/commit/fb3e72c9ee7357c8b17311097b0750082a8a1237) | [SVG](diagrams/lmc-5/overview.svg) · [Mermaid](diagrams/lmc-5/overview.mmd) | [SVG](diagrams/lmc-5/flow.svg) · [Mermaid](diagrams/lmc-5/flow.mmd) | [SVG](diagrams/lmc-5/revision.svg) · [Mermaid](diagrams/lmc-5/revision.mmd) |
| [Tideline Memory](../source-studies/tideline-memory.md) | [`76490fe`](https://github.com/ennisaaaaaaaa-stack/tideline-memory/commit/76490fe2c422f1213e735e63c289fef5ae8044f6) | [SVG](diagrams/tideline-memory/overview.svg) · [Mermaid](diagrams/tideline-memory/overview.mmd) | [SVG](diagrams/tideline-memory/flow.svg) · [Mermaid](diagrams/tideline-memory/flow.mmd) | [SVG](diagrams/tideline-memory/revision.svg) · [Mermaid](diagrams/tideline-memory/revision.mmd) |
| [Hindsight](../source-studies/hindsight.md) | [`9c7f6c6`](https://github.com/vectorize-io/hindsight/commit/9c7f6c68c4ad26be5af5d5deef63b4873d1fbc55) | [SVG](diagrams/hindsight/overview.svg) · [Mermaid](diagrams/hindsight/overview.mmd) | [SVG](diagrams/hindsight/flow.svg) · [Mermaid](diagrams/hindsight/flow.mmd) | [SVG](diagrams/hindsight/revision.svg) · [Mermaid](diagrams/hindsight/revision.mmd) |
| [OpenViking](../source-studies/openviking.md) | [`bbf2e37`](https://github.com/volcengine/OpenViking/commit/bbf2e37f88b8b15482edb83be41feb3ed510d03a) | [SVG](diagrams/openviking/overview.svg) · [Mermaid](diagrams/openviking/overview.mmd) | [SVG](diagrams/openviking/flow.svg) · [Mermaid](diagrams/openviking/flow.mmd) | [SVG](diagrams/openviking/revision.svg) · [Mermaid](diagrams/openviking/revision.mmd) |
| [LangMem](../source-studies/langmem.md) | [`9d033b4`](https://github.com/langchain-ai/langmem/commit/9d033b47d9ce53e37e92c92241b0496c0278932e) | [SVG](diagrams/langmem/overview.svg) · [Mermaid](diagrams/langmem/overview.mmd) | [SVG](diagrams/langmem/flow.svg) · [Mermaid](diagrams/langmem/flow.mmd) | [SVG](diagrams/langmem/revision.svg) · [Mermaid](diagrams/langmem/revision.mmd) |
| [A-Mem (paper reproduction)](../source-studies/a-mem.md) | [`0c8039f`](https://github.com/WujiangXu/A-mem/commit/0c8039f28fdcc08189a23c07a3437d9d2482f9c2) | [SVG](diagrams/a-mem/overview.svg) · [Mermaid](diagrams/a-mem/overview.mmd) | [SVG](diagrams/a-mem/flow.svg) · [Mermaid](diagrams/a-mem/flow.mmd) | [SVG](diagrams/a-mem/revision.svg) · [Mermaid](diagrams/a-mem/revision.mmd) |

## 证据怎样读

- **已读源码 / observed**：固定 commit 上检查到的实现；不是运行观察。状态颜色和形状区分存储、模型、选择/控制、入口、输出与外部对象；文字同时说明类型。
- **推断 / inferred**：由已读机制提出的条件性连接；虚线及文字保留其状态。
- **未知 / unknown**：外部调用方、未审计组件或不能成立的运行主张；不将其画成原生能力。
- 源码锚点可以证明“有这条代码路径”，不能证明已安装、被触发、语义正确或优于另一个系统。关系被画出也不代表它跨所有配置成立。

十份模型共列出 391 条 pinned source anchors。每份研究报告说明具体 read scope、版本差异、竞争解释与未覆盖部分。Hindsight、OpenViking 等项目的模型/队列配置不同；lmc-5 的 minimal 与 production reference、Letta 当前 local backend 与历史产品、A-MEM 论文实现与另一个 A-mem-sys repo 均不能混合。两份既有[离线源码观察](../source-studies/README.md#离线观察复现)仍是单独证据，没有因为新增图示而扩大为全系统试验。

## 编辑与重建

`models/*.json` 是图的语义真源：project boundary、节点、关系、区域、状态归属和 pinned evidence。`guide-layouts.cjs` 选择每图已有关系组成导读；`render-guide.cjs` 与 `render-svg.cjs` 负责布局和绘制，`build.cjs` 负责验证与生成。`viewer.html`、`viewer.css`、`viewer.js` 是 reader 源码。`diagrams/<project>/{overview,flow,revision}.{svg,mmd}` 与 `index.html` 都是 generated artifacts；修改模型或 renderer 后重建，不手改图，也不在报告内维护另一份手绘 topology。

从 repo root 用 Node.js 运行，无额外 package 或网络依赖：

```sh
node systems/architecture-atlas/build.cjs
node systems/architecture-atlas/build.cjs --check
python3 -B tools/check_repo.py
python3 -B -m unittest discover -s tests -v
```

CI 运行同一个 `--check`，核对模型和生成物一致性；它不验证源码语义或视觉质量。模型涉及的 view 变化后，需实际打开 SVG/reader，检查主路径、反馈/删除路径、文字和连线、缩放及 evidence interaction。模型采用三种阅读视角便于比较，不固定上游内部 ontology，也不是 system-under-study API。

研究解释由[十项目比较](../source-studies/README.md)和[agent-memory inquiry](../../research/agent-memory-inquiry.md)承担。图集只画公开、固定版本的实现；未载入私人 memory、社区聊天或真实使用者数据。
