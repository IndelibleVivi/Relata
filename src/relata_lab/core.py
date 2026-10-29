"""Transactional research state; immutable revisions and content-addressed material.

This module deliberately has no provider, subprocess, network, or repository reader.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3
import tempfile
import uuid
import zipfile

SCHEMA = 1
KINDS = {'thread', 'source', 'snapshot', 'claim', 'study', 'run', 'round', 'analysis', 'edition', 'binding'}
TRANSITIONS = {
    'planned': {'reserved', 'cancelled'},
    'reserved': {'dispatched', 'cancelled'},
    'dispatched': {'returned', 'failed', 'uncertain'},
    'uncertain': {'returned', 'failed', 'cancelled'},
    'returned': set(), 'failed': set(), 'cancelled': set(),
}


class LabError(Exception):
    def __init__(self, code, message, detail=None):
        self.code, self.message, self.detail = code, message, detail
        super().__init__(message)


def encoded(value):
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise LabError('invalid', 'Material must be finite JSON.', str(exc)) from exc


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(prefix):
    return prefix + '-' + uuid.uuid4().hex


def require(test, message, code='invalid'):
    if not test:
        raise LabError(code, message)


class Lab:
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.blobs = self.workspace / 'artifacts'
        self.blobs.mkdir(exist_ok=True)
        self.db = sqlite3.connect(self.workspace / 'lab.sqlite3', isolation_level=None)
        self.db.row_factory = sqlite3.Row
        version = self.db.execute('PRAGMA user_version').fetchone()[0]
        if version not in (0, SCHEMA):
            self.db.close()
            raise LabError('schema', 'Unsupported workspace schema.', {'found': version, 'supported': SCHEMA})
        if version == 0:
            existing = self.db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            require(not existing, 'Unversioned database cannot be migrated automatically.', 'schema')
            self.db.executescript('''
                CREATE TABLE objects(id TEXT, revision INTEGER, value TEXT NOT NULL, PRIMARY KEY(id,revision));
                CREATE TABLE records(id TEXT PRIMARY KEY, kind TEXT NOT NULL, value TEXT NOT NULL);
                CREATE TABLE working(name TEXT PRIMARY KEY, version INTEGER NOT NULL, value TEXT NOT NULL);
                CREATE TABLE commands(id TEXT PRIMARY KEY, request TEXT NOT NULL, result TEXT NOT NULL);
                CREATE TABLE artifacts(digest TEXT PRIMARY KEY, media_type TEXT NOT NULL, size INTEGER NOT NULL);
                PRAGMA user_version=1;
            ''')
        expected_columns = {
            'objects': [('id','TEXT',1),('revision','INTEGER',2),('value','TEXT',0)],
            'records': [('id','TEXT',1),('kind','TEXT',0),('value','TEXT',0)],
            'working': [('name','TEXT',1),('version','INTEGER',0),('value','TEXT',0)],
            'commands': [('id','TEXT',1),('request','TEXT',0),('result','TEXT',0)],
            'artifacts': [('digest','TEXT',1),('media_type','TEXT',0),('size','INTEGER',0)],
        }
        schema_objects = self.db.execute("SELECT type,name FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'").fetchall()
        valid = {(r[0],r[1]) for r in schema_objects} == {('table',name) for name in expected_columns}
        for table, columns in expected_columns.items():
            actual = [(r[1],r[2],r[5]) for r in self.db.execute('PRAGMA table_info(' + table + ')')]
            valid = valid and actual == columns
        if not valid:
            self.db.close()
            raise LabError('schema', 'Workspace table definitions do not match the supported schema.')
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA busy_timeout=5000')

    def close(self):
        self.db.close()

    def _rows(self, kind=None):
        rows = self.db.execute('SELECT value FROM records' + (' WHERE kind=?' if kind else '') + ' ORDER BY rowid', (kind,) if kind else ())
        return [json.loads(r[0]) for r in rows]

    def _record(self, kind, value):
        value = dict(value)
        value.setdefault('id', identity(kind))
        self.db.execute('INSERT INTO records VALUES(?,?,?)', (value['id'], kind, encoded(value)))
        return value

    def _get_record(self, ident, kind=None):
        row = self.db.execute('SELECT kind,value FROM records WHERE id=?', (ident,)).fetchone()
        require(row is not None and (kind is None or row['kind'] == kind), 'Record does not exist: ' + str(ident), 'not_found')
        return json.loads(row['value'])

    def get_object(self, id, revision=None):
        row = self.db.execute('SELECT value FROM objects WHERE id=?' + (' AND revision=?' if revision is not None else '') + ' ORDER BY revision DESC LIMIT 1', (id, revision) if revision is not None else (id,)).fetchone()
        require(row is not None, 'Object revision does not exist: ' + str(id), 'not_found')
        return json.loads(row[0])

    def list_objects(self, kind=None):
        objects = [json.loads(r[0]) for r in self.db.execute('SELECT o.value FROM objects o WHERE revision=(SELECT MAX(revision) FROM objects WHERE id=o.id) ORDER BY o.rowid')]
        return [o for o in objects if kind is None or o['kind'] == kind]

    def get_state(self):
        result = {'schema': SCHEMA, 'objects': self.list_objects(), 'working': [dict(r) | {'value': json.loads(r['value'])} for r in self.db.execute('SELECT * FROM working ORDER BY name')]}
        for key, kind in [('attempts','attempt'), ('observations','observation'), ('reviews','review'), ('dispositions','disposition'), ('events','event')]:
            result[key] = [self.get_attempt(a['id']) for a in self._rows(kind)] if kind == 'attempt' else self._rows(kind)
        result['runs'] = self.list_objects('run')
        result['rounds'] = self.list_objects('round')
        return result

    def _validate_refs(self, refs):
        require(isinstance(refs, list), 'refs must be a list.')
        for ref in refs:
            require(isinstance(ref, dict) and set(ref) == {'id','revision','relation'} and isinstance(ref['relation'], str), 'Each ref needs id, revision and relation.')
            self.get_object(ref['id'], ref['revision'])

    def _object(self, payload, revise=False):
        if revise:
            old = self.get_object(payload['id'])
            require(payload.get('expected_revision') == old['revision'], 'Object head changed; reload before revising.', 'conflict')
            require(old['kind'] not in {'run','round'}, 'Runs and review rounds are fixed; create a new object.')
            value = old | {k: payload[k] for k in ('title','body','refs','visibility') if k in payload}
            value['revision'] += 1
        else:
            value = {'id': payload.get('id', identity('obj')), 'revision': 1, 'kind': payload['kind'], 'title': payload['title'], 'body': payload.get('body', {}), 'refs': payload.get('refs', []), 'visibility': payload.get('visibility','private')}
            require(not self.db.execute('SELECT 1 FROM objects WHERE id=?', (value['id'],)).fetchone(), 'Object ID already exists.', 'conflict')
        require(value['kind'] in KINDS, 'Unsupported object kind.')
        require(isinstance(value['title'], str) and isinstance(value['body'], dict), 'title must be text and body must be an object.')
        require(value['visibility'] in {'private','public'}, 'Unsupported visibility.')
        self._validate_refs(value['refs'])
        self._validate_artifacts(value['body'])
        self.db.execute('INSERT INTO objects VALUES(?,?,?)', (value['id'],value['revision'],encoded(value)))
        return value

    def _validate_artifacts(self, value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {'artifact_digest', 'digest'} and isinstance(item, str) and re.fullmatch('[0-9a-f]{64}', item):
                    self.read_artifact(item)
                else:
                    self._validate_artifacts(item)
        elif isinstance(value, list):
            for item in value:
                self._validate_artifacts(item)

    def read_artifact(self, digest):
        require(isinstance(digest,str) and re.fullmatch('[0-9a-f]{64}', digest), 'Invalid artifact digest.')
        row = self.db.execute('SELECT size FROM artifacts WHERE digest=?', (digest,)).fetchone()
        require(row is not None, 'Artifact is not registered.', 'missing_artifact')
        try:
            data = (self.blobs / digest).read_bytes()
        except OSError as exc:
            raise LabError('missing_artifact','Artifact bytes are missing.', digest) from exc
        require(len(data) == row[0] and hashlib.sha256(data).hexdigest() == digest, 'Artifact integrity check failed.', 'integrity')
        return data

    def _put(self, p):
        require(isinstance(p.get('text'), str), 'artifact.put requires UTF-8 text.')
        data = p['text'].encode('utf-8')
        key = digest(data)
        target = self.blobs / key
        if target.exists():
            require(target.read_bytes() == data, 'Artifact digest collision or corruption.', 'integrity')
        else:
            fd, name = tempfile.mkstemp(dir=self.blobs, prefix='.pending-')
            try:
                with os.fdopen(fd, 'wb') as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(name,target)
            finally:
                if os.path.exists(name):
                    os.unlink(name)
        media = p.get('media_type','text/plain; charset=utf-8')
        require(isinstance(media,str), 'media_type must be text.')
        self.db.execute('INSERT OR IGNORE INTO artifacts VALUES(?,?,?)', (key,media,len(data)))
        return {'digest': key, 'media_type': media, 'size': len(data)}

    def command(self, name, payload, command_id: str):
        require(isinstance(command_id,str) and bool(command_id), 'A nonempty command_id is required.')
        require(isinstance(payload,dict), 'Command payload must be an object.')
        request = encoded({'name':name,'payload':payload})
        self.db.execute('BEGIN IMMEDIATE')
        try:
            old = self.db.execute('SELECT request,result FROM commands WHERE id=?',(command_id,)).fetchone()
            if old:
                require(old[0] == request, 'command_id was already used with different material.', 'idempotency_conflict')
                result = json.loads(old[1])
            else:
                result = self._dispatch(name,payload)
                self.db.execute('INSERT INTO commands VALUES(?,?,?)',(command_id,request,encoded(result)))
            self.db.execute('COMMIT')
            return result
        except (KeyError, TypeError, ValueError) as exc:
            self.db.execute('ROLLBACK')
            raise LabError('invalid', 'Missing or malformed command fields.', str(exc)) from exc
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def _run(self, id):
        run = self.get_object(id)
        require(run['kind'] == 'run', 'Expected run object.')
        return run

    def _positions(self, run_id, ids):
        run = self._run(run_id)
        require(isinstance(ids,list) and ids and len(set(ids)) == len(ids), 'Use a nonempty unique position list.')
        require(set(ids) <= {p['id'] for p in run['body']['positions']}, 'Unknown run position.')
        return run

    def get_attempt(self, id):
        a = self._get_record(id,'attempt') | {'state':'planned'}
        a['events'] = [e for e in self._rows('event') if e['attempt_id'] == id]
        for e in a['events']:
            a['state'] = e['state']
        return a

    def _round(self, id):
        r = self.get_object(id)
        require(r['kind'] == 'round', 'Expected review round.')
        return r

    def _dispatch(self, name, p):
        if name == 'artifact.put':
            return self._put(p)
        if name in {'analysis.save', 'analysis.claim'}:
            from . import analysis
            return getattr(analysis, name.split('.', 1)[1])(self, p)
        if name in {'object.create','object.revise'}:
            require(p.get('kind') not in {'run','round'}, 'Use run.create or round.create for fixed material.')
            return self._object(p,name == 'object.revise')
        if name == 'working.save':
            row = self.db.execute('SELECT version FROM working WHERE name=?',(p['name'],)).fetchone()
            version = row[0] if row else 0
            require(p.get('expected_version',version) == version, 'Working set changed; reload before saving.', 'conflict')
            self.db.execute('INSERT OR REPLACE INTO working VALUES(?,?,?)',(p['name'],version+1,encoded(p['value'])))
            return {'name':p['name'],'version':version+1,'value':p['value']}
        if name == 'run.create':
            study = self.get_object(p['study']['id'],p['study']['revision'])
            require(study['kind'] == 'study', 'run.study must reference a study revision.')
            trajectories, positions = p['trajectories'], p['positions']
            require(isinstance(trajectories,list) and trajectories and isinstance(positions,list) and positions, 'Run needs trajectories and planned positions.')
            tids = [t['id'] for t in trajectories]
            require(len(tids) == len(set(tids)), 'Duplicate trajectory ID.')
            require(len({x['id'] for x in positions}) == len(positions), 'Duplicate position ID.')
            for x in positions:
                require(x['trajectory_id'] in tids and 'condition' in x and 'checkpoint' in x, 'Position needs trajectory, condition and checkpoint.')
            return self._object({'kind':'run','title':p['title'],'body':{'study':p['study'],'trajectories':trajectories,'positions':positions},'refs':[p['study'] | {'relation':'study'}]})
        if name == 'attempt.plan':
            run = self._positions(p['run_id'],p['position_ids'])
            require(all(x['trajectory_id'] == p['trajectory_id'] for x in run['body']['positions'] if x['id'] in p['position_ids']), 'Attempt positions must share its trajectory.')
            require(isinstance(p['operation'],str) and p['operation'], 'Attempt needs operation.')
            deps = p.get('depends_on',[])
            for id in deps:
                require(self.get_attempt(id)['run_id'] == p['run_id'], 'Dependency belongs to another run.')
            previous = p.get('previous_attempt')
            predecessors = [a for a in self._rows('attempt') if a['run_id'] == p['run_id'] and a['trajectory_id'] == p['trajectory_id'] and a['operation'] == p['operation'] and set(a['position_ids']) & set(p['position_ids'])]
            if predecessors:
                require(previous == predecessors[-1]['id'], 'Overlapping repeat operation must explicitly retry its latest attempt.', 'conflict')
            if previous:
                old = self.get_attempt(previous)
                require(old['run_id'] == p['run_id'] and old['trajectory_id'] == p['trajectory_id'] and old['position_ids'] == p['position_ids'] and old['operation'] == p['operation'], 'Retry must preserve operation and positions.')
                require(old['state'] in {'failed','uncertain','cancelled'}, 'Only a failed, uncertain or cancelled attempt may be retried.')
            return self._record('attempt', {'run_id':p['run_id'],'trajectory_id':p['trajectory_id'],'position_ids':p['position_ids'],'operation':p['operation'],'depends_on':deps,'previous_attempt':previous}) | {'state':'planned','events':[]}
        if name == 'attempt.transition':
            a = self.get_attempt(p['id'])
            require(a['state'] == p['expected_state'], 'Attempt state changed.', 'conflict')
            require(p['state'] in TRANSITIONS[a['state']], 'Illegal attempt transition.')
            if p['state'] == 'dispatched':
                require(all(self.get_attempt(id)['state'] == 'returned' for id in a['depends_on']), 'Dependencies have not returned.')
            if p['state'] in {'returned','failed'}:
                require(isinstance(p.get('receipt'),dict) and p['receipt'], 'A terminal transport result requires a receipt.')
            self._record('event',{'attempt_id':a['id'],'state':p['state'],'receipt':p.get('receipt')})
            return self.get_attempt(a['id'])
        if name == 'observation.record':
            run = self._positions(p['run_id'],p['position_ids'])
            content = dict(p['content'])
            if content.get('transport') == 'returned':
                content['transport'] = 'completed'
            require(isinstance(content,dict) and content.get('transport') in {'completed','failed','uncertain'} and isinstance(content.get('shape'),str), 'Observation needs explicit transport and shape.')
            require(content['shape'] in {'text','empty','whitespace','tool-only','action','json','technical_failure','technical-failure','uncertain'}, 'Unknown observation shape.')
            text = content.get('text','')
            require(isinstance(text,str), 'Observation text must be literal text.')
            if content['shape'] == 'empty':
                require(content['transport'] == 'completed' and text == '' and not content.get('actions'), 'Empty shape requires completed empty text without actions.')
            elif content['shape'] == 'whitespace':
                require(content['transport'] == 'completed' and bool(text) and not text.strip() and not content.get('actions'), 'Whitespace shape requires completed nonempty whitespace without actions.')
            elif content['shape'] == 'uncertain':
                require(content['transport'] == 'uncertain', 'Uncertain shape requires uncertain transport.')
            elif content['shape'] in {'technical_failure','technical-failure'}:
                require(content['transport'] == 'failed', 'Technical-failure shape requires failed transport.')
            elif content['shape'] in {'text','json'}:
                require(content['transport'] == 'completed' and bool(text.strip()), 'Text/JSON shape requires completed nonblank response text.')
            elif content['shape'] in {'action','tool-only'}:
                require(content['transport'] == 'completed', 'Action/tool-only shape requires completed transport.')
            require(isinstance(p['provenance'],dict), 'Observation provenance must be an object.')
            attempt = p.get('attempt_id')
            if attempt:
                a = self.get_attempt(attempt)
                require(a['run_id'] == run['id'] and set(p['position_ids']) <= set(a['position_ids']), 'Observation does not match attempt.')
                require(a['state'] in {'returned','failed','uncertain'}, 'Record attempt transport result before observation.')
                require({'returned':'completed','failed':'failed','uncertain':'uncertain'}[a['state']] == content['transport'], 'Observation transport contradicts attempt receipt.')
            self._validate_artifacts(content)
            return self._record('observation', {'run_id':run['id'],'attempt_id':attempt,'position_ids':p['position_ids'],'content':content,'provenance':p['provenance']})
        if name == 'round.create':
            require(p['protocol'] in {'governing-history-1','delivered-input-2'}, 'Unknown evidence protocol.')
            require(p['pass'] in {'first','diagnostic'}, 'Unknown review pass.')
            require(isinstance(p['contract'],dict) and isinstance(p.get('disclosure',{}),dict), 'Contract and disclosure must be objects.')
            ids = p['observation_ids']
            require(isinstance(ids,list) and ids and len(set(ids)) == len(ids), 'Round needs unique observations.')
            for id in ids:
                self._get_record(id,'observation')
            if p['pass'] == 'diagnostic':
                require(p.get('parent_round'), 'Diagnostic review requires a parent round.')
            if p.get('parent_round'):
                parent = self._round(p['parent_round'])
                require(parent['body']['protocol'] == p['protocol'], 'Diagnostic parent must use the same evidence protocol.')
                require(set(ids) <= set(parent['body']['observation_ids']), 'Diagnostic observations must be within the parent round scope.')
            options = p['contract'].get('decision_options')
            if options is not None:
                require(isinstance(options,list) and options and all(isinstance(x,str) and x.strip() for x in options) and len(options) == len(set(options)), 'decision_options must be nonempty unique text labels.')
            body = {k:p[k] for k in ('protocol','observation_ids','contract','pass')}
            body.update(parent_round=p.get('parent_round'),disclosure=p.get('disclosure',{}))
            return self._object({'kind':'round','title':p['title'],'body':body})
        if name == 'review.submit':
            round = self._round(p['round_id'])
            require(p['observation_id'] in round['body']['observation_ids'], 'Observation is not in this round.')
            require(isinstance(p['reviewer'],str) and p['reviewer'], 'Reviewer identity is required.')
            j = p['judgment']
            require(isinstance(j,dict) and all(k in j for k in ('response_act','mapping','rationale')), 'Judgment needs response_act, mapping and rationale.')
            require(j['response_act'] in {'answer','clarification','abstention','refusal','action','empty','technical-failure','other'}, 'Unknown response_act.')
            require(j['mapping'] in {'mapped','unmapped','ambiguous','partial','not-applicable','contract-insufficient'}, 'Unknown mapping status.')
            require(isinstance(j['rationale'],str) and bool(j['rationale'].strip()), 'Review rationale must be nonempty literal text.')
            if j['mapping'] == 'mapped':
                require(isinstance(j.get('decision'),str) and bool(j['decision'].strip()), 'Mapped judgment requires an explicit decision.')
                options = round['body']['contract'].get('decision_options')
                require(options is None or j['decision'] in options, 'Decision is not allowed by this round contract.')
            else:
                require(j.get('decision') is None or j.get('decision') == '', 'A non-mapped judgment cannot carry a finite decision.')
            if 'quotes' in j:
                require(isinstance(j['quotes'],list), 'quotes must be a list.')
                content = self._get_record(p['observation_id'],'observation')['content']
                evidence_field = 'governing_history' if round['body']['protocol'] == 'governing-history-1' else 'input'
                evidence = content.get(evidence_field)
                response = content.get('text','')
                actions = encoded(content['actions']) if 'actions' in content else ''
                for quote in j['quotes']:
                    require(isinstance(quote,dict) and set(quote) == {'field','text'} and quote['field'] in {'evidence','response'} and isinstance(quote['text'],str) and bool(quote['text']), 'Quote needs field=evidence|response and nonempty literal text.')
                    haystacks = [evidence] if quote['field'] == 'evidence' else [response,actions]
                    require(any(isinstance(h,str) and quote['text'] in h for h in haystacks), 'Quote is not an exact substring of this protocol evidence/response.')
            chain = [r for r in self._rows('review') if (r['round_id'],r['observation_id'],r['reviewer']) == (p['round_id'],p['observation_id'],p['reviewer'])]
            head = chain[-1]['id'] if chain else None
            require(p.get('expected_head') == head and p.get('supersedes') == head, 'Review head changed; amendments must explicitly name the same reviewer head.', 'conflict')
            return self._record('review', {k:p.get(k) for k in ('round_id','observation_id','reviewer','supersedes','judgment')})
        if name == 'review.disposition':
            round = self._round(p['round_id'])
            refs = p['review_ids']
            require(isinstance(refs,list) and refs, 'Disposition must cite judgments.')
            for id in refs:
                require(self._get_record(id,'review')['round_id'] == round['id'], 'Disposition judgment belongs to another round.')
            return self._record('disposition', {'round_id':round['id'],'review_ids':refs,'decision':p['decision'],'rationale':p['rationale']})
        if name == 'review.import':
            return self._import_reviews(p)
        raise LabError('unknown_command', 'Unsupported command: ' + str(name))

    def coverage(self, run_id):
        run = self._run(run_id)
        observations = [o for o in self._rows('observation') if o['run_id'] == run_id]
        attempts = [self.get_attempt(a['id']) for a in self._rows('attempt') if a['run_id'] == run_id]
        reviews = self._rows('review')
        rows = []
        for position in run['body']['positions']:
            obs = [o for o in observations if position['id'] in o['position_ids']]
            ats = [a for a in attempts if position['id'] in a['position_ids']]
            js = [j for j in reviews if j['observation_id'] in {o['id'] for o in obs}]
            superseded = {j['supersedes'] for j in js if j.get('supersedes')}
            heads = [j for j in js if j['id'] not in superseded]
            rows.append(position | {'attempted':any(any(e['state']=='dispatched' for e in a['events']) for a in ats), 'returned':any(a['state']=='returned' for a in ats) or any(o['content']['transport']=='completed' for o in obs), 'failed':any(a['state']=='failed' for a in ats) or any(o['content']['transport']=='failed' for o in obs), 'uncertain':any(a['state']=='uncertain' for a in ats) or any(o['content']['transport']=='uncertain' for o in obs), 'empty':any(o['content']['transport']=='completed' and not o['content'].get('text','').strip() and not o['content'].get('actions') and o['content']['shape'] not in {'tool-only','action'} for o in obs), 'reviewed':bool(js), 'mapped':any(j['judgment']['mapping'] == 'mapped' for j in heads), 'observation_ids':[o['id'] for o in obs]})
        totals = {key:sum(bool(r[key]) for r in rows) for key in ('attempted','returned','failed','uncertain','empty','reviewed','mapped')}
        return {'run_id':run_id,'unit':'planned_position','planned':len(rows),'counts':totals,'positions':rows,'attempt_count':len(attempts),'observation_count':len(observations),'trajectory_count':len(run['body']['trajectories']), 'note':'Shared observations count once as observations; position coverage is not independent samples.'}

    def export_round(self, round_id, path=None):
        """Export only allowlisted evidence. Mapping remains in the local database."""
        self.db.execute('BEGIN IMMEDIATE')
        try:
            r = self._round(round_id)
            existing = [b for b in self._rows('blind_binding') if b['round_id'] == round_id]
            if existing:
                packet = existing[0]['packet']
            else:
                mapping, items = {}, []
                field = 'governing_history' if r['body']['protocol'] == 'governing-history-1' else 'input'
                for oid in r['body']['observation_ids']:
                    o = self._get_record(oid,'observation')
                    anon = identity('item')
                    mapping[anon] = oid
                    # Evidence must be explicit literal text, never an arbitrary metadata object.
                    evidence = o['content'].get(field)
                    require(isinstance(evidence,str), 'Protocol evidence is missing or is not literal text: ' + field)
                    response = {k:o['content'][k] for k in ('transport','shape','text','actions') if k in o['content']}
                    items.append({'id':anon,'evidence':evidence,'response':response})
                # Contract is a public reviewer worksheet, explicitly selected by the author.
                packet = {'format':'relata-blind-review-1','packet_id':identity('packet'),'protocol':r['body']['protocol'],'pass':r['body']['pass'],'contract':r['body']['contract'],'items':items}
                packet['binding'] = digest(encoded(packet).encode())
                self._record('blind_binding',{'round_id':round_id,'mapping':mapping,'packet':packet})
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise
        if path is not None:
            self._write_new(Path(path), encoded(packet).encode())
        return packet

    def import_reviews(self, packet, records, command_id):
        return self.command('review.import', {'packet':packet,'records':records},command_id)

    def _import_reviews(self, p):
        packet = p['packet']
        bindings = [b for b in self._rows('blind_binding') if b['packet'] == packet]
        require(len(bindings) == 1, 'Packet does not match an original local blind binding.', 'binding')
        bound = bindings[0]
        result = []
        require(isinstance(p['records'],list), 'Import records must be a list.')
        for record in p['records']:
            rid = record['id']
            require(isinstance(rid,str) and rid, 'Imported judgment needs a stable ID.')
            previous = [r for r in self._rows('import') if r['external_id'] == rid and r['packet_id'] == packet['packet_id']]
            if previous:
                require(previous[0]['record'] == record, 'Imported judgment ID cannot be rewritten.', 'conflict')
                result.append(self._get_record(previous[0]['review_id'],'review'))
                continue
            oid = bound['mapping'].get(record['observation_id'])
            require(oid is not None, 'Unknown anonymous observation.', 'binding')
            supersedes = record.get('supersedes')
            internal_head = None
            if supersedes:
                matches = [r for r in self._rows('import') if r['packet_id'] == packet['packet_id'] and r['external_id'] == supersedes]
                require(len(matches) == 1, 'Unknown imported amendment parent.', 'binding')
                internal_head = matches[0]['review_id']
            review = self._dispatch('review.submit', {'round_id':bound['round_id'],'observation_id':oid,'reviewer':record['reviewer'],'judgment':record['judgment'],'supersedes':internal_head,'expected_head':internal_head})
            self._record('import',{'packet_id':packet['packet_id'],'external_id':rid,'record':record,'review_id':review['id']})
            result.append(review)
        return {'reviews':result}

    @staticmethod
    def _write_new(path, data):
        path.parent.mkdir(parents=True,exist_ok=True)
        try:
            with path.open('xb') as f:
                f.write(data)
        except FileExistsError as exc:
            raise LabError('exists','Destination already exists; select a new path.',str(path)) from exc

    def _archive(self, path, object_ids=None):
        """Snapshot DB before enumerating blobs; never recursively scan the workspace."""
        path = Path(path)
        require(not path.exists(), 'Archive destination already exists.', 'exists')
        with tempfile.TemporaryDirectory() as temp:
            dbpath = Path(temp) / 'lab.sqlite3'
            snapshot = sqlite3.connect(dbpath)
            self.db.backup(snapshot)
            try:
                if object_ids is not None:
                    self._prune_snapshot(snapshot, object_ids)
                snapshot.commit()
                if object_ids is not None:
                    # DELETE leaves private bytes in SQLite free pages. A transfer must
                    # physically omit excluded drafts, commands and unrelated records.
                    snapshot.execute('VACUUM')
                artifacts = snapshot.execute('SELECT digest,size FROM artifacts').fetchall()
                inventory = {'lab.sqlite3':digest(dbpath.read_bytes())}
                data = {'lab.sqlite3':dbpath.read_bytes()}
                for key,size in artifacts:
                    try:
                        content = (self.blobs / key).read_bytes()
                    except OSError as exc:
                        raise LabError('missing_artifact', 'Referenced artifact is unavailable.', key) from exc
                    require(digest(content) == key and len(content) == size, 'Missing or corrupt referenced artifact.', 'integrity')
                    data['artifacts/' + key] = content
                    inventory['artifacts/' + key] = key
                manifest = {'format':'relata-workspace-1','schema':SCHEMA,'inventory':inventory}
                data['manifest.json'] = encoded(manifest).encode()
                path.parent.mkdir(parents=True,exist_ok=True)
                with path.open('xb') as output:
                    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
                        for name,content in data.items():
                            archive.writestr(name,content)
            finally:
                snapshot.close()
        return {'path':str(path),'schema':SCHEMA,'files':len(data)}

    def backup(self, path):
        return self._archive(path)

    def _prune_snapshot(self, db, object_ids):
        objects = [json.loads(r[0]) for r in db.execute('SELECT value FROM objects')]
        records = [(r[0],r[1],json.loads(r[2])) for r in db.execute('SELECT id,kind,value FROM records')]
        known = {o['id'] for o in objects}
        require(set(object_ids) <= known, 'Transfer selection contains unknown object.', 'not_found')
        selected, rec_ids = set(object_ids), set()
        # Selected run/round includes its complete research history; recursive named dependencies.
        changed = True
        while changed:
            before = (len(selected),len(rec_ids))
            for o in objects:
                if o['kind'] == 'round' and set(o['body']['observation_ids']) & rec_ids:
                    selected.add(o['id'])
                if o['id'] in selected:
                    selected.update(ref['id'] for ref in o['refs'])
                    if o['kind'] == 'round':
                        rec_ids.update(o['body']['observation_ids'])
                        if o['body'].get('parent_round'):
                            selected.add(o['body']['parent_round'])
            for rid,kind,r in records:
                include = rid in rec_ids or r.get('run_id') in selected or r.get('round_id') in selected or r.get('attempt_id') in rec_ids or r.get('review_id') in rec_ids
                if include:
                    rec_ids.add(rid)
                    for key in ('run_id','round_id'):
                        if r.get(key):
                            selected.add(r[key])
                    for key in ('attempt_id','previous_attempt','supersedes','review_id'):
                        if r.get(key):
                            rec_ids.add(r[key])
                    rec_ids.update(r.get('depends_on',[]))
                    rec_ids.update(r.get('review_ids',[]))
            changed = before != (len(selected),len(rec_ids))
        for o in objects:
            if o['id'] not in selected:
                db.execute('DELETE FROM objects WHERE id=?',(o['id'],))
        for rid,kind,r in records:
            if rid not in rec_ids:
                db.execute('DELETE FROM records WHERE id=?',(rid,))
        # Command material and drafts can carry unrelated private content; they are not research history.
        db.execute('DELETE FROM commands')
        db.execute('DELETE FROM working')
        blob_ids = set()
        def visit(v):
            if isinstance(v,dict):
                for k,x in v.items():
                    if k in {'digest','artifact_digest'} and isinstance(x,str) and re.fullmatch('[0-9a-f]{64}',x):
                        blob_ids.add(x)
                    else:
                        visit(x)
            elif isinstance(v,list):
                for x in v:
                    visit(x)
        for row in db.execute('SELECT value FROM objects UNION ALL SELECT value FROM records'):
            visit(json.loads(row[0]))
        for (key,) in db.execute('SELECT digest FROM artifacts').fetchall():
            if key not in blob_ids:
                db.execute('DELETE FROM artifacts WHERE digest=?',(key,))

    @classmethod
    def restore(cls, archive, destination):
        destination = Path(destination)
        require(not destination.exists() or not any(destination.iterdir()), 'Restore requires an empty destination.', 'exists')
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            require(len(names) == len(set(names)), 'Archive contains duplicate members.', 'integrity')
            for name in names:
                p = PurePosixPath(name)
                require(not p.is_absolute() and '..' not in p.parts and '\\' not in name and (name in {'manifest.json','lab.sqlite3'} or re.fullmatch('artifacts/[0-9a-f]{64}',name)), 'Unsafe archive member.', 'integrity')
                require(z.getinfo(name).file_size <= 256 * 1024 * 1024, 'Archive member exceeds restore size limit.', 'integrity')
            require('manifest.json' in names and 'lab.sqlite3' in names, 'Archive manifest or DB missing.', 'integrity')
            manifest = json.loads(z.read('manifest.json'))
            require(manifest.get('format') == 'relata-workspace-1' and manifest.get('schema') == SCHEMA, 'Unsupported archive schema.', 'schema')
            require(set(names) == set(manifest['inventory']) | {'manifest.json'}, 'Archive inventory differs from contents.', 'integrity')
            require(sum(z.getinfo(n).file_size for n in names) <= 512*1024*1024, 'Archive exceeds restore size limit.', 'integrity')
            contents = {name:z.read(name) for name in manifest['inventory']}
            require(all(digest(content) == manifest['inventory'][name] for name,content in contents.items()), 'Archive digest mismatch.', 'integrity')
        # Validate in staging before making destination observable.
        destination.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=destination.parent) as temp:
            staged = Path(temp) / 'workspace'
            staged.mkdir()
            for name,content in contents.items():
                target = staged / name
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(content)
            candidate = cls(staged)
            try:
                require(candidate.db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok','Invalid SQLite database.','integrity')
                expected = {'artifacts/'+r[0] for r in candidate.db.execute('SELECT digest FROM artifacts')}
                require(expected == {n for n in contents if n.startswith('artifacts/')}, 'Artifact inventory does not match DB.', 'missing_artifact')
                for row in candidate.db.execute('SELECT digest FROM artifacts'):
                    candidate.read_artifact(row[0])
                for row in candidate.db.execute('SELECT value FROM objects'):
                    o = json.loads(row[0])
                    candidate._validate_refs(o['refs'])
                    candidate._validate_artifacts(o['body'])
                for value in candidate._rows():
                    candidate._validate_artifacts(value)
            finally:
                candidate.close()
            # Empty existing directory is allowed, but no existing file is overwritten.
            if destination.exists():
                for child in staged.iterdir():
                    os.rename(child,destination / child.name)
            else:
                os.rename(staged,destination)
        return cls(destination)

    def _validate_selection(self, object_refs):
        require(isinstance(object_refs,list) and object_refs, 'Choose explicit object revisions.')
        for ref in object_refs:
            require(isinstance(ref,dict) and isinstance(ref.get('id'),str) and type(ref.get('revision')) is int and ref['revision'] > 0, 'Selection requires object id and positive revision.')
            self.get_object(ref['id'],ref['revision'])

    def public_projection(self, object_refs):
        """Canonical explicit-public projection shared by JSON and presentation exports."""
        self._validate_selection(object_refs)
        # Publication exports explicit public revisions and public ref closure only.
        # Private targets become anonymous withheld markers, never identifying maps.
        queue = list(object_refs)
        seen, objects, artifacts = set(), [], {}
        while queue:
            ref = queue.pop(0)
            key = (ref['id'],ref['revision'])
            if key in seen:
                continue
            seen.add(key)
            o = self.get_object(*key)
            require(o['visibility'] == 'public', 'Publication selection includes private material.', 'privacy')
            require(o['kind'] not in {'run','round'}, 'Runtime/review material needs a separately authored public edition.', 'privacy')
            require(o['body'].get('format') != 'relata-legacy-compat-source-1',
                    'Legacy registrations contain private bindings; author a separate public edition.', 'privacy')
            safe_refs = []
            for child in o['refs']:
                target = self.get_object(child['id'],child['revision'])
                if target['visibility'] == 'public':
                    safe_refs.append(child)
                    queue.append(child)
                else:
                    safe_refs.append({'relation':child['relation'],'withheld':True})
            o = o | {'refs':safe_refs}
            # Earlier public analyses may carry structural runtime IDs in body.
            # Ref closure cannot hide those copies; reject rather than silently
            # publishing a materially incomplete rewritten analysis.
            def check_structural_references(value, path='body'):
                if isinstance(value,dict):
                    for key,item in value.items():
                        location = path + '.' + key
                        if key in {'run_id','round_id','observation_id','attempt_id'}:
                            require(item is None or item == '' or item == {'withheld':True}, 'Public ' + location + ' contains a structural runtime reference; author a public edition with refs or an explicit anonymous withheld marker.', 'privacy')
                        else:
                            check_structural_references(item,location)
                elif isinstance(value,list):
                    for index,item in enumerate(value):
                        check_structural_references(item,path + '[' + str(index) + ']')
            check_structural_references(o['body'])
            # Explicit object bodies are author-approved public material; refs govern closure.
            def collect(v):
                if isinstance(v,dict):
                    for k,x in v.items():
                        if k in {'artifact_digest','digest'} and isinstance(x,str) and re.fullmatch('[0-9a-f]{64}',x):
                            artifacts[x] = self.read_artifact(x)
                        else:
                            collect(x)
                elif isinstance(v,list):
                    for x in v:
                        collect(x)
            collect(o['body'])
            objects.append(o)
        bundle = {'format':'relata-publication-1','objects':objects,'artifacts':{k:v.decode('utf-8') for k,v in artifacts.items()}}
        return bundle

    def export_bundle(self, path, profile, object_refs):
        require(profile in {'research-transfer','public-publication'}, 'Use export_round for blind review; unknown bundle profile.')
        self._validate_selection(object_refs)
        if profile == 'research-transfer':
            return self._archive(path,{ref['id'] for ref in object_refs})
        bundle = self.public_projection(object_refs)
        self._write_new(Path(path),encoded(bundle).encode())
        return {'path':str(path),'objects':len(bundle['objects']),'profile':profile}
