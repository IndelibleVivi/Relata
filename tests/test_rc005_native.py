"""Offline fixed-study plumbing; no installed Mem0 or provider access."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

EXPERIMENTS = Path(__file__).resolve().parents[1]/'experiments'
sys.path.insert(0,str(EXPERIMENTS))
import rc005_native as study
from rc005_common import Ledger, HTTP, vectors, query_text, save

class Clock:
    def __init__(self): self.now=1000
    def time(self): return self.now
    def sleep(self,seconds): self.now+=seconds

class FakeChild:
    pid=10
    calls=[]
    def __init__(self, cfgpath, cfg, state, out, ready_timeout=60):
        type(self).pid+=1
        self.state=state
        self.clock=FAKE_CLOCK
        self.ready={'pid':type(self).pid,'state':str(state)}
        self.pid=type(self).pid
    def rpc(self,method,operation,timeout=120,**args):
        type(self).calls.append((method,operation,args,self.pid,str(self.state)))
        path=self.state/'fake-state.json'
        self.state.mkdir(parents=True,exist_ok=True)
        messages=json.loads(path.read_text()) if path.exists() else []
        if method=='add':
            messages.extend(args['messages'])
            save(path,messages)
            result={'results':[]}
        else:
            result={'results':[{'memory':m['content']} for m in messages]}
        return {'ok':True,'result':result,'wall':self.clock.time(),'pid':self.pid}
    def close(self, timeout=5): return {'pid':self.pid,'exited':True}

FAKE_CLOCK=Clock()

class FakeHTTP:
    def __init__(self): self.readers=[];self.embeds=[]
    def embed(self,texts,operation,query=False):
        self.embeds.append((texts,query))
        return [[1.0]+[0.0]*1023 for _ in texts]
    def reader(self,admitted,operation):
        self.readers.append((admitted,operation))
        serialized=json.dumps(admitted)
        assert 'required_meanings' not in serialized
        assert 'hinge_value' not in serialized
        assert set(admitted)=={'context','history','current'}
        return {'choices':[{'message':{'content':'offline response'}}],'usage':{'prompt_tokens':100}}

class RC005Tests(unittest.TestCase):
    def config(self,root):
        cfg={'chat':{'base_url':'http://127.0.0.1:1/v1','model':'fake-reader','key_file':str(root/'key')},
             'embedding':{'base_url':'http://127.0.0.1:1/v1','model':'fake-encoder','key_file':str(root/'key'),'dimensions':1024,'query_instruction':'retrieve contextual evidence'},
             'ledger':str(root/'ledger.jsonl'),'native_python':sys.executable,'upstream':'placeholder'}
        (root/'key').write_text('secret-must-not-appear')
        save(root/'config.json',cfg)
        return root/'config.json'
    def test_real_child_close_is_idempotent_and_keeps_child_pid(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            child = study.Child.__new__(study.Child)
            child.noise = (Path(d)/'noise').open('a')
            child.process = subprocess.Popen([sys.executable, '-c', 'import sys; sys.stdin.read()'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=child.noise, text=True)
            pid = child.process.pid
            first = child.close()
            second = child.close()
            self.assertEqual(first, second)
            self.assertEqual(first['pid'], pid)
            self.assertNotEqual(first['pid'], __import__('os').getpid())
            self.assertTrue(first['exited'])
            self.assertIsNotNone(child.process.poll())
            child.process.stdout.close()

    def test_real_rpc_timeout_poisoned_and_operation_binding(self):
        import subprocess
        for code, timeout in [("import sys,time,json; r=json.loads(sys.stdin.readline()); time.sleep(.1); print(json.dumps(dict(ok=True,operation=r['operation'],result={})),flush=True)", .01),
                              ("import sys,json; r=json.loads(sys.stdin.readline()); print(json.dumps(dict(ok=True,operation='wrong',result={})),flush=True)", 2)]:
            with tempfile.TemporaryDirectory() as d:
                child=study.Child.__new__(study.Child)
                child.noise=(Path(d)/'noise').open('a')
                child.process=subprocess.Popen([sys.executable,'-c',code],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=child.noise,text=True)
                with self.assertRaises((TimeoutError,RuntimeError)):
                    child.rpc('search','immediate',timeout=timeout)
                with self.assertRaises(RuntimeError):
                    child.rpc('search','delayed',timeout=1)
                self.assertTrue(child._poisoned)
                self.assertIsNotNone(child.process.poll())
                child.close();child.process.stdout.close()

    def test_recovery_startup_crossing_window_never_dispatches(self):
        global FAKE_CLOCK
        FAKE_CLOCK=Clock();FakeChild.calls=[]
        class SlowRecovery(FakeChild):
            starts=0
            def __init__(self,*args,**kwargs):
                super().__init__(*args,**kwargs)
                type(self).starts+=1
                if type(self).starts>1: self.clock.sleep(121)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);runner=study.Study(self.config(root),root/'out',SlowRecovery,FAKE_CLOCK)
            runner.http=FakeHTTP()
            with patch('builtins.print'):runner.run(True)
            captures=json.loads((root/'out'/'captures'/'N-A-p1-1.json').read_text())
            self.assertIn('deadline',captures['recovered']['error'])
            self.assertEqual(len([c for c in FakeChild.calls if c[0]=='search']),2)
            coverage=json.loads((root/'out'/'coverage.json').read_text())
            self.assertEqual(next(c for c in coverage if c['id']=='N-A-p1-1-recovered')['status'],'technical-failure')

    def test_expired_checkpoint_persists_failure_captures(self):
        global FAKE_CLOCK
        FAKE_CLOCK=Clock();FakeChild.calls=[]
        class ExpiredACK(FakeChild):
            def rpc(self,*args,**kwargs):
                result=super().rpc(*args,**kwargs)
                if args[0]=='add':result['wall']-=121
                return result
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);runner=study.Study(self.config(root),root/'out',ExpiredACK,FAKE_CLOCK)
            runner.http=FakeHTTP()
            with patch('builtins.print'):runner.run(True)
            capture=json.loads((root/'out'/'captures'/'N-A-p1-1.json').read_text())
            self.assertEqual(len(capture),3)
            self.assertTrue(all('error' in v for v in capture.values()))
            self.assertFalse(any(c[0]=='search' for c in FakeChild.calls))

    def test_enumeration(self):
        cells=study.cells()
        self.assertEqual(len(cells),144)
        self.assertEqual(len({c['id'] for c in cells}),144)
        self.assertEqual(study.Counter(c['stage'] for c in cells),{'P':54,'B':36,'N':54})
    def test_full_study_resume_recovery_and_no_probe_writes(self):
        global FAKE_CLOCK
        FAKE_CLOCK=Clock();FakeChild.calls=[]
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            runner=study.Study(self.config(root),root/'out',FakeChild,FAKE_CLOCK)
            fake=FakeHTTP();runner.http=fake
            with patch('builtins.print'):
                runner.run(True)
                self.assertEqual(len(fake.readers),6)
                runner.run()
            self.assertEqual(len(fake.readers),144)
            self.assertEqual(runner.report(),{'complete':144})
            adds=[call for call in FakeChild.calls if call[0]=='add']
            self.assertEqual(len(adds),24)
            self.assertEqual(len({c[4] for c in adds}),6)
            for method,op,args,pid,state in adds:
                self.assertNotIn('offline response',json.dumps(args))
                if op.endswith('-4'):
                    self.assertEqual(args['messages'][0]['role'],'tool')
            for p in (root/'out'/'captures').glob('*.json'):
                value=json.loads(p.read_text())
                self.assertEqual(value['delayed']['started_after_ack'],30)
                recovery=value['recovered']['recovery']
                self.assertNotEqual(recovery['old']['pid'],recovery['new']['pid'])
                self.assertTrue(recovery['old']['exited'])
            with patch('builtins.print'): runner.run()
            self.assertEqual(len(fake.readers),144)
            self.assertEqual(len([c for c in FakeChild.calls if c[0]=='add']),24)
            for path in (root/'out'/'blind-review').glob('*.json'):
                value=json.loads(path.read_text())
                self.assertEqual(value['review_status'],'unreviewed')
                self.assertNotIn('required_meanings',json.dumps(value))
    def review_sources(self, root, failure=False):
        out=root/'out'
        coverage=[]
        bundle=study.source.load_case()
        for cell in study.cells():
            failed=failure and cell['id']=='N-A-p1-1-recovered'
            coverage.append(dict(cell,status='technical-failure' if failed else 'complete'))
            if failed:
                save(out/'captures'/'N-A-p1-1.json',{'recovered':{'error':'PRIVATE PID recovery condition detail'}})
            else:
                # Provider and internal keys must never cross the review export boundary.
                save(out/'operations'/(cell['id']+'.json'), {'status':'complete','result':{
                    'response':{'model':'PRIVATE_PROVIDER','choices':[{'message':{'content':'' if cell['id']=='P-A-p1-1-current-only' else 'synthetic answer'}}],
                    'usage':{'prompt_tokens':100}},'internal_cell':cell['id']}})
                variant=next(v for v in study.source.the_family(bundle)['variants'] if v['id']==cell['variant'])
                probe=next(p for p in variant['probes'] if p['id']==cell['probe'])
                record=study.source.reviewer_packet(bundle,variant,probe)
                record.update(response='' if cell['id']=='P-A-p1-1-current-only' else 'synthetic answer',review_status='unreviewed')
                save(out/'blind-review'/(cell['id']+'.json'),record)
        save(out/'coverage.json',coverage)
        return out

    def test_review_export_blinding_binding_nulls_and_stable_repeat(self):
        with tempfile.TemporaryDirectory() as d:
            out=self.review_sources(Path(d),failure=True)
            with patch.object(HTTP,'call',side_effect=AssertionError('offline export cannot call provider')), patch.object(Ledger,'note',side_effect=AssertionError('offline export cannot write ledger')):
                result=study.Study.export_review(out)
                packet_path=Path(result['packet']);map_path=Path(result['private_mapping'])
                initial=packet_path.read_bytes();mapping_bytes=map_path.read_bytes()
                second=study.Study.export_review(out)
            self.assertEqual(result,second)
            self.assertEqual(initial,packet_path.read_bytes())
            self.assertEqual(mapping_bytes,map_path.read_bytes())
            packet=json.loads(initial)
            self.assertEqual(set(packet),{'format','review_status','items'})
            self.assertEqual(len(packet['items']),144)
            self.assertEqual(len({item['review_id'] for item in packet['items']}),144)
            self.assertEqual(sum(item['response'] is None for item in packet['items']),1)
            self.assertEqual(sum(item['response']=='' for item in packet['items']),1)
            self.assertEqual(next(item for item in packet['items'] if item['response'] is None)['response_state'],'technical-failure')
            self.assertNotIn('PRIVATE',initial.decode())
            for item in packet['items']:
                self.assertEqual(set(item),set(study.source.REVIEW_FIELDS)|{'review_id','response_state'})
                self.assertRegex(item['review_id'],r'^[0-9a-f]{32}$')
                self.assertEqual(item['review_status'],'unreviewed')
            mapping=json.loads(mapping_bytes)
            self.assertEqual({item['cell_id'] for item in mapping['items']},{cell['id'] for cell in study.cells()})
            self.assertNotEqual([item['cell_id'] for item in mapping['items']],[cell['id'] for cell in study.cells()])
            # An underlying response mutation invalidates binding without overwriting either file.
            target=out/'operations'/'P-A-p1-1-full-history.json'
            record=json.loads(target.read_text())
            record['result']['response']['choices'][0]['message']['content']='changed after export'
            save(target,record)
            with self.assertRaisesRegex(ValueError,'run-bound|source changed'):study.Study.export_review(out)
            self.assertEqual(initial,packet_path.read_bytes())
            self.assertEqual(mapping_bytes,map_path.read_bytes())

    def test_review_snapshot_is_pure_and_matches_export(self):
        with tempfile.TemporaryDirectory() as d:
            out=self.review_sources(Path(d),failure=True)
            before={p.relative_to(out):p.read_bytes() for p in out.rglob('*') if p.is_file()}
            snapshots=study.review_snapshot(out)
            after={p.relative_to(out):p.read_bytes() for p in out.rglob('*') if p.is_file()}
            self.assertEqual(before,after)
            self.assertEqual(len(snapshots),144)
            self.assertEqual(sum(body['response'] is None for body in snapshots.values()),1)
            self.assertEqual(sum(body['response']=='' for body in snapshots.values()),1)
            study.Study.export_review(out)
            packet=json.loads((out/'review-packet.json').read_text())
            exported={item['review_id']:item for item in packet['items']}
            mapping=json.loads((out/'review-map.private.json').read_text())
            for item in mapping['items']:
                self.assertEqual(item['body'],snapshots[item['cell_id']])
                self.assertEqual(exported[item['review_id']],dict(item['body'],review_id=item['review_id']))

    def test_review_export_refuses_unclosed_or_conflicting_packet(self):
        for status in ('pending','started','uncertain','blocked','failed-or-uncertain'):
            with tempfile.TemporaryDirectory() as d:
                out=self.review_sources(Path(d))
                coverage=json.loads((out/'coverage.json').read_text());coverage[0]['status']=status
                save(out/'coverage.json',coverage)
                with self.assertRaises(ValueError):study.Study.export_review(out)
                self.assertFalse((out/'review-packet.json').exists())
        with tempfile.TemporaryDirectory() as d:
            out=self.review_sources(Path(d))
            study.Study.export_review(out)
            (out/'review-packet.json').write_text('{"conflict":true}\n')
            with self.assertRaisesRegex(ValueError,'refusing overwrite'):study.Study.export_review(out)
            self.assertEqual((out/'review-packet.json').read_text(),'{"conflict":true}\n')

    def test_first_review_export_rejects_fixture_change_since_run(self):
        import copy
        with tempfile.TemporaryDirectory() as d:
            out=self.review_sources(Path(d),failure=True)
            changed=copy.deepcopy(study.source.load_case())
            changed['common_context']+=' 本句是在运行后新增的背景。'
            with patch.object(study.source,'load_case',return_value=changed):
                with self.assertRaisesRegex(ValueError,'run-bound'):
                    study.Study.export_review(out)
            self.assertFalse((out/'review-packet.json').exists())
            self.assertFalse((out/'review-map.private.json').exists())
            # Restoring the actual run source permits normal export and stable reuse.
            first=study.Study.export_review(out)
            before=(out/'review-packet.json').read_bytes()
            self.assertEqual(first,study.Study.export_review(out))
            self.assertEqual(before,(out/'review-packet.json').read_bytes())

    def test_review_export_cli_needs_no_runtime_or_ledger(self):
        with tempfile.TemporaryDirectory() as d:
            out=self.review_sources(Path(d))
            with patch.object(sys,'argv',['rc005_native.py','--out',str(out),'export-review']), patch.object(study.Study,'__init__',side_effect=AssertionError('runtime initialization forbidden')), patch('builtins.print'):
                study.main()
            self.assertTrue((out/'review-packet.json').exists())
            self.assertFalse((out/'dispatches.jsonl').exists())

    def test_ledger_failures_budget_and_binding(self):
        with tempfile.TemporaryDirectory() as d:
            ledger=Ledger(Path(d)/'ledger')
            ledger.bind(Path(d)/'out',{'identity':'same'})
            with self.assertRaises(ValueError): ledger.bind(Path(d)/'different',{'identity':'same'})
            for _ in range(300): ledger.reserve('chat',b'{}','failed-request')
            with self.assertRaises(RuntimeError): ledger.reserve('chat',b'{}','over-budget')
            with self.assertRaises(ValueError): ledger.reserve('embedding',b' ' * 65537,'oversize')
            ledger.returned('test',200,b'{"usage":{"prompt_tokens":32769}}')
            with self.assertRaises(RuntimeError): ledger.reserve('embedding',b'{}','postflight-stop')
    def test_failed_operation_never_replays(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);runner=study.Study(self.config(root),root/'out')
            called=[]
            def fail(): called.append(1);raise TimeoutError('uncertain')
            for _ in range(2):
                with self.assertRaises((TimeoutError,RuntimeError)):runner.operation('uncertain',fail)
            self.assertEqual(called,[1])
    def test_literal_nohit_and_session_expansion(self):
        events=[{'role':'user','surface':'test','session':1,'text':'共同标题来自声音'},
                {'role':'assistant','surface':'test','session':1,'text':'另一个部分'},
                {'role':'user','surface':'test','session':2,'text':'无关项目'}]
        self.assertEqual(study.bm25(events,'声音')['history'],study.source.source_view(events[:2]))
        self.assertEqual(study.bm25(events,'xyz')['history'],[])
        self.assertEqual(study.terms('AB中文字符'),['ab','中文','文字','字符'])
    def test_vectors_order_dimensions_and_finite(self):
        self.assertEqual(vectors({'data':[{'index':1,'embedding':[0,2]+[0]*1022},{'index':0,'embedding':[2]+[0]*1023}]},2)[0][0],1)
        for bad in ([0]*1024,[1]*1023,[float('nan')]*1024):
            with self.assertRaises(ValueError): vectors({'data':[{'index':0,'embedding':bad}]},1)
    def test_http_request_and_failure_count(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);cfg=json.loads(self.config(root).read_text());ledger=Ledger(cfg['ledger']);http=HTTP(cfg,ledger)
            with patch('urllib.request.urlopen',side_effect=TimeoutError):
                with self.assertRaises(TimeoutError): http.reader({'context':'synthetic','history':[],'current':{'text':'question'}},'test')
            rows=[json.loads(line) for line in Path(cfg['ledger']).read_text().splitlines()]
            self.assertEqual(sum(r['event']=='dispatch' for r in rows),1)
            self.assertNotIn('secret-must-not-appear',json.dumps(rows))
            self.assertEqual(query_text('q',cfg['embedding']),'Instruct: retrieve contextual evidence\nQuery: q')

if __name__=='__main__': unittest.main()
