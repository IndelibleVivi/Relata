(() => {
  'use strict';
  const C = globalThis.RC005Review;
  const definition = JSON.parse(document.getElementById('review-contract').textContent);
  const contract = definition.contract;
  const demo = JSON.parse(document.getElementById('review-demo').textContent);
  const byId = id => document.getElementById(id);
  const clone = value => JSON.parse(JSON.stringify(value));
  const labels = {pending:'待评审',draft:'有草稿',submitted:'已提交',skipped:'暂时跳过',technical:'技术失败'};
  let state, loadSequence=0, storageTimer, noticeTimer;
  let mobilePanel='source', mobilePositions={};
  const decoder = new TextDecoder('utf-8',{fatal:true,ignoreBOM:true});
  const encode = text => new TextEncoder().encode(text);
  function element(tag,text,className) {
    const e=document.createElement(tag);
    if (text!==undefined) e.textContent=text;
    if (className) e.className=className;
    return e;
  }
  function message(text,error=false) {
    clearTimeout(noticeTimer);
    const box=byId('message'); box.hidden=false; box.textContent=text; box.classList.toggle('error',error);
    document.documentElement.style.setProperty('--notice-height',`${box.getBoundingClientRect().height}px`);
    if (!error) noticeTimer=setTimeout(()=>{box.hidden=true;document.documentElement.style.setProperty('--notice-height','0px');},14000);
  }
  function safely(action) {
    return async event => {
      try {await action(event);} catch(error) {message(error.message||String(error),true);}
    };
  }
  function item() {return state.packet.items[state.selected];}
  function entry(id=item().review_id) {
    return state.entries[id] ||= {draft:null,history:[],skipped_reason:'',editing:false,amendment_reason:''};
  }
  function status(record) {
    if (record.response_state==='technical-failure') return 'technical';
    const e=state.entries[record.review_id];
    if (e?.skipped_reason) return 'skipped';
    if (e?.editing || e?.draft) return 'draft';
    if (e?.history.length) return 'submitted';
    return 'pending';
  }
  function draftObject() {
    return {format:contract.draft_format,packet_sha256:state.identity.packet_sha256,
      contract_sha256:definition.sha256,rubric_revision:contract.revision,review_pass:'blind',
      reviewer_id:state.reviewer,practice_only:state.identity.practice_only,
      selected_review_id:item().review_id,entries:clone(state.entries)};
  }
  function requireReviewer() {C.text(state.reviewer,'Reviewer alias',true,120);}
  function storeKey(alias=state.reviewer) {return `relata-rc005-review:${state.identity.practice_only?'practice:':''}${state.identity.packet_sha256}:${encodeURIComponent(alias)}`;}
  function metaKey() {return `relata-rc005-review:last:${state.identity.practice_only?'practice:':''}${state.identity.packet_sha256}`;}
  function updateSaveState(text) {byId('save-state').textContent=text;}
  function saveLocal() {
    if (!state.remember) return;
    try {
      requireReviewer();
      const draft=draftObject(); C.validateDraft(draft,state.packet,state.identity,contract);
      localStorage.setItem(storeKey(),JSON.stringify(draft));
      localStorage.setItem(metaKey(),state.reviewer);
      state.stored=state.revision;
      updateSaveState('已保存至此浏览器 · 保留评审与引用，不复制完整原包');
      byId('forget').hidden=false;
    } catch(error) {
      state.remember=false; byId('remember').checked=false;
      updateSaveState('本机保存失败 · 内存草稿仍在，请下载保存');
      message(`本机保存未成功：${error.message}。可以继续工作并下载草稿。`,true);
    }
  }
  function changed() {
    state.revision++;
    if (state.remember) {
      updateSaveState('正在保存至此浏览器…'); clearTimeout(storageTimer); storageTimer=setTimeout(saveLocal,250);
    } else updateSaveState('内存草稿已更新 · 尚未下载本次修改');
    renderQueue();
    byId('judgment-state').textContent=labels[status(item())];
    const e=state.entries[item().review_id];
    if(e && (!e.history.length||e.editing))byId('discard-edit').hidden=!e.draft&&!e.editing;
  }
  function restore(draft) {
    C.validateDraft(draft,state.packet,state.identity,contract);
    state.entries=clone(draft.entries); state.reviewer=draft.reviewer_id;
    state.selected=state.packet.items.findIndex(i=>i.review_id===draft.selected_review_id);
    byId('reviewer').value=state.reviewer; state.revision++; state.exported=state.revision;
    renderItem(false); renderQueue();
  }
  function restoreLocal(alias) {
    try {
      const raw=localStorage.getItem(storeKey(alias));
      if (!raw) return false;
      const draft=C.strictJSON(raw); C.validateDraft(draft,state.packet,state.identity,contract);
      restore(draft); state.remember=true; byId('remember').checked=true; state.stored=state.revision;
      byId('forget').hidden=false; updateSaveState('已恢复此浏览器的草稿 · 正式导入仍由 CLI 确认');
      message('已恢复同一源包、同一合同和同一 reviewer 的本机草稿。'); return true;
    } catch(error) {state.restoreError=`本机草稿未载入：${error.message}。当前工作没有被替换。`;message(state.restoreError,true);return false;}
  }
  async function loadPacket(raw,practice=false,sequence=++loadSequence) {
    C.need(raw.byteLength<=contract.max_packet_bytes,'文件超过 8 MiB 限制。');
    const packet=C.validatePacket(C.strictJSON(decoder.decode(raw)),practice);
    const hash=await C.sha256(raw);
    if (sequence!==loadSequence) return;
    if (state && Object.values(state.entries).some(e=>e.draft||e.history.length||e.skipped_reason)) {
      if (!confirm('换包会关闭当前内存工作区。请确认已经下载草稿，或已开启并成功完成本机保存。继续换包？')) return;
    }
    clearTimeout(storageTimer);
    state={packet,identity:{packet_sha256:hash,contract_sha256:definition.sha256,practice_only:practice},
      entries:Object.create(null),selected:0,reviewer:'',remember:false,revision:0,exported:0,stored:0};
    byId('landing').hidden=true; byId('workspace').hidden=false;
    byId('reviewer').value=''; byId('remember').checked=false; byId('forget').hidden=true;
    byId('queue-search').value=''; byId('queue-filter').value='all';
    byId('packet-kind').textContent=`${practice?`合成练习 · ${packet.items.length} 个位置`:'RC-005 · 144 个位置'} · 包 ${hash.slice(0,8)}`;
    byId('packet-kind').title=`原包字节 SHA-256: ${hash}`;
    updateSaveState('只在内存 · 请及时下载草稿');
    let restored=false;
    try {const alias=localStorage.getItem(metaKey()); if(alias) restored=restoreLocal(alias);} catch {}
    if (!restored) {renderItem(false);renderQueue();message(state.restoreError||(practice?'已打开作者编写的合成练习包。所有导出都会保留 practice-only 标记。':'匿名包已读入。这里只检查格式；原运行与导出来源由 operator 的 CLI 验证。'),Boolean(state.restoreError));}
    window.scrollTo({top:0,behavior:'instant'});
  }
  function renderQueue() {
    if (!state) return;
    const query=byId('queue-search').value.trim().toLowerCase(); const filter=byId('queue-filter').value;
    const queueKey=[state.selected,query,filter,...state.packet.items.map(record=>`${status(record)}:${Boolean(state.entries[record.review_id]?.history.length)}`)].join('|');
    // A 144-position queue need not replace its controls on every text edit.
    // A nonempty search still re-evaluates the edited notes and quotations.
    if(queueKey===state.queueKey&&!query)return;
    state.queueKey=queueKey;
    const counts={pending:0,draft:0,submitted:0,skipped:0,technical:0};
    for (const record of state.packet.items) counts[status(record)]++;
    const currentJudgments=Object.values(state.entries).filter(e=>e.history.length).length;
    const reviewable=state.packet.items.length-counts.technical;
    byId('progress').textContent=`${currentJudgments} / ${reviewable}`;
    byId('progress-detail').textContent=`${state.packet.items.length} 位置 · ${counts.technical} 技术失败 · ${counts.draft} 草稿 · ${counts.skipped} 暂跳过。分子是已有提交的回答，不是得分。`;
    const list=byId('queue'); list.replaceChildren(); let matches=0;
    state.packet.items.forEach((record,index)=>{
      const kind=status(record),e=state.entries[record.review_id];
      const haystack=[record.review_id,record.response||'',e?JSON.stringify(e):''].join(' ').toLowerCase();
      if ((filter!=='all' && filter!==kind) || (query && !haystack.includes(query))) return;
      matches++;
      const button=element('button',undefined,'queue-item'); button.type='button'; button.dataset.reviewId=record.review_id;
      button.setAttribute('aria-current',String(index===state.selected));
      button.append(element('span',String(index+1).padStart(3,'0'),'queue-number'));
      const name=element('span'); name.append(element('span',record.review_id.slice(-8),'queue-alias'),element('span',labels[kind],'queue-state')); button.append(name);
      button.addEventListener('click',()=>navigate(index)); list.append(button);
    });
    byId('queue-empty').hidden=matches!==0;
    byId('download-reviews').textContent=`导出已提交判断${currentJudgments?` (${currentJudgments})`:''}`;
    byId('mobile-item').textContent=`${state.selected+1} / ${state.packet.items.length} · ${item().review_id.slice(-8)} · ${labels[status(item())]}`;
  }
  function setMobilePanel(name,restorePosition=false) {
    if(restorePosition) mobilePositions[mobilePanel]=window.scrollY;
    document.querySelector('.reading-area').dataset.mobilePanel=name;
    mobilePanel=name;
    byId('show-source').setAttribute('aria-pressed',String(name==='source'));
    byId('show-form').setAttribute('aria-pressed',String(name==='form'));
    if(restorePosition&&innerWidth<=700) {
      const tabs=document.querySelector('.mobile-tabs');
      const start=tabs.getBoundingClientRect().top+window.scrollY-byId('message').getBoundingClientRect().height;
      window.scrollTo({top:mobilePositions[name]??start,behavior:'instant'});
    }
  }
  function navigate(index) {
    if(index<0||index>=state.packet.items.length) return;
    state.selected=index; renderItem(); renderQueue();
    byId('item-title').tabIndex=-1;byId('item-title').focus({preventScroll:true});
    if(state.remember) saveLocal();
  }
  function renderItem(scroll=true) {
    const record=item();
    byId('skip-panel').hidden=true;
    byId('position-label').textContent=`${state.identity.practice_only?'PRACTICE':'BLIND PASS'} / ${String(state.selected+1).padStart(3,'0')} OF ${state.packet.items.length}`;
    byId('item-title').textContent=`回答 · ${record.review_id.slice(-8)}`;
    byId('mobile-item').textContent=`${state.selected+1} / ${state.packet.items.length} · ${record.review_id.slice(-8)} · ${labels[status(record)]}`;
    byId('case-boundary').textContent=record.context;
    byId('packet-instructions').textContent=record.instructions;
    byId('history').replaceChildren(...record.governing_history.map((event,index)=>{
      const article=element('article',undefined,'history-event'); article.id=`history-H${index+1}`;
      const head=element('div',undefined,'event-head');head.append(element('span',`H${index+1}`,'event-id'),element('span',`Session ${event.session} · ${event.role} · ${event.surface}`));
      article.append(head,element('p',event.text));return article;
    }));
    byId('current').textContent=record.current.text;
    byId('response-state').textContent=record.response_state==='technical-failure'?'技术失败 · 无回答':record.response===''?'完成 · 实际空字符串':!record.response.trim()?'完成 · 仅空白字符':'完成 · 文本';
    byId('response').replaceChildren(record.response===null?element('p','没有收到回答；不作语义判断。','empty-response'):record.response===''?element('p','实际回答为空字符串。此位置仍可评审；请描述未完成之处或保留未决。','empty-response'):document.createTextNode(record.response));
    if(record.response && !record.response.trim())byId('response').replaceChildren(element('p','原回答只含空白字符；下方以 JSON 转义展示，复制按钮仍返回原文。','empty-response'),element('code',JSON.stringify(record.response)));
    byId('copy-response').disabled=record.response===null;
    byId('rubric-label').textContent=`${contract.revision} · development worksheet。证据支持相对完整历史判断；实际送达材料的消费诊断另行记录。`;
    byId('previous').disabled=state.selected===0; byId('next').disabled=state.selected===state.packet.items.length-1;
    byId('mobile-next').disabled=state.selected===state.packet.items.length-1;
    mobilePositions={};setMobilePanel('source'); renderForm();
    if(scroll) document.querySelector('.position-bar').scrollIntoView({block:'start',behavior:'instant'});
  }
  function fieldDefinition(id,claim=false) {return (claim?contract.claim_fields:contract.dimensions).find(f=>f.id===id);}
  function optionsFor(id,claim=false) {
    if(claim&&id==='kind') return contract.claim_kind_options;
    if(claim&&id==='support') return contract.claim_support_options;
    return fieldDefinition(id,claim)?.options||[];
  }
  function formField(id,label,value,help,options=null) {
    const wrapper=element('label',undefined,'field');wrapper.append(element('span',label,'field-label'));
    let control;
    if(options) {
      control=element('select');const blank=element('option','请选择，或明确保留未决');blank.value='';control.append(blank);
      for(const option of options){const e=element('option',option.label);e.value=option.value;control.append(e);}
    } else control=element('textarea');
    control.dataset.field=id;control.name=id;control.value=value||'';wrapper.append(control);
    if(help) wrapper.append(element('span',help,'field-help'));
    return wrapper;
  }
  function renderForm() {
    const record=item(),e=entry();const technical=record.response_state==='technical-failure';
    byId('technical-note').hidden=!technical;byId('judgment-form').hidden=technical;byId('judgment-actions').hidden=technical;
    byId('judgment-state').textContent=labels[status(record)];
    const locked=e.history.length>0&&!e.editing;
    byId('submit-review').hidden=locked;byId('skip-review').hidden=locked;
    byId('reopen-review').hidden=!locked;byId('discard-edit').hidden=locked||(!e.draft&&!e.editing);
    const form=byId('judgment-form');form.replaceChildren();
    if(!technical) {
      const value=clone(e.draft||e.history.at(-1)||C.emptyForm());
      const claims=element('fieldset',undefined,'form-section');claims.append(element('legend','01 / 回答表达了什么'));
      claims.append(element('p',fieldDefinition('claims').help,'field-help'));
      value.claims.forEach((claim,index)=>{
        const block=element('div',undefined,'claim');block.dataset.claim=index;
        const heading=element('div',undefined,'claim-heading');heading.append(element('strong',`字句 ${index+1}`));
        const remove=element('button','移除');remove.type='button';remove.disabled=locked;
        remove.addEventListener('click',()=>{captureForm();const current=entry();if(current.draft.claims[index].quote&&!confirm('移除这项尚未提交的字句？已提交历史会保留。'))return;current.draft.claims.splice(index,1);changed();renderForm();});heading.append(remove);block.append(heading);
        for(const id of ['quote','kind','attribution','support']) {
          const definition=fieldDefinition(id,true);
          block.append(formField(id,definition.label,claim[id],definition.help,['kind','support'].includes(id)?optionsFor(id,true):null));
        }
        block.append(element('p','引用完整历史的位置（H1…）或当前问题。','field-help'));
        const refs=element('div',undefined,'evidence-checks');
        for(const ref of [...record.governing_history.map((_,i)=>`H${i+1}`),'current']) {
          const label=element('label');const check=element('input');check.type='checkbox';check.value=ref;check.dataset.ref=ref;check.checked=claim.evidence_refs.includes(ref);label.append(check,document.createTextNode(ref));refs.append(label);
        }
        block.append(refs,formField('rationale','这项字句的理由',claim.rationale,'解释依据、时态、归属或未决之处。'));claims.append(block);
      });
      const add=element('button','＋ 添加一项字句');add.type='button';add.disabled=locked;
      add.addEventListener('click',()=>{captureForm();entry().draft.claims.push({quote:'',kind:'',attribution:'',support:'',evidence_refs:[],rationale:''});changed();renderForm();byId('judgment-form').querySelector('.claim:last-of-type textarea')?.focus();});claims.append(add);form.append(claims);
      const actions=element('fieldset',undefined,'form-section');actions.append(element('legend','02 / 行动、澄清与使用'));
      for(const id of ['current_action','clarification','selective_use','confidence_limits']) {const d=fieldDefinition(id);actions.append(formField(id,d.label,value[id],d.help,d.options));}form.append(actions);
      const guess=element('fieldset',undefined,'form-section');guess.append(element('legend','03 / 盲化诊断与理由'));
      for(const id of ['guessability','guess_confidence']) {const d=fieldDefinition(id);guess.append(formField(id,d.label,value[id],d.help,d.options));}
      guess.append(formField('guess_cue','条件猜测的文字线索',value.guess_cue,'无法判断时可留空；其他猜测需要指明回答中的线索。'),formField('rationale','整体理由与未决',value.rationale,'综合说明行动、澄清和限制；保留不同的合法解释。'),formField('notes','补充笔记（可选）',value.notes,'使用不含个人身份或其他私人材料的说明。'));
      if(e.editing&&e.history.length) guess.append(formField('amendment_reason','为什么修订之前的判断？',e.amendment_reason,'新判断保留旧记录，并明确替代当前版本。'));
      form.append(guess);
      for(const control of form.querySelectorAll('textarea,select,input')) control.disabled=locked;
    }
    renderHistory();
  }
  function captureForm() {
    if(!state||item().response_state!=='complete') return;
    const e=entry();if(e.history.length&&!e.editing)return;
    const form=byId('judgment-form'),value=C.emptyForm();
    value.claims=[...form.querySelectorAll('.claim')].map(block=>{
      const claim={};for(const id of ['quote','kind','attribution','support','rationale'])claim[id]=block.querySelector(`[data-field="${id}"]`).value;
      claim.evidence_refs=[...block.querySelectorAll('input[data-ref]:checked')].map(check=>check.value);return claim;
    });
    for(const id of C.formFields.filter(id=>id!=='claims')) value[id]=form.querySelector(`:scope > fieldset [data-field="${id}"]`)?.value||'';
    // A claim also has rationale; the overall rationale lives in section 03.
    value.rationale=form.querySelector(':scope > fieldset:last-child [data-field="rationale"]').value;
    e.draft=value;e.skipped_reason='';e.amendment_reason=form.querySelector('[data-field="amendment_reason"]')?.value||'';
  }
  function renderHistory() {
    const target=byId('review-history');target.replaceChildren();
    for(const record of entry().history.slice().reverse()) {
      const details=element('details');details.append(element('summary',`${record.supersedes?'修订':'首份'}判断 · ${record.created_at.replace('T',' ').replace('Z',' UTC')}`));
      const content=element('div');
      if(record.amendment_reason)content.append(element('p',`修订理由：${record.amendment_reason}`));
      content.append(element('p',record.rationale));
      for(const id of ['current_action','clarification','selective_use','confidence_limits','guessability','guess_confidence']) {
        content.append(element('p',`${fieldDefinition(id).label}：${optionsFor(id).find(o=>o.value===record[id])?.label||record[id]}`));
      }
      for(const claim of record.claims)content.append(element('p',`「${claim.quote}」 · ${claim.support} · ${claim.evidence_refs.join(', ')||'未引位置'} · ${claim.rationale}`));
      details.append(content);target.append(details);
    }
  }
  function download(value,name) {
    const bytes=JSON.stringify(value,null,2)+'\n';
    const url=URL.createObjectURL(new Blob([bytes],{type:'application/json;charset=utf-8'}));
    const link=element('a');link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function baseBatch() {
    return {format:contract.batch_format,packet_sha256:state.identity.packet_sha256,contract_sha256:definition.sha256,
      rubric_revision:contract.revision,review_pass:'blind',reviewer_id:state.reviewer,practice_only:state.identity.practice_only};
  }
  byId('packet-file').addEventListener('change',safely(async event=>{
    const file=event.target.files[0];event.target.value='';if(!file)return;
    const sequence=++loadSequence;C.need(file.size<=contract.max_packet_bytes,'文件超过 8 MiB 限制。');
    const bytes=await file.arrayBuffer();if(sequence!==loadSequence)return;
    const decoded=C.strictJSON(decoder.decode(bytes));
    if(decoded.practice_only===true) {
      C.shape(decoded,['practice_only','packet'],'练习包');
      await loadPacket(encode(JSON.stringify(decoded.packet,null,2)+'\n'),true,sequence);
    } else await loadPacket(bytes,false,sequence);
  }));
  byId('practice').addEventListener('click',safely(()=>loadPacket(encode(JSON.stringify(demo.packet,null,2)+'\n'),true)));
  byId('judgment-form').addEventListener('input',()=>{captureForm();changed();});
  byId('judgment-form').addEventListener('change',()=>{captureForm();changed();});
  byId('submit-review').addEventListener('click',safely(()=>{
    requireReviewer();captureForm();const e=entry(),record=item();C.validateForm(e.draft,record,contract);
    const supersedes=e.history.at(-1)?.judgment_id||null;
    if(supersedes)C.text(e.amendment_reason,'修订理由');
    const bytes=crypto.getRandomValues(new Uint8Array(16));
    const judgment={judgment_id:Array.from(bytes,b=>b.toString(16).padStart(2,'0')).join(''),review_id:record.review_id,
      supersedes,amendment_reason:supersedes?e.amendment_reason:'',created_at:new Date().toISOString(),...clone(e.draft)};
    C.validateRecord(judgment,record,contract);e.history.push(judgment);e.draft=null;e.editing=false;e.amendment_reason='';e.skipped_reason='';
    changed();renderForm();message('本工作区已保留这条判断。导出后由 operator 的 CLI 验证并导入研究记录。');
  }));
  byId('reopen-review').addEventListener('click',()=>{const e=entry();e.editing=true;e.draft=Object.fromEntries(C.formFields.map(key=>[key,clone(e.history.at(-1)[key])]));changed();renderForm();});
  byId('discard-edit').addEventListener('click',()=>{if(!confirm('撤回这次尚未提交的编辑？此前已提交判断会保留。'))return;const e=entry();e.draft=null;e.editing=false;e.amendment_reason='';changed();renderForm();});
  byId('skip-review').addEventListener('click',()=>{
    byId('skip-panel').hidden=false;byId('skip-reason').value=entry().skipped_reason;byId('skip-reason').focus();
  });
  byId('confirm-skip').addEventListener('click',safely(()=>{
    const reason=byId('skip-reason').value;C.text(reason,'留待回访的原因');
    const e=entry();e.skipped_reason=reason;changed();renderForm();message('已标为暂时跳过，已有草稿保留；它仍属于未完成评审。');
    byId('skip-panel').hidden=true;byId('skip-review').focus();
  }));
  const cancelSkip=()=>{byId('skip-panel').hidden=true;byId('skip-review').focus();};
  byId('cancel-skip').addEventListener('click',cancelSkip);
  byId('skip-reason').addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();cancelSkip();}});
  byId('download-draft').addEventListener('click',safely(()=>{requireReviewer();const draft=draftObject();C.validateDraft(draft,state.packet,state.identity,contract);download(draft,'rc005-review-draft.json');state.exported=state.revision;updateSaveState('已生成草稿下载 · 请确认浏览器保存了文件');}));
  byId('draft-file').addEventListener('change',safely(async event=>{
    const file=event.target.files[0];event.target.value='';if(!file)return;C.need(file.size<=contract.max_packet_bytes,'草稿超过 8 MiB。');
    const draft=C.strictJSON(decoder.decode(await file.arrayBuffer()));C.validateDraft(draft,state.packet,state.identity,contract);
    if(state.revision>state.exported&&!confirm('恢复文件会替换当前内存草稿。确认已经保留当前工作？'))return;
    restore(draft);if(state.remember)saveLocal();message('草稿已恢复；已提交版本、未完成编辑与当前阅读位置均已保留。');
  }));
  byId('download-reviews').addEventListener('click',safely(()=>{
    requireReviewer();const records=state.packet.items.flatMap(record=>entry(record.review_id).history);C.need(records.length,'尚无已提交判断；可以先下载未完成草稿。');
    records.forEach(record=>C.validateRecord(record,state.packet.items.find(i=>i.review_id===record.review_id),contract));
    download({...baseBatch(),records},'rc005-review-judgments.json');
    message(`已生成 ${records.length} 份判断（含修订历史）的下载。草稿与暂跳过项未当作判断；研究导入状态仍以 CLI 为准。`);
  }));
  byId('reviewer').addEventListener('change',safely(event=>{
    const alias=event.target.value.trim();try{C.text(alias,'Reviewer alias',true,120);}catch(error){event.target.value=state.reviewer;throw error;}
    if(state.reviewer&&alias!==state.reviewer&&Object.values(state.entries).some(e=>e.draft||e.history.length||e.skipped_reason)) {
      if(!confirm('更换 reviewer 会开始独立评审。请确认已保存原 reviewer 的草稿。继续？')){event.target.value=state.reviewer;return;}
      if(state.remember)saveLocal();state.entries=Object.create(null);state.remember=false;byId('remember').checked=false;
    }
    state.reviewer=alias;if(!restoreLocal(alias)){changed();renderForm();}
  }));
  byId('remember').addEventListener('change',safely(event=>{
    if(event.target.checked){try{requireReviewer();}catch(error){event.target.checked=false;throw error;}state.remember=true;saveLocal();}
    else{state.remember=false;clearTimeout(storageTimer);updateSaveState('已停止本机自动保存 · 既有副本可用右侧按钮移除');}
  }));
  byId('forget').addEventListener('click',safely(()=>{localStorage.removeItem(storeKey());if(localStorage.getItem(metaKey())===state.reviewer)localStorage.removeItem(metaKey());state.remember=false;byId('remember').checked=false;byId('forget').hidden=true;clearTimeout(storageTimer);updateSaveState('本机副本已移除 · 当前内存草稿仍在');}));
  byId('queue-search').addEventListener('input',renderQueue);byId('queue-filter').addEventListener('change',renderQueue);
  byId('previous').addEventListener('click',()=>navigate(state.selected-1));byId('next').addEventListener('click',()=>navigate(state.selected+1));
  byId('next-pending').addEventListener('click',()=>{
    const length=state.packet.items.length;for(let offset=1;offset<=length;offset++){const index=(state.selected+offset)%length;if(['pending','draft','skipped'].includes(status(state.packet.items[index]))){navigate(index);return;}}message('本批所有可评审回答都已有提交判断。');
  });
  byId('show-source').addEventListener('click',()=>setMobilePanel('source',true));byId('show-form').addEventListener('click',()=>setMobilePanel('form',true));
  byId('mobile-next').addEventListener('click',()=>navigate(state.selected+1));
  byId('copy-response').addEventListener('click',safely(async()=>{try{await navigator.clipboard.writeText(item().response);message('已复制原样回答。');}catch{message('浏览器未允许复制；可在原样回答中直接选择文字。',true);}}));
  byId('change-packet').addEventListener('click',()=>{byId('packet-file').click();});
  new ResizeObserver(()=>document.documentElement.style.setProperty('--notice-height',`${byId('message').getBoundingClientRect().height}px`)).observe(byId('message'));
  addEventListener('beforeunload',event=>{if(state&&state.revision>state.exported&&(!state.remember||state.stored<state.revision)){event.preventDefault();event.returnValue='';}});
  addEventListener('keydown',event=>{if(!state||event.isComposing||!event.altKey)return;if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();navigate(state.selected+(event.key==='ArrowLeft'?-1:1));}});
})();
