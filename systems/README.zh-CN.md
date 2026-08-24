**简体中文** | [English](README.md)
<!-- language: zh-CN; mirror: README.md; translation-status: synchronized -->

# Relata System Census

System Census 在 Relata 选择 system-under-study boundary 之前，先描绘真实 memory / companion systems 怎样维持 continuity。

Census object 可以是 memory engine、context compiler、完整 companion agent、local personal stack、manually curated archive、agent framework 或 mixed architecture。System 不必暴露 discrete memories、retrieval candidates 或 write/search API，仍可被表示。

## Classification

- `N` — system-native，且已 observed 或 contributor-confirmed；
- `E` — 在 native boundary 外 adapter-emulated；
- `O` — 在 selected boundary 下 opaque；
- `U` — represented system/version 不支持；
- `?` — unknown 或未检查；
- `—` — 对此 architecture 不适用。

`O`、`U`、`?` 是不同 findings，均不等于“inferior”。

## Census workflow

1. **Permission and scope：** 确认 contributor 是否有 authority 描述 system、exact version/date、visibility 与 forbidden details。
2. **System-native description：** 用 system 自己的 vocabulary 描述 components、retained/reconstructed material、update / activation behavior、surfaces 与 outputs。
3. **Evidence and limits：** 分开 public source、contributor-reviewed description、reproduced probe、inference 与 unknown behavior。
4. **Contributor review：** 让 authorized contributor correction System Card，并批准 public-safe fields。
5. **Boundary pressure：** individual cards reviewed 后，才放进 Architecture Pressure Map 比较。
6. **Research transfer：** 记录 proposed Relata boundary 测到的是 system、adapter、opaque composite，还是 out-of-scope capability。

Census 不要求 source code、production access、credentials、raw chats 或 private configuration。Restricted cards 留在 public repo 外；只有 contributor-approved summaries 可以加入。

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
