# 来源、固定版本与证据边界

**日期：**2026-11-05（Asia/Singapore）。**状态：**候选研究的来源札记与静态源码审计；没有经过 Relata source-fidelity acceptance。本文件不替代已接受 Evidence Card，也不自动产生 System Claim。正文见 [README](README.md)。


**2026-11-06 集成复核：**下表保留 2026-11-05 原研究包的阅读范围报告。本次另核查 EAL v2 的摘要、§4.6 及表 28 的关键分母与过滤取舍；通过固定 commit 的 GitHub 文件核查 `gate.py` 的引用检查及 `core.py` 的 `PublicEventReducer.apply`／32-event 上限；核对相邻三篇的相关边界。没有重做全文审计或上游实验。以下 PDF／HTML／源码 SHA-256 为原包记录，本次未重新验证原始下载字节；它们不作为本次复核通过的依据。Relata 自有 fixtures、脚本、结果与 receipt 的身份则已按 `diagnose.py` 复算校验。

## 证据账目

| 标识 | 材料 | 本轮实际做了什么 | 可以支持 | 不能支持 |
| --- | --- | --- | --- | --- |
| E1 | EAL arXiv v2 | 阅读全文主干、方法定义、干预及缓解结果；定点核查相关附录 | 作者如何定义、测量和解释其结果 | Relata 复现、实际部署概率、所有防御普遍有效 |
| E2 | EAL 公开代码固定 commit | 全读 source-authority gate；定点读 event reducer、schema 与 validation 接口 | 这些文件在该 commit 的操作语义 | 运行结果、公开代码与 v2 全部实验逐项对应 |
| M1 | Macaroons 原论文 | 阅读设计与 caveat / attenuation 机制 | 同一授权后裔如何受附加限制 | 自然语言授权抽取正确、当前现实部署安全 |
| T1–T3 | Abadi / Hohfeld / Nissenbaum | 团队对原始文本定点阅读，范围记录在相邻研究笔记 | 陈述与权威、构成事件与规范状态、事实适当性与流动规范的概念区分 | 当代司法辖区法律判断、可直接移植的唯一政策 |
| N1–N3 | MasDrift / HarnessAudit / permission survey | 团队阅读固定版本的具体章节 | 限定本轮新颖性与比较边界 | 独立系统复现或对当前全领域的穷尽调查 |
| R1 | 本研究的形式反例 | 初等关系推导和有条件的轨迹归纳 | 所给前提下存在的反例与充分条件 | 不带前提的安全证明 |
| S1 | 本研究的有限诊断 | 实际执行 32 个手写 fixture 与两组穷举；保存 JSON 和 receipt | 实现与给定 oracle / 计数的一致性 | 模型能力、自然语言解释能力、独立验证 |
| P1 | 后续辨别协议 | 设计完成，原始历史与分离作者解释已离线准备；模型／表示干预未执行 | 可检查的输入准备与后续设计 | 已经观察到的干预效应或用户体验 |

## E1. EAL v2

### 对象与版本

Tommaso Cerruti、Mika Okamoto、Ansel Kaplan Erol，*Agent Memory Is a Surface for Endogenous Authorization Laundering*。

