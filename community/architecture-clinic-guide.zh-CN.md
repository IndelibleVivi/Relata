# Architecture Clinic 中文指南

## 目的

在决定 Relata 怎样测试系统之前，先理解一套真实 memory / companion architecture 怎样工作。Clinic 不是产品排名，也不是答辩会。

## 输入

- 一张 System Card；
- 可选的 diagram 或 artifact trace；
- 一个 known success 与一个 known failure；
- 贡献者选择的 privacy boundary。

## 讨论顺序

1. **System identity 与 use：** 它实际维持什么关系或工作？
2. **Remembered objects：** raw events、summaries、claims、state、identity、intentions，还是其他形式？
3. **Write path：** 什么会自动进入，什么靠手动、reflection 或 consolidation？
4. **Change path：** correction、supersession、coexistence、expiry、deletion、uncertainty 怎样处理？
5. **Recall path：** trigger、search、working memory、active context 与 response use 怎样连接？
6. **Authority：** speaker、source、inference 与 acceptance 怎样区分？
7. **Surfaces 与 migration：** app、model、instance 或 device 改变时，什么保持，什么断裂？
8. **User control：** inspect、amend、revoke、export、explain。
9. **Known failures：** 连续性在哪里断，memory 什么时候变得 intrusive？
10. **Relata pressure：** 哪个拟议 operation 是 native、emulated、impossible 或 misleading？

## 输出

- 一张 reviewed System Card；
- Architecture Pressure Map 的一列或一行；
- 一份会扭曲该系统的 protocol assumptions；
- candidate case ideas；
- unresolved questions。

## 规则

- 不要求 source code、credentials 或 production logs。
- `unsupported` 不等于 `inferior`。
- 区分“能力不存在”和“能力被拟议 boundary 挡住了”。
- 先保留系统自己的 vocabulary，再讨论怎样翻译成 Relata terms。
