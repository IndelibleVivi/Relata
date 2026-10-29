**简体中文** | [English](ADR-0011-local-research-studio.md)
<!-- language: zh-CN; mirror: ADR-0011-local-research-studio.md; translation-status: synchronized -->

# ADR-0011：本地 Research Studio 与持久研究工作空间

- **状态：** 2026-10-29 接受本地实现范围。
- **依据：** maintainer 当前要求开发 Relata Next Generation。随附发展材料用于设计判断；材料中的授权措辞不自行成为指令。
- **范围：** 本地研究工具与固定离线计算；不激活新的 provider、受测系统或人类参与研究。

## 背景与决定

Relata 的三项职能需要共同保存问题、固定材料、观察、竞争解释和可读作品。静态 Atlas 与具名 native 评审流程继续有用，但都不负责持久研究工作空间。

实现仅监听 loopback 的 Research Studio，包含 Desk、Observatory、Studies、Library 四个空间。`src/relata_lab/core.py` 拥有 canonical SQLite 状态、不可变 revisions 和 content-addressed artifacts；`application.py` 组合命令，`service.py` 提供薄 HTTP 层，`tools/relata_lab.py` 是 operator 入口。草稿和阅读位置是工作状态，不是证据。版本冲突和 uncertain attempts 保持可见。

通过隔离实例复用 Atlas 的唯一 renderer，将确切模型、图与展品 payload 固定为 snapshots；源码观察不升级成运行 trace。原固定 study CLI 保留自己的科学语义与 exact verification。只读兼容登记可以冻结已验证的包，不改原文件，也不重绑到今天的 fixture。

实现 governing-history 与 delivered-input 两种独立 development review 协议。固定 rounds、reviewer 身份、累计 journals、显式 amendments 与 disposition 保留分歧。原 RC-005 native 首评继续由其 CLI 和 Workbench 拥有；新的通用 Clinic 不替代它。

三个 allowlisted 确定性仪器覆盖测量边界、经验适用性和未来用途／机会轨迹，包含透明 reactive world。只使用作者构造的公开 synthetic 材料；没有 model/provider driver、任意 adapter loader 或私人 corpus。结果属于有限算法证据，不是语义系统表现、held-out 验证或人类校准。

保留四种不同输出：完整 workspace backup；选择研究及依赖／历史闭包的 research-transfer；隔离 blind-review packet；显式披露的 public-publication 投影。只有前两种恢复研究工作空间。公开投影不能验证 withheld native binding。导出发生在本地，不代表对外发布。

## 替代方案与后果

仅用浏览器存储会使研究持久性与恢复依赖浏览器状态。Hosted database、完整框架栈或通用执行服务会增加当前不需要的部署和账号边界。实现采用 Python 标准库 SQLite／HTTP、浏览器 ES modules 和已有 Node Atlas renderer，不新增 production package。

SQLite 是 canonical 数据，不是可丢弃索引。Artifacts、不可变历史和草稿需要一致备份。恢复拒绝非空目标；材料缺失或损坏时明确失败。应用服务于单人本地研究，不支持实时多人协作。协议与 schema 版本是工程格式，不是已经接受的科学协议。

## 边界与撤回条件

这个例外允许本地应用 transport 和具名固定离线仪器，替代原笼统 service 禁令中与之冲突的部分。它不授权 benchmark 平台、跨系统 provider runner、system API、SDK、排行榜、hosting、招募、私人资料发布或 Tilia 实现。ADR-0009/0010 和 P0 执行包保留独立限制；既有证据接受状态不变。

执行、披露、迁移或 hosting 范围的变化需要相应 maintainer 决定。撤回 reader 前保留并导出现有 workspace。[Studio 使用说明](../docs/studio.md)维护命令、失败处理与恢复；[存储说明](../docs/lab-storage.md)维护 schema ownership；[STATUS](../STATUS.zh-CN.md)维护实现与证据状态。
