"""Public synthetic observations; stdlib only, in-memory SQLite, no provider calls.
Run with --source pointing to the exact public source commit in the study.
"""
import argparse
import json
from pathlib import Path
import sys
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True, help='lmc-5 checkout at the report commit')
source_root = parser.parse_args().source.resolve()
expected_commit = 'fb3e72c9ee7357c8b17311097b0750082a8a1237'
actual_commit = subprocess.check_output(['git', '-C', str(source_root), 'rev-parse', 'HEAD'], text=True).strip()
dirty = subprocess.check_output(['git', '-C', str(source_root), 'status', '--porcelain'], text=True)
if actual_commit != expected_commit or dirty:
    parser.error('The observation requires a clean checkout at ' + expected_commit)
sys.path[:0] = [str(source_root / 'src'), str(source_root)]
from lmc5 import MemoryStore
from extras.pgvector_backend.night_dream import NightDream, Chunk
out = {}
with MemoryStore(':memory:') as store:
    store.init()
    a, _ = store.add_memory(title='Clinic A delivery', content='The synthetic Clinic A package arrives Tuesday.', thread='clinic_a', fact_key='delivery_day')
    b, _ = store.add_memory(title='Clinic B delivery', content='The synthetic Clinic B package arrives Thursday.', thread='clinic_b', fact_key='delivery_day')
    out['same_fact_key_across_threads'] = {'a_status': store.get_memory(a.id).status, 'b_status': store.get_memory(b.id).status, 'audit_rows': store.conn.execute('SELECT COUNT(*) FROM z_conflict_audits').fetchone()[0]}
source = Chunk(id=1, text='Synthetic adult-user project note: the public rehearsal delivery is on Tuesday. No other delivery dates are established in this source text.')
proposal = {'type': 'fact', 'title': 'Delivery assertion', 'content': 'The synthetic project delivery is definitely on Friday, according to this proposed memory.', 'importance': 8, 'risk': 'normal', 'evidence': 'This quoted evidence does not occur in the supplied chunk.', 'source_chunk_ids': [999]}
r = NightDream(proposer=lambda chunks: [proposal]).run([source], apply=False)
out['night_dream_nonmatching_evidence'] = {'promoted': len(r.promoted), 'rejected': len(r.rejected), 'source_ids': r.promoted[0].source_chunk_ids if r.promoted else []}
print(json.dumps(out, ensure_ascii=False, indent=2))
