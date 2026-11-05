# Relata 授权研究：相邻工作的去重与开放边界

**性质：**原始文献定点阅读与本轮研究判断；没有复现这些论文的系统或实验。编辑日：2026-11-05。本文帮助限定原创贡献，不要求 Relata 引入下列 benchmark、runner 或 policy schema。

## 当前固定版本与阅读范围

| 论文 | 版本与读过的位置 | 对本轮选题的约束 |
| --- | --- | --- |
| Xu 等，*MasDrift: Benchmarking Authorization Preservation Across Multi-Agent Architectures* | [2608.07556v3](https://arxiv.org/html/2608.07556v3)，2026-10-15；§§3.1、4、Appendix D，以及结果与限制的相关段落 | 已经明确讨论 authority lineage、单调收缩、完成目标不会自行授予权限，并同时评价 required work 与越权。不能把这些原则声称为本轮首创 |
| Liu 等，*Auditing Agent Harness Safety* | [2605.14271v2](https://arxiv.org/html/2605.14271v2)，2026-05-16；§3.1–3.4 | 已经分别定义工具／资源 permission 和 information-flow policy，评价完整轨迹。不能把“最终答案正确仍可能发生中途越权”包装成新发现 |
| Michael 与 Roesner，*How Agents Ask for Permission* | [2607.13718v3](https://arxiv.org/html/2607.13718v3)，2026-10-15；§§3、4.1、5.1.3、6 | 区分界面指定、内部策略推导与执行，并指出持续修改／撤回和一次决定被泛化之间的差别。其 21 个研究系统／5 个商用系统是作者限定时期的样本，不是本轮对全领域的最新穷尽核查 |

MasDrift 的 Source 防御从原始请求和公共工具说明编译策略；Chain 在交接时继续收缩。其报告中，低越权率可以伴随原本应完成的工作损失。因此 Relata 的正面持续授权控制有直接的相邻文献依据；不能只看 false grant。§6 同时明确：它研究显式静态授权，主要 defended runs 自动同意所有 confirmation，另有全拒绝 replay；深度与 handoff 数及行动暴露共同变化。不能据此声称已经测量真实用户的确认负担、动态授权维护，或识别了纯粹深度的独立因果效应。

## 本轮仍值得研究的窄问题

**历史更新后的权威依据。**一次初始请求会被后来的合法接受、修订、缩小或撤回改变。只回到最早请求也可能拒绝后来确实授予的行动。候选机制应引用当前有效的授权链；不能把“来源锚定”实现成永远锁定最早状态。

**授权依据和语义依赖分开。**助手写出方案，用户以“按这个做”接受。助手文本提供被接受内容，用户的接受事件使其取得相应授权地位。仅保留用户那句话会丢失指代对象；把助手原提案本身当授权则会越权。应在两个反例上同时成立：完全相同的提案，有接受与无接受；完全相同的接受措辞，指向不同版本的方案。后者尤其能检验摘要是否丢失版本绑定。

**真实行记录在组合后是否保持关系。**每个 grant 的主体、目的、对象和接收者分别真实，并不许可把不同 grant 的维度自由重组。即使单步 permission 完整，跨步信息流也须符合相应条件。全链压缩应保留哪些关系，才同时避免越权和不必要中止，是 memory-transformation 的具体问题。

这些是本轮面向 Relata 的研究切口。它们建立在 access control、information flow 与既有 Relata 工作之上，不声称发明新的权限理论；有限诊断只能确认具名反例与检查器的性质，真实模型的表现须另行研究。

## 基础理论的定位

[Abadi、Burrows、Lampson 与 Plotkin（1993）](https://era.ed.ac.uk/bitstreams/b16c4f2f-2fe9-49a2-905c-483fb6d6796c/download)的 §2、§3.2 与 §5 区分 quoting、speaks-for、controls 和 delegation。本文使用其区分思路，不把自然语言对话直接等同于已认证的密码学 principal。

[Hohfeld（1913）](https://persweb.wabash.edu/facstaff/helmang/phi213-1314S/phi213-txtbrwsr/Hohfeld/Hohfeld1913.html)的 *Powers and Liabilities* 区分引起关系变化的授权事实与由此产生的 powers／privileges。这提示研究分别记录“发生过什么”“哪一事件改变了规范状态”“当前允许什么”。这里是概念比较，没有对任何现实司法辖区作法律结论。

[Nissenbaum（2004）](https://nissenbaum.tech.cornell.edu/papers/H.%20Nissenbaum,%20_Privacy%20as%20Contextual%20Integrity.pdf)的 §III.A–B 区分信息在情境中的适当性与其流动规范。它为真实、相关且可读取的信息仍可能不宜进入另一行动提供解释资源；具体的规范来源与合理变更必须另行说明，不能用抽象 context 标签代替论证。
