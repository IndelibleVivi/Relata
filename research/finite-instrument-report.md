# 方法、来源与机会：三个有限仪器实际算出了什么

**证据性质：deterministic authored environment。** 2026-10-29，本文读取 [`src/relata_lab/instruments.py`](../src/relata_lab/instruments.py)，在新的临时目录逐一运行 `compute('measurement')`、`compute('applicability')` 与 `compute('opportunity')`，将返回对象写成 JSON 后重新读取，并核对事件、轨迹与 analysis。随后在另一个临时 workspace 实际运行三条 `instrument` CLI，分别返回 7、80、35 个事件。版本标记为 `relata-finite-instruments-1`。没有调用模型、encoder、provider 或原生 system under study，也没有使用私人材料或人类判断。

三个计算支持一个有限论点：**表示中尚存的区别、方法的用途条件、以及行动机会的有效性，必须分别成为可检查对象。** 它们不能互相代签。取回旧文本不保证此时可以回答；停止一个错误方法不保证保住它原来的用途；反复收到纠正也不保证行为会改变。下面给出论点的具体构造、复算结果及其最容易被高估的地方。

## 先数清计划单位

本次复算不是 122 次独立试验。源代码为每个事件指定 trajectory 与 position；这些位置由同一作者环境和规则生成，通常共享材料、条件与答案判定。

| 仪器 | 轨迹与计划位置 | 实际 compute 结果 | 分析单位 |
| --- | --- | --- | --- |
| measurement | `projections` 3；`finite` 1；`expressibility` 3 | 3 条轨迹，7 个事件 | 同一返回对象的三种投影、一个逻辑见证、三个作者构造返回形态 |
| applicability | 2 种 mode × 5 种 policy；每轨迹 1 个形成／提供位置 + 7 个任务位置 | 10 条轨迹，80 个事件；其中 70 个 task judgments | 同一任务族内的相关位置，不是 70 个案例 |
| opportunity | `reaccess` 6；3 种行动 policy 各 7；2 种 reactive policy 各 4 | 6 条轨迹，35 个事件 | 六种访问条件、共享机会序列及短反馈轨迹 |

三个 suite 合计 19 条轨迹、122 个事件。measurement 还嵌入既有 fixed bundle 的 audit：7 个 authored families、15 个 worlds、15 个 questions、105 个分析 cells。105 是 audit 内部的相关投影条件数，没有在上述事件计数之外执行 105 次模型请求，也不增加独立案例数。[既有研究与原始合同](future-question-memory/README.md)。

## measurement：两两相容，为什么仍不能共同成立

最小见证给三个世界分别规定允许选择集合：

| 世界 | 允许的有限选择 |
| --- | --- |
| a | `{庭院, 书房}` |
| b | `{书房, 茶室}` |
| c | `{庭院, 茶室}` |

a 与 b 共享书房，b 与 c 共享茶室，a 与 c 共享庭院；三者的全体交集却为空。复算中 `before` 得到三个分开的可见类，各自 `max_correct_probability=1`；`after` 把三个世界投成同一个 `{"summary":"相同记录"}`，得到一个类，`pairwise_intersections_nonempty=true`、`common_choices=[]`、`witness_kind="global-only"`，均匀世界先验下的有限 ideal lookup 上界为 `2/3`。选择庭院、书房或茶室都恰好满足两个世界，没有一个同时满足三个。

这证明的是所声明有限选择域内的区分损失。它不证明任意自然语言 reader 至多答对三分之二；若任务允许共同澄清或另一个合法回答，允许集合就应包含它，交集也可能改变。投影前的可见输入分别是“我们约定可在庭院或书房碰面。”、“我们约定可在书房或茶室碰面。”与“我们约定可在庭院或茶室碰面。”；a/b/c 仅用于作者侧绑定，不作为 `source` 输入。这里的允许集合仍由作者规定，原句的自然语言充分性未经独立评审。既有 seven-family 工具对 world IDs、答案和实际 input body 有独立隔离规则；这个最小算例不扩展其 subject 输入范围。[投影与全体交集实现](../tools/future_question_inputs.py)、[既有研究的形式范围](future-question-memory/README.md)。

