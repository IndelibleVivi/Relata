"""Browser contract, recovery and actual JS -> Python review interoperability."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools import rc005_review as review

ROOT = Path(__file__).resolve().parents[1]
DESK = ROOT / "case-lab" / "reviews" / "workbench"


class WorkbenchTests(unittest.TestCase):
    def node(self, body):
        prefix = r"""
const fs=require('node:fs');const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const C=require('./case-lab/reviews/workbench/core.js');
const raw=fs.readFileSync('case-lab/reviews/rc005-review-contract.json');
const contract=JSON.parse(raw);
const wrapper=JSON.parse(fs.readFileSync('case-lab/reviews/workbench/demo.json','utf8'));
const packet=wrapper.packet,item=packet.items[0];
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
const identity={packet_sha256:sha(JSON.stringify(packet,null,2)+'\n'),contract_sha256:sha(raw),practice_only:true};
const form={claims:[{quote:item.response,kind:'ambiguous',attribution:'练习中的回答者',support:'underdetermined',evidence_refs:[],rationale:'仅检查工具互操作，未作语义校准。'}],current_action:'unresolved',clarification:'unresolved',selective_use:'unresolved',confidence_limits:'unresolved',guessability:'cannot-tell',guess_confidence:'unsure',guess_cue:'',rationale:'这是一条作者练习判断。',notes:''};
const judgment={judgment_id:'a'.repeat(32),review_id:item.review_id,supersedes:null,amendment_reason:'',created_at:'2026-10-25T00:00:00.000Z',...form};
const draft={format:contract.draft_format,...identity,rubric_revision:contract.revision,review_pass:'blind',reviewer_id:'练习评审者',selected_review_id:item.review_id,entries:{[item.review_id]:{draft:null,history:[judgment],skipped_reason:'',editing:false,amendment_reason:''}}};
"""
        result = subprocess.run(["node", "-e", prefix + body], cwd=ROOT,
                                text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result.stdout

    def test_generated_reader_has_only_public_practice_and_current_contract(self):
        result = subprocess.run(["node", str(DESK / "build.cjs"), "--check"],
                                cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (DESK / "index.html").read_text()
        for boundary in ("connect-src 'none'", "base-uri 'none'", "form-action 'none'"):
            self.assertIn(boundary, html)
        self.node("C.validatePacket(packet,true); assert.ok(wrapper.practice_only);")

    def test_duplicate_json_and_ambiguous_technical_states_are_rejected(self):
        self.node(r"""
assert.throws(()=>C.strictJSON('{"a":1,"a":2}'),/重复字段/);
assert.throws(()=>C.strictJSON('{"x":{"y":1,"y":2}}'),/重复字段/);
assert.throws(()=>C.strictJSON('[1,]'));
assert.deepEqual(JSON.parse(JSON.stringify(C.strictJSON('{"a":[1,"中",null,false]}'))),{a:[1,'中',null,false]});
for(const change of [i=>{i.response_state='technical-failure';},i=>{i.response=null;},i=>{i.condition='private';}]){
  const p=structuredClone(packet);change(p.items[0]);assert.throws(()=>C.validatePacket(p,true));
}
const p=structuredClone(packet);p.items[0].response='';C.validatePacket(p,true);
assert.throws(()=>C.validatePacket(packet,false),/144/);
""")

    def test_quotes_evidence_and_partial_fields_cannot_become_completed_judgments(self):
        self.node(r"""
C.validateForm(C.emptyForm(),item,contract,true);
assert.throws(()=>C.validateForm(C.emptyForm(),item,contract),/至少记录/);
C.validateRecord(judgment,item,contract);
const wrong=structuredClone(judgment);wrong.claims[0].quote='not in the response';
assert.throws(()=>C.validateRecord(wrong,item,contract),/连续原文/);
wrong.claims[0].quote=item.response;wrong.claims[0].evidence_refs=['H999'];
assert.throws(()=>C.validateRecord(wrong,item,contract),/当前历史/);
wrong.claims[0].evidence_refs=['H1','H1'];
assert.throws(()=>C.validateRecord(wrong,item,contract),/重复/);
const empty=packet.items.find(i=>i.response==='');
C.validateForm({...form,claims:[]},empty,contract);
const technical=packet.items.find(i=>i.response===null);
assert.throws(()=>C.validateForm(form,technical,contract),/技术失败/);
""")

    def test_drafts_bind_exact_packet_contract_practice_and_current_revision(self):
        self.node(r"""
C.validateDraft(draft,packet,identity,contract);
for(const field of ['packet_sha256','contract_sha256','rubric_revision','practice_only']){
 const d=structuredClone(draft);d[field]=field==='practice_only'?false:'changed';
 assert.throws(()=>C.validateDraft(d,packet,identity,contract),/不匹配/);
}
const d=structuredClone(draft);d.private_map={};
assert.throws(()=>C.validateDraft(d,packet,identity,contract),/字段不符合/);
""")

    def test_draft_revisions_retain_one_connected_history_and_reject_forks(self):
        self.node(r"""
const e=draft.entries[item.review_id];
const amended={...structuredClone(judgment),judgment_id:'b'.repeat(32),supersedes:judgment.judgment_id,amendment_reason:'重新判断支持。'};
e.history.push(amended);e.draft=C.emptyForm();e.editing=true;
C.validateDraft(draft,packet,identity,contract);
e.history.push({...amended,judgment_id:'c'.repeat(32)});
assert.throws(()=>C.validateDraft(draft,packet,identity,contract),/修订链断裂/);
""")

    def test_unicode_limits_count_code_points_without_penalizing_chinese(self):
        self.node(r"""
C.text('评'.repeat(120),'alias',true,120);C.text('🌿'.repeat(120),'alias',true,120);
assert.throws(()=>C.text('评'.repeat(121),'alias',true,120));
assert.throws(()=>C.text('🌿'.repeat(121),'alias',true,120));
""")

    def test_real_javascript_submission_imports_into_python_practice_workspace(self):
        encoded = self.node(r"""
C.validateRecord(judgment,item,contract);
process.stdout.write(JSON.stringify({format:contract.batch_format,...identity,rubric_revision:contract.revision,review_pass:'blind',reviewer_id:'练习评审者',records:[judgment]}));
""")
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            workspace = root / "review"
            review.prepare_practice(DESK / "demo.json", workspace)
            source = root / "submitted.json"
            source.write_text(encoded)
            imported = review.import_review(workspace, source)
            self.assertEqual(imported["records"], 1)
            report, _ = review.report(workspace, "json")
            self.assertTrue(report["practice_only"])
            self.assertEqual(report["counts"]["reviewed_current"], 1)
            self.assertEqual(report["counts"]["technical_failures"], 1)


if __name__ == "__main__":
    unittest.main()
