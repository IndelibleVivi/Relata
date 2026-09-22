**简体中文** | [English](README.md)
<!-- language: zh-CN; mirror: README.md; translation-status: synchronized -->

# Relata System Census

System Census 研究真实 memory / agent systems 怎样工作、架构选择带来什么可能性或约束，以及怎样维持 continuity。它既支持独立的比较研究，也帮助未来选择 system-under-study boundary。通用 agent 使用情境与成人长期亲密关系都在范围内；从 [agent-memory inquiry](../research/agent-memory-inquiry.md) 进入。

Census object 可以是 memory engine、context compiler、完整 companion agent、local personal stack、manually curated archive、agent framework 或 mixed architecture。System 不必暴露 discrete memories、retrieval candidates 或 write/search API，仍可被表示。

[十份源码研究](source-studies/README.md) 固定 Mem0、当前 Letta、Graphiti、lmc-5、Tideline Memory、Aelios、Hindsight、OpenViking、LangMem 与 A-MEM 的公开 commits，包含有条件的架构比较与两组窄范围离线观察。[架构图集](architecture-atlas/README.md) 为每个项目提供三幅绑定源码的视图，含独立 SVG 和离线交互 reader。它们保持 source-study draft 状态，不等于 reviewed 或 accepted System Cards。

## Classification

- `N` — system-native，且已 observed 或 contributor-confirmed；
- `E` — 在 native boundary 外 adapter-emulated；
- `O` — 在 selected boundary 下 opaque；
- `U` — represented system/version 不支持；
- `?` — unknown 或未检查；
- `—` — 对此 architecture 不适用。

`O`、`U`、`?` 是不同 findings，均不等于“inferior”。

## Census workflow

1. **Basis and scope：** 选择公开源码研究、获授权的 contributor description，或明确分开的两者组合。固定 repository/version，区分公开实现、托管服务与历史源码。对 contributor material 确认 disclosure authority 与 forbidden details。
2. **System-native description：** 用 system 自己的 vocabulary 描述 components、retained/reconstructed material、update / activation behavior、surfaces 与 outputs。
3. **Evidence and limits：** 分开 public source、contributor-reviewed description、reproduced probe、inference 与 unknown behavior。
4. **Review：** 公开源码 card 接受 source-fidelity review，保留已读路径与未解决 claims；不要求、也不暗示 maintainer endorsement。来自 contributor 的材料还需要 authorized contributor 修正描述并批准 public-safe fields。
5. **Boundary pressure：** individual cards reviewed 后，才放进 Architecture Pressure Map 比较。
6. **Research transfer：** 记录 proposed Relata boundary 测到的是 system、adapter、opaque composite，还是 out-of-scope capability。

Census 不要求 production access、credentials、raw chats 或 private configuration；contributor 描述的系统不必公开 source code。Restricted cards 留在 public repo 外，公开摘要需 contributor approval。独立分析已经公开的来源，不需要 system owner 批准，也不能暗示 insider knowledge 或 endorsement。

架构判断应带着条件：机制使什么成为可能、引入什么成本或限制、谁补上缺少的集成，以及每项说法的证据。Source inspection 与 runtime observation 分开；上方 classification 不是性能等级。System Card review 尚未完成时，source essay 可以明确保持 draft 状态。

每张 first-round System Card 还应追问：

- Ordinary personal history 与 operational/project history 如何被表示（若有）？
- Multiple projects、roles、people、surfaces、accounts 与 instances 怎样隔离或连接？
- System 怎样决定 personal、relational 或 operational material 是否进入 current context？
- Full-history / full-search exposure 下会发生什么？哪些 native boundaries 会让该 comparison meaningful 或 distorted？

从[中文](system-card-template.zh-CN.md)或 [English](system-card-template.md) System Card 开始，再使用 [Architecture Pressure Map](architecture-pressure-map-template.md)。

## Source evidence 打开的第一批 pressure dimensions

[`EC-001`](../research/evidence-cards/EC-001-agent-memory-leaderboard.md) 不为 Relata 选择 interface；它提供第一组需要跨 materially different systems 测试的 concrete boundaries。第一张 Architecture Pressure Map 必须 classify 而不能 assume：

- synchronous ingestion 与 immediate search visibility；
- external chunking 对 system-native episode/session boundaries；
- `user_id` / `session_id` 作为 isolation / organization surfaces；
- Search 是否看到 question 与 answer options；
- discrete、textual、relevance-ordered evidence 与 fixed Top K；
- correction、revocation、expiry、provenance、authority 与 disagreement semantics；
- final-answer generation 位于 system-native boundary 内还是外；
- public version identity，以及绑定 result 的 evidence；
- multi-project isolation 与 cross-domain context contamination；
- artifact/source authority 与 decision supersession；
- role/surface routing 与 full-history behavior。

这些是 pressure questions，不是 required capabilities 或 scoring dimensions。
