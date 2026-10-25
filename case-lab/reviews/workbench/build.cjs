/* Build a standalone offline reviewer. No run folder is read or embedded. */
const fs = require('node:fs');
const path = require('node:path');
const {createHash} = require('node:crypto');
const root = __dirname;
const check = process.argv.slice(2);
if (check.some(arg => arg !== '--check')) throw new Error('Usage: node build.cjs [--check]');
const contractBytes = fs.readFileSync(path.join(root, '../rc005-review-contract.json'));
const contract = JSON.parse(contractBytes);
const contractHash = createHash('sha256').update(contractBytes).digest('hex');
const demo = JSON.parse(fs.readFileSync(path.join(root, 'demo.json'), 'utf8'));
if (demo.practice_only !== true) throw new Error('Only the public authored practice fixture may be embedded');
const json = value => JSON.stringify(value).replaceAll('<', '\\u003c');
const html = fs.readFileSync(path.join(root, 'viewer.html'), 'utf8')
  .replace('/* REVIEW_STYLES */', fs.readFileSync(path.join(root, 'viewer.css'), 'utf8'))
  .replace('<!-- REVIEW_CONTRACT -->', `<script id="review-contract" type="application/json">${json({contract, sha256:contractHash})}</script>`)
  .replace('<!-- REVIEW_DEMO -->', `<script id="review-demo" type="application/json">${json(demo)}</script>`)
  .replace('/* REVIEW_LOGIC */', fs.readFileSync(path.join(root, 'core.js'), 'utf8') + '\n' + fs.readFileSync(path.join(root, 'viewer.js'), 'utf8'));
const target = path.join(root, 'index.html');
if (check.includes('--check')) {
  if (fs.readFileSync(target, 'utf8') !== html) throw new Error('Offline review workbench is stale; rebuild it');
  console.log('Offline review workbench: generated artifact current');
} else {
  fs.writeFileSync(target, html);
  console.log('Offline review workbench built with public practice data only');
}
