# Case Clinic 中文指南

## 目的

把一个抽象 relational incident 变成最小 synthetic test，同时避免把作者个人解释洗成 universal truth。

## 输入

- 一份或多份 Incident Seeds；
- 可选的 Evidence Cards / System Cards；
- 一个拟议的 bounded distinction。

## Clinic 顺序

1. 用一句话写出 distinction。
2. 找出让 distinction 成立所需的最小历史。
3. 写一个不会自己泄漏答案的 current turn。
4. 只改变一个关键历史变量，做至少一组 counterfactual twins。
5. 分开写 event evidence、explicit accord、observed pattern、author interpretation、probe expectation 和 hard prohibition。
6. 通过 Memory Necessity Gate。
7. 定义 current-turn-only、no-memory、full-minimal-history 与 reference-context controls。
8. 标出 architecture assumptions 与 adapter distortion。
9. 写 high-scoring behavior region，不写唯一完美回复。
10. 记录合理分歧、语言与文化说明。
11. 完成 privacy / provenance declaration。
12. 选择 accept、revise、split 或 reject。

## 输出

- Case Card；
- counterfactual twin group；
- baseline packet；
- review record；
- failure-attribution hypothesis；
- 剩余 ambiguity 的明确理由。

## 应当退回重写的信号

- current turn 自己已经包含正确行为；
- twins 不需要不同 output regions；
- probe evidence contract 主要依赖未承认的作者 interpretation；
- universal relationship norm 替代了 case-local evidence；
- 强制某一种 architecture，却没有声明；
- 需要几百条无关 events 才显得困难；
- reviewers 说不清 must / must-not boundary。
