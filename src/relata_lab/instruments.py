"""Fixed, transparent offline instruments. No provider or arbitrary driver loader."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import future_question_inputs as future
from experiments import rc005_exposure as exposure

VERSION = 'relata-finite-instruments-1'
CATALOG = {
    'measurement': ('观察仪器看不见什么', '固定同一材料，比较投影、全体交集与可表达的行为。'),
    'applicability': ('方法何时应该停用', '表面与目的正交变化；局部修复后仍检验有效邻居。'),
    'opportunity': ('记起、行动与退休', '在时间、权限与注意预算下重访原文，响应机会并停止过期行动。'),
}


def event(trajectory, position, operation, supplied, result, **extra):
    return dict(trajectory=trajectory, position=position, operation=operation,
                input=supplied, output=result, **extra)


def measurement():
    native = {'results': [
        {'id': 'synthetic-1', 'memory': '保留逐字原文', 'role': 'user', 'metadata': {}, 'score': None},
        {'id': 'synthetic-2', 'text': '', 'metadata': None, 'attributed_to': 'author'},
        {'id': 'synthetic-3', 'memory': '方法有局部例外', 'role': 'assistant'},
    ]}
    projections = {arm: exposure.project(native, arm) for arm in exposure.ARMS}
    fields = exposure.audit_fields([native])
    full = future.audit(future.read_json(future.HISTORIES), future.read_json(future.CONTRACTS))
    regions = {'a': ['庭院', '书房'], 'b': ['书房', '茶室'], 'c': ['庭院', '茶室']}
    originals = {'a': '我们约定可在庭院或书房碰面。', 'b': '我们约定可在书房或茶室碰面。', 'c': '我们约定可在庭院或茶室碰面。'}
    before = future.group_views({w: {'source': text} for w, text in originals.items()}, regions)
    after = future.group_views({w: {'summary': '相同记录'} for w in regions}, regions)
    rows = [event('projections', arm, 'project', native, projections[arm]) for arm in exposure.ARMS]
    rows += [event('finite', 'global-intersection', 'intersect', {'originals': list(originals.values()), 'projection': '相同记录'},
                   {'before': before, 'after': after})]
    for label, text in [('empty', ''), ('whitespace', '  \n'), ('clarification', '请提供最初讨论记录。')]:
        rows.append(event('expressibility', label, 'record-return',
                          {'current': '这段文字是谁提出的？'}, text))
    return {'events': rows, 'analysis': {
        'projections': projections, 'field_audit': fields,
        'finite_witness': {'before': before, 'after': after},
        'existing_fixed_bundle': full,
        'interpretation': '三世界两两交集非空，全体交集为空。该见证只证明所声明有限投影的区分损失。',
        'limits': ['无模型输出或独立人类判断。', '换判读后的差异本身不证明仪器失效。',
                   'empty 与澄清是作者构造的可表达性见证，不是系统质量结果。']}}


def _apply(policy, supplied, method, repaired):
    """Algorithms see task input; acceptance labels remain in the evaluator."""
    purpose, surface, source = supplied['request'], supplied['surface'], supplied['source']
    if policy == 'current-only':
        # A strong no-history baseline follows the explicit current instruction.
        return sorted(set(source.split('；'))) if purpose == '整理要点' else source
    if policy == 'surface-rule':
        enabled = surface == method['surface']
    elif policy == 'global-disable':
        enabled = not repaired
    else:  # a transparent human-authored rule / raw-history lookup baseline
        enabled = purpose == '整理要点'
    return sorted(set(source.split('；'))) if enabled else source


def applicability():
    # These are task instructions visible to every algorithm, not oracle skill IDs.
    source = '检查来源；保留例外；检查来源'
    experience = {'surface': '访谈', 'request': '整理要点', 'source': source,
                  'result': ['保留例外', '检查来源']}
    tasks = [(surface, purpose) for surface in ('访谈', '实验记录')
             for purpose in ('整理要点', '保留逐字稿')]
    policies = ('current-only', 'raw-history', 'human-rule', 'surface-rule', 'global-disable')
    rows, judgments = [], []
    for mode in ('formation', 'consumption'):
        for policy in policies:
            trajectory = f'{mode}:{policy}'
            method = {'surface': experience['surface'], 'request': experience['request']}
            rows.append(event(trajectory, f'{trajectory}:learn', 'derive-rule' if mode == 'formation' else 'supply-rule',
                              experience if mode == 'formation' else method, method))
            sequence = [(s, p, False, 'transfer') for s, p in tasks]
            sequence += [('访谈', '保留逐字稿', True, 'exception'),
                         ('访谈', '整理要点', True, 'valid-neighbour'),
                         ('实验记录', '整理要点', True, 'different-surface-neighbour')]
            for i, (surface, purpose, repaired, phase) in enumerate(sequence):
                supplied = {'surface': surface, 'request': purpose, 'source': source}
                output = _apply(policy, supplied, method, repaired)
                accepted = sorted(set(source.split('；'))) if purpose == '整理要点' else source
                row = event(trajectory, f'{trajectory}:{i}', phase, supplied, output,
                            comparison={'policy': policy, 'mode': mode, 'phase': phase,
                                        'matches_task': output == accepted,
                                        'surface_same': surface == '访谈', 'purpose_same': purpose == '整理要点'})
                rows.append(row)
                judgments.append(row['comparison'])
    summaries = []
    for mode in ('formation', 'consumption'):
        for policy in policies:
            subset = [r for r in judgments if r['mode'] == mode and r['policy'] == policy]
            summaries.append({'mode': mode, 'policy': policy, 'planned_tasks': len(subset),
                              'matches': sum(r['matches_task'] for r in subset),
                              'failed_phases': [r['phase'] for r in subset if not r['matches_task']]})
    return {'events': rows, 'analysis': {'comparisons': summaries,
        'unit': '同一作者任务族内的相关任务；非独立案例',
        'interpretation': '表面规则会误用；全面停用会伤害修复后的有效邻居。简单按任务目的选择的规则可以获胜。',
        'limits': ['formation 是透明算法从示例读取字段，不是 LLM 自主学习。',
                   '当前任务已明确给出目的；current-only、human-rule 与 raw-history 行为相同，此材料不证明记忆必要性。',
                   '局部修复是预先声明的干预；不声称算法从失败自主发现了例外。',
                   '人工规则属于诊断基线；没有候选模型、held-out 或语义校准。']}}


def opportunity():
    rows, access_results = [], []
    for access in ('allowed', 'denied', 'missing', 'stale', 'deadline', 'budget'):
        store = {'original': {'version': 2, 'text': '蓝图标题保留为“潮汐”。'}}
        if access == 'missing':
            store.clear()
        if access == 'stale':
            store['original'] = {'version': 1, 'text': '早期标题为“晨光”（旧版）。'}
        request = {'pointer': 'original', 'current': '沿用当前版本的标题',
                   'required_version': 2, 'allowed': access != 'denied',
                   'tick': 6 if access == 'deadline' else 2, 'deadline': 5,
                   'remaining_reads': 0 if access == 'budget' else 1}
        recovered, read_count = None, 0
        if not request['allowed']:
            reason = 'denied'
        elif request['tick'] > request['deadline']:
            reason = 'deadline'
        elif request['remaining_reads'] < 1:
            reason = 'budget'
        else:
            read_count = 1
            recovered = store.get(request['pointer'])
            reason = 'missing' if recovered is None else 'stale' if recovered['version'] != request['required_version'] else 'allowed'
        action = 'answer' if reason == 'allowed' else 'clarify'
        result = {'action': action, 'source_read': recovered, 'read_count': read_count,
                  'remaining_reads': request['remaining_reads'] - read_count,
                  'reason': reason, 'task_completed': action == 'answer'}
        access_results.append(result)
        rows.append(event('reaccess', f'reaccess:{access}', 'read-source', request, result))
    intentions = {'draft': {'due': 2}, 'withdrawn': {'due': 2}, 'later': {'due': 3}}
    schedule = [('create', 0, None), ('withdraw', 1, 'withdrawn'),
                ('opportunity', 2, 'draft'), ('repeat', 2, 'draft'),
                ('withdrawn-opportunity', 2, 'withdrawn'),
                ('permission-revoked', 3, 'later'), ('opportunity', 4, 'later')]
    outcomes = []
    for policy in ('task-ledger', 'surface-reminder', 'current-only'):
        retired, revoked = set(), set()
        effects, wrong, failures = [], 0, []
        for index, (kind, tick, cue) in enumerate(schedule):
            if kind == 'withdraw':
                retired.add(cue)
            if kind == 'permission-revoked':
                revoked.add(cue)
            eligible = [key for key, val in intentions.items() if tick >= val['due'] and key not in retired and key not in revoked]
            actions = []
            if kind in ('opportunity', 'repeat', 'withdrawn-opportunity'):
                choices = ([cue] if cue in eligible else []) if policy == 'task-ledger' else ([cue] if policy == 'surface-reminder' else [])
                actions = choices[:1]  # one action per delivered event
            receipts = []
            for action in actions:
                valid = action in eligible
                wrong += not valid
                if not valid:
                    failures.append(kind)
                receipts.append({'intent': action, 'effect': 'completed' if valid else 'rejected', 'tick': tick})
                if valid:
                    effects.append(action)
                    retired.add(action)
            rows.append(event(policy, f'{policy}:{index}', kind,
                              {'tick': tick, 'event': kind, 'cue': cue, 'attention_budget': 1,
                               'initial_intentions': intentions if index == 0 else None}, receipts, shape='action'))
        outcomes.append({'policy': policy, 'completed': effects, 'invalid_attempts': wrong,
                         'invalid_events': failures, 'delivered_events': len(schedule), 'attention_budget': 1})
    feedback = []
    for memory in ('confirmed-source', 'frequency-only'):
        frequency = {'stable': 1, 'disputed': 1}
        for tick in range(4):
            selected = 'stable' if memory == 'confirmed-source' else max(frequency, key=lambda k: (frequency[k], k == 'disputed'))
            correction = selected != 'stable'
            if correction:
                frequency['disputed'] += 1
            outcome = {'selected': selected, 'correction': correction, 'counts': dict(frequency)}
            feedback.append({'policy': memory, 'tick': tick, **outcome})
            rows.append(event('reactive:' + memory, f'{memory}:{tick}', 'reactive-step',
                              {'rule': '错误选择产生一次纠正；频次策略对纠正对象加一'}, outcome))
    return {'events': rows, 'analysis': {'source_reaccess': access_results, 'opportunities': outcomes,
        'reactive_world': feedback, 'unit': '固定合成轨迹及其相关事件',
        'limits': ['task-ledger 是外部记忆，不叫 no-memory。',
                   '重复与强化直接由模拟规则规定；只支持该模型下的存在性反例。',
                   '源重访可恢复性与机会退休属于不同合同，不合成总体准确率。',
                   '期限使用虚拟时钟、成本使用读取次数；没有真实计时、token 费用或人类资料。',
                   '没有原生系统机制或长期互动效应。']}}


def compute(suite):
    if suite not in CATALOG:
        raise ValueError('Unknown fixed instrument')
    result = {'measurement': measurement, 'applicability': applicability, 'opportunity': opportunity}[suite]()
    return {'format': VERSION, 'suite': suite, 'label': CATALOG[suite][0],
            'evidence': 'deterministic authored environment', **result}


def run(lab, suite, command_id):
    result = compute(suite)
    call = lambda name, p, suffix: lab.command(name, p, command_id + ':' + suffix)
    study = call('object.create', {'kind': 'study', 'title': result['label'], 'body': {
        'instrument': suite, 'instrument_version': VERSION,
        'evidence': result['evidence'], 'analysis_unit': 'correlated trajectory positions',
        'assignment_unit': 'authored family', 'source_refs': [
            'research/experience-adaptation-study.md', 'research/future-question-memory/README.md'],
        'limits': result['analysis']['limits']}, 'visibility': 'public'}, 'study')
    trajectories = list(dict.fromkeys(e['trajectory'] for e in result['events']))
    positions = [{'id': e['position'], 'trajectory_id': e['trajectory'], 'condition': e['operation'],
                  'checkpoint': str(i)} for i, e in enumerate(result['events'])]
    native_run = call('run.create', {'title': result['label'], 'study': {'id': study['id'], 'revision': study['revision']},
        'trajectories': [{'id': t, 'label': t} for t in trajectories], 'positions': positions}, 'run')
    last, history = {}, {}
    for i, e in enumerate(result['events']):
        attempt = call('attempt.plan', {'run_id': native_run['id'], 'trajectory_id': e['trajectory'],
            'position_ids': [e['position']], 'operation': e['operation'],
            'depends_on': [last[e['trajectory']]] if e['trajectory'] in last else []}, f'{i}:plan')
        for previous, state in [('planned', 'reserved'), ('reserved', 'dispatched'), ('dispatched', 'returned')]:
            call('attempt.transition', {'id': attempt['id'], 'expected_state': previous, 'state': state,
                'receipt': {'driver': VERSION, 'suite': suite, 'event': i} if state == 'returned' else None}, f'{i}:{state}')
        text = e['output'] if isinstance(e['output'], str) else json.dumps(e['output'], ensure_ascii=False, indent=2)
        shape = e.get('shape', 'empty' if text == '' else 'whitespace' if not text.strip() else 'text')
        history.setdefault(e['trajectory'], []).append({'operation': e['operation'], 'input': e['input']})
        call('observation.record', {'run_id': native_run['id'], 'attempt_id': attempt['id'],
            'position_ids': [e['position']], 'content': {'transport': 'returned', 'shape': shape,
            'text': text, 'input': json.dumps(e['input'], ensure_ascii=False, indent=2),
            'governing_history': json.dumps(history[e['trajectory']], ensure_ascii=False, indent=2),
            **({'actions': e['output']} if shape == 'action' else {})},
            'provenance': {'kind': 'deterministic', 'driver': VERSION, 'comparison': e.get('comparison')}}, f'{i}:observation')
        history[e['trajectory']].append({'previous_output': e['output']})
        last[e['trajectory']] = attempt['id']
    analysis = call('object.create', {'kind': 'analysis', 'title': result['label'] + ' · 计算记录',
        'body': result['analysis'] | {'instrument_version': VERSION, 'evidence': result['evidence']},
        'refs': [{'id': native_run['id'], 'revision': native_run['revision'], 'relation': 'computed-from'}],
        'visibility': 'public'}, 'analysis')
    return {'study': study, 'run': native_run, 'analysis': analysis, 'events': len(result['events'])}