同一个 suite 还把三个 synthetic native entries 送入 [`rc005_exposure.project`](../experiments/rc005_exposure.py) 的 legacy、full-native、format-only 三条纯投影路径。原始 entries 包含两条 `memory` 文本、一条空 `text`，两个 native role、一个 `attributed_to`，以及缺失、null、空对象三种 metadata 情形。结果是：

| 字段区别 | legacy 与 format-only | full-native |
| --- | --- | --- |
| 3 个原 entry IDs | 均未暴露 | 保留 3 个 |
| 2 个 native roles | 均未暴露；legacy 的 `role=memory` 是投影标记 | 保留 user／assistant |
| 1 个 attributed_to | 未暴露 | 保留原字段 |
| metadata 的缺失／null／空对象 | 缺失一项被补为 null；已有 null 与空对象仍在 | 保留原对象中的区别 |
| score 的缺失／null | 两项缺失被补为 null | 保留原对象中的区别 |

format-only 只是将同一历史字段包装进 `historical_fields`，没有恢复被丢弃的来源字段。full-native 用 `native_entry` 保存返回条目的原字段。这是结构可见性的实际复算，不是“完整字段改善了回答”的结果；原字段也可能错误，归属字段不认证作者，所有 field audit 的 semantic check 仍为 `unreviewed`。本文没有读取固定 RC-005 run，也不借这个 synthetic 对象报告该 run 的错误数。

最后三个 `expressibility` 事件分别返回空字符串、空白字符串和“请提供最初讨论记录。”。它们说明当前记录路径能够区分这些返回形态；没有 scorer 判定它们的语义质量。澄清可能是合法行动，不能为了让仪器看起来能评分而将它等同失败。反过来，某种判读方式给出不同数字，也不单独证明旧仪器失效。

## applicability：停用错误规则之后，还剩下什么

源材料固定为“检查来源；保留例外；检查来源”。四种初始任务将 surface 与 purpose 正交组合：surface 为“访谈”或“实验记录”，purpose 为“整理要点”或“保留逐字稿”。整理要点的 authored contract 要求去重、排序后的列表；逐字稿要求保留原字符串。随后追加三个位置：访谈逐字稿例外、修复后的访谈整理有效邻居、不同 surface 的实验记录整理有效邻居。它们共享同一段短材料。

formation 位置从一个例子的字段读取 `surface` 与 `request`；consumption 位置直接提供相同 method 字段。后续 `_apply` 的五种 policy 都是透明手写算法。复算得到两种 mode 完全相同的 task matches：

| policy | formation：匹配／计划任务 | consumption：匹配／计划任务 | 关键表现 |
| --- | --- | --- | --- |
| current-only | 7 / 7 | 7 / 7 | 直接遵循当前明确 purpose，整理或保留原文，无须历史 |
| raw-history | 7 / 7 | 7 / 7 | 按当前 purpose 判断是否去重整理 |
| human-rule | 7 / 7 | 7 / 7 | 与 raw-history 调用同一个 purpose 判断分支 |
| surface-rule | 3 / 7 | 3 / 7 | 把访谈等同于适用，误改逐字稿，并漏掉不同 surface 的整理 |
| global-disable | 3 / 7 | 3 / 7 | 修复前一律整理，修复后全面停用，伤害两个有效邻居 |

这些比例只描述各 policy 在七个相关任务位置与作者合同的匹配，不是模型 accuracy 或估计泛化效果。**current-only 的 7/7 是对这份材料中“记忆必要性”的直接反证**：当前请求已经明确用途，透明算法不需要旧经验也能满足全部合同。这不否定记忆在其他任务可能有益，却要求本研究放弃用此材料证明 memory 必不可少。`current-only`、`raw-history` 与 `human-rule` 在这个有限环境行为相同，没有执行不同的信息获取或计算成本模型；命名不能代替机制差异。

