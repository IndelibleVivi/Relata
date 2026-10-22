#!/usr/bin/env python3
"""Finite RC-005→pinned Mem0 study; no arbitrary corpus, adapter registry or scorer."""
import argparse
from collections import Counter
import json
import math
import os
from pathlib import Path
import re
import selectors
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import continuity_inputs as source
from rc005_common import HTTP, Ledger, PIN, dump, save, stamp

CONDITIONS = {'P': source.CONDITIONS, 'B': ('bm25', 'vector'), 'N': ('immediate', 'delayed', 'recovered')}

def cells():
    return [{'id': f'{stage}-{v}-{p}-{r}-{c}', 'stage': stage, 'variant': v, 'probe': p,
             'repeat': r, 'condition': c}
            for stage, conditions in CONDITIONS.items() for v in ('A', 'B')
            for p in ('p1', 'p2', 'p3') for r in (1, 2, 3) for c in conditions]

def terms(text):
    result = re.findall(r'[a-z0-9]+', text.lower())
    for run in re.findall(r'[\u3400-\u9fff]+', text):
        result.extend(run[i:i+2] for i in range(len(run)-1))
    return result

def expand(events, indices):
    sessions = {events[i]['session'] for i in indices}
    return source.source_view([e for e in events if e['session'] in sessions])

def bm25(events, query):
    docs = [Counter(terms(e['text'])) for e in events]
    lengths = [sum(d.values()) for d in docs]
    average = sum(lengths) / len(docs) or 1
    scores = []
    for i, doc in enumerate(docs):
        score = 0
        for token in terms(query):
            df = sum(token in d for d in docs)
            frequency = doc[token]
            score += math.log(1 + (len(docs)-df+.5)/(df+.5)) * frequency*2.2/(frequency + 1.2*(.25+.75*lengths[i]/average))
        if score > 0:
            scores.append((score, i))
    scores.sort(key=lambda item: (-item[0], item[1]))
    return {'candidates': scores[:10], 'history': expand(events, [i for _, i in scores[:10]])}

class Child:
    def __init__(self, cfg_path, cfg, state, out, ready_timeout=60):
        self.noise = (out / 'native-stderr.log').open('a')
        env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'OPENROUTER_'))}
        # Key env references must survive route cleanup, but are never recorded.
        for section in ('chat', 'embedding'):
            name = cfg[section].get('api_key_env')
            if name:
                env[name] = os.environ[name]
        self.process = subprocess.Popen([cfg['native_python'], '-B', str(Path(__file__).with_name('rc005_native_child.py')),
            str(cfg_path), str(state)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.noise,
            text=True, env=env, bufsize=1)
        try:
            self.ready = self.read(ready_timeout)
        except BaseException:
            if self.process.poll() is None:
                self.process.terminate()
            self.close()
            raise
    def read(self, timeout):
        selector = selectors.DefaultSelector()
        selector.register(self.process.stdout, selectors.EVENT_READ)
        try:
            if not selector.select(max(.001, timeout)):
                raise TimeoutError('native child response deadline')
            line = self.process.stdout.readline()
            if not line:
                raise RuntimeError('native child exited; inspect native-stderr.log')
            return json.loads(line)
        finally:
            selector.close()
    def rpc(self, method, operation, timeout=120, **kwargs):
        if getattr(self, '_poisoned', False) or hasattr(self, '_closed'):
            raise RuntimeError('native RPC channel is closed or uncertain; no reuse')
        request = dict(method=method, operation=operation, **kwargs)
        try:
            self.process.stdin.write(dump(request)+'\n')
            self.process.stdin.flush()
            response = self.read(timeout)
            if response.get('operation') != operation:
                raise RuntimeError('native RPC operation binding mismatch')
            if not response['ok']:
                raise RuntimeError(response['error'])
            return response
        except BaseException:
            self._poisoned = True
            if self.process.poll() is None:
                self.process.terminate()
            self.close()
            raise
    def close(self, timeout=5):
        if hasattr(self, '_closed'):
            return self._closed
        pid = self.process.pid
        self.process.stdin.close()
        try:
            self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:
                self.process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=timeout)
        self.noise.close()
        self._closed = dict(stamp(), pid=pid, exited=True, returncode=self.process.returncode)
        return self._closed

