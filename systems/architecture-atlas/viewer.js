(() => {
  'use strict';
  const atlas = JSON.parse(document.getElementById('atlas-data').textContent);
  const byId = id => document.getElementById(id);
  const order = ['aelios','mem0','letta','graphiti','lmc-5','tideline-memory','hindsight','openviking','langmem','a-mem'];
  const models = [...atlas.models].sort((a,b) => order.indexOf(a.id) - order.indexOf(b.id));
  const labels = {overview:'全景与边界',flow:'写入 → 使用',revision:'修订与控制'};
  const statusNames = {observed:'已读源码 · 静态观察',inferred:'有条件的编辑推断',unknown:'未检查 / 外部边界'};
  let selectedModel;
  let selectedView;
  let scale = 1;
  let naturalWidth = 0;
  let naturalHeight = 0;
  function el(tag, text, className) {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  }
  function sourceLinks(ids) {
    const box = el('div',undefined,'evidence-links');
    for (const id of [...new Set(ids)]) {
      const source = selectedModel.sources.find(s => s.id === id);
      const link = el('a',id); link.href = source.url; link.target = '_blank'; link.rel = 'noreferrer'; link.title = source.note; box.append(link);
    }
    return box;
  }
  function projectList() {
    const q = byId('project-search').value.trim().toLowerCase();
    const matches = models.filter(m => [m.name,m.summary,...m.mechanisms].join(' ').toLowerCase().includes(q));
    const list = byId('project-list'); list.replaceChildren();
    for (const model of matches) {
      const button = el('button',undefined,'project-item'); button.type = 'button';
      button.dataset.project = model.id; button.setAttribute('aria-current', String(model === selectedModel));
      button.append(el('span',String(models.indexOf(model)+1).padStart(2,'0'),'number'),el('strong',model.name),el('small',model.mechanisms.slice(0,2).join(' / ')));
      button.addEventListener('click',() => navigate(model.id,selectedView?.id || 'overview'));
      list.append(button);
    }
    byId('search-empty').hidden = matches.length !== 0;
  }
  function navigate(project, view) { location.hash = `${project}/${view}`; }
  function loadRoute() {
    const [project,view] = location.hash.slice(1).split('/');
    selectedModel = models.find(m => m.id === project) || models[0];
    selectedView = selectedModel.views.find(v => v.id === view) || selectedModel.views.find(v => v.id === 'overview');
    projectList(); renderProject(); renderView();
  }
  function renderProject() {
    byId('project-count').textContent = String(models.length).padStart(2,'0');
    byId('project-number').textContent = `STUDY ${String(models.indexOf(selectedModel)+1).padStart(2,'0')} / ${String(models.length).padStart(2,'0')} · SOURCE ARCHITECTURE`;
    byId('project-name').textContent = selectedModel.name;
    document.title = `${selectedModel.name} · Relata Architecture Atlas`;
    byId('project-summary').textContent = selectedModel.summary;
    byId('boundary').textContent = selectedModel.boundary;
    byId('upstream-link').href = selectedModel.repository;
    byId('commit-link').href = `${selectedModel.repository}/commit/${selectedModel.commit}`;
    byId('commit-link').textContent = selectedModel.commit.slice(0,12);
    byId('report-link').href = `../source-studies/${selectedModel.id}.md`;
    for (const field of ['strengths','limits']) byId(field).replaceChildren(...selectedModel[field].map(text => el('li',text)));
    const tabs = byId('view-tabs'); tabs.replaceChildren();
    Object.entries(labels).forEach(([id,label],i) => {
      const button = el('button',undefined,'view-tab'); button.type = 'button'; button.dataset.view = id;
      button.setAttribute('aria-current',String(id === selectedView.id));
      button.append(el('span',String(i+1).padStart(2,'0'),'tab-number'),document.createTextNode(label));
      button.addEventListener('click',() => navigate(selectedModel.id,id)); tabs.append(button);
    });
  }
  function renderView() {
    byId('view-title').textContent = selectedView.title;
    byId('view-instruction').textContent = innerWidth <= 700 ? '左右滑动读图；点击节点查看证据' : '点击节点，沿源码查看它的职责';
    byId('view-question').textContent = selectedView.question;
    byId('reading-guide').textContent = selectedView.reading_guide;
    byId('export-source').href = `diagrams/${selectedModel.id}/${selectedView.id}.mmd`;
    const stage = byId('diagram-stage');
    stage.innerHTML = atlas.assets[`${selectedModel.id}--${selectedView.id}`];
    const svg = stage.querySelector('svg');
    for (const link of svg.querySelectorAll('a')) link.setAttribute('tabindex','-1');
    const viewBox = svg.viewBox.baseVal; naturalWidth = viewBox.width; naturalHeight = viewBox.height;
    svg.setAttribute('role','img'); svg.setAttribute('aria-label',`${selectedModel.name}：${selectedView.title}`);
    const picker = byId('node-picker'); picker.replaceChildren(el('option','选择节点…')); picker.firstChild.value = '';
    for (const node of selectedView.nodes) {
      const number = `N${String(selectedView.nodes.indexOf(node)+1).padStart(2,'0')}`;
      const option = el('option',`${number} · ${node.label.replaceAll('\n',' · ')}`); option.value = node.id; picker.append(option);
      const groups = [...svg.querySelectorAll('g.node, g.guide-node')].filter(g => g.dataset.nodeReference === node.id || g.id.includes(`-flowchart-${node.id}-`));
      for (const group of groups) {
        group.dataset.node = node.id; group.setAttribute('tabindex','0'); group.setAttribute('role','button'); group.setAttribute('aria-label',`查看证据：${node.label.replaceAll('\n','，')}`);
        group.addEventListener('click',event => {event.preventDefault();inspectNode(node.id);});
        group.addEventListener('keydown',event => {if (event.key === 'Enter' || event.key === ' ') {event.preventDefault();inspectNode(node.id);}});
      }
    }
    byId('detail-title').textContent = '从一个节点开始';
    byId('detail-body').replaceChildren(el('p','选择图中的节点，查看职责、状态归属、相邻关系和固定版本的源码。所有箭头的证据也可在下方展开。'));
    byId('state-notes').replaceChildren(...selectedView.state_notes.map(state => {
      const block = el('div',undefined,'state-note');
      for (const [key,label] of [['owner','状态归属'],['writers','谁能写入'],['changes','变化与传播'],['limits','边界']]) {
        const line = el('p');line.append(el('b',`${label} · `),document.createTextNode(state[key]));block.append(line);
      }
      block.append(sourceLinks(state.evidence)); return block;
    }));
    byId('coverage').replaceChildren(el('p','本视图有意保留的覆盖限制：'),el('ul'));
    byId('coverage').querySelector('ul').replaceChildren(...selectedView.omissions.map(t => el('li',t)));
    byId('source-list').replaceChildren(...selectedModel.sources.map(source => {
      const row = el('div',undefined,'source-row'); const link = el('a',`${source.id} · ${source.url.replace('https://github.com/','')}`);
      link.href=source.url;link.target='_blank';link.rel='noreferrer';row.append(link,el('p',source.note));return row;
    }));
    byId('edge-evidence').replaceChildren(...selectedView.edges.map(edge => {
      const row = el('div',undefined,'edge-row');
      const from=selectedView.nodes.find(n=>n.id===edge.from).label.split('\n')[0];
      const to=selectedView.nodes.find(n=>n.id===edge.to).label.split('\n')[0];
      row.append(el('p',`${from} → ${to} · ${edge.label} · ${statusNames[edge.status]}`),sourceLinks(edge.evidence));return row;
    }));
    fit('reading'); byId('diagram-viewport').scrollTo(0,0);
  }
  function inspectNode(id) {
    const node = selectedView.nodes.find(n => n.id === id); if (!node) return;
    byId('node-picker').value=id;
    byId('detail-title').textContent=node.label.replaceAll('\n',' · ');
    const region=selectedView.regions.find(r=>r.id===node.region);
    byId('detail-body').replaceChildren(el('span',statusNames[node.status],'status-label'),el('p',node.note),el('p',`所属区域：${region.label}。${region.responsibility}`),sourceLinks([...node.evidence,...region.evidence]));
    const adjacent = selectedView.edges.filter(e=>e.from===id||e.to===id);
    const list = el('ul');list.style.fontSize='12px';
    for(const edge of adjacent) {
      const otherId=edge.from===id?edge.to:edge.from;
      const other=selectedView.nodes.find(n=>n.id===otherId);
      const item=el('li',`${edge.from===id?'→':'←'} ${other.label.split('\n')[0]}：${edge.label}`);item.append(sourceLinks(edge.evidence));list.append(item);
    }
    byId('detail-body').append(list);
    for(const group of byId('diagram-stage').querySelectorAll('g.node, g.guide-node')) group.classList.toggle('selected',group.dataset.node===id);
    selectedView.edges.forEach((edge,i) => {
      const edgeId=`E${String(i+1).padStart(2,'0')}`;
      for(const group of byId('diagram-stage').querySelectorAll(`[data-edge="${edgeId}"], [data-edge-reference="${edgeId}"]`)) group.classList.toggle('related',edge.from===id||edge.to===id);
    });
    byId('view-instruction').textContent=`已选：${node.label.split('\n')[0]} · 证据见图下方`;
  }
  function zoom(next) {
    scale=Math.max(.12,Math.min(2.5,next));
    const svg=byId('diagram-stage').querySelector('svg'); if(!svg) return;
    svg.style.width=`${naturalWidth*scale}px`;svg.style.height=`${naturalHeight*scale}px`;
    svg.setAttribute('width',naturalWidth*scale);svg.setAttribute('height',naturalHeight*scale);
    byId('zoom-value').textContent=`${Math.round(scale*100)}%`;
  }
  function fit(mode) {
    const viewport=byId('diagram-viewport');
    const padding=innerWidth<=700?36:52;
    const width=(viewport.clientWidth-padding)/naturalWidth;
    zoom(mode==='all'?Math.min(width,(viewport.clientHeight-padding)/naturalHeight):mode==='reading'?Math.min(1,Math.max(.85,width)):Math.min(1,width));
  }
  byId('project-search').addEventListener('input',projectList);
  byId('node-picker').addEventListener('change',event=>inspectNode(event.target.value));
  byId('zoom-in').addEventListener('click',()=>zoom(scale*1.25));
  byId('zoom-out').addEventListener('click',()=>zoom(scale/1.25));
  byId('fit-reading').addEventListener('click',()=>fit('reading'));
  byId('fit-width').addEventListener('click',()=>fit('width'));
  byId('fit-all').addEventListener('click',()=>fit('all'));
  byId('export-svg').addEventListener('click',()=>{
    const svg=atlas.assets[`${selectedModel.id}--${selectedView.id}`];
    const url=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml;charset=utf-8'}));
    const link=el('a');link.href=url;link.download=`${selectedModel.id}-${selectedView.id}.svg`;link.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  addEventListener('hashchange',loadRoute);
  let resizeTimer;addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>fit('reading'),120);});
  loadRoute();
})();
