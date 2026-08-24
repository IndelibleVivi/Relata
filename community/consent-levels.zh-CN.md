# Relata Community Contribution Consent Modes

这些 labels 只说明“一份 contribution 可以怎样被使用”。它们**不是**投入程度、身份、信任或研究价值的升级阶梯。同一个人可以对不同 artifacts 选择不同 mode，也可以完全不参加某条路径。

这里的 project contribution consent 不能替代未来 formal human-participant study 可能需要的 institutional ethics / consent process。

## Mode 0 — 只用于当次私下 conversation

材料只服务当次私下交流，不进入 project files、summary、aggregate finding 或 case design。如果后来觉得某个 insight 有研究价值，必须先重新询问，不能把当时的沉默或熟悉关系当成授权。

## Mode 1 — 只形成 aggregate insight

Relata 可以保留一个在研究 artifact 中无法合理回连到具体贡献者或 incident 的概括性洞见。这个 mode 不允许保存 Incident Seed、direct quote、public attribution 或 synthetic derivation。

## Mode 2 — Restricted abstract contribution

Relata 可以在 restricted workspace 保存一份去识别化的 Incident Seed、System Card 或 review。这个 mode 不允许 public release，也不允许转化为 public synthetic case。

## Mode 3 — Public synthetic derivation

一份 restricted abstract contribution 可以启发完全 synthetic、角色均为成人的 case。公开 case 不得复制原关系，也不能声称代表原关系。除非另有明确记录，公开前必须让贡献者 review proposed derivation。

## Mode 4 — Public contribution

一份明确指定的 artifact 可以按贡献者选择的实名、网名、集体署名或匿名方式公开。授权只覆盖这份 artifact，不自动允许 raw-chat publication、direct quotation、architecture disclosure、future derivatives 或其他项目复用。

## 每份 contribution 必须分开记录

- contribution ID 与 artifact type；
- consent mode 与允许的 uses；
- attribution form；
- 是否允许在 public synthetic case 之外 direct quote；
- 哪些 architecture details 可以公开；
- 是否允许 synthetic derivation；
- 是否要求 pre-publication review，以及什么动作才算 approval；
- 是否允许 follow-up contact；
- restricted storage location、steward、retention / review date；
- withdrawal contact 与 public release 后的现实限制。

除非本人事先明确同意了该机制，否则沉默不算 approval。

## Withdrawal

公开 release 前，贡献者可以撤回，不需要证明理由。除非贡献者同意其他处理，Relata 也应移除实质依赖该 contribution 的 unpublished derivatives。

公开 release 后，maintainers 可以在未来维护版本中删除、弃用、停止 active use、尽量移除 identity link，并发布 correction；但无法保证第三方 clone、fork、archive、citation 或已经分发的 release 被同步删除。公开前必须说明这个限制。

## Record separation

填好的 identifying consent records 不得进入本 repo。它们应与去识别化 research artifacts 分开，保存在 restricted location。Public provenance 可以说明 derivation method 与 permission mode，但不能暴露 identity 或 private source material。

字段清单见 [`contribution-consent-record-template.md`](contribution-consent-record-template.md)；填好的 record 必须保存在 public repo 之外。
