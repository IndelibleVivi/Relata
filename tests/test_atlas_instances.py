"""Canonical Atlas snapshot payloads and independent component lifecycles."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / 'systems' / 'architecture-atlas'


class AtlasInstanceTests(unittest.TestCase):
    def node(self, *args):
        return subprocess.run(['node', *args], cwd=ROOT, text=True,
                              capture_output=True, check=False)

    def test_snapshot_reuses_schema_and_renders_only_validated_model(self):
        original = json.loads((ATLAS / 'models/a-mem.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            model_file = Path(directory) / 'snapshot.json'
            snapshot = {**original, 'commit': 'a' * 40}
            snapshot['sources'] = [{**source, 'url': source['url'].replace(original['commit'], snapshot['commit'])}
                                   for source in original['sources']]
            model_file.write_text(json.dumps(snapshot))
            result = self.node(str(ATLAS / 'studio-payload.cjs'), '--project', 'a-mem',
                               '--model-file', str(model_file))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload['models'], [snapshot])
            self.assertEqual(len(payload['assets']), 3)
            self.assertEqual(len(payload['guides']), 3)
            self.assertIsNone(payload['collection'])
            self.assertIn('a' * 40, payload['assets']['a-mem--overview'])
            snapshot['repository'] = 'javascript:alert(1)'
            model_file.write_text(json.dumps(snapshot))
            rejected = self.node(str(ATLAS / 'studio-payload.cjs'), '--project', 'a-mem',
                                 '--model-file', str(model_file))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(rejected.stdout, '')
            self.assertIn('public GitHub repository required', rejected.stderr)

    def test_two_browser_instances_and_dispose(self):
        available = self.node('-e', "try{require.resolve('playwright')}catch{process.exit(42)}")
        if available.returncode == 42:
            self.skipTest('Playwright unavailable; set NODE_PATH to the bundled runtime packages')
        script = r"""
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const {buildComponent} = require('./systems/architecture-atlas/build.cjs');
const {payload} = require('./systems/architecture-atlas/studio-payload.cjs');
(async () => {
  const browser = await chromium.launch({headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1600,height:1000}});
    const errors = []; page.on('pageerror',error => errors.push(error.message));
    await page.setContent('<div style="display:flex;gap:20px"><div id="left" style="width:550px;height:720px;overflow:auto"></div><div id="right" style="width:550px;height:720px;overflow:auto"></div></div>');
    await page.addScriptTag({content:buildComponent()});
    const data = payload('a-mem');
    await page.evaluate(data => {
      window.events = [];
      const old = structuredClone(data); old.models[0].commit='a'.repeat(40);
      window.a = RelataAtlas.mount(document.querySelector('#left'), {data, embedded:true, route:'#a-mem/overview',
        resolveSource:({commit,source}) => ({status:'saved',url:'#saved-'+commit+'-'+source.id}),
        onSelect:selection => events.push(['left',selection])});
      window.navListeners = new Set();
      window.navRoute = '#a-mem/overview';
      window.b = RelataAtlas.mount(document.querySelector('#right'), {data:old, embedded:true, navigation:{getRoute:()=>navRoute, navigate:route=>{navRoute=route;}, subscribe:fn=>{navListeners.add(fn); return ()=>navListeners.delete(fn);}},
        resolveSource:({commit,source}) => ({status:'missing',label:'缺失 '+commit+' '+source.id}),
        onSelect:selection => events.push(['right',selection])});
    }, data);
    const layout = await page.evaluate(() => ['left','right'].map(id => {
      const host = document.getElementById(id), root = host.shadowRoot;
      return {top:root.getElementById('diagram-viewport').getBoundingClientRect().top-host.getBoundingClientRect().top,
        directoryOpen:root.querySelector('.embedded-directory').open,
        contextOpen:root.querySelector('.embedded-project-context').open};
    }));
    for (const item of layout) {assert.ok(item.top < 300);assert.equal(item.directoryOpen,false);assert.equal(item.contextOpen,false);}
    await page.locator('#left .embedded-directory > summary').click();
    await page.locator('#left #project-search').fill('a-mem');
    assert.equal(await page.locator('#left #project-list .project-item').count(),1);
    assert.equal(await page.locator('#right .embedded-directory').getAttribute('open'),null);
    await page.locator('#left .embedded-directory > summary').click();
    const node = data.models[0].views[0].nodes[0].id;
    await page.locator('#left #node-picker').selectOption(node);
    let states = await page.evaluate(() => [a.getState(),b.getState(),location.hash]);
    assert.equal(states[0].node,node); assert.equal(states[1].node,''); assert.equal(states[2],'');
    const rightScale = states[1].scale;
    await page.locator('#left #zoom-in').click();
    states = await page.evaluate(() => [a.getState(),b.getState()]);
    assert.notEqual(states[0].scale,rightScale); assert.equal(states[1].scale,rightScale);
    await page.locator('#right #node-picker').selectOption(node);
    const sources = await page.evaluate(() => ['left','right'].map(id => {
      const link=document.querySelector('#'+id).shadowRoot.querySelector('#detail-body .evidence-links a');
      return {href:link.getAttribute('href'),status:link.dataset.sourceStatus};
    }));
    assert.match(sources[0].href,/^#saved-/); assert.equal(sources[0].status,'saved');
    assert.equal(sources[1].href,null); assert.equal(sources[1].status,'missing');
    await page.locator('#right #detail-body .evidence-links a').first().click();
    const selection=await page.evaluate(() => events.at(-1));
    assert.equal(selection[0],'right'); assert.equal(selection[1].commit,'a'.repeat(40));
    const exhibit=data.collection.exhibits[0];
    if (exhibit) {
      await page.evaluate(route => a.setState(route), '#exhibit/'+exhibit.id+'/'+exhibit.conditions[0].id);
      await page.locator('#left #condition-switcher button').first().focus();
      await page.keyboard.press('ArrowRight');
      states=await page.evaluate(() => [a.getState(),b.getState()]);
      assert.equal(states[0].condition,exhibit.conditions[1].id); assert.equal(states[1].mode,'project');
      await page.evaluate(() => {
        const button=document.querySelector('#left').shadowRoot.querySelector('#condition-switcher [aria-selected="true"]');
        button.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',isComposing:true,bubbles:true}));
      });
      assert.equal(await page.evaluate(() => a.getState().condition),exhibit.conditions[1].id);
    }
    await page.evaluate(() => {
      window.before = events.length;
      window.detached = document.querySelector('#right').shadowRoot.querySelector('#zoom-in');
      window.lateNav = [...navListeners][0];
      b.dispose(); detached.click(); b.setState('#questions'); lateNav('#questions');
      location.hash='#questions';
    });
    assert.equal(await page.evaluate(() => document.querySelector('#right').shadowRoot.childNodes.length),0);
    assert.equal(await page.evaluate(() => navListeners.size),0);
    assert.equal(await page.evaluate(() => events.length),await page.evaluate(() => before));
    assert.equal(await page.evaluate(() => a.getState().mode),'exhibit');
    // A remount creates a fresh owner, and malicious artifact SVG is inert.
    await page.evaluate(data => {
      data.assets['a-mem--overview']=data.assets['a-mem--overview'].replace('</svg>',
        '<script>window.injected=true</script><foreignObject><div xmlns="http://www.w3.org/1999/xhtml" onclick="window.injected=true">BAD</div></foreignObject></svg>');
      window.b=RelataAtlas.mount(document.querySelector('#right'),{data,route:'#a-mem/overview'});
    },data);
    assert.equal(await page.evaluate(() => Boolean(window.injected)),false);
    assert.equal(await page.locator('#right #diagram-stage foreignObject').count(),0);
    assert.deepEqual(errors,[]);
    console.log('two independent snapshots; source identity; keyboard/IME; zoom; dispose; inert SVG verified');
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode=1;});
"""
        result = self.node('-e', script)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
