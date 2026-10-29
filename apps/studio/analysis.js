// Authored analysis stays separate from immutable observations and computed results.
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const format = 'relata-authored-analysis-1';
const relationNames = {supports:'支持', challenges:'反证', context:'背景 / 待解释'};
const fieldNames = {text:'原样响应', input:'实际 delivered input', governing_history:'Governing history', actions:'结构化动作', rationale:'判断理由'};
const canonical = value => value && typeof value === 'object'
  ? Array.isArray(value) ? '[' + value.map(canonical).join(',') + ']'
    : '{' + Object.keys(value).sort().map(k => JSON.stringify(k) + ':' + canonical(value[k])).join(',') + '}'
  : JSON.stringify(value);

export async function mountAnalysis(root, options) {
  const {command, working, saved, refresh, loadObject, notice, modal, download, exportWorkspace} = options;
  const context = await command('analysis.context', {run_id:options.run.id});
  if (!root.isConnected) return null;
  const authored = context.analyses.filter(a => a.body.format === format);
  let current = options.id === 'new' ? null : authored.find(a => a.id === options.id) || (!options.id ? authored.at(-1) : null);
  if (options.id && options.id !== 'new' && !current) throw new Error('这个分析不属于当前运行。');
  const head = current;
  if (current && options.revision) current = await loadObject(current.id, Number(options.revision));
  if (!root.isConnected) return null;
  const historical = current && current.revision !== head.revision;
  const name = 'analysis-draft:' + context.run.id + ':' + (current?.id || 'new');
  const fresh = () => ({title:current?.title || options.study.title + ' · 分析', text:current?.body.text || '',
    alternatives:current?.body.alternatives || '', limits:(current?.body.limits || []).join('\n'),
    evidence:structuredClone(current?.body.evidence_items || []),
    base_revision:current?.revision || 0, inspector:null});
  let draft = historical ? fresh() : structuredClone(saved(name)?.value || fresh());
  let dirty = false, timer, disposed = false, saving = null;
  let selected = draft.inspector?.id ? {kind:draft.inspector.kind,id:draft.inspector.id} : null;
  const $ = s => root.querySelector(s);
  const $$ = s => [...root.querySelectorAll(s)];
  const observations = new Map(context.observations.map(o => [o.id,o]));
  const reviews = new Map(context.reviews.map(r => [r.id,r]));
  const rounds = new Map(context.rounds.map(r => [r.id,r]));
  const heads = new Map();
  context.reviews.forEach(r => heads.set([r.round_id,r.observation_id,r.reviewer].join('|'),r.id));
  const isOldReview = r => heads.get([r.round_id,r.observation_id,r.reviewer].join('|')) !== r.id;
  const route = (id, revision) => '#study/' + options.study.id + '/analysis/' + id + (revision ? '/' + revision : '');
  const status = text => { if (!disposed) { $('#analysis-save-status').textContent = text; options.status(text); } };

  function schedule() {
    dirty = true;
    status('分析草稿等待保存…');
    clearTimeout(timer);
    timer = setTimeout(() => flush().catch(() => {}), 450);
  }
  function flush() {
    clearTimeout(timer);
    if (historical) return Promise.resolve();
    if (saving) return saving;
    if (!dirty) return Promise.resolve();
    saving = (async () => {
      // Navigation waits for every edit made while an earlier save was in flight.
      while (dirty && !disposed) {
        const value = structuredClone(draft);
        dirty = false;
        try {
          await working(name,value);
          status(dirty ? '分析草稿等待保存…' : '分析草稿已保存');
        } catch (error) {
          dirty = true;
          status('分析草稿未保存');
          notice(error.message + '；请下载草稿保留本次文字。');
          throw error;
        }
      }
    })().finally(() => { saving = null; });
    return saving;
  }

  async function act(button, fn) {
    if (button.disabled) return;
    button.disabled = true;
    try { await fn(); } catch (e) { notice(e.message); }
    finally { if (button.isConnected) button.disabled = false; }
  }
  function literal(kind,id,field) {
    if (kind === 'observation' && context.observation_text?.[id]?.[field] !== undefined) return context.observation_text[id][field];
    const record = kind === 'review' ? reviews.get(id) : observations.get(id);
    const value = kind === 'review' ? record?.judgment.rationale : record?.content[field];
    return typeof value === 'string' ? value : value === undefined ? '' : canonical(value);
  }
  function label(kind,id) {
    const record = kind === 'review' ? reviews.get(id) : observations.get(id);
    if (!record) return '材料缺失 · ' + id;
    return kind === 'review' ? record.reviewer + ' · ' + (rounds.get(record.round_id)?.body.protocol || '') + ' / ' + (rounds.get(record.round_id)?.body.pass || '') + ' · ' + record.judgment.mapping
      : record.position_ids.join(', ') + ' · ' + record.content.shape;
  }
  function selectPanel(panel) {
    $('#analysis-workbench').dataset.panel = panel;
    $$('.analysis-mobile-tabs button').forEach(b => b.setAttribute('aria-pressed',String(b.dataset.panel === panel)));
  }

  const reviewChanged = current && context.review_snapshot ? canonical(current.body.review_snapshot) !== canonical(context.review_snapshot) : head?.review_changed;
  const computedFirst = Boolean(options.computed && !options.id && !current && !draft.text && !draft.evidence.length);
  root.innerHTML = `${options.computed ? '<div class="tabs analysis-modes"><button id="analysis-mode-computed">仪器计算</button><button id="analysis-mode-authored">作者分析</button></div>' : ''}<section id="analysis-authored" ${computedFirst?'hidden':''}><div class="analysis-intro"><div><div class="eyebrow">INTERPRETATION / KEEP THE EVIDENCE CLOSE</div><h2>把解释放在证据旁边。</h2><p class="muted">支持与反证可以并存。冻结的是这一次分析，原始观察与评审继续保留。</p></div><button id="transfer">导出完整研究迁移包</button></div>
    <div class="analysis-toolbar"><label>分析<select id="analysis-select"><option value="new">＋ 写新的分析</option>${authored.map(a => `<option value="${esc(a.id)}" ${a.id === current?.id ? 'selected' : ''}>${esc(a.title)}</option>`).join('')}</select></label>
    ${current ? `<label>固定版本<select id="analysis-revision">${Array.from({length:head.revision},(_,i) => i+1).reverse().map(r => `<option value="${r}" ${r===current.revision?'selected':''}>revision ${r}${r===head.revision?' · 当前':''}</option>`).join('')}</select></label>` : ''}
    <span id="analysis-save-status" role="status">${historical?'历史版本 · 只读':current?'固定版本与草稿分开保存':'尚未冻结 · 私人草稿'}</span></div>
    ${reviewChanged ? '<p class="note" id="analysis-review-warning">这份分析冻结后，评审有新增、修订或处置变化。检查新材料，再决定是否另存分析修订；旧版不会自动更新。</p>' : ''}
    ${historical ? '<p class="note">正在检查历史版本。<button class="quiet" id="analysis-current">回到当前版继续编辑 →</button></p>' : ''}
    ${!historical && current && draft.base_revision !== current.revision ? `<div class="note" id="analysis-conflict">草稿基于 r${draft.base_revision}，当前固定版本为 r${current.revision}。<details><summary>检查当前固定正文</summary><pre>${esc(current.body.text)}</pre></details><button id="analysis-adopt">保留草稿，以当前版本为起点</button></div>` : ''}
    <div class="analysis-mobile-tabs" role="group" aria-label="分析工作区"><button data-panel="write" aria-pressed="true">写分析</button><button data-panel="evidence" aria-pressed="false">查材料</button></div>
    <div id="analysis-workbench" class="analysis-workbench" data-panel="write"><section class="analysis-writing" aria-label="分析正文">
      <label>分析标题<input id="analysis-title" value="${esc(draft.title)}" ${historical?'readonly':''}></label>
      <label>目前怎样解释这些观察<textarea id="analysis-text" rows="10" ${historical?'readonly':''}>${esc(draft.text)}</textarea></label>
      <label>竞争解释与反例<textarea id="analysis-alternatives" rows="4" ${historical?'readonly':''}>${esc(draft.alternatives)}</textarea></label>
      <label>适用范围、尚缺证据（每行一项）<textarea id="analysis-limits" rows="3" ${historical?'readonly':''}>${esc(draft.limits)}</textarea></label>
      <div class="analysis-evidence-heading"><h3>这一次使用的证据</h3><button id="browse-evidence" class="quiet">查找材料 ↗</button></div><div id="analysis-citations"></div>
      <div class="actions section-rule">${historical?'':'<button id="analysis-freeze" class="primary">冻结分析版本</button><button id="analysis-draft-download">下载草稿</button>'}${current?'<button id="analysis-claim">从这一固定版本写主张 →</button>':''}</div>
      <p class="muted analysis-disclosure">分析默认私人；主张另写正文并明确选择披露。保存不提升证据接受状态。</p>
    </section><aside class="analysis-materials" aria-label="原始证据"><div class="eyebrow">OBSERVATIONS & JUDGMENTS</div><h3>回到实际发生的事情</h3>
      <label>在本次运行的材料中查找<input id="evidence-search" type="search" placeholder="位置、原文、reviewer 或判断…"></label>
      <div id="evidence-list" class="evidence-list"></div>${context.dispositions.length ? `<details class="section-rule"><summary>另存的分歧处置 · ${context.dispositions.length}</summary>${context.dispositions.map(d=>`<p><strong>${esc(d.decision)}</strong><br>${esc(d.rationale)}</p>`).join('')}<small>处置意见不替代原判断，也不自动建立共识。</small></details>` : ''}<div id="evidence-inspector"></div>
    </aside></div><details class="section-rule analysis-denominators"><summary>检查完整计划分母</summary>${options.coverage}</details></section>${options.computed ? `<section id="analysis-computed" ${computedFirst?'':'hidden'}><p class="note">固定算法产生的结果保持原样。选择「作者分析」可以引用实际观察、讨论反例和另写解释。</p><div class="actions"><button id="analysis-computed-claim">从计算结果写主张</button><button id="analysis-computed-transfer">导出完整研究迁移包</button></div>${options.coverage}${options.computed}</section>` : ''}`;
  if (options.computed) {
    const showMode = mode => {
      $('#analysis-authored').hidden = mode !== 'authored';
      $('#analysis-computed').hidden = mode !== 'computed';
      $('#analysis-mode-authored').classList.toggle('active',mode==='authored');
      $('#analysis-mode-computed').classList.toggle('active',mode==='computed');
    };
    showMode(computedFirst?'computed':'authored');
    $('#analysis-mode-authored').onclick=()=>showMode('authored');
    $('#analysis-mode-computed').onclick=()=>showMode('computed');
  }

  function drawCitations() {
    $('#analysis-citations').innerHTML = draft.evidence.length ? draft.evidence.map((e,i) => `<article class="analysis-citation" data-relation="${esc(e.relation)}"><div class="stateline"><span>${esc(relationNames[e.relation])}</span><button class="quiet citation-open" data-index="${i}">${esc(label(e.kind,e.id))} ↗</button></div>${e.quote?`<blockquote>${esc(e.quote.text)}</blockquote>`:''}<p>${esc(e.note)}</p>${e.kind==='review' && reviews.has(e.id) && isOldReview(reviews.get(e.id))?'<p class="badge ochre">引用的是历史判断 · 已有同人修订</p>':''}${historical?'':`<button class="quiet citation-remove" data-index="${i}">移出本次草稿</button>`}</article>`).join('') : '<p class="muted">先选一条观察或判断，说明它怎样支持、挑战或限定你的解释。</p>';
    $$('.citation-open').forEach(b => b.onclick = () => inspect(draft.evidence[Number(b.dataset.index)]));
    $$('.citation-remove').forEach(b => b.onclick = () => { draft.evidence.splice(Number(b.dataset.index),1); schedule(); drawCitations(); });
  }
  function drawList() {
    const query = $('#evidence-search').value.toLocaleLowerCase();
    const items = [...context.observations.map(o => ({kind:'observation',record:o,search:JSON.stringify(o)})),
      ...context.reviews.map(r => ({kind:'review',record:r,search:JSON.stringify(r)}))];
    $('#evidence-list').innerHTML = items.filter(i => i.search.toLocaleLowerCase().includes(query)).map(i => `<button class="evidence-open ${selected?.id===i.record.id?'selected':''}" data-kind="${i.kind}" data-id="${esc(i.record.id)}"><span>${i.kind==='observation'?'观察':'判断'} · ${esc(label(i.kind,i.record.id))}</span><small>${esc((i.kind==='review'?i.record.judgment.rationale:i.record.content.text||'〔无正文；展开检查输入与动作〕').slice(0,100))}</small></button>`).join('') || '<p class="muted">没有符合条件的材料。可先在观察页记录原样响应。</p>';
    $$('.evidence-open').forEach(b => b.onclick = () => inspect({kind:b.dataset.kind,id:b.dataset.id}));
  }
  function inspect(target) {
    selected = {kind:target.kind,id:target.id};
    const record = target.kind==='review' ? reviews.get(target.id) : observations.get(target.id);
    if (!record) { notice('所选材料不在本次运行中。'); return; }
    const selectedDraft = draft.inspector?.id === target.id ? draft.inspector : null;
    const existing = draft.evidence.find(e => e.id===target.id && e.kind===target.kind);
    const data = selectedDraft || (existing ? {relation:existing.relation,note:existing.note,quote:existing.quote?.text,quote_field:existing.quote?.field} : {});
    const fields = target.kind==='review' ? ['rationale'] : ['text','input','governing_history','actions'].filter(f => Object.hasOwn(record.content,f));
    const selectedField = fields.includes(data.quote_field) ? data.quote_field : fields[0];
    const associated = target.kind==='observation' ? context.reviews.filter(r => r.observation_id===target.id) : [];
    $('#evidence-inspector').innerHTML = `<section class="evidence-detail"><div class="stateline"><span>${target.kind==='review'?'固定判断':'原样观察'}</span><small>${target.kind==='review'?(isOldReview(record)?'历史判断':'当前判断'):esc(record.content.transport)}</small></div><h3>${esc(label(target.kind,target.id))}</h3>
      <label>检查原文区域<select id="evidence-field">${fields.map(f => `<option value="${f}" ${f===selectedField?'selected':''}>${fieldNames[f]}</option>`).join('')}</select></label><pre id="evidence-literal" tabindex="0"></pre><p id="evidence-empty" class="muted"></p>
      ${target.kind==='review'?'<button id="review-observation" class="quiet">查看所判断的原始观察 →</button>':''}
      ${associated.length?`<details><summary>同一观察的 ${associated.length} 条判断与修订</summary>${associated.map(r=>`<button class="quiet related-review" data-id="${esc(r.id)}">${esc(r.reviewer)} · ${esc(r.judgment.mapping)}${isOldReview(r)?' · 历史':''}</button><p>${esc(r.judgment.rationale)}</p>`).join('')}</details>`:''}
      ${historical?'<p class="muted">历史分析的引用保持原样。</p>':`<div class="section-rule"><label>与分析的关系<select id="evidence-relation">${Object.entries(relationNames).map(([k,v])=>`<option value="${k}" ${data.relation===k?'selected':''}>${v}</option>`).join('')}</select></label><label>怎样支持、挑战或限定这次解释<textarea id="evidence-note" rows="3">${esc(data.note)}</textarea></label><button id="quote-selection" class="quiet">引用上方所选原文 ↓</button><label>精确引文（可留空，不能改写）<textarea id="evidence-quote" rows="3">${esc(data.quote)}</textarea></label><button id="evidence-add">${existing?'更新这条证据':'加入分析证据'}</button></div>`}</section>`;
    const showLiteral = () => { const value=literal(target.kind,target.id,$('#evidence-field').value); $('#evidence-literal').textContent=value; $('#evidence-empty').textContent=value===''?'此区域原文为空。空返回本身可以成为证据，无须编造引文。':''; };
    const saveInspector = () => { if(historical)return; draft.inspector={...selected,quote_field:$('#evidence-field').value,relation:$('#evidence-relation').value,note:$('#evidence-note').value,quote:$('#evidence-quote').value}; schedule(); };
    showLiteral();
    if ($('#review-observation')) $('#review-observation').onclick=()=>inspect({kind:'observation',id:record.observation_id});
    $('#evidence-field').onchange = () => {showLiteral();saveInspector();};
    $$('.related-review').forEach(b=>b.onclick=()=>inspect({kind:'review',id:b.dataset.id}));
    if (!historical) {
      ['#evidence-relation','#evidence-note','#evidence-quote'].forEach(s => $(s).oninput=saveInspector);
      $('#quote-selection').onclick=()=>{const selection=getSelection();if(!selection?.rangeCount||!$('#evidence-literal').contains(selection.anchorNode)||!$('#evidence-literal').contains(selection.focusNode)||!selection.toString()){notice('先在上方原文区域选中文字。');return;}$('#evidence-quote').value=selection.toString();saveInspector();};
      $('#evidence-add').onclick=()=>{
        const quote=$('#evidence-quote').value, field=$('#evidence-field').value;
        if(quote && !literal(target.kind,target.id,field).includes(quote)){notice('引文必须是当前区域的精确原文。');return;}
        const citation={...selected,relation:$('#evidence-relation').value,note:$('#evidence-note').value,...(quote?{quote:{field,text:quote}}:{})};
        const index=draft.evidence.findIndex(e=>e.id===target.id&&e.kind===target.kind);
        if(index<0)draft.evidence.push(citation);else draft.evidence[index]=citation;
        saveInspector();drawCitations();selectPanel('write');notice('证据已加入草稿；冻结分析后形成固定引用。');
      };
    }
    drawList();selectPanel('evidence');
  }
  drawCitations();drawList();
  if(selected) {inspect(selected);selectPanel('write');}
  $('#evidence-search').oninput=drawList;
  $$('.analysis-mobile-tabs button').forEach(b=>b.onclick=()=>selectPanel(b.dataset.panel));
  $('#browse-evidence').onclick=()=>{selectPanel('evidence');$('#evidence-search').focus();};
  $('#analysis-select').onchange=async e=>{try{await flush();location.hash=route(e.target.value);}catch{}};
  if($('#analysis-revision'))$('#analysis-revision').onchange=async e=>{try{await flush();location.hash=route(current.id,e.target.value);}catch{}};
  if($('#analysis-current'))$('#analysis-current').onclick=()=>location.hash=route(current.id);
  if($('#analysis-adopt'))$('#analysis-adopt').onclick=()=>{draft.base_revision=current.revision;schedule();$('#analysis-conflict').remove();};
  const transfer=e=>act(e.currentTarget,async()=>{await flush();await exportWorkspace('research-transfer',[{id:context.run.id,revision:context.run.revision},...context.analyses.map(a=>({id:a.id,revision:a.revision}))]);});
  $('#transfer').onclick=transfer;
  if(options.computed){
    $('#analysis-computed-transfer').onclick=transfer;
    $('#analysis-computed-claim').onclick=options.claimComputed;
  }
  if (!historical) {
    ['title','text','alternatives','limits'].forEach(key=>$('#analysis-'+key).oninput=e=>{draft[key]=e.target.value;schedule();});
    $('#analysis-draft-download').onclick=()=>download({format:'relata-analysis-draft-1',run_id:context.run.id,analysis:current?{id:current.id,revision:draft.base_revision}:null,draft},'analysis-draft.json');
    $('#analysis-freeze').onclick=e=>act(e.currentTarget,async()=>{
      await flush();
      const payload={run_id:context.run.id,title:draft.title,text:draft.text,alternatives:draft.alternatives,limits:draft.limits.split('\n').filter(x=>x.trim()),evidence:draft.evidence};
      if(current)Object.assign(payload,{id:current.id,expected_revision:draft.base_revision});
      const result=await command('analysis.save',payload);
      await refresh();
      draft.base_revision=result.revision;
      await working('analysis-draft:'+context.run.id+':'+result.id,draft);
      if(!current)await working(name,{...fresh(),title:options.study.title+' · 分析',text:'',alternatives:'',limits:'',evidence:[],base_revision:0,inspector:null});
      notice('分析已固定；原始材料与旧版本继续保留。');
      options.reopen(result.id,result.revision);
    });
  }
  if ($('#analysis-claim')) $('#analysis-claim').onclick=()=>modal('从固定分析写一条主张',
    `<p class="note">引用 ${esc(current.title)} · r${current.revision}。仅保存下方明确填写的正文；私人分析和原始材料不会自动复制进公开作品。</p><label>主张标题<input name="title" required></label><label>准备披露的主张正文<textarea name="text" rows="6" required></textarea></label><label>适用范围与限制（每行一项）<textarea name="limits" rows="3"></textarea></label><label class="check-row"><input type="checkbox" name="public"><span>这些文字可用于公开预览</span></label>`,async data=>{
      const claim=await command('analysis.claim',{analysis:{id:current.id,revision:current.revision},title:data.get('title'),text:data.get('text'),limits:data.get('limits').split('\n').filter(x=>x.trim()),visibility:data.has('public')?'public':'private'});
      await refresh();notice('主张已保存，并引用这个固定分析版本。');location.hash='#library';
    });
  return {flush,isDirty:()=>dirty || Boolean(saving),dispose(){disposed=true;clearTimeout(timer);}};
}