局部修复的含义也需要收紧。`repaired` 是序列给定的布尔条件；global-disable 根据这个条件停用，其他 policy 不会从反馈更新内部参数。purpose-aware policy 从一开始就有正确用途规则，并非在例外发生后才学会局部修订。因此，这个计算支持的是一个存在性反例：**全面停用可以修好当前逐字任务，同时毁掉仍有效的整理任务；一个简单的用途条件可以同时保住两者。** 它没有观察自主 formation、自然语言适用识别或反馈学习。

formation 与 consumption 在这里相同，恰好暴露下一步研究仍欠缺什么：若要比较经验形成与方法使用，应让形成者从可见经历产生方法，再单独检验方法是否被保存、实际采用以及怎样应对新任务。不能把作者已编码的正确 purpose 分支当作系统发现。原文 reader、短人工规则与当前指令足够的控制仍须保留。[经验适应研究及其作者 worksheet](experience-adaptation-study.md)。

## opportunity：能回查、值得行动、应该停止，是三件事

source re-access 的六个位置使用同一当前要求：“沿用当前版本的标题”。它们操纵允许访问、拒绝、缺失、旧副本、期限和预算。实际结果如下。

| access | source_read 与 read_count | 剩余读取预算 | action / task_completed |
| --- | --- | --- | --- |
| allowed | version 2“潮汐”；1 | 0 | answer / true |
| denied | null；0 | 1 | clarify / false |
| missing | null；1 | 0 | clarify / false |
| stale | version 1“晨光”；1 | 0 | clarify / false |
| deadline | null；0 | 1 | clarify / false |
| budget | null；0 | 0 | clarify / false |

旧副本这项特别重要：成功读到一段文字仍可能没有恢复当前所需依据。实现先检查 `allowed` 权限、当前虚拟 tick 是否超过 deadline=5，再检查 `remaining_reads`；可读时消耗一次预算，随后按指针查 store，并比较文档 version 与 required_version=2。通常 tick=2，deadline 条件改为 tick=6；budget 条件将初始读取预算改为 0。missing 实际尝试一次 lookup，因此即使未找到内容也消耗一次。这里运行了分支与扣减，并非按条件名称直接填答案；但过期判断使用显式版本字段，权限和时钟由作者供给，没有测真实权限系统、访问延迟、token 费用或自然语言版本识别。

行动部分有三个意图：draft 与 withdrawn 在 tick 2 到期，later 在 tick 3 到期。固定序列是 create(0)、withdraw(1, withdrawn)、opportunity(2, draft)、repeat(2, draft)、withdrawn-opportunity(2, withdrawn)、permission-revoked(3, later)、opportunity(4, later)。括号中第二项为本次 cue。每个送达事件最多允许一次行动，两个 opportunity、一个 repeat 与一个 withdrawn-opportunity 会触发选择；因此每条七事件轨迹最多有四个行动位置。

| policy | 完成意图 | invalid_attempts | 解释 |
| --- | --- | --- | --- |
| task-ledger | draft 一次 | 0 | 过滤未到期、已退休与撤权项；完成后将 draft 退休 |
| surface-reminder | draft 一次 | 3 | 分别在重复完成、已撤回与已撤权 cue 上作无效尝试 |
| current-only | 无 | 0 | 没有采取行动，也没有完成原本有效的 draft 机会 |

外部 task-ledger 是一种 memory，不能标成 no-memory。它在这个环境里把完成、撤回和撤权作为 eligibility 条件，显示了 retirement 如何避免重复行动。surface-reminder 直接响应 cue，task-ledger 则先检验 cue 对应的意图是否仍 eligible；于是三次无效尝试分别对应 repeat 的 draft、withdrawn-opportunity 的 withdrawn 与 tick 4 的 later，均留下 rejected 回执。它区分了三种退休原因，但没有模拟真实工具越权造成的外部影响，也没有比较另一种调度顺序、多项同时竞争的机会或不同注意预算。

