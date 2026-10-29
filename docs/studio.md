# Relata Studio：本地研究与恢复

Studio 把研究线程、版本化 Atlas、Study、Clinic 与离线作品放在同一私人工作空间。[ADR-0011](../decisions/ADR-0011-local-research-studio.zh-CN.md)界定实现范围，[存储合同](lab-storage.md)解释 canonical 数据；[当前覆盖](../research/next-generation.md)区分可操作工具、有限计算和未激活的研究。

## 启动与保存

需要 Python 3.11+、Node.js 18+、Git 和现代浏览器。Git 用于应用内置作品的来源 ignore 边界检查。macOS 已验证；其他平台尚未验证。没有第三方 production package、登录或云数据库。在 repository 根目录执行：

```bash
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" serve
```

打开 `http://127.0.0.1:8765`。端口占用时增加 `--port 8766` 并使用命令输出的确切地址；不能改用 `localhost` 或公网 Host。按 Ctrl-C 停止，再运行相同命令恢复。workspace 必须位于 checkout 之外；CLI 会拒绝仓库内目标。不要把 workspace 放进同步或发布目录。

服务只绑定 `127.0.0.1`，API 同时检查 Host、Origin 和每次启动的新 token。应用不自动下载来源、不派发 provider、不接受任意执行程序。点击固定源码的外部链接会访问该网站；保存原文操作只保存你明确输入的文字。停止服务后，静态 Atlas、独立 reviewer HTML 与已导出作品仍可读，Studio 编辑需要服务。

研究桌允许先留一句问题。笔记、竞争解释、下一步和暂停原因自动保存为 draft；**冻结研究版本**才产生 immutable revision。版本冲突会显示当前固定正文，允许明确采用新 head 作为修订起点；未保存时先用**下载草稿**保留文本。多窗口并发编辑会遇到 version conflict，应用不自动覆盖。Reading position 与 drafts 是工作状态，不计入研究证据。

## 一条来源研究路径

1. 研究桌留下问题，写竞争解释；保存一段原文，填来源定位、确切版本与实际读取范围。默认私人。
2. Observatory 选择**导入当前十系统馆藏**。这冻结十个现有模型、三十图和五个展品，不下载上游 checkout。
3. 两侧独立选择系统／版本、条件、节点与缩放。导入另一版模型接受 Atlas JSON，经原验证器与 renderer 生成；作者输入不等于独立核验。跨版本映射必须引用各自节点，可记录 one-to-one、split、merge、unknown。
4. 把比较加入当前问题。在线程点开固定引用，再点**回到这个固定比较**，恢复两侧旧材料与位置。当前来源后来变化时，旧引用仍固定，并显示新版本提示。
5. 来源链接标明作者已保存、需联网或缺失；保存原文需填写与 Atlas 完全相同的 pinned URL。缺失材料不回退到今天的源码。

## Study、attempt 与原样观察

自定义 Study 可**另存设计修订**，每个 run 继续绑定创建时的确切 revision；修改标题、问题或分析单位不会改写旧观察。内置仪器的固定设计由其源码和 fixture 维护。

Study 的 design matrix 每行是 `trajectory | condition | checkpoint`。规划只创建位置，不派发请求。同一次操作可服务多个同轨迹位置；dependent attempts 仅在依赖已经 returned 后登记 dispatched。底层命令入口保留完整依赖与 command ID。

界面的 attempt 是外部执行声明：planned → reserved → dispatched，再登记 returned／failed 回执或明确 uncertain。这里的 reserved 是状态记录，不会替任何 provider 账本扣费。原 RC-005 的真实预算与执行仍由其 CLI 负责。服务重启不会自动重发 dispatched；检查实际回执，无法确认时标记 uncertain，再明确建立新 attempt。旧 attempt 和已报告成本保留在事件链中。

外部观察可不带派发证明；有回执时关联对应 attempt。正文允许 empty、whitespace；动作／tool-only 使用结构化 actions，technical failure 与 uncertain 单独记录。输入和 governing history 必须是原样文字，不能用摘要替代。没有实际来源时只能保存作者声明，不能标成 native 实测。

