# System Cards

Suggested naming:

```text
SC-001-<system-name>.md
```

Restricted cards and identifying consent records must not be committed to the public repository. A contributor-approved public summary may omit implementation secrets while preserving enough evidence to explain observability, adapter reconstruction, and boundary distortion.

Use the card states `draft`, `source-reviewed` (bounded public-source fidelity review), `contributor-reviewed`, `accepted-for-census`, and `superseded`. Source review does not imply contributor approval, independent human review or runtime evidence. `Accepted-for-census` authorizes the declared comparison use; it is not a quality rating or general endorsement.

## 当前静态集合 / Current source collection

| Card | Public source and boundary | Status |
|---|---|---|
| [Mem0](SC-001-mem0.md) · [中文](SC-001-mem0.zh-CN.md) | Python OSS memory library; caller supplies final reader | source-reviewed |
| [Graphiti](SC-002-graphiti.md) · [中文](SC-002-graphiti.zh-CN.md) | temporal graph library; raw retention is configurable | source-reviewed |
| [Letta](SC-003-letta.md) · [中文](SC-003-letta.zh-CN.md) | file/Git-first current pinned architecture | source-reviewed |

三张 cards 基于已有 source studies 与 atlas 的有界核对；没有重读全部 upstream 或运行系统。十系统 [pressure map](../architecture-pressure-map.md)（[中文](../architecture-pressure-map.zh-CN.md)）逐项解释机制、观测空缺和 adapter 压力。Technical scope、version history、maintenance scheduling 分别不等于完整权限、决定权或未来意向保证。

The cards preserve pinned source boundaries and unverified stages. The pressure map identifies mechanisms and observation limits; it supplies no product ranking or proof of working full-history controls.