不行动的 current-only 同时没有无效尝试和有效完成，说明只看错误次数会奖励永不行动；只看完成次数又看不见重复越界。有效机会、非法尝试与注意负担应各自报告。不能把 source re-access 的 `task_completed` 与机会完成列表合成一个总体分数，它们执行的是不同合同。

## reactive world：纠正本身可以制造下一轮材料

最后两条轨迹各运行四个 tick，起始频次都是 stable=1、disputed=1。confirmed-source 规则始终选择 stable；frequency-only 选择较高频项，平局偏向 disputed。环境规定：选 disputed 就产生一次纠正，并给 disputed 的频次再加一。

复算中 confirmed-source 四次都选 stable，没有纠正，计数保持 1/1；frequency-only 四次都选 disputed，四次都触发纠正，其计数依次变为 2、3、4、5，stable 始终为 1。这个反馈回路是写在模拟规则里的：纠正没有被解释成负证据，而被频次策略当成了出现次数。

它支持一个可具体检验的警告：当系统自己的行为决定后来又出现什么材料时，固定历史上的检索判断不能代表后续闭环。未来若观察到真实系统保留纠正的角色、状态和来源，并因纠正降低 disputed 的采用，这个 frequency-only 机制解释便不适用于它。本文既没有观察用户不断纠正的心理负担，也没有证明任何原生 memory 系统会这样强化错误；真实人类影响与长期共同演化仍未测试。

## 复算与反驳入口

从仓库根运行下面的标准库命令，可在新的临时目录产生三份 compute 结果并输出各轨迹位置数。临时文件离开上下文后删除；没有读取现存私人 workspace。

```sh
python3 -B - <<'PY'
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
import json
from src.relata_lab.instruments import compute

with TemporaryDirectory(prefix='relata-finite-report-') as directory:
    for suite in ('measurement', 'applicability', 'opportunity'):
        result = compute(suite)
        path = Path(directory) / (suite + '.json')
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        checked = json.loads(path.read_text(encoding='utf-8'))
        print(suite, len(checked['events']),
              dict(Counter(event['trajectory'] for event in checked['events'])))
PY
```

若要把同一有限结果记入本地 study/run/analysis 工作区，以下三条 CLI 也已用全新临时 workspace 实际验证。`/path/to/private-workspace` 是占位符，须换成仓库外的本地目录；该路径执行确定性仪器，不调用 provider。

```sh
python3 -B tools/relata_lab.py --workspace /path/to/private-workspace instrument measurement
python3 -B tools/relata_lab.py --workspace /path/to/private-workspace instrument applicability
python3 -B tools/relata_lab.py --workspace /path/to/private-workspace instrument opportunity
```

三条命令的返回含 study、run、analysis 与 events；它们建立的 attempt/observation 记录是本地确定性计算的记录，不是远端 dispatch 收据。`run` 的 governing_history 按各自 trajectory 累积先前 input/output，再加入本次 operation/input；本次 output 在记录 observation 后才进入后来历史，不能成为自己的输入。行动形态另写结构化 `content.actions`，保留 intent、effect 与 tick，不用一段可读文字代替动作证据。本文未将临时 workspace 或其动态 IDs 纳入公开材料。

本研究下一步最有判别力的改进也由局限直接给出：测用途识别，须让 reader 真正处理当前请求；测 formation，须让方法成为待观察产物；测局部修复，须让规则在反馈前后实际变化；扩展 revocation，须让时序与并发、真实能力边界或更复杂机会选择有机会推翻当前结果；测反应性，须明确环境反馈如何改变后续输入。只要这些条件尚未分开，扩大相关事件数也不能补齐证据。

三个小仪器的价值在于让错误解释有处可查：全体交集可以直接计算，用途条件可以和 surface 分开，机会完成可以和停止行动分别记录。它们给后续研究提供反例与正常控制，仍没有建立模型能力、独立人类校准、原生系统优劣或长期关系效果。
