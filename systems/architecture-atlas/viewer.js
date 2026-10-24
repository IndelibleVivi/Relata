(() => {
  'use strict';

  const atlas = JSON.parse(document.getElementById('atlas-data').textContent);
  const byId = id => document.getElementById(id);
  const order = ['aelios','mem0','letta','graphiti','lmc-5','tideline-memory','hindsight','openviking','langmem','a-mem'];
  const models = [...atlas.models].sort((a,b) => order.indexOf(a.id) - order.indexOf(b.id));
  const collection = atlas.collection;
  const exhibits = Array.isArray(collection?.exhibits) ? collection.exhibits : [];
  const labels = {overview:'全景与边界',flow:'写入 → 使用',revision:'修订与控制'};
  const statusNames = {observed:'已读源码 · 静态观察',inferred:'有条件的编辑推断',unknown:'未检查 / 外部边界'};
  const functionNames = {benchmark:'Benchmark 研究',collection:'System collection',incubator:'Incubator'};
  let mode = 'questions';
  let selectedModel;
  let selectedView;
  let selectedExhibit;
  let selectedCondition;
  let selectedNode = '';
  let returnContext;
  let restoreConditionFocus = false;
  let renderedProjectRoute = '';
  let pendingNodeFocus = '';
  let readingRoute = '';
  let scale = 1;
  let naturalWidth = 0;
  let naturalHeight = 0;

  function el(tag, text, className) {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  }

  function paragraph(text, className) {
    return el('p', text, className);
  }

  function modelFor(project) {
    return models.find(model => model.id === project);
  }

  function viewFor(model, id) {
    return model?.views.find(view => view.id === id);
  }

  function exhibitFor(id) {
    return exhibits.find(exhibit => exhibit.id === id);
  }

  function conditionFor(exhibit, id) {
    return exhibit?.conditions.find(condition => condition.id === id) || exhibit?.conditions[0];
  }

  function sourceFor(model, id) {
    return model?.sources.find(source => source.id === id);
  }

  function decodeSegment(value = '') {
    try {
      return decodeURIComponent(value);
    } catch {
      return '';
    }
  }

  function exhibitSearchText(exhibit) {
    return [
      exhibit.id,
      exhibit.title,
      exhibit.question,
      exhibit.summary,
      exhibit.scenario,
      ...exhibit.conditions.flatMap(condition => [condition.title, condition.task, condition.focus]),
      ...exhibit.comparisons.flatMap(comparison => {
        const model = modelFor(comparison.project);
        return [
          comparison.project,
          comparison.view,
          model?.id || '',
          model?.name || '',
          model?.summary || '',
          ...(model?.mechanisms || []),
          comparison.observation,
          comparison.benefit,
          comparison.limit,
          comparison.check,
          ...Object.values(comparison.reading),
          ...comparison.nodes,
          ...comparison.sources
        ];
      }),
      ...exhibit.controls.flatMap(control => [control.title, control.detail]),
      ...Object.values(exhibit.takeaways),
      ...exhibit.links.map(link => link.label),
      ...exhibit.revisions.map(revision => revision.summary)
    ].join(' ').toLowerCase();
  }

  function matchingExhibits(query) {
    const q = query.trim().toLowerCase();
    return q ? exhibits.filter(exhibit => exhibitSearchText(exhibit).includes(q)) : exhibits;
  }

  function sourceLinks(ids, project = selectedModel?.id) {
    const model = modelFor(project);
    const box = el('div', undefined, 'evidence-links');
    for (const id of [...new Set(ids)]) {
      const source = sourceFor(model, id);
      if (!source) continue;
      const link = el('a', id);
      link.href = source.url;
      link.target = '_blank';
      link.rel = 'noreferrer';
      link.title = source.note;
      box.append(link);
    }
    return box;
  }

  function showView(name) {
    for (const id of ['questions-view','exhibit-view','project-view']) byId(id).hidden = id !== `${name}-view`;
    mode = name;
    for (const [id,active] of [['questions-mode-link',name !== 'project'],['systems-mode-link',name === 'project']]) {
      byId(id).classList.toggle('active', active);
      if (active) byId(id).setAttribute('aria-current','page');
      else byId(id).removeAttribute('aria-current');
    }
    byId('search-label').textContent = name !== 'project' ? '寻找研究问题或系统' : '寻找系统或机制';
    byId('project-search').placeholder = name !== 'project' ? '搜索问题、系统或机制' : '搜索系统名或机制';
    byId('github-reader-link').hidden = !collection;
  }

  function encodeRoute(parts, params = {}) {
    const query = new URLSearchParams();
    for (const [key,value] of Object.entries(params)) if (value) query.set(key,value);
    return `#${parts}${query.size ? `?${query}` : ''}`;
  }

  function navigateProject(project, view, context = returnContext, node = '') {
    location.hash = encodeRoute(`${project}/${view}`, {
      node,
      exhibit: context?.exhibit,
      condition: context?.condition
    });
  }

  function navigateExhibit(exhibit, condition = exhibit?.conditions[0]?.id) {
    if (!exhibit) return;
    returnContext = undefined;
    location.hash = `#exhibit/${encodeURIComponent(exhibit.id)}/${encodeURIComponent(condition)}`;
  }

  function projectList(query = byId('project-search').value) {
    const list = byId('project-list');
    const empty = byId('search-empty');
    list.replaceChildren();
    if (mode !== 'project') {
      if (!collection) {
        empty.textContent = '研究问题目录由 build 生成后在这里出现；当前仍可从“系统图集”阅读十个固定源码版本。';
        empty.hidden = false;
        byId('project-count').textContent = '';
        byId('questions-search-context').textContent = '';
        return;
      }
      const q = query.trim().toLowerCase();
      const matches = matchingExhibits(query);
      for (const exhibit of matches) {
        const button = el('button', undefined, 'project-item exhibit-nav-item');
        button.type = 'button';
        button.dataset.exhibit = exhibit.id;
        button.setAttribute('aria-current', String(exhibit.id === selectedExhibit?.id));
        const systems = [...new Set(exhibit.comparisons.map(comparison => modelFor(comparison.project)?.name || comparison.project))];
        button.append(
          el('span', String(exhibits.indexOf(exhibit)+1).padStart(2,'0'), 'number'),
          el('strong', exhibit.title),
          el('small', systems.join(' · ')),
          el('span', `${systems.length} systems · ${exhibit.conditions.length} conditions`, 'exhibit-meta')
        );
        button.addEventListener('click', () => navigateExhibit(exhibit));
        list.append(button);
      }
      byId('project-count').textContent = String(exhibits.length).padStart(2,'0');
      byId('questions-search-context').textContent = q
        ? `当前搜索 “${byId('project-search').value.trim()}”：${matches.length} / ${exhibits.length} 个研究问题。`
        : `${exhibits.length} 个研究问题，每项比较 3–4 个固定源码机制。`;
      empty.textContent = '没有匹配的研究问题。搜索会检查问题、条件、源码观察、阅读结论、控制与三职能 takeaways；清除搜索可查看全部五项。';
      empty.hidden = matches.length !== 0;
      return;
    }
    const q = query.trim().toLowerCase();
    const matches = models.filter(model => [model.id, model.name, model.summary, ...model.mechanisms].join(' ').toLowerCase().includes(q));
    for (const model of matches) {
      const button = el('button', undefined, 'project-item');
      button.type = 'button';
      button.dataset.project = model.id;
      button.setAttribute('aria-current', String(model === selectedModel));
      button.append(
        el('span', String(models.indexOf(model)+1).padStart(2,'0'), 'number'),
        el('strong', model.name),
        el('small', model.mechanisms.slice(0,2).join(' / '))
      );
      button.addEventListener('click', () => navigateProject(model.id, selectedView?.id || 'overview'));
      list.append(button);
    }
    empty.textContent = '没有匹配系统。试试系统名、节点或机制中的词。';
    empty.hidden = matches.length !== 0;
    byId('project-count').textContent = String(selectedModel ? models.indexOf(selectedModel)+1 : 0).padStart(2,'0');
  }

  function renderQuestions() {
    showView('questions');
    selectedExhibit = undefined;
    selectedNode = '';
    returnContext = undefined;
    byId('project-search').value = '';
    byId('questions-empty').hidden = true;
    if (collection) {
      byId('questions-title').textContent = collection.title;
      byId('questions-boundary').textContent = collection.boundary;
      byId('questions-updated').textContent = `Updated ${collection.updated}`;
      byId('github-reader-link').href = 'exhibits.md';
      byId('github-reader-link').hidden = false;
    } else {
      byId('questions-title').textContent = '研究问题目录尚未生成';
      byId('questions-boundary').textContent = '当前构建只包含系统图集。研究问题与条件比较需由 build 嵌入 atlas.collection 后显示。';
      byId('questions-updated').textContent = '';
      byId('github-reader-link').hidden = true;
    }
    renderQuestionCatalogue('');
    document.title = collection ? `${collection.title} · Relata` : '研究问题目录 · Relata';
    byId('page-kicker').textContent = 'RESEARCH QUESTIONS / 从问题进入实现';
    projectList('');
    if (!collection) byId('questions-empty').hidden = false;
  }

  function renderQuestionCatalogue(query) {
    const matches = matchingExhibits(query);
    const target = byId('exhibit-list');
    target.replaceChildren();
    for (const exhibit of matches) {
      const index = exhibits.indexOf(exhibit);
      const article = el('article', undefined, 'exhibit-entry');
      article.append(
        el('div', `0${index+1} / ${exhibit.id.toUpperCase()}`, 'eyebrow'),
        el('h2', exhibit.title),
        el('p', exhibit.question, 'exhibit-entry-question'),
        el('p', exhibit.summary, 'exhibit-entry-summary')
      );
      const systems = [...new Set(exhibit.comparisons.map(comparison => comparison.project))];
      const systemRow = el('div', undefined, 'system-chip-row');
      for (const project of systems) {
        const model = modelFor(project);
        const chip = el('span', model?.name || project, 'system-chip');
        chip.title = model ? model.name : project;
        systemRow.append(chip);
      }
      systemRow.append(el('span', `${exhibit.conditions.length} 个阅读条件`, 'condition-chip'));
      article.append(systemRow);
      const link = el('a', '进入这个研究问题 →', 'entry-link');
      link.href = `#exhibit/${encodeURIComponent(exhibit.id)}/${encodeURIComponent(exhibit.conditions[0].id)}`;
      link.addEventListener('click', event => { event.preventDefault(); navigateExhibit(exhibit); });
      article.append(link);
      target.append(article);
    }
    const q = query.trim();
    byId('questions-search-context').textContent = collection
      ? q ? `当前搜索 “${q}”：${matches.length} / ${exhibits.length} 个研究问题。`
          : `${exhibits.length} 个研究问题，每项比较 3–4 个固定源码机制。`
      : '';
    byId('questions-empty').hidden = !collection || matches.length !== 0;
  }

  function searchQuestions() {
    const query = byId('project-search').value;
    projectList(query);
    renderQuestionCatalogue(query);
  }

  function renderExhibit(exhibit, condition) {
    showView('exhibit');
    byId('exhibit-view').hidden = false;
    selectedExhibit = exhibit;
    selectedNode = '';
    selectedCondition = condition.id;
    returnContext = undefined;
    const index = exhibits.indexOf(exhibit);
    byId('exhibit-number').textContent = `EXHIBIT ${String(index+1).padStart(2,'0')} / ${String(exhibits.length).padStart(2,'0')} · STATIC SYNTHESIS`;
    byId('exhibit-title').textContent = exhibit.title;
    byId('exhibit-question').textContent = exhibit.question;
    byId('exhibit-summary').textContent = exhibit.summary;
    byId('exhibit-scenario').textContent = exhibit.scenario;
    const crumbs = byId('exhibit-breadcrumbs');
    const home = el('a','研究问题'); home.href = '#questions';
    crumbs.replaceChildren(home, el('span','/'), el('span',exhibit.title));
    byId('exhibit-github-link').href = `exhibits.md#${encodeURIComponent(exhibit.id)}`;
    const switcher = byId('condition-switcher');
    while (switcher.children.length > exhibit.conditions.length) switcher.lastChild.remove();
    const focusIndex = restoreConditionFocus
      ? exhibit.conditions.findIndex(item => item.id === condition.id)
      : -1;
    restoreConditionFocus = false;
    for (const [index,item] of exhibit.conditions.entries()) {
      let button = switcher.children[index];
      if (!button) {
        button = el('button', undefined, 'condition-tab');
        button.type = 'button';
        switcher.append(button);
      }
      button.id = `condition-tab-${index}`;
      button.dataset.condition = item.id;
      button.setAttribute('role','tab');
      button.setAttribute('aria-selected', String(item.id === condition.id));
      button.setAttribute('aria-controls','condition-panel');
      button.tabIndex = item.id === condition.id ? 0 : -1;
      button.replaceChildren(el('span', item.title, 'condition-title'), el('span', item.task, 'condition-task-preview'));
      // Buttons survive condition changes; replace handlers with current closures.
      button.onclick = () => {
        if (item.id === condition.id) return;
        restoreConditionFocus = true;
        location.hash = `#exhibit/${encodeURIComponent(exhibit.id)}/${encodeURIComponent(item.id)}`;
      };
      button.onkeydown = event => {
        if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
        event.preventDefault();
        const offset = event.key === 'ArrowLeft' ? -1 : event.key === 'ArrowRight' ? 1 : 0;
        const current = exhibit.conditions.findIndex(candidate => candidate.id === condition.id);
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? exhibit.conditions.length-1 : (current + offset + exhibit.conditions.length) % exhibit.conditions.length;
        restoreConditionFocus = true;
        location.hash = `#exhibit/${encodeURIComponent(exhibit.id)}/${encodeURIComponent(exhibit.conditions[next].id)}`;
      };
    }
    byId('condition-task').textContent = condition.task;
    byId('condition-focus').textContent = condition.focus;
    byId('condition-panel').setAttribute('aria-labelledby', `condition-tab-${exhibit.conditions.findIndex(item => item.id === condition.id)}`);
    renderComparisons(exhibit, condition);
    document.title = `${exhibit.title} · Relata`;
    byId('page-kicker').textContent = 'COLLECTION / 研究问题与源码比较';
    projectList(byId('project-search').value);
    renderQuestionCatalogue(byId('project-search').value);
    if (focusIndex >= 0) switcher.children[focusIndex]?.focus({preventScroll:true});
  }

  function comparisonCard(comparison, exhibit, condition) {
    const model = modelFor(comparison.project);
    const view = viewFor(model, comparison.view);
    if (!model || !view) return null;
    const article = el('article', undefined, 'comparison-item');
    article.id = `exhibit-${exhibit.id}-${comparison.project}`;
    const heading = el('header', undefined, 'comparison-heading-row');
    const titleBlock = el('div');
    titleBlock.append(
      el('div', `${labels[comparison.view]} · ${comparison.view}`, 'eyebrow'),
      el('h3', model.name)
    );
    const identity = el('div', undefined, 'comparison-identity');
    const boundary = el('details', undefined, 'boundary-details');
    boundary.append(el('summary','对象边界'), paragraph(model.boundary));
    identity.append(
      el('span', model.commit.slice(0,12), 'commit-label'),
      Object.assign(el('a','查看固定 commit ↗'), {href:`${model.repository}/commit/${model.commit}`, target:'_blank', rel:'noreferrer'}),
      boundary
    );
    heading.append(titleBlock, identity);
    article.append(heading);
    const observation = el('section', undefined, 'comparison-block');
    observation.append(el('span', statusNames.observed, 'status-label'), paragraph(comparison.observation, 'comparison-observation'));
    const columns = el('div', undefined, 'comparison-columns');
    const benefit = el('section', undefined, 'comparison-block');
    benefit.append(el('div','POSSIBLE VALUE / 可能价值', 'block-label'), paragraph(comparison.benefit));
    const limit = el('section', undefined, 'comparison-block');
    limit.append(el('div','LIMIT / 当前边界', 'block-label'), paragraph(comparison.limit));
    columns.append(benefit, limit);
    const reading = el('section', undefined, 'comparison-reading');
    reading.append(el('div', `当前 reading · ${condition.title}`, 'block-label'), paragraph(comparison.reading[condition.id] || '该条件尚未提供 reading。'));
    const next = el('section', undefined, 'comparison-check');
    next.append(el('div','NEXT CHECK / 下一步观察', 'block-label'), paragraph(comparison.check));
    article.append(observation, columns, reading, next);
    const footer = el('footer', undefined, 'comparison-footer');
    const evidence = el('div');
    evidence.append(el('div','PINNED EVIDENCE / 精确源码', 'block-label'));
    const sourceList = el('ul', undefined, 'source-notes');
    for (const id of comparison.sources) {
      const source = sourceFor(model, id);
      if (!source) continue;
      const item = el('li');
      const link = el('a', `${id} · ${source.note}`);
      link.href = source.url;
      link.target = '_blank';
      link.rel = 'noreferrer';
      item.append(link);
      sourceList.append(item);
    }
    evidence.append(sourceList);
    const nodeRow = el('div', undefined, 'node-action-row');
    nodeRow.append(el('span','定位节点','block-label'));
    for (const id of comparison.nodes) {
      const node = view.nodes.find(candidate => candidate.id === id);
      if (!node) continue;
      const link = el('a', node.label.replaceAll('\n',' · '), 'node-chip');
      link.href = encodeRoute(`${model.id}/${comparison.view}`, {node:id, exhibit:exhibit.id, condition:condition.id});
      link.addEventListener('click', event => {
        event.preventDefault();
        returnContext = {exhibit:exhibit.id, condition:condition.id};
        navigateProject(model.id, comparison.view, returnContext, id);
      });
      nodeRow.append(link);
    }
    const diagram = el('a','在图中查看 →','entry-link');
    diagram.href = encodeRoute(`${model.id}/${comparison.view}`, {exhibit:exhibit.id, condition:condition.id});
    diagram.addEventListener('click', event => {
      event.preventDefault();
      returnContext = {exhibit:exhibit.id, condition:condition.id};
      navigateProject(model.id, comparison.view, returnContext);
    });
    nodeRow.append(diagram);
    footer.append(evidence, nodeRow);
    article.append(footer);
    return article;
  }

  function renderComparisons(exhibit, condition) {
    const target = byId('comparison-list');
    target.replaceChildren();
    for (const comparison of exhibit.comparisons) {
      const card = comparisonCard(comparison, exhibit, condition);
      if (card) target.append(card);
    }
    byId('comparison-count').textContent = `${exhibit.comparisons.length} 个机制 · 固定提交与对象边界`;
    byId('condition-task').textContent = condition.task;
    byId('condition-focus').textContent = condition.focus;
    const controls = byId('exhibit-controls');
    controls.replaceChildren();
    for (const control of exhibit.controls) {
      const item = el('div', undefined, 'control-item');
      item.append(el('h3', control.title), paragraph(control.detail));
      controls.append(item);
    }
    const takeaways = byId('exhibit-takeaways');
    takeaways.replaceChildren();
    for (const key of ['benchmark','collection','incubator']) {
      const item = el('div', undefined, 'takeaway-row');
      item.append(el('dt', functionNames[key]), el('dd', exhibit.takeaways[key]));
      takeaways.append(item);
    }
    const links = byId('exhibit-links');
    links.replaceChildren();
    for (const linkData of exhibit.links) {
      const item = el('li');
      const link = el('a', `${linkData.label} ↗`);
      link.href = linkData.path;
      item.append(link);
      links.append(item);
    }
    const revisions = byId('exhibit-revisions');
    revisions.replaceChildren();
    for (const revision of exhibit.revisions) {
      const item = el('li');
      item.append(el('time', revision.date), paragraph(revision.summary));
      revisions.append(item);
    }
    byId('exhibit-github-link').href = `exhibits.md#${encodeURIComponent(exhibit.id)}`;
  }

  function loadRoute() {
    const raw = location.hash.replace(/^#/, '');
    const [path,query = ''] = raw.split('?');
    const segments = path.split('/').filter(Boolean);
    const params = new URLSearchParams(query);
    if (!segments.length || segments[0] === 'questions') {
      enterReadingRoute('questions');
      renderQuestions();
      return;
    }
    if (segments[0] === 'exhibit') {
      const exhibit = exhibitFor(decodeSegment(segments[1])) || exhibits[0];
      if (!exhibit) {
        enterReadingRoute('questions');
        renderQuestions();
        return;
      }
      enterReadingRoute(`exhibit/${exhibit.id}`);
      renderExhibit(exhibit, conditionFor(exhibit, decodeSegment(segments[2])));
      return;
    }
    const model = modelFor(decodeSegment(segments[0])) || models[0];
    const view = viewFor(model, segments[1]) || viewFor(model,'overview');
    selectedModel = model;
    selectedView = view;
    enterReadingRoute(`${model.id}/${view.id}`);
    // Both supported shapes: project/view/node and project/view?node=...
    selectedNode = params.get('node') || (segments[2] && view.nodes.some(node => node.id === segments[2]) ? segments[2] : '');
    const contextExhibit = exhibitFor(params.get('exhibit'));
    returnContext = contextExhibit
      ? {exhibit:contextExhibit.id, condition:(conditionFor(contextExhibit, params.get('condition')) || contextExhibit.conditions[0]).id}
      : undefined;
    renderProject();
  }

  function enterReadingRoute(next) {
    // New questions and systems start at their heading; changing a condition
    // or a node preserves the current reading position and keyboard context.
    if (readingRoute && readingRoute !== next) window.scrollTo({top:0,left:0,behavior:'instant'});
    readingRoute = next;
  }

  function renderProject() {
    showView('project');
    projectList('');
    byId('project-count').textContent = String(models.indexOf(selectedModel)+1).padStart(2,'0');
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
    const tabs = byId('view-tabs');
    tabs.replaceChildren();
    Object.entries(labels).forEach(([id,label],i) => {
      const button = el('button',undefined,'view-tab');
      button.type='button'; button.dataset.view=id;
      button.id = `view-tab-${id}`;
      button.setAttribute('aria-current',String(id===selectedView.id));
      button.append(el('span',String(i+1).padStart(2,'0'),'tab-number'),document.createTextNode(label));
      button.addEventListener('click',() => {
        if (id === selectedView.id) return;
        navigateProject(selectedModel.id,id);
      });
      tabs.append(button);
    });
    tabs.setAttribute('aria-labelledby','view-tab-' + selectedView.id);
    const crumbs = byId('project-breadcrumbs');
    const systems = el('a','系统图集'); systems.href = '#mem0/overview';
    crumbs.replaceChildren(systems, el('span','/'), el('span',selectedModel.name));
    renderReturnContext();
    const projectRoute = `${selectedModel.id}/${selectedView.id}`;
    if (renderedProjectRoute === projectRoute && byId('diagram-stage').querySelector('svg')) {
      restoreProjectNodeState();
    } else {
      renderedProjectRoute = projectRoute;
      renderView();
    }
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
      const groups = [...svg.querySelectorAll('g.node, g.guide-node')].filter(group => group.dataset.nodeReference === node.id || group.id.includes(`-flowchart-${node.id}-`));
      for (const group of groups) {
        group.dataset.node = node.id; group.setAttribute('tabindex','0'); group.setAttribute('role','button'); group.setAttribute('aria-label',`查看证据：${node.label.replaceAll('\n','，')}`);
        group.addEventListener('click',event => {event.preventDefault();selectNode(node.id,true);});
        group.addEventListener('keydown',event => {if (event.key === 'Enter' || event.key === ' ') {event.preventDefault();selectNode(node.id,true);}});
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
    byId('coverage').querySelector('ul').replaceChildren(...selectedView.omissions.map(text => el('li',text)));
    byId('source-list').replaceChildren(...selectedModel.sources.map(source => {
      const row = el('div',undefined,'source-row'); const link = el('a',`${source.id} · ${source.url.replace('https://github.com/','')}`);
      link.href=source.url;link.target='_blank';link.rel='noreferrer';row.append(link,paragraph(source.note));return row;
    }));
    byId('edge-evidence').replaceChildren(...selectedView.edges.map(edge => {
      const row = el('div',undefined,'edge-row');
      const fromNode=selectedView.nodes.find(node=>node.id===edge.from);
      const toNode=selectedView.nodes.find(node=>node.id===edge.to);
      row.append(el('p',`${fromNode?.label.split('\n')[0] || edge.from} → ${toNode?.label.split('\n')[0] || edge.to} · ${edge.label} · ${statusNames[edge.status]}`),sourceLinks(edge.evidence));
      return row;
    }));
    fit('reading');
    byId('diagram-viewport').scrollTo(0,0);
    if (selectedNode && selectedView.nodes.some(node => node.id === selectedNode)) {
      selectNode(selectedNode,false,false);
      requestAnimationFrame(revealSelectedNode);
    }
  }

  function renderReturnContext() {
    const box = byId('return-context');
    box.replaceChildren();
    const exhibit = returnContext ? exhibitFor(returnContext.exhibit) : undefined;
    if (!exhibit) {
      box.hidden = true;
      return;
    }
    const condition = conditionFor(exhibit,returnContext.condition);
    const link = el('a',`← 返回「${exhibit.title}」`);
    link.href = `#exhibit/${encodeURIComponent(exhibit.id)}/${encodeURIComponent(condition.id)}`;
    box.append(el('span',`从研究问题进入 · ${condition.title}`,'return-label'),link);
    box.hidden = false;
  }

  function updateNodeHash(value, push = false) {
    selectedNode = value;
    if (mode !== 'project' || !selectedModel) return;
    const nextHash = encodeRoute(`${selectedModel.id}/${selectedView.id}`, {
      node:value,
      exhibit:returnContext?.exhibit,
      condition:returnContext?.condition
    });
    if (location.hash === nextHash) return;
    if (push) history.pushState(history.state,'',nextHash);
    else history.replaceState(history.state,'',nextHash);
  }

  function selectNode(id, pushHash = true, moveFocus = true) {
    const node = selectedView.nodes.find(candidate => candidate.id === id);
    if (!node) return;
    selectedNode = id;
    byId('node-picker').value = id;
    byId('detail-title').textContent = node.label.replaceAll('\n',' · ');
    const region = selectedView.regions.find(candidate => candidate.id === node.region);
    byId('detail-body').replaceChildren(
      el('span',statusNames[node.status],'status-label'),
      el('p',node.note),
      el('p',`所属区域：${region?.label || node.region}。${region?.responsibility || ''}`),
      sourceLinks([...node.evidence,...(region?.evidence || [])])
    );
    const adjacentList = el('ul',undefined,'adjacent-list');
    for (const edge of selectedView.edges.filter(candidate => candidate.from===id || candidate.to===id)) {
      const otherId = edge.from===id ? edge.to : edge.from;
      const other = selectedView.nodes.find(candidate => candidate.id===otherId);
      const item = el('li',`${edge.from===id?'→':'←'} ${other?.label.split('\n')[0] || otherId}：${edge.label}`);
      item.append(sourceLinks(edge.evidence));
      adjacentList.append(item);
    }
    byId('detail-body').append(adjacentList);
    paintProjectNodeState();
    byId('view-instruction').textContent = `已选：${node.label.split('\n')[0]} · 证据见图下方`;
    updateNodeHash(id, pushHash);
    if (moveFocus) {
      pendingNodeFocus = id;
      revealSelectedNode();
    }
  }

  function paintProjectNodeState() {
    for (const group of byId('diagram-stage').querySelectorAll('g.node, g.guide-node')) group.classList.toggle('selected',group.dataset.node===selectedNode);
    selectedView.edges.forEach((edge,i) => {
      const edgeId=`E${String(i+1).padStart(2,'0')}`;
      for (const group of byId('diagram-stage').querySelectorAll(`[data-edge="${edgeId}"], [data-edge-reference="${edgeId}"]`)) group.classList.toggle('related',edge.from===selectedNode||edge.to===selectedNode);
    });
  }

  function restoreProjectNodeState() {
    projectList('');
    renderReturnContext();
    if (selectedNode && selectedView.nodes.some(node => node.id === selectedNode)) {
      selectNode(selectedNode,false,false);
      requestAnimationFrame(revealSelectedNode);
    } else {
      selectedNode = '';
      byId('node-picker').value = '';
      byId('detail-title').textContent = '从一个节点开始';
      byId('detail-body').replaceChildren(el('p','选择图中的节点，查看职责、状态归属、相邻关系和固定版本的源代码。所有箭头的证据也可在下方展开。'));
      byId('view-instruction').textContent = innerWidth <= 700 ? '左右滑动读图；点击节点查看证据' : '点击节点，沿源码查看它的职责';
      paintProjectNodeState();
    }
  }

  function revealSelectedNode() {
    const viewport = byId('diagram-viewport');
    const group = byId('diagram-stage').querySelector(`g[data-node="${CSS.escape(selectedNode)}"]`);
    if (!group) return;
    const restoreFocus = pendingNodeFocus === selectedNode;
    pendingNodeFocus = '';
    const rect = group.getBoundingClientRect();
    const frame = viewport.getBoundingClientRect();
    if (rect.left < frame.left || rect.right > frame.right || rect.top < frame.top || rect.bottom > frame.bottom) {
      group.scrollIntoView({block:'center', inline:'center', behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    }
    if (restoreFocus) group.focus({preventScroll:true});
  }

  function zoom(next) {
    scale=Math.max(.12,Math.min(2.5,next));
    const svg=byId('diagram-stage').querySelector('svg'); if(!svg) return;
    svg.style.width=`${naturalWidth*scale}px`;svg.style.height=`${naturalHeight*scale}px`;
    svg.setAttribute('width',naturalWidth*scale);svg.setAttribute('height',naturalHeight*scale);
    byId('zoom-value').textContent=`${Math.round(scale*100)}%`;
  }

  function fit(fitMode) {
    const viewport=byId('diagram-viewport');
    const padding=innerWidth<=700?36:52;
    const width=(viewport.clientWidth-padding)/naturalWidth;
    zoom(fitMode==='all'?Math.min(width,(viewport.clientHeight-padding)/naturalHeight):fitMode==='reading'?Math.min(1,Math.max(.85,width)):Math.min(1,width));
  }

  async function copyCurrentLink() {
    const feedback = byId('copy-feedback');
    const link = location.href;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
      await navigator.clipboard.writeText(link);
      feedback.textContent = '当前阅读链接已复制。';
    } catch {
      feedback.replaceChildren();
      const input = el('input');
      input.type = 'text'; input.value = link; input.readOnly = true; input.className = 'copy-fallback';
      feedback.append(el('span','请手动复制地址：'),input);
      input.focus(); input.select();
    }
  }

  byId('project-search').addEventListener('input',() => {
    if (mode === 'project') projectList();
    else searchQuestions();
  });
  document.getElementsByClassName('skip-link')[0].addEventListener('click', event => {
    event.preventDefault();
    byId('main-content').focus({preventScroll:true});
    byId('main-content').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth', block:'start'});
  });
  byId('node-picker').addEventListener('change',event=>{
    selectNode(event.target.value,true,false);
    revealSelectedNode();
  });
  byId('zoom-in').addEventListener('click',()=>zoom(scale*1.25));
  byId('zoom-out').addEventListener('click',()=>zoom(scale/1.25));
  byId('fit-reading').addEventListener('click',()=>fit('reading'));
  byId('fit-width').addEventListener('click',()=>fit('width'));
  byId('fit-all').addEventListener('click',()=>fit('all'));
  byId('copy-reading-link').addEventListener('click',copyCurrentLink);
  byId('export-svg').addEventListener('click',()=>{
    const svg=atlas.assets[`${selectedModel.id}--${selectedView.id}`];
    const url=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml;charset=utf-8'}));
    const link=el('a');link.href=url;link.download=`${selectedModel.id}-${selectedView.id}.svg`;link.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  addEventListener('hashchange',loadRoute);
  let resizeTimer;
  addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(mode==='project')fit('reading');},120);});
  loadRoute();
})();
