"""Original public synthetic records for P0; no actual run, provider or subject."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

EXPERIMENTS = Path(__file__).resolve().parents[1]/'experiments'
sys.path.insert(0, str(EXPERIMENTS))
import rc005_exposure as audit
from rc005_common import HTTP, Ledger, PIN, dump, query_text, save
from rc005_native import Child, Study, cells, historical_native_history
from tools import continuity_inputs as source


def write_run(root):
    """Build a complete finite fictional evidence set, not a fake live result."""
    run, ledger = root/'synthetic-run', root/'synthetic-ledger.jsonl'
    bundle = source.load_case()
    identity = {'pin': PIN, 'source': bundle,
                'chat': {'model': 'synthetic-reader', 'base_url': 'https://generation.example.invalid/v1'},
                'embedding': {'model': 'synthetic-encoder', 'base_url': 'https://encoder.example.invalid/v1',
                              'dimensions': 1024, 'query_instruction': 'Retrieve relevant synthetic passages.'}}
    rows = [{'event': 'binding', 'out': str(run), 'identity': identity}]
    save(run/'plan.json', cells())
    save(run/'effective-config.json', {key: identity[key] for key in ('pin','chat','embedding')})
    # These two failed positions are original test choices, unrelated to real runs.
    failed = {'N-A-p2-2-delayed', 'N-B-p3-3-recovered'}
    coverage = [dict(cell, status='technical-failure' if cell['id'] in failed else 'complete',
                     error='synthetic offline capture failure' if cell['id'] in failed else None,
                     semantic_status='unreviewed') for cell in cells()]
    save(run/'coverage.json', coverage)
    variants = {v['id']: v for v in source.the_family(bundle)['variants']}
    for cell in cells():
        if cell['stage'] != 'N':
            continue
        name = cell['id']
        base = f"N-{cell['variant']}-{cell['probe']}-{cell['repeat']}"
        capture_path = run/'captures'/(base+'.json')
        captures = json.loads(capture_path.read_text()) if capture_path.exists() else {}
        if name in failed:
            captures[cell['condition']] = {'error': 'synthetic offline capture failure', 'elapsed': 121}
            save(capture_path, captures)
            continue
        entries = [
            {'id': 'fictional-'+name, 'memory': 'An original synthetic memory fragment.',
             'attributed_to': ['synthetic-speaker'], 'role': 'native-speaker',
             'created_at': 123, 'updated_at': None, 'user_id': 'synthetic-scope', 'score': .6,
             'metadata': {'source': 'fictional-tool', 'enabled': False, 'count': 0}},
            {'memory': None, 'text': 'This fallback must remain suppressed.', 'attributed_to': None,
             'metadata': None, 'score': None, 'role': None, 'processing_time': []},
            {'text': 'The fallback is used only when memory is absent.', 'attributed_to': [], 'scope': {}, 'last_access': 0}]
        result = {'results': entries, 'synthetic_envelope_note': 'not reader evidence'}
        raw = {'ok': True, 'result': result, 'pid': 101, 'wall': 1000}
        if cell['condition'] != 'immediate':
            raw['operation'] = name+'-search'
        captures[cell['condition']] = {'native': raw, 'started_after_ack': 30 if cell['condition']=='delayed' else 0}
        save(capture_path, captures)
        save(run/'operations'/(name+'-search.json'), {'status': 'complete', 'result': raw})
        variant = variants[cell['variant']]
        probe = next(p for p in variant['probes'] if p['id']==cell['probe'])
        context = {'context': bundle['common_context'], 'history': historical_native_history(result), 'current': probe['current']}
        save(run/'contexts'/(name+'.json'), context)
        response = {'choices': [{'message': {'content': 'Original fictional answer.'}}], 'model': 'synthetic-pool-label', 'usage': {'prompt_tokens': 50}}
        save(run/'operations'/(name+'.json'), {'status': 'complete', 'result': {'response': response, 'semantic_status': 'unreviewed'}})
        governing = source.reviewer_packet(bundle, variant, probe)
        governing.update(response=response['choices'][0]['message']['content'], review_status='unreviewed')
        save(run/'blind-review'/(name+'.json'), governing)
        reader_body = {'model': 'synthetic-reader', 'temperature': 0, 'top_p': 1,
                       'max_tokens': 1024, 'stream': False, 'messages': audit.reader_messages(context)}
        rows.extend([{'event': 'dispatch', 'kind': 'chat', 'id': name+'-reader', 'operation': name, 'body': reader_body},
                     {'event': 'return', 'dispatch': name+'-reader', 'status': 200, 'body': response},
                     {'event': 'dispatch', 'kind': 'embedding', 'id': name+'-embed', 'operation': name+'-search',
                      'body': {'model': 'synthetic-encoder', 'input': [query_text(probe['current']['text'], identity['embedding'])], 'encoding_format': 'float'}},
                     {'event': 'return', 'dispatch': name+'-embed', 'status': 200,
                      'body': {'data': [{'index': 0, 'embedding': [1.0]+[0.0]*1023}]}}])
    ledger.write_text('\n'.join(dump(row) for row in rows)+'\n')
    return run, ledger


class ExposureTests(unittest.TestCase):
    def root(self, value):
        # macOS temporary roots may contain a system symlink; pass its explicit real path.
        return Path(value).resolve()

    def test_historical_projection_serialization_and_native_losslessness(self):
        entries = [{'memory': None, 'text': 'suppressed', 'metadata': None, 'score': False,
                    'role': 'native-role', 'attributed_to': ['synthetic'], 'id': 0},
                   {'text': 'fallback', 'metadata': {'x': []}}, {'memory': '', 'score': 0.0}]
        for result in (entries, {'results': entries}):
            old = [{'role':'memory','surface':'native-search','text':item.get('memory',item.get('text','')),
                    'metadata':item.get('metadata'),'score':item.get('score')} for item in entries]
            self.assertEqual(dump(historical_native_history(result)).encode(), dump(old).encode())
            self.assertEqual(dump(audit.project(result,'legacy')).encode(), dump(old).encode())
            full = audit.project(result,'full-native')
            self.assertTrue(audit.same([item['native_entry'] for item in full], entries))
            self.assertNotIn('role',full[0])
            self.assertIn('role',full[0]['native_entry'])
            self.assertNotIn('score',full[1]['native_entry'])
            self.assertIsNone(full[0]['native_entry']['memory'])
            self.assertIs(full[0]['native_entry']['score'],False)
            self.assertEqual([item['historical_fields'] for item in audit.project(result,'format-only')],old)
            full[1]['native_entry']['metadata']['x'].append('copy')
            self.assertEqual(entries[1]['metadata']['x'],[])
        self.assertFalse(audit.same(False,0))
        self.assertFalse(audit.same(0,0.0))

    def test_field_presence_null_empty_types_and_dropped_exposed(self):
        result = [{'memory':'synthetic','attributed_to':'unverified-text','metadata':{},'score':0},
                  {'text':'fallback','attributed_to':None,'metadata':None,'score':False},
                  {'memory':'','attributed_to':[]}, {'memory':None}]
        fields = {f['path']:f for f in audit.audit_fields([result])['fields']}
        field = fields['/attributed_to']
        self.assertEqual(field['presence'],{'missing':1,'null':1,'empty':1,'nonempty':1})
        self.assertEqual(field['arms']['legacy'],{'exposed':0,'dropped':3,'missing':1})
        self.assertEqual(field['arms']['full-native'],{'exposed':3,'dropped':0,'missing':1})
        self.assertEqual(field['semantic_check'],'unreviewed')
        self.assertEqual(fields['/score']['native_types'],{'int':1,'bool':1})
        self.assertEqual(fields['/text']['arms']['legacy']['exposed'],1)
        self.assertEqual(fields['/agent_id']['presence'],{'missing':4,'null':0,'empty':0,'nonempty':0})
        for native_field in ('actor_id', 'expiration_date'):
            self.assertEqual(fields['/'+native_field]['presence'],{'missing':4,'null':0,'empty':0,'nonempty':0})
        nested=audit.audit_fields([[{'metadata':{'0':{'actor':False}}}, {'metadata':[{'actor':0}]}]])
        nested_field=next(field for field in nested['fields'] if field['path']=='/metadata/0/actor')
        self.assertEqual(nested_field['native_types'],{'bool':1,'int':1})
        self.assertEqual(nested_field['arms']['legacy']['exposed'],2)

    def test_offline_full_preparation_binding_denominators_and_immutability(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.root(d);run,ledger=write_run(root);out=root/'separate-preparation'
            before = {p.relative_to(run):p.read_bytes() for p in run.rglob('*.json')}
            ledger_before=ledger.read_bytes()
            with patch.object(HTTP,'call',side_effect=AssertionError('no HTTP')), \
                    patch.object(Ledger,'__init__',side_effect=AssertionError('no ledger initialization')), \
                    patch.object(Study,'__init__',side_effect=AssertionError('no study')), \
                    patch.object(Child,'__init__',side_effect=AssertionError('no subject')):
                prepared=audit.prepare(run,ledger,out)
                saved={name:(out/name).read_bytes() for name in audit.OUTPUTS}
                self.assertEqual(prepared['paired_positions'],52)
                self.assertEqual(prepared['technical_failures'],2)
                self.assertEqual(prepared['requests'],156)
                self.assertEqual(audit.prepare(run,ledger,out),prepared)
                self.assertEqual(audit.prepare(run,ledger,out,check=True)['status'],'verified-existing')
            self.assertEqual(saved,{name:(out/name).read_bytes() for name in audit.OUTPUTS})
            self.assertEqual(ledger.read_bytes(),ledger_before)
            self.assertEqual(before,{p.relative_to(run):p.read_bytes() for p in run.rglob('*.json')})
            report=json.loads((out/'audit.json').read_text())
            self.assertEqual(report['native_positions'],54)
            self.assertEqual(report['field_audit']['native_entries'],156)
            packet=json.loads((out/'paired-inputs.json').read_text())
            private=json.loads((out/'author-governing-map.private.json').read_text())
            self.assertEqual(len(private['cells']),52)
            self.assertEqual(len(private['technical_failures']),2)
            for request in packet['requests']:
                self.assertEqual(request['execution_status'],'prepared-not-dispatched')
                self.assertNotIn('response',request)
                body=request['request']
                self.assertEqual(body['max_tokens'],1024)
                self.assertEqual([message['role'] for message in body['messages']],['system','user'])
                serialized=dump(body)
                self.assertNotIn('required_meanings',serialized)
                self.assertNotIn('hinge_value',serialized)
                if request['arm']=='legacy':
                    record=next(c for c in private['cells'] if request['request_id'] in c['request_ids'])
                    self.assertEqual(dump(body),dump(record['reader_dispatch']['body']))
            for record in private['cells']:
                self.assertIn('authoring_review_contract',record)
                if record['cell']['condition']=='immediate':
                    self.assertEqual(record['rpc_echo_binding'],'unavailable-historical-protocol')
            # Never replace an existing, non-equivalent prepared output.
            (out/'audit.json').write_text('{"tampered":true}\n')
            with self.assertRaisesRegex(ValueError,'differs'):
                audit.prepare(run,ledger,out)
            self.assertEqual((out/'audit.json').read_text(),'{"tampered":true}\n')
            self.assertEqual((out/'paired-inputs.json').read_bytes(),saved['paired-inputs.json'])

    def test_binding_mutations_fail_closed_before_writing(self):
        changes = ('fixture','plan','coverage','search','context','governing','answer','reader-body','reader-return',
                   'embedding-query','embedding-missing-return','embedding-wrong-success',
                   'embedding-invalid-vector','embedding-extra-fields','missing-ledger')
        for change in changes:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                root=self.root(d);run,ledger=write_run(root);out=root/'prepared'
                name='N-A-p1-1-immediate'
                def mutate(path, function):
                    value=json.loads(path.read_text());function(value);save(path,value)
                if change=='fixture':
                    changed=deepcopy(source.load_case());changed['common_context']+=' added after run'
                    with patch.object(source,'load_case',return_value=changed):
                        with self.assertRaises(ValueError):audit.prepare(run,ledger,out)
                    self.assertFalse(out.exists());continue
                if change=='plan':mutate(run/'plan.json',lambda v:v.pop())
                elif change=='coverage':mutate(run/'coverage.json',lambda v:v[0].update(condition='forged'))
                elif change=='search':mutate(run/'operations'/(name+'-search.json'),lambda v:v['result']['result']['results'][0].update(id='forged'))
                elif change=='context':mutate(run/'contexts'/(name+'.json'),lambda v:v['history'][0].update(text='forged'))
                elif change=='governing':mutate(run/'blind-review'/(name+'.json'),lambda v:v.update(context='forged'))
                elif change=='answer':mutate(run/'operations'/(name+'.json'),lambda v:v['result']['response']['choices'][0]['message'].update(content='forged'))
                else:
                    rows=[json.loads(line) for line in ledger.read_text().splitlines()]
                    if change=='missing-ledger':rows=[]
                    elif change=='reader-body':next(r for r in rows if r.get('id')==name+'-reader')['body']['messages'][1]['content']='forged'
                    elif change=='reader-return':next(r for r in rows if r.get('dispatch')==name+'-reader')['body']['choices'][0]['message']['content']='forged'
                    elif change=='embedding-query':next(r for r in rows if r.get('id')==name+'-embed')['body']['input']=['wrong query']
                    elif change in ('embedding-missing-return','embedding-wrong-success'):
                        rows=[r for r in rows if r.get('dispatch') != name+'-embed']
                        if change=='embedding-wrong-success':
                            wrong=deepcopy(next(r for r in rows if r.get('id')==name+'-embed'))
                            wrong.update(id=name+'-wrong-embed');wrong['body']['input']=['wrong query']
                            rows.extend([wrong,{'event':'return','dispatch':wrong['id'],'status':200,
                                               'body':{'data':[{'index':0,'embedding':[1.0]+[0.0]*1023}]}}])
                    elif change=='embedding-invalid-vector':
                        next(r for r in rows if r.get('dispatch')==name+'-embed')['body']['data'][0]['embedding']=[0.0]*1024
                    elif change=='embedding-extra-fields':
                        next(r for r in rows if r.get('id')==name+'-embed')['body']['dimensions']=1024
                    ledger.write_text('\n'.join(dump(r) for r in rows)+'\n')
                with self.assertRaises((ValueError,FileNotFoundError)):
                    audit.prepare(run,ledger,out)
                self.assertFalse(out.exists())

    def test_failed_capture_does_not_become_zero_or_paired_input(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.root(d);run,ledger=write_run(root)
            report=audit.bind_run(run,ledger)[-1]
            self.assertEqual(report['technical_failures'],2)
            self.assertEqual(sum(f['paired_inputs'] for f in report['failure_cells']),0)
            name='N-A-p2-2-delayed'
            save(run/'contexts'/(name+'.json'),{'history':[]})
            with self.assertRaisesRegex(ValueError,'reconcile'):
                audit.bind_run(run,ledger)

    def test_paths_symlinks_and_output_overlap_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.root(d);run,ledger=write_run(root)
            for out in (run,run/'nested',root):
                with self.assertRaises(ValueError):audit.prepare(run,ledger,out)
            with self.assertRaises(ValueError):audit.prepare(run/'..'/'synthetic-run',ledger,root/'prepared')
            (root/'run-link').symlink_to(run,target_is_directory=True)
            with self.assertRaises(ValueError):audit.bind_run(root/'run-link',ledger)
            (root/'ledger-link').symlink_to(ledger)
            with self.assertRaises(ValueError):audit.bind_run(run,root/'ledger-link')
            (root/'out-link').symlink_to(root/'real-output',target_is_directory=True)
            with self.assertRaises(ValueError):audit.prepare(run,ledger,root/'out-link')
            name=run/'contexts'/'N-A-p1-1-immediate.json'
            held=root/'held.json';name.replace(held);name.symlink_to(held)
            with self.assertRaises(ValueError):audit.bind_run(run,ledger)

    def test_cli_audit_has_no_runtime_or_output_write(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.root(d);run,ledger=write_run(root)
            with patch.object(sys,'argv',['rc005_exposure.py','audit','--run',str(run),'--ledger',str(ledger)]), patch('builtins.print') as output:
                audit.main()
            self.assertEqual(json.loads(output.call_args[0][0])['execution_status'],'not-run')
            self.assertFalse((root/'prepared').exists())


if __name__=='__main__':
    unittest.main()