class Study:
    def __init__(self, cfg_path, out, child_factory=Child, clock=time):
        self.cfg_path, self.out = Path(cfg_path).resolve(), Path(out).resolve()
        self.cfg = json.loads(self.cfg_path.read_text())
        if self.cfg['embedding']['dimensions'] != 1024 or not self.cfg['embedding']['query_instruction']:
            raise ValueError('fixed study requires encoder dimension 1024 and explicit Qwen query instruction')
        self.out.mkdir(parents=True, exist_ok=True)
        self.ledger = Ledger(self.cfg['ledger'])
        self.bundle = source.load_case()
        source.validate(self.bundle)
        identity = {'pin': PIN, 'source': self.bundle, 'chat': {k:v for k,v in self.cfg['chat'].items() if k not in ('key_file','api_key_env')},
                    'embedding': {k:v for k,v in self.cfg['embedding'].items() if k not in ('key_file','api_key_env')}}
        self.ledger.bind(self.out, identity)
        self.http = HTTP(self.cfg, self.ledger)
        self.child_factory, self.clock = child_factory, clock
        save(self.out / 'plan.json', cells())
        save(self.out / 'effective-config.json', {k: identity[k] for k in ('pin','chat','embedding')})
    def operation(self, name, function):
        path = self.out / 'operations' / (name+'.json')
        if path.exists():
            old = json.loads(path.read_text())
            if old['status'] == 'complete':
                return old['result']
            raise RuntimeError('prior operation failed/uncertain; explicit repair required: '+name)
        save(path, {'status': 'started', **stamp()})
        try:
            result = function()
            save(path, {'status': 'complete', 'result': result, **stamp()})
            return result
        except Exception as error:
            save(path, {'status': 'failed-or-uncertain', 'error': str(error), **stamp()})
            raise
    def answer(self, cell, variant, probe, admitted):
        name = cell['id']
        def execute():
            save(self.out/'contexts'/(name+'.json'), admitted)
            response = self.http.reader(admitted, name)
            review = source.reviewer_packet(self.bundle, variant, probe)
            review.update(response=response['choices'][0]['message']['content'], review_status='unreviewed')
            save(self.out/'blind-review'/(name+'.json'), review)
            return {'response': response, 'semantic_status': 'unreviewed'}
        return self.operation(name, execute)
    def raw_vector(self, events, query, operation):
        sessions = sorted({e['session'] for e in events})
        groups = [('\n'.join(dump(e) for e in source.source_view([event])), [i]) for i, event in enumerate(events)]
        groups += [('\n'.join(dump(e) for e in source.source_view([e for e in events if e['session']==s])),
                    [i for i,e in enumerate(events) if e['session']==s]) for s in sessions]
        docs = self.operation(operation+'-docs', lambda: self.http.embed([text for text,_ in groups], operation+'-docs'))
        q = self.operation(operation+'-query', lambda: self.http.embed([query], operation+'-query', query=True))[0]
        scores = [(sum(a*b for a,b in zip(vector,q)), i) for i,vector in enumerate(docs)]
        event_ranks = sorted(scores[:len(events)], key=lambda x:(-x[0],x[1]))[:10]
        session_ranks = sorted(scores[len(events):], key=lambda x:(-x[0],x[1]))[:10]
        chosen = [j for _,i in event_ranks+session_ranks for j in groups[i][1]]
        return {'candidates': {'events':event_ranks,'sessions':session_ranks}, 'history':expand(events,chosen), 'vectors':docs,'query_vector':q}
    def nonnative(self, selected):
        for cell in selected:
            if cell['stage'] == 'N':
                continue
            variant = next(v for v in source.the_family(self.bundle)['variants'] if v['id']==cell['variant'])
            probe = next(p for p in variant['probes'] if p['id']==cell['probe'])
            try:
                if cell['stage']=='P':
                    admitted = source.subject_input(self.bundle,variant,probe,cell['condition'])
                else:
                    events = source.history_prefix(variant,probe)
                    retrieve = lambda: bm25(events,probe['current']['text']) if cell['condition']=='bm25' else self.raw_vector(events,probe['current']['text'],cell['id'])
                    retrieval = self.operation(cell['id']+'-retrieval',retrieve)
                    admitted = {'context':self.bundle['common_context'],'history':retrieval['history'],'current':probe['current']}
                self.answer(cell,variant,probe,admitted)
            except Exception as error:
                self.ledger.note(event='cell-error',cell=cell['id'],error=str(error))
    def native(self, selected):
        wanted = {c['id'] for c in selected if c['stage']=='N'}
        for variant in source.the_family(self.bundle)['variants']:
            for repeat in (1,2,3):
                trajectory = f"native-{variant['id']}-{repeat}"
                probes = [p for p in variant['probes'] if any(f"N-{variant['id']}-{p['id']}-{repeat}-{c}" in wanted for c in CONDITIONS['N'])]
                if not probes:
                    continue
                state = self.out/'states'/trajectory
                child = None
                try:
                    child = self.child_factory(self.cfg_path,self.cfg,state,self.out)
                    self.ledger.note(event='native-ready',trajectory=trajectory,ready=child.ready)
                    for probe in probes:
                        prefix = source.history_prefix(variant,probe)
                        for session in sorted({e['session'] for e in prefix}):
                            messages = [{'role':e['role'],'content':f"[session={e['session']} surface={e['surface']}] {e['text']}"} for e in prefix if e['session']==session]
                            op = trajectory+f'-add-{session}'
                            def add():
                                save(self.out/'native-inputs'/(op+'.json'),messages)
                                return child.rpc('add',op,messages=messages)
                            ack = self.operation(op,add)
                        base = f"N-{variant['id']}-{probe['id']}-{repeat}"
                        capture_path = self.out/'captures'/(base+'.json')
                        if capture_path.exists():
                            captures = json.loads(capture_path.read_text())
                        else:
                            # An existing add without captures means its original observation window cannot be recreated.
                            ack_wall = ack['wall']
                            captures = {}
                            for condition in CONDITIONS['N']:
                                now = self.clock.time()
                                if condition=='delayed':
                                    self.clock.sleep(max(0,ack_wall+30-now))
                                elapsed = self.clock.time()-ack_wall
                                if elapsed >= 120:
                                    captures[condition] = {'error':'missed 120 second observation window','elapsed':elapsed}
                                    save(capture_path,captures)
                                    continue
                                try:
                                    if condition=='recovered':
                                        recovery_deadline = min(ack_wall+120,self.clock.time()+60)
                                        old = child.close(timeout=max(.001,min(5,recovery_deadline-self.clock.time())))
                                        child = None
                                        remaining = recovery_deadline-self.clock.time()
                                        if remaining <= 0:
                                            raise TimeoutError('recovery deadline reached before restart')
                                        child = self.child_factory(self.cfg_path,self.cfg,state,self.out,ready_timeout=remaining)
                                        recovery = {'old':old,'new':child.ready,'same_state':str(state)}
                                        if child.ready['pid']==old['pid']:
                                            raise RuntimeError('recovery did not change PID')
                                    else:
                                        recovery = None
                                    elapsed = self.clock.time()-ack_wall
                                    remaining = ack_wall+120-self.clock.time()
                                    if condition=='recovered':
                                        remaining = min(remaining,recovery_deadline-self.clock.time())
                                    if remaining <= 0:
                                        raise TimeoutError('observation/recovery deadline reached before search dispatch')
                                    timeout = min(60,remaining)
                                    op = base+'-'+condition+'-search'
                                    result = self.operation(op,lambda: child.rpc('search',op,timeout=timeout,query=probe['current']['text']))
                                    captures[condition] = {'native':result,'started_after_ack':elapsed,'recovery':recovery}
                                except Exception as error:
                                    captures[condition] = {'error':str(error),'elapsed':elapsed}
                                save(capture_path,captures)
                        # All search contexts captured before any reader call.
                        for condition in CONDITIONS['N']:
                            name = base+'-'+condition
                            if name not in wanted or condition not in captures or 'error' in captures[condition]:
                                continue
                            result = captures[condition]['native']['result']
                            entries = result.get('results',[]) if isinstance(result,dict) else result
                            history = [{'role':'memory','surface':'native-search','text':item.get('memory',item.get('text','')),'metadata':item.get('metadata'),'score':item.get('score')} for item in entries]
                            admitted = {'context':self.bundle['common_context'],'history':history,'current':probe['current']}
                            cell = next(c for c in selected if c['id']==name)
                            try:
                                self.answer(cell,variant,probe,admitted)
                            except Exception as error:
                                self.ledger.note(event='cell-error',cell=name,error=str(error))
                except Exception as error:
                    self.ledger.note(event='trajectory-error',trajectory=trajectory,error=str(error))
                finally:
                    if child:
                        self.ledger.note(event='native-exit',trajectory=trajectory,evidence=child.close())
    def report(self):
        coverage = []
        rows = []
        if self.ledger.path.exists():
            rows = [json.loads(line) for line in self.ledger.path.read_text().splitlines() if line.strip()]
        for cell in cells():
            path = self.out/'operations'/(cell['id']+'.json')
            record = json.loads(path.read_text()) if path.exists() else {'status':'pending'}
            status = record['status']
            reason, evidence = record.get('error'), None
            if status == 'started':
                status, reason = 'uncertain', 'operation started without terminal record; no automatic replay'
            if cell['stage'] == 'N' and status == 'pending':
                base = f"N-{cell['variant']}-{cell['probe']}-{cell['repeat']}"
                capture = self.out/'captures'/(base+'.json')
                if capture.exists():
                    value = json.loads(capture.read_text()).get(cell['condition'])
                    if value and 'error' in value:
                        status, reason, evidence = 'technical-failure', value['error'], str(capture.relative_to(self.out))
                    elif value is None:
                        status, reason, evidence = 'uncertain', 'checkpoint capture incomplete; original timing cannot be replayed', str(capture.relative_to(self.out))
                trajectory = f"native-{cell['variant']}-{cell['repeat']}"
                errors = [row for row in rows if row.get('event')=='trajectory-error' and row.get('trajectory')==trajectory]
                if status == 'pending' and errors:
                    status, reason, evidence = 'blocked', errors[-1]['error'], 'dispatch ledger: trajectory-error'
            if status == 'pending':
                reason = 'not yet attempted; quick covers only A/p1/repeat1 P and N; run resumes remaining positions'
            coverage.append(dict(cell,status=status,semantic_status='unreviewed',error=reason,evidence=evidence))
        save(self.out/'coverage.json',coverage)
        return dict(Counter(row['status'] for row in coverage))
    def run(self, quick=False):
        selected = [c for c in cells() if not quick or (c['variant']=='A' and c['repeat']==1 and c['probe']=='p1' and c['stage'] in ('P','N'))]
        try:
            self.nonnative([c for c in selected if c['stage']=='P'])
            required = [c for c in selected if c['stage']=='P']
            if any(not (self.out/'operations'/(c['id']+'.json')).exists() or json.loads((self.out/'operations'/(c['id']+'.json')).read_text())['status']!='complete' for c in required):
                raise RuntimeError('preflight technical failures: native progression stopped')
            self.ledger.note(event='preflight-disposition', disposition='unreviewed exploratory continuation; no semantic success claim')
            self.nonnative([c for c in selected if c['stage']=='B'])
            self.native(selected)
        finally:
            print(dump(self.report()))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-config',type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('command',choices=['plan','run','quick','report','retry-operation'])
    parser.add_argument('--operation', help='failed/uncertain operation name only')
    parser.add_argument('--reason', help='evidence-based repair and duplicate/state-risk disposition')
    args = parser.parse_args()
    if args.command=='plan':
        print(dump(cells()))
        return
    if not args.runtime_config or not args.out:
        parser.error('runtime-config and out are required')
    study = Study(args.runtime_config,args.out)
    if args.command=='retry-operation':
        if not args.operation or not args.reason or '/' in args.operation or '..' in args.operation:
            parser.error('retry-operation requires an exact operation name and repair reason')
        path = study.out/'operations'/(args.operation+'.json')
        record = json.loads(path.read_text())
        if record['status']=='complete':
            raise ValueError('completed operations cannot be retried')
        archive = study.out/'prior-attempts'/(args.operation+'-'+str(time.time_ns())+'.json')
        archive.parent.mkdir(parents=True,exist_ok=True)
        study.ledger.note(event='operator-repair',operation=args.operation,reason=args.reason,prior=record)
        path.replace(archive)
        print('Prior attempt retained; next run may retry under the same ledger. Native timing windows remain bound to original ACK.')
    elif args.command=='report':
        print(dump(study.report()))
    else:
        study.run(args.command=='quick')

if __name__=='__main__':
    main()
