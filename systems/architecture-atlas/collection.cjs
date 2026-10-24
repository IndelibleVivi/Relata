/* Static research reading paths. Model topology and source URLs remain in models/.
 * This module never imports a subject, private run, runtime config or provider.
 */
const fs = require('node:fs');
const path = require('node:path');

function requireThat(value, message) {
  if (!value) throw new Error(`Collection: ${message}`);
}
function text(value, label) {
  requireThat(typeof value === 'string' && value.trim().length > 0, `${label} requires text`);
}
function unique(items, label) {
  requireThat(new Set(items).size === items.length, `duplicate ${label}`);
}
function dated(value, label) {
  requireThat(typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) && Number.isFinite(Date.parse(value)) && new Date(value).toISOString().slice(0, 10) === value, `${label} requires a calendar date`);
}
function validateCollection(collection, models, atlasRoot = __dirname) {
  text(collection.title, 'title');
  text(collection.boundary, 'boundary');
  dated(collection.updated, 'updated');
  requireThat(Array.isArray(collection.exhibits) && collection.exhibits.length > 0, 'no exhibits');
  unique(collection.exhibits.map(e => e.id), 'exhibit id');
  const repoRoot = path.resolve(atlasRoot, '../..');
  for (const exhibit of collection.exhibits) {
    requireThat(/^[a-z][a-z0-9-]*$/.test(exhibit.id), 'invalid exhibit id');
    for (const key of ['title', 'question', 'summary', 'scenario']) text(exhibit[key], `${exhibit.id}/${key}`);
    requireThat(Array.isArray(exhibit.conditions) && exhibit.conditions.length >= 2, `${exhibit.id}: multiple reading conditions required`);
    unique(exhibit.conditions.map(c => c.id), `${exhibit.id} condition`);
    for (const condition of exhibit.conditions) {
      requireThat(/^[a-z][a-z0-9-]*$/.test(condition.id), `${exhibit.id}: invalid condition id`);
      for (const key of ['title', 'task', 'focus']) text(condition[key], `${exhibit.id}/${condition.id}/${key}`);
    }
    requireThat(Array.isArray(exhibit.comparisons) && exhibit.comparisons.length >= 2, `${exhibit.id}: comparison needs different systems`);
    unique(exhibit.comparisons.map(c => c.project), `${exhibit.id} comparison system`);
    for (const comparison of exhibit.comparisons) {
      const model = models.find(m => m.id === comparison.project);
      requireThat(model, `${exhibit.id}: unknown project ${comparison.project}`);
      const view = model.views.find(v => v.id === comparison.view);
      requireThat(view, `${exhibit.id}/${model.id}: unknown view ${comparison.view}`);
      requireThat(Array.isArray(comparison.nodes) && comparison.nodes.length > 0, `${exhibit.id}/${model.id}: no graph targets`);
      unique(comparison.nodes, `${exhibit.id}/${model.id} node`);
      for (const id of comparison.nodes) requireThat(view.nodes.some(n => n.id === id), `${exhibit.id}/${model.id}: unknown node ${id}`);
      requireThat(Array.isArray(comparison.sources) && comparison.sources.length > 0, `${exhibit.id}/${model.id}: no source evidence`);
      unique(comparison.sources, `${exhibit.id}/${model.id} source`);
      for (const id of comparison.sources) {
        const source = model.sources.find(s => s.id === id);
        requireThat(source, `${exhibit.id}/${model.id}: unknown source ${id}`);
        requireThat(source.url.startsWith(`${model.repository}/blob/${model.commit}/`), `${exhibit.id}/${model.id}: source ${id} does not match model revision`);
      }
      for (const key of ['observation', 'benefit', 'limit', 'check']) text(comparison[key], `${exhibit.id}/${model.id}/${key}`);
      requireThat(comparison.reading && typeof comparison.reading === 'object', `${exhibit.id}/${model.id}: missing conditional reading`);
      const conditionIds = exhibit.conditions.map(c => c.id);
      requireThat(Object.keys(comparison.reading).length === conditionIds.length && Object.keys(comparison.reading).every(id => conditionIds.includes(id)), `${exhibit.id}/${model.id}: reading conditions do not match`);
      for (const id of conditionIds) text(comparison.reading[id], `${exhibit.id}/${model.id}/${id}`);
    }
    requireThat(Array.isArray(exhibit.controls) && exhibit.controls.length > 0, `${exhibit.id}: no controls`);
    for (const control of exhibit.controls) {
      text(control.title, `${exhibit.id}/control title`);
      text(control.detail, `${exhibit.id}/control detail`);
    }
    requireThat(exhibit.takeaways && typeof exhibit.takeaways === 'object', `${exhibit.id}: no research destinations`);
    for (const key of ['benchmark', 'collection', 'incubator']) text(exhibit.takeaways[key], `${exhibit.id}/${key}`);
    requireThat(Array.isArray(exhibit.links) && exhibit.links.length > 0, `${exhibit.id}: no research links`);
    for (const link of exhibit.links) {
      text(link.label, `${exhibit.id}/link label`);
      text(link.path, `${exhibit.id}/link path`);
      requireThat(!path.isAbsolute(link.path) && !/[:\r\n?#\\]/.test(link.path), `${exhibit.id}: only relative research documents may be linked`);
      const target = path.resolve(atlasRoot, link.path);
      const relative = path.relative(repoRoot, target).split(path.sep).join('/');
      requireThat(/^(research|case-lab|systems)\/.+\.md$/.test(relative) && fs.existsSync(target), `${exhibit.id}: missing or non-research link ${link.path}`);
      requireThat(fs.realpathSync(target) === target, `${exhibit.id}: research link crosses a symlink`);
    }
    requireThat(Array.isArray(exhibit.revisions) && exhibit.revisions.length > 0, `${exhibit.id}: no judgment history`);
    let previous = '';
    for (const revision of exhibit.revisions) {
      dated(revision.date, `${exhibit.id}/revision`);
      requireThat(revision.date >= previous && revision.date <= collection.updated, `${exhibit.id}: revision dates out of order`);
      text(revision.summary, `${exhibit.id}/revision summary`);
      previous = revision.date;
    }
  }
}

function renderExhibitsMarkdown(collection, models) {
  const lines = [
    '<!-- Generated by build.cjs from exhibits.json and models/*.json. Do not edit. -->',
    '# Relata · 从研究问题进入系统集合', '',
    '**状态：** 静态 source synthesis；独立人类 review 与行为验证待完成。', '',
    `${collection.boundary}`, '',
    '[离线交互 reader](index.html#questions) · [源码图集与重建说明](README.md) · [研究室方向与能力版图](../../research/lab-development.md)', '',
    '情境、条件和判断由 `exhibits.json` 维护；节点、边界、固定版本与来源由 `models/*.json` 维护。下面的系统解释不能当作实际回答。条件是阅读视角，不是执行配置或新的 case family。', ''
  ];
  for (const exhibit of collection.exhibits) lines.push(`- [${exhibit.title}](#${exhibit.id}) — ${exhibit.question}`);
  lines.push('');
  for (const exhibit of collection.exhibits) {
    lines.push(`<a id="${exhibit.id}"></a>`, '', `## ${exhibit.title}`, '', `**${exhibit.question}**`, '', exhibit.summary, '', '**合成情境**', '', exhibit.scenario, '', '### 改变当前任务，保留同一情境', '');
    for (const condition of exhibit.conditions) lines.push(`- **${condition.title}：** ${condition.task} ${condition.focus}`);
    lines.push('');
    for (const comparison of exhibit.comparisons) {
      const model = models.find(m => m.id === comparison.project);
      const view = model.views.find(v => v.id === comparison.view);
      lines.push(`### ${model.name} · ${model.commit.slice(0, 7)}`, '', `**对象边界：** ${model.boundary}`, '', `**静态源码观察：** ${comparison.observation}`, '', `**可能价值：** ${comparison.benefit}`, '', `**条件与限制：** ${comparison.limit}`, '', '**按条件阅读：**', '');
      for (const condition of exhibit.conditions) lines.push(`- **${condition.title}：** ${comparison.reading[condition.id]}`);
      lines.push('', `**仍需观察：** ${comparison.check}`, '', '**固定源码：**', '');
      for (const id of comparison.sources) {
        const source = model.sources.find(s => s.id === id);
        lines.push(`- [${model.name} ${id}](${source.url}) — ${source.note}`);
      }
      lines.push('', '**沿图继续检查：**', '');
      for (const id of comparison.nodes) {
        const node = view.nodes.find(n => n.id === id);
        lines.push(`- [${node.label.replaceAll('\n', ' / ')}](index.html#${model.id}/${view.id}/${id}?exhibit=${exhibit.id}&condition=${exhibit.conditions[0].id})`);
      }
      lines.push('', `[完整 source study](../source-studies/${model.id}.md) · [可独立阅读的 ${view.title} SVG](diagrams/${model.id}/${view.id}.svg)`, '');
    }
    lines.push('### 比较时保留的对照', '');
    for (const control of exhibit.controls) lines.push(`- **${control.title}：** ${control.detail}`);
    lines.push('', '### 对三项研究职责的用途', '');
    for (const [key, label] of [['benchmark', 'Benchmark research'], ['collection', 'System collection'], ['incubator', 'Incubator']]) lines.push(`- **${label}：** ${exhibit.takeaways[key]}`);
    lines.push('', exhibit.links.map(link => `[${link.label}](${link.path})`).join(' · '), '', '### 判断修订', '');
    for (const revision of exhibit.revisions) lines.push(`- ${revision.date} — ${revision.summary}`);
    lines.push('');
  }
  return lines.join('\n').replace(/\n+$/, '') + '\n';
}

module.exports = {validateCollection, renderExhibitsMarkdown};