三组内置仪器在 Study 页按需运行，也可用 CLI：

```bash
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" instrument measurement
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" instrument applicability
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" instrument opportunity
```

分别保存 7／80／35 个事件，属于 3／10／6 条相关轨迹。测量页可切换 legacy、full-native、format-only 原样 exposure；算法基线与机会回执可展开检查。每次 CLI 调用创建独立 run；需要恢复同一命令时使用下方 `command --key`。完整 planned positions 保留在分母中；shared checkpoints 不是独立样本。

## 从观察写到自己的分析

Study 的**分析**页允许为同一次 run 写多份作者分析。左侧写解释、竞争解释与适用范围，右侧检查原始观察和固定判断；搜索仅限当前 run。将材料标为支持、反证或背景／待解释，并说明关系。可以从实际响应、delivered input、governing history、结构化动作或判断理由摘取精确原文；空返回可以直接引用，不需要编造引文。

分析草稿沿用 workspace 的自动保存与冲突检查。**冻结分析版本**才保存不可变 analysis，至少绑定一条材料；材料 ID、精确引文和运行范围由后端核验。已有版本可另存修订，历史版本只读。评审新增、同人修订或处置变化后，页面提示重新检查；不会自动改写分析，也不表示原结论已经错误。引用历史判断时仍显示它已有修订。完整计划分母可在下方展开；原有确定性结果保留在**仪器计算**视图，仍可直接写主张或导出研究迁移包。

从一个固定分析版本**写主张**时，需要另填准备披露的正文、范围与限制，默认私人。私人分析和原始响应不会自动拷入主张正文。Library 中可回到主张引用的确切分析版本；新 analysis revision 不改变已有主张的引用。公开预览只显示匿名 withheld 依赖，不能凭此验证私人分析。迁移时导出当前 run 与 analyses，保留历次分析和所依赖的观察／判断；正文草稿仍只随 workspace backup 保存。

## 两种新协议与原 RC-005 评审

在 Study 的评审视角选择 observations 并新建 round。`governing-history-1` 给 reviewer 该观察固定的 governing history；`delivered-input-2` 给实际 delivered input。两者各自记录 response act 与 optional finite mapping，不合成统一 accuracy。合同为 development-unvalidated；新 rubric 或新披露建立新 round／diagnostic pass，不改旧首评。

导出隔离盲包，打开独立 Clinic，载入 packet，填写 alias。选择正文可加入精确引文；每条判断保留 response act、mapping、理由。同人修改显式提交 amendment，跨人意见并存。下载 draft 后可刷新再恢复；草稿不会自动存进浏览器 localStorage。下载自包含 reviewer HTML 可断网使用；下载累计 journal 后在作者侧导入，精确 packet binding 和同 reviewer amendment chain 由 core 检查。导入重试不重复记数；篡改旧 ID 会失败。Disposition 另存，不抹掉分歧。

原 RC-005 native blind packet 使用[原 Workbench](../case-lab/reviews/workbench/README.md)与 `tools/rc005_review.py`，Studio 提供原评审台下载。原 144 位置完整关闭导出的检查保持原样；新通用 partial run 不能冒充它。Future-question v2 可直接在独立 Clinic 多选导出的 `items/*.json`，不选择 hidden key；填写实际引用区域，下载当前首评 batch 再交回原 `import-reviews`。该格式不覆盖已导入的同人判断；新研究轮次仍另存。Future-question v1/v2 的独立语义见[其说明](../research/future-question-memory/README.md)。未招募或验证独立 reviewer 时，不声称完成校准。

## 只读登记旧研究

登记由 CLI 显式选择路径；HTTP 不提供任意目录扫描。先用旧 CLI 完成原格式验证，再登记：

```bash
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" register-legacy /path/to/practice-workspace --format rc005-practice-workspace-1
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" register-legacy /path/to/future-question-workspace --format future-question-workspace-1
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" register-legacy /path/to/native-review-workspace --format rc005-native-workspace-1 --native-run /path/to/original-closed-run
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" read-legacy SOURCE_OBJECT_ID
```

