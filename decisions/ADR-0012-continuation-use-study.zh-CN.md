[English](ADR-0012-continuation-use-study.md) | **简体中文**
<!-- language: zh-CN; mirror: ADR-0012-continuation-use-study.md; translation-status: synchronized -->

# ADR-0012：固定经历后继续研究

- **状态：** 2026-11-07，已接受的有界执行委托。
- **授权来源：** 维护者明确委托实施与执行前述纵向继续研究，选择既有官方 OpenAI API，并同意使用两种拟定模型配置。本记录保存这项委托，不从既有研究借用 provider 权限。
- **Canonical packet：** [经历之后，怎样继续？](../research/continuation-use/README.md)。

## 决定

实施并执行一个固定的原创成人合成研究，包含12条开发历史和48条冻结比较历史。每条六个episode、三个后来任务。记忆形成阶段不接收后来任务或作者criteria。比较current-only、原文混合检索、滚动摘要加相同检索、工作笔记加相同检索和full-history参照。使用官方 `gpt-6.1-sol` 与 `gpt-6-luna` reader，主writer固定Sol。这些是控制回放条件，不声称历史中的作者化assistant对话由该writer实际生成，也不把独立Tilia实现当作被测对象。

具名实现可以准备材料、形成记忆、创建新的固定 `text-embedding-3-small` / 1536维合成索引、取得响应、产生盲化AI辅助criterion review并计算描述性配对分析。整段history的单位和共同构造来源必须可见；请求数不是独立样本数。选定的诊断干预可以解释观察到的差异，但须与冻结主比较分开并明确条件性。Metabolism和作者性仍是独立问题，不能当作notes条件的既定收益。

有限工程envelope最多6,000次generation、300次embedding dispatch，包含开发、材料生成、验证/修复、评审、失败和诊断。协调者为本次委托选择USD120的本地成本上限，通过每次请求的保守预留和返回usage计量；它不是已核实账户余额或账单。generation完整body最多131,072 UTF8 bytes；材料创作输出最多12,000 tokens，其他最多4,096。研究请求reported input tokens须不超过32,768，超限停止后续dispatch。本委托不包括充值、账户设置变更或provider fallback。

## 证据与恢复

Runtime config、不可变请求/响应、ledger、生成草稿、review和结果报告均在checkout之外。发送前持久化dispatch，恢复须绑定同一研究输入与精确request。不自动重发未知结果。已知HTTP失败可在同一累计envelope中明确重试至多两次，保留所有attempt。空正文、未完成、格式无效、技术失败与语义判断分开。记录model alias与returned identity；alias不是不可变snapshot。

固定offline core和transport只属于本研究。不因此产生任意语料/provider registry、跨系统runner、benchmark promotion、model-judge acceptance、独立人工校准、人类招募、Tilia产品更改、hosting、release或结果发布。公开source材料与工具按通常repo Git授权维护；raw run与私人解释不包含其中。后续发表仍需选定证据及其相应授权。

## 影响

研究可以为长期memory写作与独立incubation提供可读经历、反例和有条件的设计启发。它不能建立意识、主观连续性感受、一般memory优越性或真实长期关系质量的结论。强原文与current-only对照可以推翻拟议记忆收益。
