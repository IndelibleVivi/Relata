"""Offline acceptance tests for the local research state boundary."""
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'src'))
from relata_lab import Lab, LabError


class LabTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.lab = Lab(self.root / 'work')
        self.seq = 0

    def tearDown(self):
        self.lab.close()
        self.temp.cleanup()

    def cmd(self,command_name,**payload):
        self.seq += 1
        return self.lab.command(command_name,payload,str(self.seq))

    def obj(self,kind='study',**kw):
        return self.cmd('object.create',kind=kind,title='Research',body={},**kw)

    def fixture(self):
        study = self.obj()
        run = self.cmd('run.create',study={'id':study['id'],'revision':1},title='Fixed study',trajectories=[{'id':'a','label':'A'},{'id':'b','label':'B'}],positions=[{'id':'p1','trajectory_id':'a','condition':'hidden-A','checkpoint':'1'},{'id':'p2','trajectory_id':'a','condition':'hidden-A','checkpoint':'2'},{'id':'p3','trajectory_id':'b','condition':'hidden-B','checkpoint':'1'}])
        return study,run

    def observation(self,run,**content):
        content = {'transport':'completed','text':'hello','input':'delivered evidence','governing_history':'governing evidence',**content}
        content.setdefault('shape','technical_failure' if content['transport'] == 'failed' else 'empty' if content['text'] == '' else 'whitespace' if not content['text'].strip() else 'text')
        return self.cmd('observation.record',run_id=run['id'],position_ids=['p1','p2'],content=content,provenance={'private':'DO-NOT-LEAK'})

    def round(self,observation,**kw):
        return self.cmd('round.create',title='Review',protocol='governing-history-1',observation_ids=[observation['id']],contract={'question':'Read response'},**{'pass':'first',**kw})

    def review(self,round,obs,reviewer='r',**kw):
        return self.cmd('review.submit',round_id=round['id'],observation_id=obs['id'],reviewer=reviewer,judgment={'response_act':'answer','mapping':'mapped','decision':'supported','rationale':'literal'},**kw)

    def test_revision_idempotency_and_working_conflicts(self):
        payload = {'kind':'source','title':'Pinned','body':{'text':'old'}}
        first = self.lab.command('object.create',payload,'fixed')
        self.assertEqual(first,self.lab.command('object.create',payload,'fixed'))
        with self.assertRaises(LabError) as err:
            self.lab.command('object.create',payload | {'title':'changed'},'fixed')
        self.assertEqual(err.exception.code,'idempotency_conflict')
        new = self.cmd('object.revise',id=first['id'],expected_revision=1,body={'text':'new'})
        self.assertEqual(new['revision'],2)
        self.assertEqual(self.lab.get_object(first['id'],1)['body']['text'],'old')
        with self.assertRaises(LabError):
            self.cmd('object.revise',id=first['id'],expected_revision=1)
        self.cmd('working.save',name='draft',value={'text':'one'},expected_version=0)
        with self.assertRaises(LabError):
            self.cmd('working.save',name='draft',value={},expected_version=0)

    def test_pinned_run_and_transaction_rollback(self):
        study,run = self.fixture()
        self.cmd('object.revise',id=study['id'],expected_revision=1,body={'changed':True})
        self.assertEqual(self.lab.get_object(run['id'])['body']['study']['revision'],1)
        with self.assertRaises(LabError):
            self.cmd('object.revise',id=run['id'],expected_revision=1,body={})
        with self.assertRaises(LabError):
            self.cmd('attempt.plan',run_id=run['id'],trajectory_id='a',position_ids=['p1','p3'],operation='reader')
        self.assertEqual(self.lab.get_state()['attempts'],[])

    def test_uncertain_receipts_and_explicit_retry(self):
        _,run = self.fixture()
        a = self.cmd('attempt.plan',run_id=run['id'],trajectory_id='a',position_ids=['p1'],operation='read')
        for old,new in [('planned','reserved'),('reserved','dispatched')]:
            self.cmd('attempt.transition',id=a['id'],expected_state=old,state=new)
        self.lab.close()
        self.lab = Lab(self.root / 'work')
        self.assertEqual(self.lab.get_attempt(a['id'])['state'],'dispatched')
        with self.assertRaises(LabError):
            self.cmd('attempt.plan',run_id=run['id'],trajectory_id='a',position_ids=['p1'],operation='read',previous_attempt=a['id'])
        self.cmd('attempt.transition',id=a['id'],expected_state='dispatched',state='uncertain')
        retry = self.cmd('attempt.plan',run_id=run['id'],trajectory_id='a',position_ids=['p1'],operation='read',previous_attempt=a['id'])
        self.assertNotEqual(retry['id'],a['id'])
        self.assertTrue(self.lab.coverage(run['id'])['positions'][0]['uncertain'])
        self.assertEqual(self.lab.get_attempt(a['id'])['state'],'uncertain')

    def test_empty_failure_actions_and_shared_denominators(self):
        _,run = self.fixture()
        self.observation(run,text='  ')
        self.observation(run,transport='failed',text='')
        self.observation(run,shape='tool-only',text='',actions=[{'name':'tool'}])
        coverage = self.lab.coverage(run['id'])
        self.assertEqual(coverage['planned'],3)
        self.assertEqual(coverage['observation_count'],3)
        self.assertEqual(coverage['counts']['empty'],2)
        self.assertEqual(coverage['counts']['failed'],2)
        self.assertFalse(coverage['positions'][2]['returned'])
        other = self.cmd('observation.record',run_id=run['id'],position_ids=['p3'],content={'transport':'completed','shape':'tool-only','text':''},provenance={})
        self.assertFalse(self.lab.coverage(run['id'])['positions'][2]['empty'])

    def test_reviewer_heads_diagnostic_disagreement_and_blind_import(self):
        _,run = self.fixture()
        obs = self.observation(run)
        r = self.round(obs)
        one = self.review(r,obs)
        with self.assertRaises(LabError):
            self.review(r,obs)
        self.review(r,obs,'other')
        two = self.review(r,obs,expected_head=one['id'],supersedes=one['id'])
        self.assertEqual(two['supersedes'],one['id'])
        diag = self.round(obs,**{'pass':'diagnostic','parent_round':r['id']})
        self.assertNotEqual(diag['id'],r['id'])
        packet = self.lab.export_round(r['id'])
        raw = json.dumps(packet)
        for private in (obs['id'],run['id'],'hidden-A','DO-NOT-LEAK','delivered evidence'):
            self.assertNotIn(private,raw)
        self.assertIn('governing evidence',raw)
        record = {'id':'j1','observation_id':packet['items'][0]['id'],'reviewer':'external','judgment':{'response_act':'empty','mapping':'ambiguous','rationale':'review'}}
        first = self.lab.import_reviews(packet,[record],'import-1')
        self.assertEqual(first,self.lab.import_reviews(packet,[record],'import-2'))
        with self.assertRaises(LabError):
            self.lab.import_reviews(packet,[record | {'reviewer':'rewrite'}],'import-3')
        with self.assertRaises(LabError):
            self.lab.import_reviews(packet | {'pass':'diagnostic'},[record],'import-4')
        self.assertEqual(len(self.lab.get_state()['reviews']),4)

    def test_backup_restore_and_transfer_complete_history(self):
        blob = self.cmd('artifact.put',text='source bytes')
        source = self.cmd('object.create',kind='source',title='Source',body={'artifact_digest':blob['digest']})
        self.cmd('object.revise',id=source['id'],expected_revision=1,body={'text':'second'})
        _,run = self.fixture()
        obs = self.observation(run)
        r = self.round(obs)
        one = self.review(r,obs)
        self.review(r,obs,expected_head=one['id'],supersedes=one['id'])
        self.lab.export_round(r['id'])
        self.cmd('working.save',name='private-draft',value='not transfer material')
        backup = self.root / 'backup.zip'
        self.lab.backup(backup)
        restored = Lab.restore(backup,self.root / 'restored')
        try:
            self.assertEqual(restored.get_state(),self.lab.get_state())
            self.assertEqual(restored.read_artifact(blob['digest']),b'source bytes')
        finally:
            restored.close()
        transfer = self.root / 'transfer.zip'
        self.lab.export_bundle(transfer,'research-transfer',[{'id':r['id'],'revision':1},{'id':source['id'],'revision':1}])
        restored = Lab.restore(transfer,self.root / 'transfer')
        try:
            self.assertEqual(restored.get_object(source['id'],1)['body']['artifact_digest'],blob['digest'])
            self.assertEqual(restored.get_object(source['id'])['revision'],2)
            self.assertEqual(len(restored.get_state()['reviews']),2)
            self.assertEqual(restored.get_state()['working'],[])
            self.assertEqual(restored.coverage(run['id'])['observation_count'],1)
            self.assertEqual(restored.export_round(r['id']),self.lab.export_round(r['id']))
        finally:
            restored.close()

    def test_publication_withholds_private_ref_and_unselected_drafts(self):
        private = self.obj('source')
        public = self.cmd('object.create',kind='edition',title='Public',visibility='public',body={'text':'approved'},refs=[{'id':private['id'],'revision':1,'relation':'context'}])
        output = self.root / 'public.json'
        self.lab.export_bundle(output,'public-publication',[{'id':public['id'],'revision':1}])
        content = output.read_text()
        self.assertNotIn(private['id'],content)
        self.assertTrue(json.loads(content)['objects'][0]['refs'][0]['withheld'])
        with self.assertRaises(LabError):
            self.lab.export_bundle(self.root / 'bad.json','public-publication',[{'id':private['id'],'revision':1}])

    def test_dependencies_transport_receipts_and_no_unlinked_resend(self):
        _, run = self.fixture()
        parent = self.cmd('attempt.plan',run_id=run['id'],trajectory_id='a',position_ids=['p1'],operation='ingest')
        child = self.cmd('attempt.plan',run_id=run['id'],trajectory_id='a',position_ids=['p1'],operation='read',depends_on=[parent['id']])
        self.cmd('attempt.transition',id=child['id'],expected_state='planned',state='reserved')
        with self.assertRaises(LabError):
            self.cmd('attempt.transition',id=child['id'],expected_state='reserved',state='dispatched')
        for old,new in [('planned','reserved'),('reserved','dispatched')]:
            self.cmd('attempt.transition',id=parent['id'],expected_state=old,state=new)
        with self.assertRaises(LabError):
            self.cmd('attempt.plan',run_id=run['id'],trajectory_id='a',position_ids=['p1'],operation='ingest')
        with self.assertRaises(LabError):
            self.cmd('attempt.transition',id=parent['id'],expected_state='dispatched',state='returned')
        self.cmd('attempt.transition',id=parent['id'],expected_state='dispatched',state='returned',receipt={'driver':'deterministic'})
        self.cmd('attempt.transition',id=child['id'],expected_state='reserved',state='dispatched')
        self.cmd('attempt.transition',id=child['id'],expected_state='dispatched',state='returned',receipt={'output':'receipt'})
        with self.assertRaises(LabError):
            self.cmd('observation.record',run_id=run['id'],attempt_id=child['id'],position_ids=['p1'],content={'transport':'failed','shape':'technical_failure'},provenance={})
        observation = self.cmd('observation.record',run_id=run['id'],attempt_id=child['id'],position_ids=['p1'],content={'transport':'returned','shape':'text','text':'yes'},provenance={})
        self.assertEqual(observation['content']['transport'],'completed')

    def test_cumulative_amendment_atomic_import_and_disposition(self):
        _,run = self.fixture()
        obs = self.observation(run)
        r = self.round(obs)
        packet = self.lab.export_round(r['id'])
        record = {'id':'j1','observation_id':packet['items'][0]['id'],'reviewer':'external','judgment':{'response_act':'answer','mapping':'mapped','decision':'supported','rationale':'first'}}
        self.lab.import_reviews(packet,[record],'first-import')
        amendment = record | {'id':'j2','supersedes':'j1','judgment':record['judgment'] | {'mapping':'ambiguous','decision':None}}
        with self.assertRaises(LabError):
            self.lab.import_reviews(packet,[amendment,record | {'id':'bad','observation_id':'missing'}],'bad-batch')
        self.assertEqual(len(self.lab.get_state()['reviews']),1)
        reviews = self.lab.import_reviews(packet,[record,amendment],'good-batch')['reviews']
        self.assertEqual(len(self.lab.get_state()['reviews']),2)
        self.assertEqual(self.lab.coverage(run['id'])['counts']['mapped'],0)
        self.cmd('review.disposition',round_id=r['id'],review_ids=[x['id'] for x in reviews],decision='unresolved',rationale='retain both')
        self.assertEqual(len(self.lab.get_state()['reviews']),2)
        self.assertEqual(len(self.lab.get_state()['dispositions']),1)
        archive = self.root / 'run-with-reviews.zip'
        self.lab.export_bundle(archive,'research-transfer',[{'id':run['id'],'revision':1}])
        restored = Lab.restore(archive,self.root / 'run-with-reviews')
        try:
            self.assertEqual(len(restored.get_state()['rounds']),1)
            self.assertEqual(len(restored.get_state()['reviews']),2)
            self.assertEqual(len(restored.get_state()['dispositions']),1)
        finally:
            restored.close()

    def test_transfer_excludes_unselected_material_and_schema_spoof(self):
        private = self.obj('source')
        source = self.cmd('object.create',kind='source',title='Selected',body={})
        output = self.root / 'selected.zip'
        self.lab.export_bundle(output,'research-transfer',[{'id':source['id'],'revision':1}])
        restored = Lab.restore(output,self.root / 'selected')
        try:
            with self.assertRaises(LabError):
                restored.get_object(private['id'])
            self.assertEqual(len(restored.list_objects()),1)
        finally:
            restored.close()
        self.lab.db.execute('CREATE TABLE injected(secret TEXT)')
        with self.assertRaises(LabError) as err:
            Lab(self.root / 'work')
        self.assertEqual(err.exception.code,'schema')

    def test_review_protocol_validation_quotes_and_non_mapping_states(self):
        _,run = self.fixture()
        obs = self.observation(run)
        r = self.cmd('round.create',title='Review',protocol='governing-history-1',observation_ids=[obs['id']],contract={'decision_options':['supported','unsupported']},**{'pass':'first'})
        base = {'response_act':'answer','mapping':'mapped','decision':'supported','rationale':'literal'}
        invalid = [base | {'response_act':'made-up'},base | {'mapping':'wrong'},base | {'mapping':'unmapped'},base | {'rationale':'  '},base | {'decision':''},base | {'decision':'outside'}, {k:v for k,v in base.items() if k != 'decision'},base | {'quotes':[{'field':'evidence','text':'delivered evidence'}]},base | {'quotes':[{'field':'response','text':'invented'}]},base | {'quotes':[{'field':'provenance','text':'DO-NOT-LEAK'}]}]
        for judgment in invalid:
            with self.subTest(judgment=judgment), self.assertRaises(LabError):
                self.cmd('review.submit',round_id=r['id'],observation_id=obs['id'],reviewer='r',judgment=judgment)
        self.assertEqual(self.lab.get_state()['reviews'],[])
        self.cmd('review.submit',round_id=r['id'],observation_id=obs['id'],reviewer='r',judgment=base | {'quotes':[{'field':'evidence','text':'governing evidence'},{'field':'response','text':'hello'}]})
        for mapping in ('unmapped','ambiguous','partial','not-applicable','contract-insufficient'):
            # A separate reviewer can preserve an unresolved opinion without a decision.
            self.cmd('review.submit',round_id=r['id'],observation_id=obs['id'],reviewer=mapping,judgment={'response_act':'abstention','mapping':mapping,'rationale':'no decision'})
        self.assertEqual(self.lab.coverage(run['id'])['counts']['mapped'],2)
        another = self.cmd('round.create',title='Input protocol',protocol='delivered-input-2',observation_ids=[obs['id']],contract={},**{'pass':'first'})
        with self.assertRaises(LabError):
            self.cmd('review.submit',round_id=another['id'],observation_id=obs['id'],reviewer='r',judgment=base | {'quotes':[{'field':'evidence','text':'governing evidence'}]})

    def test_observation_shape_and_diagnostic_scope_validation(self):
        _,run = self.fixture()
        bad = [('empty','completed','nonempty'),('empty','failed',''),('whitespace','completed',''),('whitespace','completed','words'),('technical_failure','completed','oops'),('text','completed',''),('tool-only','failed','')]
        for shape,transport,text in bad:
            with self.subTest(shape=shape,transport=transport,text=text), self.assertRaises(LabError):
                self.observation(run,shape=shape,transport=transport,text=text)
        obs = self.observation(run,shape='action',text='',actions=[{'name':'notify'}])
        parent = self.round(obs)
        other = self.observation(run)
        with self.assertRaises(LabError):
            self.round(other,**{'pass':'diagnostic','parent_round':parent['id']})
        with self.assertRaises(LabError):
            self.cmd('round.create',title='Changed protocol',protocol='delivered-input-2',observation_ids=[obs['id']],contract={},parent_round=parent['id'],**{'pass':'diagnostic'})
        self.round(obs,**{'pass':'diagnostic','parent_round':parent['id']})
        self.observation(run,shape='uncertain',transport='uncertain',text='')
        self.assertEqual(self.lab.coverage(run['id'])['counts']['empty'],0)

    def test_transfer_omits_excluded_bytes_not_just_sql_rows(self):
        secret = 'EXCLUDED-PRIVATE-MARKER-' + 'z' * 4096
        unused = self.cmd('artifact.put',text=secret)
        self.cmd('object.create',kind='source',title='Unselected',body={'text':secret,'artifact_digest':unused['digest']})
        self.cmd('working.save',name='private draft',value=secret)
        old_blob = self.cmd('artifact.put',text='historical selected source')
        dependency = self.cmd('object.create',kind='source',title='Dependency',body={'artifact_digest':old_blob['digest']})
        selected = self.cmd('object.create',kind='claim',title='Chosen',body={},refs=[{'id':dependency['id'],'revision':1,'relation':'source'}])
        self.cmd('object.revise',id=selected['id'],expected_revision=1,body={'changed':'later head'},refs=[])
        archive = self.root / 'bounded-transfer.zip'
        self.lab.export_bundle(archive,'research-transfer',[{'id':selected['id'],'revision':1}])
        with zipfile.ZipFile(archive) as z:
            self.assertNotIn(('artifacts/' + unused['digest']),z.namelist())
            self.assertNotIn(b'EXCLUDED-PRIVATE-MARKER-',z.read('lab.sqlite3'))
        restored = Lab.restore(archive,self.root / 'bounded-transfer')
        try:
            self.assertEqual({o['id'] for o in restored.list_objects()},{selected['id'],dependency['id']})
            self.assertEqual(restored.get_object(selected['id'])['revision'],2)
            self.assertEqual(restored.get_object(selected['id'],1)['refs'][0]['id'],dependency['id'])
            self.assertEqual(restored.read_artifact(old_blob['digest']),b'historical selected source')
        finally:
            restored.close()

    def test_public_projection_withholds_run_round_and_private_artifacts(self):
        _,run = self.fixture()
        obs = self.observation(run)
        r = self.round(obs)
        private_blob = self.cmd('artifact.put',text='private-source-body-never-public')
        private = self.cmd('object.create',kind='source',title='Hidden',body={'artifact_digest':private_blob['digest']})
        public_blob = self.cmd('artifact.put',text='approved-public-source')
        public = self.cmd('object.create',kind='source',title='Visible',visibility='public',body={'artifact_digest':public_blob['digest']})
        edition = self.cmd('object.create',kind='edition',title='Publication',visibility='public',body={'text':'Authored conclusion'},refs=[{'id':o['id'],'revision':1,'relation':relation} for o,relation in [(run,'research'),(r,'review'),(private,'context'),(public,'source')]])
        refs = [{'id':edition['id'],'revision':1}]
        projection = self.lab.public_projection(refs)
        raw = json.dumps(projection)
        for hidden in (run['id'],r['id'],private['id'],obs['id'],private_blob['digest'],'private-source-body-never-public'):
            self.assertNotIn(hidden,raw)
        self.assertEqual(len(projection['objects']),2)
        self.assertEqual(sum(ref.get('withheld',False) for ref in projection['objects'][0]['refs']),3)
        self.assertEqual(set(projection['artifacts']),{public_blob['digest']})
        path = self.root / 'publication.json'
        self.lab.export_bundle(path,'public-publication',refs)
        self.assertEqual(json.loads(path.read_text()),projection)

    def test_blind_evidence_and_rubric_survive_upstream_revision_and_transfer(self):
        source = self.cmd('object.create',kind='source',title='Source',body={'text':'original source'})
        _,run = self.fixture()
        obs = self.observation(run,governing_history='frozen old history',input='frozen delivered input')
        contract = {'decision_options':['supported','unsupported'],'instructions':'frozen worksheet'}
        r = self.cmd('round.create',title='Review',protocol='governing-history-1',observation_ids=[obs['id']],contract=contract,**{'pass':'first'})
        contract['instructions'] = 'changed in caller memory'
        self.cmd('object.revise',id=source['id'],expected_revision=1,body={'text':'changed upstream'})
        packet = self.lab.export_round(r['id'])
        self.assertEqual(packet['contract']['instructions'],'frozen worksheet')
        self.assertEqual(packet['items'][0]['evidence'],'frozen old history')
        changed = self.cmd('round.create',title='New rubric',protocol='governing-history-1',observation_ids=[obs['id']],contract={'instructions':'different worksheet'},**{'pass':'diagnostic','parent_round':r['id']})
        self.assertEqual(self.lab.export_round(r['id']),packet)
        archive = self.root / 'frozen-round.zip'
        self.lab.export_bundle(archive,'research-transfer',[{'id':r['id'],'revision':1}])
        restored = Lab.restore(archive,self.root / 'frozen-round')
        try:
            self.assertEqual(restored.export_round(r['id']),packet)
            self.assertEqual(restored.get_object(changed['id'])['body']['contract']['instructions'],'different worksheet')
            self.assertEqual(restored._get_record(obs['id'],'observation')['content']['input'],'frozen delivered input')
            with self.assertRaises(LabError):
                restored.get_object(source['id'])
        finally:
            restored.close()

    def test_public_analysis_legacy_structural_runtime_reference_rejected(self):
        _,run = self.fixture()
        obs = self.observation(run)
        r = self.round(obs)
        for field, value in [('run_id',run['id']),('round_id',r['id']),('observation_id',obs['id']),('attempt_id','internal-attempt')]:
            analysis = self.cmd('object.create',kind='analysis',title='Legacy analysis',visibility='public',body={'result':{'summary':'authored','detail':{field:value}}})
            refs = [{'id':analysis['id'],'revision':1}]
            with self.subTest(field=field), self.assertRaises(LabError) as err:
                self.lab.public_projection(refs)
            self.assertEqual(err.exception.code,'privacy')
            self.assertIn(field,err.exception.message)
            self.assertNotIn(value,err.exception.message)
            output = self.root / (field + '.json')
            with self.assertRaises(LabError):
                self.lab.export_bundle(output,'public-publication',refs)
            self.assertFalse(output.exists())
        # Arbitrary authored prose is preserved, not scanned or rewritten.
        edition = self.cmd('object.create',kind='edition',title='Reviewed edition',visibility='public',body={'text':'The run_id field is discussed here.','run_id':{'withheld':True}},refs=[{'id':run['id'],'revision':1,'relation':'derived-from'}])
        projected = self.lab.public_projection([{'id':edition['id'],'revision':1}])
        self.assertEqual(projected['objects'][0]['body']['text'],'The run_id field is discussed here.')
        self.assertNotIn(run['id'],json.dumps(projected))

    def test_archive_traversal_missing_blob_and_future_schema(self):
        evil = self.root / 'evil.zip'
        with zipfile.ZipFile(evil,'w') as z:
            z.writestr('../escape',b'bad')
        with self.assertRaises(LabError):
            Lab.restore(evil,self.root / 'evil')
        blob = self.cmd('artifact.put',text='bytes')
        archive = self.root / 'good.zip'
        self.lab.backup(archive)
        broken = self.root / 'missing.zip'
        with zipfile.ZipFile(archive) as src, zipfile.ZipFile(broken,'w') as dst:
            for n in src.namelist():
                if not n.startswith('artifacts/'):
                    dst.writestr(n,src.read(n))
        with self.assertRaises(LabError):
            Lab.restore(broken,self.root / 'broken')
        (self.lab.blobs / blob['digest']).unlink()
        with self.assertRaises((LabError,OSError)):
            self.lab.backup(self.root / 'missing-source.zip')
        self.lab.db.execute('PRAGMA user_version=999')
        with self.assertRaises(LabError) as err:
            Lab(self.root / 'work')
        self.assertEqual(err.exception.code,'schema')


if __name__ == '__main__':
    unittest.main()