首次登记调用原 canonical verifier，并冻结精确 inventory、原文与合同；原文件完全不改。原 native run 或依赖缺失时登记失败，不降级成伪造 binding。之后在 Library 的来源列表打开冻结成员，即使当前 fixture／rubric 或原目录已经变化，也读取原 bytes；没有当前源材料时不会默默替换。返回的 verification 记录首次检查的 provenance，不声称每次查看都重新验证 live native run。冻结 legacy source 始终不能直接进入公开 projection；它可能包含 private mapping，应另写公开主张。可随 research-transfer 或 workspace backup 私人迁移。

## 作品、披露与四种导出

Library 可载入两篇已经写好的研究作品，或保存自己的 conditional claim。来源、主张可另存 revision，并以 supports／challenges／reviews 关联固定对象。来源有新版本会标记需重新审视，原 claim 不自动变化。选择允许公开的版本，检查清单，预览文章，再下载自包含 HTML、Markdown 或披露 JSON。原文可离线展开；图以隔离 image 显示，不运行外来 HTML/SVG。点击外部链接仍可能联网。

| Profile | 包含 | 恢复能力 |
| --- | --- | --- |
| workspace-backup | 完整 canonical DB、已登记 artifacts、drafts、working sets、command receipts | 新空 workspace 完整恢复 |
| research-transfer | 显式选择的对象身份、其全部 revisions 与依赖，相关 observations／review chains | 新空 workspace 恢复选定研究；不带无关草稿或命令 |
| blind-review | 固定协议允许的 literal evidence、raw response、匿名 item IDs | 供 reviewer；无作者 map、来源导航或原 native binding |
| public-publication | 明确公开版本与公开依赖；private refs 匿名 withheld | 可读披露投影，不恢复作者工作空间或私有绑定 |

公开标记是作者对正文的披露选择，不是自动脱敏。不要将私人文字放进 public body。结构化 `run_id`／`round_id`／`observation_id`／`attempt_id` 内部引用会被拒绝；应另存公开主张，使用允许的 refs，不能用正文绕过。一个 public 对象引用 private 来源时，读者只看到 withheld，不会得到身份或原文。预览和下载都不会发布网站或上传文件。

```bash
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" backup "$HOME/relata-backup.zip"
python3 -B tools/relata_lab.py --workspace "$HOME/RelataRestored" restore "$HOME/relata-backup.zip"
```

目标 archive 必须不存在，restore 目标必须不存在或为空。不要覆盖原 workspace；先在新路径恢复并检查，再自行决定保留策略。CLI `export --profile research-transfer --refs <selection.json> <archive>` 接受 `[{"id":"...","revision":1}]`；Study Analysis 的迁移按钮同时选择 run 和该 run 的 analyses。选择仅一个 run 的低层导出不自动纳入所有反向引用它的文章。

## 可审查的命令与失败恢复

```bash
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" state
python3 -B tools/relata_lab.py --workspace "$HOME/RelataWorkspace" command instrument.run --input request.json --key study-operation-001
```

`request.json` 可为 `{"suite":"measurement"}`。同 command ID、同 payload 重试返回原 receipt；同 ID 改 payload 报冲突。CLI JSON 错误保留 code；HTTP冲突返回 409。服务断开时下载未保存 draft，恢复服务后刷新获得新 token。缺 blob／损坏 archive 必须补回确切材料，不自动用当前 fixture 替换。SQLite 是真源，不能删除后“重建索引”。无自动 schema migration；未来未知 schema 明确拒绝。

## 维护验证

```bash
python3 -B tools/check_repo.py
python3 -B -m unittest discover -s tests -v
node systems/architecture-atlas/build.cjs --check
node case-lab/reviews/workbench/build.cjs --check
```

有 Playwright 和 bundled Chromium 时，`NODE_PATH` 指向其 Node modules 目录可运行 browser tests；没有时相应 tests 明确 skip。涉及界面的变更仍需实际完成研究桌→双图→Study、观察→盲评→修订导入、作品→离线阅读／迁移恢复三条旅程，检查 1440／1024／390px 与键盘焦点。测试只证明对应工程行为，不提升研究证据等级。
