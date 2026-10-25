/* Shared browser/Node checks for a bounded first-pass review workspace.
 * Authoritative research import and native-source verification stay in Python.
 */
((root, factory) => {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.RC005Review = api;
})(globalThis, () => {
  'use strict';
  const fail = message => { throw new Error(message); };
  const need = (value, message) => { if (!value) fail(message); };
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  function shape(value, fields, label) {
    need(object(value) && Object.keys(value).length === fields.length && fields.every(key => Object.hasOwn(value,key)), `${label} 字段不符合合同。`);
  }
  function text(value, label, required = true, max = 20000) {
    need(typeof value === 'string' && [...value].length <= max && (!required || value.trim().length > 0), `${label} 需要${required?'非空':''}文本，且不超过 ${max} 字符。`);
  }
  function strictJSON(raw) {
    // JSON.parse accepts duplicate object keys; source identity must not depend
    // on which duplicate a particular reader happens to keep.
    let at = 0;
    const space = () => { while (/[\x20\t\r\n]/.test(raw[at] || '\0')) at++; };
    const string = () => {
      const start = at++;
      while (at < raw.length) {
        if (raw[at] === '\\') { at += 2; continue; }
        if (raw[at++] === '"') return JSON.parse(raw.slice(start,at));
      }
      return fail('JSON 字符串未结束。');
    };
    const value = (depth = 0) => {
      need(depth <= 64,'JSON 嵌套过深。'); space();
      if (raw[at] === '"') return string();
      if (raw[at] === '{') {
        at++; space(); const result = Object.create(null);
        if (raw[at] === '}') { at++; return result; }
        for (;;) {
          need(raw[at] === '"','JSON 对象键无效。'); const key = string();
          need(!Object.hasOwn(result,key),`JSON 含重复字段：${key}`); space();
          need(raw[at++] === ':','JSON 缺少冒号。'); result[key] = value(depth+1); space();
          const end = raw[at++]; if (end === '}') return result;
          need(end === ',','JSON 对象未结束。'); space();
        }
      }
      if (raw[at] === '[') {
        at++; space(); const result = [];
        if (raw[at] === ']') { at++; return result; }
        for (;;) {
          result.push(value(depth+1)); space(); const end = raw[at++];
          if (end === ']') return result;
          need(end === ',','JSON 数组未结束。'); space();
        }
      }
      for (const [word,parsed] of [['true',true],['false',false],['null',null]]) {
        if (raw.slice(at,at+word.length) === word) { at += word.length; return parsed; }
      }
      const number = raw.slice(at).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/);
      need(number && Number.isFinite(Number(number[0])),'JSON 值无效。');
      at += number[0].length; return Number(number[0]);
    };
    const result = value(); space(); need(at === raw.length,'JSON 末尾含多余内容。'); return result;
  }
  const recordFields = ['judgment_id','review_id','supersedes','amendment_reason','created_at','claims','current_action','clarification','selective_use','confidence_limits','guessability','guess_confidence','guess_cue','rationale','notes'];
  const formFields = ['claims','current_action','clarification','selective_use','confidence_limits','guessability','guess_confidence','guess_cue','rationale','notes'];
  const claimFields = ['quote','kind','attribution','support','evidence_refs','rationale'];
  function validatePacket(packet, practice = false) {
    shape(packet,['format','review_status','items'],'匿名包');
    need(packet.format === 'review-packet-1' && packet.review_status === 'unreviewed','只接受原有 RC-005 未评审匿名包。');
    need(Array.isArray(packet.items) && packet.items.length > 0 && (practice || packet.items.length === 144),'正式 RC-005 匿名包必须含完整 144 个位置。');
    const seen = new Set();
    for (const item of packet.items) {
      shape(item,['context','governing_history','current','response','review_status','instructions','review_id','response_state'],'匿名回答');
      need(typeof item.review_id === 'string' && /^[0-9a-f]{32}$/.test(item.review_id) && !seen.has(item.review_id),'回答 ID 无效或重复。'); seen.add(item.review_id);
      text(item.context,'情境',true,65536); text(item.instructions,'阅读说明',true,10000);
      need(item.review_status === 'unreviewed','源包必须保持未评审状态。');
      need(['complete','technical-failure'].includes(item.response_state),'只接受已经关闭的回答位置。');
      need(item.response_state === 'complete' ? typeof item.response === 'string' : item.response === null,'回答状态与正文不一致。');
      if (item.response !== null) text(item.response,'回答',false,65536);
      shape(item.current,['surface','text'],'当前问题'); text(item.current.surface,'当前 surface'); text(item.current.text,'当前问题');
      need(Array.isArray(item.governing_history) && item.governing_history.length > 0,'缺少 governing history。');
      for (const event of item.governing_history) {
        shape(event,['session','role','surface','text'],'历史事件');
        need(Number.isInteger(event.session) && event.session>0,'历史 session 无效。');
        for (const key of ['role','surface','text']) text(event[key],`历史 ${key}`);
      }
    }
    return packet;
  }
  function fieldOptions(contract, id, claim = false) {
    if (claim && id==='kind') return contract.claim_kind_options.map(option=>option.value);
    if (claim && id==='support') return contract.claim_support_options.map(option=>option.value);
    const group = claim ? contract.claim_fields : contract.dimensions;
    const field = Array.isArray(group) ? group.find(field => field.id === id) : undefined;
    need(field && Array.isArray(field.options),`评审合同缺少 ${id} 选项。`);
    return field.options.map(option => option.value);
  }
  function validateForm(form, item, contract, partial = false) {
    shape(form,formFields,'评审内容');
    need(Array.isArray(form.claims),'主张列表无效。');
    if (!partial) need(item.response_state === 'complete','技术失败不能提交语义判断。');
    if (!partial && item.response?.trim()) need(form.claims.length > 0,'请至少记录一项主张、提案、问题或承诺。');
    for (const claim of form.claims) {
      shape(claim,claimFields,'主张');
      for (const id of ['quote','attribution','rationale']) text(claim[id],`主张 ${id}`,!partial,id==='attribution'?2000:20000);
      if (!partial) need(item.response.includes(claim.quote),'引用必须是原样回答中的连续原文。');
      for (const id of ['kind','support']) need((partial && claim[id]==='') || fieldOptions(contract,id,true).includes(claim[id]),`主张 ${id} 选项无效。`);
      need(Array.isArray(claim.evidence_refs) && new Set(claim.evidence_refs).size === claim.evidence_refs.length,'证据引用无效或重复。');
      if(!partial&&['supported','contradicted'].includes(claim.support))need(claim.evidence_refs.length>0,'支持或矛盾判断需要至少一处历史或当前问题引用。');
      for (const ref of claim.evidence_refs) need(ref==='current' || (typeof ref==='string' && /^H[1-9]\d*$/.test(ref) && Number(ref.slice(1))<=item.governing_history.length),'证据引用不属于当前历史。');
    }
    for (const id of ['current_action','clarification','selective_use','confidence_limits','guessability','guess_confidence']) {
      need((partial && form[id]==='') || fieldOptions(contract,id).includes(form[id]),`${id} 选项尚未填写或无效。`);
    }
    text(form.guess_cue,'条件猜测的文字线索',!partial && form.guessability!=='cannot-tell',2000);
    text(form.rationale,'整体理由',!partial); text(form.notes,'补充笔记',false);
    return form;
  }
  function validateRecord(record,item,contract) {
    shape(record,recordFields,'已提交判断');
    need(typeof record.judgment_id==='string' && /^[0-9a-f]{32}$/.test(record.judgment_id),'判断 ID 无效。');
    need(record.review_id===item.review_id,'判断与回答不匹配。');
    need(record.supersedes===null || (typeof record.supersedes==='string' && /^[0-9a-f]{32}$/.test(record.supersedes)),'被修订判断 ID 无效。');
    text(record.amendment_reason,'修订理由',record.supersedes!==null);
    need(record.supersedes!==null || record.amendment_reason==='','首份判断不能带修订理由。');
    need(typeof record.created_at==='string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$/.test(record.created_at) && Number.isFinite(Date.parse(record.created_at)) && new Date(record.created_at).toISOString().slice(0,19)===record.created_at.slice(0,19),'判断日期无效。');
    validateForm(Object.fromEntries(formFields.map(key=>[key,record[key]])),item,contract);
  }
  function emptyForm() {
    return {claims:[],current_action:'',clarification:'',selective_use:'',confidence_limits:'',guessability:'',guess_confidence:'',guess_cue:'',rationale:'',notes:''};
  }
  function validateDraft(draft,packet,identity,contract) {
    shape(draft,['format','packet_sha256','contract_sha256','rubric_revision','review_pass','reviewer_id','practice_only','selected_review_id','entries'],'草稿');
    need(draft.format==='rc005-review-draft-1' && draft.packet_sha256===identity.packet_sha256 && draft.contract_sha256===identity.contract_sha256 && draft.rubric_revision===contract.revision && draft.review_pass==='blind' && draft.practice_only===identity.practice_only,'草稿与当前源包、评审合同或练习状态不匹配。');
    text(draft.reviewer_id,'Reviewer alias',true,120);
    const byId = new Map(packet.items.map(item=>[item.review_id,item]));
    need(byId.has(draft.selected_review_id),'草稿选择的回答不存在。'); need(object(draft.entries),'草稿记录无效。');
    const ids = new Set();
    for (const [id,entry] of Object.entries(draft.entries)) {
      const item = byId.get(id); need(item,'草稿含未知回答。');
      shape(entry,['draft','history','skipped_reason','editing','amendment_reason'],'草稿条目');
      need(typeof entry.editing==='boolean' && Array.isArray(entry.history),'草稿状态无效。');
      text(entry.skipped_reason,'跳过原因',false); text(entry.amendment_reason,'修订理由',false);
      if (entry.draft!==null) validateForm(entry.draft,item,contract,true);
      need(!entry.editing || entry.draft!==null,'正在编辑的条目缺少草稿。');
      need(!entry.history.length || entry.draft===null || entry.editing,'已提交判断的未完成修订需要明确编辑状态。');
      let head = null;
      for (const record of entry.history) {
        validateRecord(record,item,contract); need(!ids.has(record.judgment_id),'草稿含重复判断。'); ids.add(record.judgment_id);
        need(record.supersedes===head,'草稿修订链断裂。'); head=record.judgment_id;
      }
      need(item.response_state==='complete' || (entry.history.length===0 && entry.draft===null),'技术失败不能带语义评审。');
    }
    return draft;
  }
  async function sha256(bytes) {
    const hash = await globalThis.crypto.subtle.digest('SHA-256',bytes);
    return Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,'0')).join('');
  }
  return {need,shape,text,strictJSON,validatePacket,validateForm,validateRecord,validateDraft,emptyForm,formFields,recordFields,fieldOptions,sha256};
});
