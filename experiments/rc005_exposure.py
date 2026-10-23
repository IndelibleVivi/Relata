#!/usr/bin/env python3
"""P0 offline exposure audit and pending paired inputs for the fixed RC-005 run.

No runtime config, provider, subject, semantic scorer, replay or artifact mutation.
Only explicitly selected records and ledger are read; outputs are a separate packet.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
import os
from pathlib import Path
import sys

# Script imports do not initialize Study, HTTP, Ledger or the pinned subject.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rc005_native import cells, historical_native_history
from rc005_common import PIN, dump, query_text, vectors
from tools import continuity_inputs as source

ARMS = ('legacy', 'full-native', 'format-only')
# Audit-interest fields from the pinned source study, not a required result schema.
AUDIT_FIELDS = ('id', 'memory', 'text', 'metadata', 'score', 'attributed_to', 'actor_id',
                'role', 'expiration_date', 'created_at', 'updated_at', 'user_id', 'agent_id', 'run_id')
OUTPUTS = ('audit.json', 'paired-inputs.json', 'author-governing-map.private.json')
JSON_LIMIT = 16 * 1024 * 1024
LEDGER_LIMIT = 128 * 1024 * 1024


def require(test, message):
    if not test:
        raise ValueError(message)


def same(left, right):
    """Type-sensitive JSON equality: bool, integer, float, null stay distinct."""
    return json.dumps(left, ensure_ascii=False, sort_keys=True, allow_nan=False) == json.dumps(
        right, ensure_ascii=False, sort_keys=True, allow_nan=False)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()


def safe_path(value, directory=False, exists=True):
    path = Path(value).expanduser()
    require('..' not in path.parts, 'parent traversal is not allowed')
    path = Path(os.path.abspath(path))
    for component in [*reversed(path.parents), path]:
        require(not component.is_symlink(), 'symlink path is not allowed')
    if exists:
        require(path.is_dir() if directory else path.is_file(), 'missing or wrong-type input path')
    return path


def _unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON field')
        result[key] = value
    return result


def parse(text):
    def invalid_constant(value):
        raise ValueError('non-finite JSON constant: ' + value)
    return json.loads(text, object_pairs_hook=_unique, parse_constant=invalid_constant)


def read_file(path, limit=JSON_LIMIT):
    path = safe_path(path)
    require(path.stat().st_size <= limit, 'input file exceeds fixed study bound')
    # Named paths only, no recursion or following links into other source areas.
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, 'r', encoding='utf-8') as stream:
        return stream.read()


def read_json(path):
    return parse(read_file(path))


def native_entries(result):
    entries = result.get('results') if isinstance(result, dict) else result
    require(isinstance(entries, list) and all(isinstance(item, dict) for item in entries),
            'native result must have an ordered list of object entries')
    return entries


def project(result, arm):
    require(arm in ARMS, 'unknown fixed P0 arm')
    entries = native_entries(result)
    if arm == 'legacy':
        return historical_native_history(result)
    if arm == 'full-native':
        # Native role and scope fields stay inside the native object, never API turns.
        return [{'native_entry': deepcopy(entry)} for entry in entries]
    return [{'historical_fields': deepcopy(item)} for item in historical_native_history(result)]


def reader_messages(admitted):
    return [{'role': 'system', 'content': admitted['context']},
            {'role': 'user', 'content': dump({'history': admitted['history'], 'current': admitted['current']})}]


def field_paths(value, prefix=()):
    paths = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = prefix + (key,)
            paths.add(path)
            paths.update(field_paths(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            paths.update(field_paths(item, prefix + (str(index),)))
    return paths


def lookup(value, path):
    for key in path:
        if isinstance(value, dict) and isinstance(key, str) and key in value:
            value = value[key]
        elif isinstance(value, list) and isinstance(key, str) and key.isdigit() and int(key) < len(value):
            value = value[int(key)]
        else:
            return False, None
    return True, value


def presence(present, value):
    if not present:
        return 'missing'
    if value is None:
        return 'null'
    if isinstance(value, (str, dict, list)) and not value:
        return 'empty'
    return 'nonempty'


def pointer(path):
    return '/' + '/'.join(str(part).replace('~', '~0').replace('/', '~1') for part in path)


def exposure_destination(entry, path, arm):
    if arm == 'full-native':
        return ('native_entry',) + path
    first = path[0]
    if first in ('metadata', 'score'):
        destination = path
    elif first == 'memory':
        destination = ('text',) + path[1:]
    elif first == 'text' and 'memory' not in entry:
        destination = path
    else:
        return None
    return ('historical_fields',) + destination if arm == 'format-only' else destination


def audit_fields(results):
    entries = [entry for result in results for entry in native_entries(result)]
    paths = sorted({(name,) for name in AUDIT_FIELDS} | {path for entry in entries for path in field_paths(entry)}, key=pointer)
    fields = []
    for path in paths:
        states, types = Counter(), Counter()
        arms = {arm: Counter({'exposed': 0, 'dropped': 0, 'missing': 0}) for arm in ARMS}
        for entry in entries:
            present, value = lookup(entry, path)
            state = presence(present, value)
            states[state] += 1
            if present:
                types[type(value).__name__] += 1
            for arm in ARMS:
                if not present:
                    arms[arm]['missing'] += 1
                    continue
                destination = exposure_destination(entry, path, arm)
                projected = project([entry], arm)[0]
                exposed, visible = lookup(projected, destination) if destination else (False, None)
                require(not exposed or same(value, visible), 'projection changed an exposed native field')
                arms[arm]['exposed' if exposed else 'dropped'] += 1
        fields.append({'path': pointer(path), 'presence': {state: states[state] for state in ('missing', 'null', 'empty', 'nonempty')},
                       'native_types': dict(types), 'arms': {arm: dict(counts) for arm, counts in arms.items()},
                       'semantic_check': 'unreviewed'})
    return {'native_entries': len(entries), 'fields': fields,
            'historical_synthesis': {'role': 'memory marker, not native role or machine-certified attribution',
                'surface': 'native-search marker',
                'missing_metadata_materialized_as_null': sum('metadata' not in e for e in entries),
                'missing_score_materialized_as_null': sum('score' not in e for e in entries),
                'missing_memory_and_text_materialized_as_empty_string': sum('memory' not in e and 'text' not in e for e in entries)},
            'semantic_check': 'unreviewed',
            'field_census': 'audit-interest fields plus every returned field path; absent interest fields are missing, not schema failures',
            'limit': 'Field visibility and text mentioning attribution do not authenticate authorship or semantic use.'}


def _one(rows, message):
    require(len(rows) == 1, message)
    return rows[0]


def bind_run(run_path, ledger_path):
    """Cross-check only the 54 native positions and the fixed 144-position plan."""
    run = safe_path(run_path, directory=True)
    ledger = safe_path(ledger_path)
    bundle = source.load_case()
    source.validate(bundle)
    plan = read_json(run/'plan.json')
    require(same(plan, cells()), 'run plan differs from exact fixed 144 cells')
    coverage = read_json(run/'coverage.json')
    require(isinstance(coverage, list) and len(coverage) == 144, 'coverage must contain exact 144 positions')
    by_id = {}
    expected = {cell['id']: cell for cell in cells()}
    for row in coverage:
        require(isinstance(row, dict) and row.get('id') in expected and row['id'] not in by_id, 'coverage identity is missing, duplicate or outside fixed study')
        require(all(same(row.get(key), value) for key, value in expected[row['id']].items()), 'coverage cell metadata changed')
        by_id[row['id']] = row
    require(set(by_id) == set(expected), 'coverage has missing positions')
    rows = [parse(line) for line in read_file(ledger, LEDGER_LIMIT).splitlines() if line.strip()]
    require(all(isinstance(row, dict) for row in rows), 'ledger rows must be JSON objects')
    binding = _one([row for row in rows if row.get('event') == 'binding'], 'one exact run binding is required')
    require(binding.get('out') == str(run), 'ledger output binding does not identify this run')
    identity = binding.get('identity', {})
    require(same(identity.get('source'), bundle) and identity.get('pin') == PIN, 'fixture or pinned source differs from run-time ledger binding')
    config = read_json(run/'effective-config.json')
    require(same(config, {key: identity[key] for key in ('pin', 'chat', 'embedding')}), 'effective configuration differs from ledger binding')
    dispatches, returns = {}, {}
    for row in rows:
        if row.get('event') == 'dispatch':
            require(isinstance(row.get('id'), str) and row['id'] not in dispatches, 'ambiguous dispatch identity')
            dispatches[row['id']] = row
        elif row.get('event') == 'return':
            require(isinstance(row.get('dispatch'), str), 'return missing dispatch identity')
            returns.setdefault(row['dispatch'], []).append(row)
    require(all(identifier in dispatches for identifier in returns), 'ledger return has no dispatch')
    bound, failures, historical_results = [], [], []
    governing_pairs = set()
    variants = {variant['id']: variant for variant in source.the_family(bundle)['variants']}
    for cell in cells():
        if cell['stage'] != 'N':
            continue
        name = cell['id']
        base = f"N-{cell['variant']}-{cell['probe']}-{cell['repeat']}"
        captures = read_json(run/'captures'/(base+'.json'))
        require(set(captures) == set(('immediate', 'delayed', 'recovered')), 'checkpoint has incomplete or extra captures')
        capture = captures[cell['condition']]
        require(isinstance(capture, dict), 'capture is not an object')
        variant = variants[cell['variant']]
        probe = next(probe for probe in variant['probes'] if probe['id'] == cell['probe'])
        status = by_id[name].get('status')
        if 'error' in capture:
            require(status == 'technical-failure' and isinstance(capture['error'], str) and capture['error'], 'failure capture is not an explicit technical-failure position')
            require(same(by_id[name].get('error'), capture['error']), 'failure reason disagrees with coverage')
            require('native' not in capture, 'capture mixes failure and successful native return')
            for folder in ('operations', 'contexts', 'blind-review'):
                path = run/folder/(name+'.json')
                safe_path(path, exists=False)
                require(not path.exists(), 'failed capture also has an answer/context record; reconcile before audit')
            require(not any(row.get('operation') == name for row in dispatches.values()), 'failed capture also has reader dispatch; reconcile before audit')
            failures.append({'cell': cell, 'capture': capture, 'status': 'technical-failure',
                             'paired_inputs': 0, 'semantic_check': 'not-applicable-no-response'})
            continue
        require(status == 'complete', 'native success is not a complete reader position')
        raw_search = capture.get('native')
        require(isinstance(raw_search, dict) and raw_search.get('ok') is True, 'missing successful native return')
        search_name = name+'-search'
        search_record = read_json(run/'operations'/(search_name+'.json'))
        require(search_record.get('status') == 'complete' and same(search_record.get('result'), raw_search), 'capture differs from completed search operation')
        echo = raw_search.get('operation')
        require(echo is None or echo == search_name, 'native RPC operation echo mismatches capture')
        result = raw_search.get('result')
        native_entries(result)
        historical_results.append(result)
        admitted = read_json(run/'contexts'/(name+'.json'))
        expected_admitted = {'context': bundle['common_context'], 'history': historical_native_history(result), 'current': probe['current']}
        require(same(admitted, expected_admitted), 'sent context differs from historical projection or fixed current request')
        answer = read_json(run/'operations'/(name+'.json'))
        require(answer.get('status') == 'complete', 'missing completed reader operation')
        response = answer['result']['response']
        text = response['choices'][0]['message']['content']
        require(isinstance(text, str), 'completed historical reader response must be a string')
        governing = read_json(run/'blind-review'/(name+'.json'))
        expected_governing = source.reviewer_packet(bundle, variant, probe)
        expected_governing.update(response=text, review_status='unreviewed')
        require(same(governing, expected_governing), 'run-time governing record differs from fixture or actual historical answer')
        governing_pairs.add((cell['variant'], cell['probe']))
        attempts = [row for row in dispatches.values() if row.get('operation') == name]
        require(attempts and all(row.get('kind') == 'chat' for row in attempts), 'missing or wrong-kind historical reader dispatch')
        matches = []
        for attempt in attempts:
            body = attempt.get('body')
            require(isinstance(body, dict) and same(body.get('messages'), reader_messages(admitted)), 'reader dispatch payload differs from actually admitted context')
            require(body.get('model') == identity['chat']['model'], 'reader model identity differs from bound config')
            require(same({key: body.get(key) for key in ('temperature', 'top_p', 'max_tokens', 'stream')},
                         {'temperature': 0, 'top_p': 1, 'max_tokens': 1024, 'stream': False}), 'historical reader parameters changed')
            require(set(body) == {'model','temperature','top_p','max_tokens','stream','messages'}, 'unexpected reader body fields or tools')
            terminal = returns.get(attempt['id'], [])
            require(len(terminal) <= 1, 'ambiguous terminal returns for reader dispatch')
            if terminal and isinstance(terminal[0].get('status'), int) and 200 <= terminal[0]['status'] < 300 and same(terminal[0].get('body'), response):
                matches.append((attempt, terminal[0]))
        dispatched, returned = _one(matches, 'no unique successful reader return bound to actual answer')
        query = query_text(probe['current']['text'].replace('\n', ' '), identity['embedding'])
        search_attempts = [row for row in dispatches.values() if row.get('operation') == search_name]
        require(search_attempts and all(row.get('kind') == 'embedding' for row in search_attempts), 'native search lacks its embedding dispatch evidence')
        expected_search = {'model': identity['embedding']['model'], 'input': [query], 'encoding_format': 'float'}
        successful_search_returns = 0
        for attempt in search_attempts:
            require(same(attempt.get('body'), expected_search),
                    'native search attempt does not match fixed query and encoder policy')
            terminal = returns.get(attempt['id'], [])
            require(len(terminal) <= 1, 'ambiguous terminal returns for native search dispatch')
            if terminal and isinstance(terminal[0].get('status'), int) and 200 <= terminal[0]['status'] < 300:
                vectors(terminal[0]['body'], 1)
                successful_search_returns += 1
        require(successful_search_returns > 0, 'native search lacks a successful valid encoder return')
        bound.append({'cell': cell, 'capture': capture, 'search_operation': search_record,
                      'rpc_echo_binding': 'present-matched' if echo else 'unavailable-historical-protocol',
                      'search_dispatches': search_attempts, 'search_returns': [row for attempt in search_attempts for row in returns.get(attempt['id'], [])],
                      'admitted': admitted, 'answer_operation': answer, 'governing_record': governing,
                      'reader_attempts': attempts, 'reader_dispatch': dispatched, 'reader_return': returned,
                      'authoring_review_contract': probe['review']})
    require(all((failure['cell']['variant'], failure['cell']['probe']) in governing_pairs for failure in failures),
            'technical failure lacks same variant/probe run-bound governing evidence')
    audit = {'format': 'rc005-p0-native-exposure-audit-1', 'status': 'offline-bound-record-audit',
             'plan_positions': 144, 'native_positions': 54, 'successful_captures': len(bound), 'technical_failures': len(failures),
             'paired_positions': len(bound), 'prepared_requests': len(bound)*len(ARMS),
             'binding': {'fixture': 'matched-run-ledger-and-governing-records', 'capture_search': 'matched',
                         'historical_context': 'matched', 'reader_dispatch_and_return': 'matched',
                         'scope': 'record consistency; not cryptographic attestation or independent observation'},
             'arms': list(ARMS), 'field_audit': audit_fields(historical_results),
             'result_envelope': 'full-native preserves each returned entry, not non-entry result-envelope fields; original result retained in private mapping',
             'execution_status': 'not-run', 'semantic_check': 'unreviewed',
             'failure_cells': [{'cell_id': failure['cell']['id'], 'status': 'technical-failure', 'paired_inputs': 0} for failure in failures],
             'limits': ['No historical artifact is rewritten.', 'No provider or subject is executed.',
                        'No paired response, semantic score or causal benefit is observed.',
                        'Native attribution text/fields remain source claims, not authenticated author truth.']}
    return run, ledger, bundle, binding, plan, coverage, bound, failures, audit


def prepare(run_path, ledger_path, out_path, check=False):
    run = safe_path(run_path, directory=True)
    ledger = safe_path(ledger_path)
    out = safe_path(out_path, exists=False)
    require(not out.is_relative_to(run) and not run.is_relative_to(out), 'output must be separate from run, its descendants and ancestors')
    require(not ledger.is_relative_to(out), 'output must not contain the source ledger')
    run, ledger, bundle, binding, plan, coverage, bound, failures, audit = bind_run(run, ledger)
    requests, mapping = [], []
    for number, record in enumerate(bound, 1):
        pair_id = f'p0-{number:03d}'
        inputs = []
        for arm in ARMS:
            body = deepcopy(record['reader_dispatch']['body'])
            admitted = dict(record['admitted'], history=project(record['capture']['native']['result'], arm))
            body['messages'] = reader_messages(admitted)
            if arm == 'legacy':
                require(dump(body) == dump(record['reader_dispatch']['body']), 'legacy reader body serialization changed')
            require(len(dump(body).encode()) <= 65536, 'prepared complete body exceeds existing study byte bound')
            request_id = pair_id+'-'+arm
            requests.append({'request_id': request_id, 'pair_id': pair_id, 'arm': arm,
                             'execution_status': 'prepared-not-dispatched', 'request': body})
            inputs.append(request_id)
        mapping.append(dict(record, pair_id=pair_id, request_ids=inputs))
    packet = {'format': 'rc005-p0-pending-paired-inputs-1', 'execution_status': 'not-run',
              'semantic_check': 'unreviewed', 'arms': list(ARMS), 'requests': requests,
              'warning': 'Pending paired input preparation only; no response or receipt exists; not a blind review packet.'}
    private = {'format': 'rc005-p0-author-governing-map-private-1', 'run_path': str(run), 'ledger_path': str(ledger),
               'run_binding': binding, 'fixed_plan': plan, 'coverage': coverage, 'cells': mapping,
               'technical_failures': failures, 'privacy': 'Retain this file and original study records privately; never send author contracts to a reader.'}
    documents = dict(zip(OUTPUTS, (audit, packet, private)))
    if out.exists():
        require(out.is_dir(), 'output is not a directory')
        require(set(path.name for path in out.iterdir()) <= set(OUTPUTS), 'output contains unrelated files; refusing to mix artifacts')
    else:
        require(not check, 'check requires an existing prepared output')
    # Compare all existing outputs before creating any missing file. Never overwrite.
    for name, value in documents.items():
        path = safe_path(out/name, exists=False)
        if path.exists():
            require(path.is_file() and read_file(path).encode() == encoded(value), 'prepared output differs; historical or prepared content changed')
        else:
            require(not check, 'prepared output is incomplete')
    if not check:
        out.mkdir(parents=True, exist_ok=True)
        for name, value in documents.items():
            path = out/name
            if not path.exists():
                descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                with os.fdopen(descriptor, 'wb') as stream:
                    stream.write(encoded(value))
    return {'output': str(out), 'status': 'verified-existing' if check else 'prepared-not-dispatched',
            'native_positions': 54, 'paired_positions': len(bound), 'technical_failures': len(failures),
            'requests': len(requests), 'semantic_check': 'unreviewed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('audit', 'prepare', 'check'))
    parser.add_argument('--run', required=True, type=Path)
    parser.add_argument('--ledger', required=True, type=Path, help='explicit read-only ledger; no runtime config')
    parser.add_argument('--out', type=Path, help='separate local derived output, outside historical run')
    args = parser.parse_args()
    if args.command == 'audit':
        print(json.dumps(bind_run(args.run, args.ledger)[-1], ensure_ascii=False, indent=2))
    else:
        if args.out is None:
            parser.error('prepare/check require out')
        print(dump(prepare(args.run, args.ledger, args.out, check=args.command == 'check')))


if __name__ == '__main__':
    main()
