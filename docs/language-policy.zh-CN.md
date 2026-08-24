**简体中文** | [English](language-policy.md)
<!-- language: zh-CN; mirror: language-policy.md; translation-status: synchronized -->

# Relata R0 语言政策

## 工作语言

R0 阶段，中文是 Relata 当前主要工作与社区参与语言。英文继续作为完整公共入口，服务国际研究者、maintainers、source review 与引用。

Code、schemas、field names、IDs、CLI commands、failure codes、artifact filenames、exact quoted source terms 与 `AGENTS.md` 保持英文。中文文档解释这些 identifiers，但不发明翻译后的 canonical names。

## 稳定 authority 配对

以下稳定表面使用英文 `.md` 与简体中文 `.zh-CN.md` 镜像：

- root README、Start Here、Charter、Status、Research Questions、Assumption Register 与 Contributing guide；
- working terminology 与本 language policy；
- Case Lab README、Case Card template、acceptance checklist 与 Distinction Atlas；
- System Census README 与 System Card template；
- 稳定的 community clinic、consent、Incident Seed、participation、invitation 与 consent-record materials；
- 本政策生效后新增或实质修订的 accepted ADRs。

每一对文件必须：

1. 包含 reciprocal language link；
2. 在顶部 machine-readable HTML comment 中声明 `language`、`mirror` 与 `translation-status`；
3. 任一成员的意义改变时，两份文件在同一次 change 中同步；
4. 只有经过 human review、确认两份文件表达同一项当前 authority 后，才使用 `translation-status: synchronized`。

Repo checker 只验证这些结构与 Git-change properties，不能验证语义等价。

## 提供双语摘要的研究 artifacts

Evidence Cards、System Cards、accepted ADRs 与 actively maintained review documents 同时提供 `中文摘要` 和 `English summary`。完整正文可以保留最能维护 source 或 authoring context 的语言。Exact quoted source terms 保持不变。

## Locale-sensitive cases 与 Incident Seeds

Case 或 Incident Seed 保留 original locale。翻译可能改变 tone、private language、code-switching、cue strength、tokenization、隐含关系信息或 reviewer interpretation。因此跨语言版本是拥有自己 variant identity 的 provenance-linked adaptation，不是自动等价的 mirror。

例如：

```text
RC-002-zh-CN
RC-002-en-adaptation
```

Adaptation 需要记录 source variant、adapter/translator、实质语言变化与独立 review state。

## 历史与技术例外

- Target Architecture Draft 0.1 继续以原语言保存，作为 non-normative historical object。
- Code 与 generated artifacts 不会为了形式对称而复制翻译版本。
- Exact-source objects 保留原始名称与 terms，通过链接或原文引用使用。
- Private continuity 使用对 owners 有用的工作语言，不属于公共 pair contract。

## Drift 处理

稳定 pair 不同步时：

- 将受影响 pair 标为 `translation-status: drifted`，不冒充 synchronized；
- 指明哪一份文件包含较新的 authority，以及改变了什么；
- 在接受 release 或 public authority change 前修复两份文件；
- 不把 structural checker PASS 描述成 translation quality 的证明。

参见 [`ADR-0004`](../decisions/ADR-0004-r0-bilingual-documentation.zh-CN.md)。