- [arXiv 2609.01836v2 HTML](https://arxiv.org/html/2609.01836v2)；[固定 v2 PDF](https://arxiv.org/pdf/2609.01836v2)。v2 日期 2026-10-24；首次提交 2026-09-01。
- 本轮以 v2 为论文证据对象。旧页面中“5 writers / 50.2% / 98.6%”属于不同版本，未与 v2 混写。
- 保存的 v2 PDF SHA-256：`eff56966e59f16c3657a3add5a1fa9ab36bcfbbcf05dd5cce1de5b0f8892ca72`。
- HTML 准确 SHA-256：`6207761500b6db6298ecd1176c36f79b2597a346d4900b1341472fb8d5e255b8`。

以上 hash 是本次取得字节的身份记录，不表示服务器日后 HTML 不会改变。论文以 arXiv 版本号为主要固定对象，代码另行固定。

### 方法细读：两个不同的错误位置

§3.1–3.3 把底层历史维护的授权状态、writer 记忆及 executor 后续行为分开。writer 看到持续变化的合成组织历史，executor 看到记忆与请求而不看到完整原历史。作者用隐藏的确定性 ledger 规定请求是否合法。

在 typed memory 中，可检查底层状态不允许某动作、而记忆中的状态允许该动作，即 false-authority formation。后续 exact requested action 是否发生又是另一指标。作者报告的条件传播率以已经出现 false authority 的样本为分母，不能读成所有请求的无条件失败率。free-text 的行为可测，但没有相同的 deterministic formation checker，因此不能把 typed 的 formation 测量直接移植到 free-text。

incremental 更新让 writer 从上一份记忆和新 block 更新；原始历史不自动回流。typed 结构提升可检查性，但结构本身不能保证正确保留 scope、有效期或状态。作者还进行 memory-only repair：固定下游条件，把错误 typed 记忆修复为精确状态，再比较 executor 行动。这个干预针对作者选定任务中记忆误差的下游作用；它不证明每一种真实部署错误均由记忆造成。

### 与本文有关的作者结果

| 位置 | v2 作者报告 | 分母与解释边界 |
| --- | --- | --- |
| Abstract、§4.2 | 7 个 writer、2 个 calibrated executor；typed incremental formation 最高 45.4%；出现假授权的匹配样本中行动传播为 99.0% | “最高”用于 formation；99.0% 是给定形成条件后的报告，不是全请求错误率 |
| §4.6，打印页 8–9 | source filtering：unauthorized action 23.5% → 7.3%；legitimate action 93.1% → 53.2% | typed-incremental 缓解比较；相关汇总跨领域、writer、3 seeds 与两个 executor 按请求加权；不是单一采购场景，也不是各领域都相同 |
| 同处 | source filtering 后 false authority 仍为 5.4%；有效条目可能因同时引用同事而被删；有权 grantor 被正确引用仍可能错在 scope、validity、revocation | 给出来源检查不足与合法工作损失的机制线索；未证明本文的 P1/A1 场景已被该 benchmark 测过 |
| 同处 | event-based memory：unauthorized action 23.4% → 9.3%；legitimate action 93.0% → 68.6% | baseline 数值与 source-filter 比较并不完全相同，不宜强行拼成同一个完全配对估计 |
| 同处 | 两种防御均未改善 cybersecurity；finance 合法行动降到 28% / 24% | 说明领域机制差异；不是所有 event sourcing 或 source checking 的必然结局 |
| §4.6、相关附录 | rebuilding 改善未授权行动，合法行动提高或在 baseline 1 个百分点内，writer input 为 1.2–3.0 倍；authority instruction 在 procurement / finance 有改善，在 cyber 的 unauthorized action 从 10.5% 增至 20.4% | 计算预算、失败写入与领域机制有混淆边界；作者未解决该 instruction 为何增加 malformed writes |

本轮没有复算论文所有表格，也没有执行模型或验证其跨 seed 稳健性。上述数字均保留为作者报告，主要论证不依赖将它们视为 Relata 已证实事实。

### 研究推论与不重复的边界

EAL 已经研究随历史更新的授权状态、撤销、替换与失败更新。因此“记忆应保留动态授权”“来源检查不够”“安全与合法工作要同时看”不能被本文当成新发现。

本文从其混合来源过滤损失出发，进一步提出一个明确可构造的区别：一个非授权主体可以提供被接受的语义对象，而有效接受事件来自另一主体。是否能保留这两种角色及其绑定，应通过有 / 无接受、同目标不同版本、有效 standing discretion 的对照检验。这是本轮研究判断，不能写成 EAL 已测出的结论。

## E2. EAL-Bench pinned code

### 固定对象与覆盖

仓库：[tommasocerruti/eal-bench](https://github.com/tommasocerruti/eal-bench)。固定 commit：[`51648690bc52d7a9c7ac080a2c67a784fe9d56cb`](https://github.com/tommasocerruti/eal-bench/tree/51648690bc52d7a9c7ac080a2c67a784fe9d56cb)，commit 时间 2026-09-23T15:02:25+02:00。

**版本关系：**公开快照时间早于论文 v2 的 2026-10-24。即使路径名称和机制相符，也没有由此证明这个 commit 重现 v2 的全部模型、配置、实验或表格。本轮不运行 upstream suite，不安装 provider 依赖，不从保存的结果文件反推当前能力。

| 文件 | 阅读覆盖 | 可核查观察 |
| --- | --- | --- |
| [`experiments/mitigations/source_authority/gate.py`](https://github.com/tommasocerruti/eal-bench/blob/51648690bc52d7a9c7ac080a2c67a784fe9d56cb/experiments/mitigations/source_authority/gate.py) | 全文件，尤其 `apply_cited_source_authority_gate`、`evaluate_cited_sources`、`_citation_decision` | 保留条目的必要条件是每个 cited visible source 都 authority-capable；空引用、未来引用、未知引用和 incapable source 被区分拒绝 |
| [`experiments/mitigations/event_sourcing/core.py`](https://github.com/tommasocerruti/eal-bench/blob/51648690bc52d7a9c7ac080a2c67a784fe9d56cb/experiments/mitigations/event_sourcing/core.py) | 定点阅读 `ExtractedEvent`、`PublicEventReducer.apply`、bounded event schema 与 validation 分支；不是全仓库审计 | issue / patch / revoke / replace 的显式状态变化；32 events per block 上限；事件由 model extraction 后进入确定性 reducer |

`gate.py` SHA-256：`17f85e312ca982da133c94ed88ad37d150bb011f9f0bd1e22ae4aef18eac39fe`。
`event_sourcing/core.py` SHA-256：`40d1151133a70d0cdafc777d3d08c7cb66781bae8e03c57f1d8724f79286af48`。

### 观察一：来源能力 gate 并不进行语义蕴含检验

`apply_cited_source_authority_gate` 先序列化 typed memory，再遍历 `authorizations`。resolver 分别取得当前 block 可见 sources 和全部 sources，读取条目引用 IDs。`evaluate_cited_sources` 拒绝空列表，并在任一个 citation 失败时拒绝整条记录；通过的记录保留原内容。

`_citation_decision` 把 source ID 映射到 metadata。它区分未来来源与未知来源，检查 `authorization_capable`，但没有对被引用源句与该条 authorization 的完整 scope / validity / revocation 做蕴含验证。**这只是该 gate 的局部语义，不等于整个系统再无其他检查。**

本轮推论：如果一条合法授权把有权接受事件和非授权描述操作数都列成同一种 source ID，整条引用全通过的要求可能误删；如果仅引用一个正确有权主体，却错误扩大其实际授予的范围，这个 gate 本身也不足以排除。上游确实报告混合来源损失；本文的助手提案接受控制则需要自己的实验，尚未在上游运行。

### 观察二：确定性 reducer 的边界在上游事件是否正确

`PublicEventReducer.apply` 对 issue 建立 active 记录；patch 修改指定字段，其中 scope 使用浅层字段合并；revoke 将现有目标标为 revoked；replace 将旧记录标为 superseded，建立新的 active 记录。patch / revoke 的 provenance 会合并已有与新增 source IDs。schema 约束事件种类、字段形状、目标引用与最大数量。

这些机制让状态转移可复查，不能确保提取的事件类型、target 或范围对应原历史。被错提为 issue 的普通描述、指向错误 grant 的 revoke、对 accepted proposal 内容的错误重建，都可能在格式正确的事件中发生。**这项推论没有通过上游模型运行验证，也不声称该 repository 中已经实际观察到每一种失败。**

本研究自己的 `resolve()` 更窄：它读取预先给定的当前 grant 状态，既不是 EAL reducer 复刻，也没有实现自然语言 event extraction。

## M1. Macaroons

Birgisson 等，*Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud*（2014）。[作者机构页面](https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/)；[原论文 PDF](https://research.google.com/pubs/archive/41892.pdf)。保存 PDF SHA-256：`1bbb26fbbae6f8a148595a3539decafc3459d256d5639b1e559c4c1796b828d7`。

阅读重点是 credential 的 delegation 与 caveats 如何限制使用上下文。附加 caveat 对同一凭据带来进一步限制，而不是创造原凭据没有的权限。这有助于澄清“沿一条委托链求限制交集”的含义。过期与撤销仍有 freshness、有效期及验证环境条件，不能由记忆中保留一个旧 token 的事实自动解决。

本文没有实现 macaroon，也没有把独立 grants 的授权集合强制求交。它是形式化比较资源：自然语言接受的解释与身份绑定发生在 cryptographic attenuation 之前，仍需另行验证。

## 其他原始文献的阅读边界

MasDrift v3、HarnessAudit v2、*How Agents Ask for Permission* v3，以及 Abadi / Hohfeld / Nissenbaum 的精确 URL、章节和新颖性约束，见 [nearby-research.md](nearby-research.md)。这些由本轮团队定点阅读，共享阅读笔记只是一份证据，不算独立验证。

## 本项目证据的边界

[fixtures.json](fixtures.json) 是作者手写的公共合成研究输入，不是自然抽样数据集或 canonical Relata schema。authority capability、有效状态、时间、指代及 lineage 均由作者规定。

[results.json](results.json) 是实际执行 [diagnose.py](diagnose.py) 的确定性输出；[receipt.json](receipt.json) 记录执行时间和三个文件的字节身份。默认运行会验证结果与 receipt，而 `--write` 会产生一份新 receipt。该 receipt 证明某次计算与这些字节相符，不能证明 oracle 的规范判断正确。

[protocol.md](protocol.md) 提出下一阶段的自然语言形成 / 消费研究与可能的人类复核。没有执行这些研究，也没有把提出的干预、样本量或测量项写成结果。任何后续 promotion、provider execution、正式人类研究、公开数据或 Tilia 实现仍遵守现有 canonical 决策边界。
