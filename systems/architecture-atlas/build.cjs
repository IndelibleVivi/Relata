/* Build Mermaid topology, fixed-width native SVG plates and an offline reader.
 * Uses only Node built-ins. No upstream project is executed; no network is used.
 */
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const { renderSvg } = require('./render-svg.cjs');
const statuses = new Set(['observed', 'inferred', 'unknown']);
const kinds = new Set(['entry', 'process', 'decision', 'store', 'model', 'output', 'external']);
const args = process.argv.slice(2);
const checkOnly = args.includes('--check');

function requireThat(condition, message) {
  if (!condition) throw new Error(message);
}
function readModels() {
  return fs.readdirSync(path.join(root, 'models')).filter(n => n.endsWith('.json')).sort()
    .map(name => JSON.parse(fs.readFileSync(path.join(root, 'models', name), 'utf8')));
}
function validate(model) {
  requireThat(/^[a-z][a-z0-9-]+$/.test(model.id), 'Invalid project id');
  requireThat(/^[a-f0-9]{40}$/.test(model.commit), `${model.id}: exact commit required`);
  requireThat(model.views.length === 3 && ['overview', 'flow', 'revision'].every(id => model.views.some(v => v.id === id)), `${model.id}: three reader views required`);
  const sources = new Set(model.sources.map(s => s.id));
  requireThat(sources.size === model.sources.length, `${model.id}: duplicate source id`);
  for (const s of model.sources) requireThat(/^https:\/\/github\.com\/[^/]+\/[^/]+\/blob\/[a-f0-9]{40}\/.+/.test(s.url), `${model.id}: unpinned source ${s.id}`);
  function evidence(item, label) {
    requireThat(statuses.has(item.status), `${model.id}: missing evidence status ${label}`);
    requireThat(Array.isArray(item.evidence), `${model.id}: missing evidence list ${label}`);
    requireThat(item.status === 'unknown' || item.evidence.length, `${model.id}: unsupported ${label}`);
    for (const id of item.evidence) requireThat(sources.has(id), `${model.id}: unknown source ${id}`);
  }
  for (const view of model.views) {
    const regions = new Set(view.regions.map(r => r.id));
    const nodes = new Set(view.nodes.map(n => n.id));
    requireThat(nodes.size === view.nodes.length && regions.size === view.regions.length, `${model.id}/${view.id}: duplicate ids`);
    for (const region of view.regions) evidence(region, region.id);
    for (const node of view.nodes) {
      requireThat(/^[a-zA-Z][a-zA-Z0-9_]*$/.test(node.id) && kinds.has(node.kind) && regions.has(node.region), `${model.id}/${view.id}: invalid node ${node.id}`);
      evidence(node, node.id);
    }
    for (const edge of view.edges) {
      requireThat(nodes.has(edge.from) && nodes.has(edge.to) && edge.label, `${model.id}/${view.id}: incomplete edge`);
      evidence(edge, `${edge.from} -> ${edge.to}`);
    }
    for (const state of view.state_notes) {
      requireThat(state.owner && state.writers && state.changes && state.limits, `${model.id}/${view.id}: incomplete state note`);
      for (const id of state.evidence) requireThat(sources.has(id), `${model.id}: unknown state source ${id}`);
    }
  }
}
function label(text) {
  return String(text).replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('\n', '<br/>').replaceAll('|', '&#124;');
}
function mermaid(model, view) {
  const lines = ['---', 'config:', '  layout: elk', '---', 'flowchart TB'];
  for (const region of view.regions) {
    lines.push(`  subgraph region_${region.id}["${label(region.label)}"]`);
    for (const node of view.nodes.filter(n => n.region === region.id)) {
      const suffix = node.status === 'observed' ? '' : `\n${node.status === 'inferred' ? '〔推断〕' : '〔未知〕'}`;
      const text = `"${label(node.label + suffix)}"`;
      const shape = node.kind === 'store' ? `[(${text})]` : node.kind === 'decision' ? `{${text}}` : node.kind === 'model' ? `[[${text}]]` : `[${text}]`;
      lines.push(`    ${node.id}${shape}:::${node.kind}`);
      if (node.status !== 'observed') lines.push(`    class ${node.id} ${node.status}`);
    }
    lines.push('  end');
  }
  for (const edge of view.edges) {
    const arrow = edge.status === 'observed' ? '-->' : '-.->';
    lines.push(`  ${edge.from} ${arrow}|"${label(edge.label)}"| ${edge.to}`);
  }
  lines.push('  classDef entry fill:#e8f0f3,stroke:#365665,color:#173644');
  lines.push('  classDef process fill:#ffffff,stroke:#76828a,color:#20313a');
  lines.push('  classDef decision fill:#fff1d9,stroke:#b88733,color:#5d441a');
  lines.push('  classDef store fill:#e4efe9,stroke:#54836b,color:#204a36');
  lines.push('  classDef model fill:#eeeaf7,stroke:#8371aa,color:#453467');
  lines.push('  classDef output fill:#e8f0f3,stroke:#365665,color:#173644');
  lines.push('  classDef external fill:#f5f3ef,stroke:#8e897f,color:#49453e');
  lines.push('  classDef inferred stroke-dasharray:5 4');
  lines.push('  classDef unknown stroke-dasharray:2 4');
  return lines.join('\n') + '\n';
}
function buildReader(models, assets) {
  const css = fs.readFileSync(path.join(root, 'viewer.css'), 'utf8');
  const js = fs.readFileSync(path.join(root, 'viewer.js'), 'utf8');
  const data = JSON.stringify({date:'2026-09-22', renderer:'relata-native-svg-1', models, assets}).replaceAll('<', '\\u003c');
  return fs.readFileSync(path.join(root, 'viewer.html'), 'utf8')
    .replace('/* ATLAS_STYLES */', css).replace('/* ATLAS_LOGIC */', js)
    .replace('<!-- ATLAS_DATA -->', `<script id="atlas-data" type="application/json">${data}</script>`);
}
async function main() {
  const models = readModels();
  requireThat(models.length > 0, 'No architecture models');
  models.forEach(validate);
  const assets = {};
  for (const model of models) {
    for (const view of model.views) {
      const key = `${model.id}--${view.id}`;
      const dir = path.join(root, 'diagrams', model.id);
      const source = mermaid(model, view);
      const sourcePath = path.join(dir, view.id + '.mmd');
      const svgPath = path.join(dir, view.id + '.svg');
      if (checkOnly) {
        requireThat(fs.readFileSync(sourcePath, 'utf8') === source, `${key}: Mermaid is stale`);
      } else {
        fs.mkdirSync(dir, {recursive:true});
        fs.writeFileSync(sourcePath, source);
        const svg = renderSvg(model, view);
        fs.writeFileSync(svgPath, svg);
      }
      const svg = fs.readFileSync(svgPath, 'utf8');
      requireThat(svg === renderSvg(model, view), `${key}: SVG is stale`);
      for (let i=0;i<view.edges.length;i++) requireThat(svg.includes(`data-edge="E${String(i+1).padStart(2,'0')}"`), `${key}: edge missing from SVG: ${i+1}`);
      for (const node of view.nodes) requireThat(svg.includes(`-flowchart-${node.id}-`), `${key}: node missing from SVG: ${node.id}`);
      assets[key] = svg;
      console.log(`${checkOnly ? 'checked' : 'rendered'} ${key}: ${view.nodes.length} nodes / ${view.edges.length} edges`);
    }
  }
  const reader = buildReader(models, assets);
  const target = path.join(root, 'index.html');
  if (checkOnly) requireThat(fs.readFileSync(target, 'utf8') === reader, 'Offline reader is stale');
  else fs.writeFileSync(target, reader);
  console.log(`${models.length} projects / ${Object.keys(assets).length} diagrams; ${checkOnly ? 'all derived artifacts current' : 'offline reader built'}`);
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
