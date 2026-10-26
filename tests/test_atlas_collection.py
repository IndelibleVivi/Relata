"""Cross-reference and publication boundaries for the static research reader."""
import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "systems" / "architecture-atlas"


class CollectionTests(unittest.TestCase):
    EXAMPLE_FIXTURE = """
const exampleExhibit = collection.exhibits[0];
exampleExhibit.episodes = [
  {id:'earlier', title:'Earlier title', text:'PAST VISIBLE'},
  {id:'later', title:'Later title', text:'LATER VISIBLE'},
  {id:'not-selected', title:'Unselected title', text:'NEVER EXPOSED'}
];
const example = {
  title:'Example title', visibleHistory:['earlier'], current:'Current task',
  proposal:'Author proposal', analysis:'Author analysis',
  acceptable:['First permitted action','Second permitted action'], pitfall:'Pitfall'
};
exampleExhibit.conditions[0].workedExample = example;
exampleExhibit.conditions[1].workedExample = {...example, visibleHistory:['later']};
"""

    def run_node(self, body):
        script = """
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const dir = path.resolve('systems/architecture-atlas');
const {validateCollection, renderExhibitsMarkdown} = require(path.join(dir, 'collection.cjs'));
const models = fs.readdirSync(path.join(dir, 'models')).filter(n => n.endsWith('.json'))
  .map(n => JSON.parse(fs.readFileSync(path.join(dir, 'models', n), 'utf8')));
const collection = JSON.parse(fs.readFileSync(path.join(dir, 'exhibits.json'), 'utf8'));
""" + body
        result = subprocess.run(["node", "-e", script], cwd=ROOT,
                                text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_authored_reading_paths_resolve_and_export_exact_sources(self):
        self.run_node("""
validateCollection(collection, models, dir);
const markdown = renderExhibitsMarkdown(collection, models);
for (const exhibit of collection.exhibits) {
  assert.ok(markdown.includes(`<a id="${exhibit.id}"></a>`));
  for (const comparison of exhibit.comparisons) {
    const model = models.find(m => m.id === comparison.project);
    for (const id of comparison.sources) {
      assert.ok(markdown.includes(model.sources.find(s => s.id === id).url));
    }
    for (const id of comparison.nodes) {
      assert.ok(markdown.includes(`#${model.id}/${comparison.view}/${id}?exhibit=${exhibit.id}`));
    }
    for (const condition of exhibit.conditions) assert.ok(markdown.includes(comparison.reading[condition.id]));
  }
}
assert.ok(markdown.includes('不是实际回答') || markdown.includes('不能当作实际回答'));
""")

    def test_rejects_evidence_or_diagram_references_that_no_longer_exist(self):
        self.run_node("""
for (const [field, value, pattern] of [
  ['project', 'missing-system', /unknown project/],
  ['view', 'missing-view', /unknown view/],
  ['nodes', ['missing-node'], /unknown node/],
  ['sources', ['missing-source'], /unknown source/]
]) {
  const changed = structuredClone(collection);
  changed.exhibits[0].comparisons[0][field] = value;
  assert.throws(() => validateCollection(changed, models, dir), pattern);
}
""")

    def test_rejects_source_at_another_commit(self):
        self.run_node("""
const comparison = collection.exhibits[0].comparisons[0];
const model = models.find(m => m.id === comparison.project);
const source = model.sources.find(s => s.id === comparison.sources[0]);
source.url = source.url.replace(model.commit, '0'.repeat(40));
assert.throws(() => validateCollection(collection, models, dir), /does not match model revision/);
""")

    def test_rejects_missing_or_unrelated_condition_analysis(self):
        self.run_node("""
const reading = collection.exhibits[0].comparisons[0].reading;
const id = collection.exhibits[0].conditions[0].id;
delete reading[id];
assert.throws(() => validateCollection(collection, models, dir), /conditions do not match/);
reading['unrelated-condition'] = 'not the selected task';
assert.throws(() => validateCollection(collection, models, dir), /conditions do not match/);
""")

    def test_rejects_private_or_external_document_paths(self):
        self.run_node("""
for (const target of ['../../experiments/artifacts/private.md', '/private/tmp/notes.md',
  '../../../../../private.md', 'https://example.com/private', 'javascript:alert(1)']) {
  const changed = structuredClone(collection);
  changed.exhibits[0].links[0].path = target;
  assert.throws(() => validateCollection(changed, models, dir), /relative research|non-research link/);
}
""")

    def test_rejects_ambiguous_routes_and_fabricated_future_history(self):
        self.run_node("""
let changed = structuredClone(collection);
changed.exhibits[1].id = changed.exhibits[0].id;
assert.throws(() => validateCollection(changed, models, dir), /duplicate exhibit/);
changed = structuredClone(collection);
changed.exhibits[0].conditions[1].id = changed.exhibits[0].conditions[0].id;
assert.throws(() => validateCollection(changed, models, dir), /duplicate.*condition/);
changed = structuredClone(collection);
changed.exhibits[0].revisions[0].date = '2099-01-01';
assert.throws(() => validateCollection(changed, models, dir), /dates out of order/);
""")

    def test_worked_example_exports_only_each_conditions_visible_history(self):
        self.run_node(self.EXAMPLE_FIXTURE + """
validateCollection(collection, models, dir);
const markdown = renderExhibitsMarkdown(collection, models);
const first = markdown.split('### 展开情境 · ')[1];
const second = markdown.split('### 展开情境 · ')[2];
assert.ok(first.includes('Earlier title') && first.includes('PAST VISIBLE'));
assert.ok(!first.includes('LATER VISIBLE'));
assert.ok(second.includes('Later title') && second.includes('LATER VISIBLE'));
assert.ok(!second.includes('PAST VISIBLE'));
assert.ok(!markdown.includes('NEVER EXPOSED'));
for (const field of ['title','current','proposal','analysis','pitfall']) assert.ok(first.includes(example[field]));
for (const action of example.acceptable) assert.ok(first.includes(action));
assert.ok(first.includes('不是系统输出'));
// Optional data must not become mandatory for existing exhibits.
delete exampleExhibit.episodes;
delete exampleExhibit.conditions[0].workedExample;
delete exampleExhibit.conditions[1].workedExample;
validateCollection(collection, models, dir);
assert.ok(!renderExhibitsMarkdown(collection, models).includes('PAST VISIBLE'));
""")

    def test_rejects_malformed_present_examples_and_episode_references(self):
        self.run_node(self.EXAMPLE_FIXTURE + """
const original = structuredClone(collection);
const changes = [
  e => { e.episodes = null; },
  e => { e.episodes = []; },
  e => { e.episodes[0] = null; },
  e => { e.episodes[0].id = 'bad/id'; },
  e => { e.episodes[1].id = 'earlier'; },
  e => { e.episodes[0].text = ''; },
  e => { e.conditions[0].workedExample = null; },
  e => { e.conditions[0].workedExample = []; },
  e => { e.conditions[0].workedExample.visibleHistory = []; },
  e => { e.conditions[0].workedExample.visibleHistory = ['earlier','earlier']; },
  e => { e.conditions[0].workedExample.visibleHistory = ['other-exhibit']; },
  e => { e.conditions[0].workedExample.visibleHistory = [null]; },
  e => { delete e.episodes; },
  e => { e.conditions[0].workedExample.acceptable = []; },
  e => { e.conditions[0].workedExample.acceptable = ['']; },
  e => { e.conditions[0].workedExample.acceptable = 'one'; }
];
for (const key of ['title','current','proposal','analysis','pitfall']) {
  changes.push(e => { e.conditions[0].workedExample[key] = ''; });
}
for (const change of changes) {
  const changed = structuredClone(original);
  change(changed.exhibits[0]);
  assert.throws(() => validateCollection(changed, models, dir), /Collection:/);
}
""")

    def test_authored_example_text_cannot_inject_markdown_or_html(self):
        self.run_node(self.EXAMPLE_FIXTURE + """
const hostile = '<script>alert(1)</script>\\n![image](https://invalid.example/private)\\n# invented heading | [link](javascript:run)';
exampleExhibit.episodes[0].title = hostile;
exampleExhibit.episodes[0].text = hostile;
for (const key of ['title','current','proposal','analysis','pitfall']) example[key] = hostile;
example.acceptable = [hostile];
validateCollection(collection, models, dir);
const first = renderExhibitsMarkdown(collection, models).split('### 展开情境 · ')[1];
for (const executable of ['<script>','![image]','# invented','[link]','https://invalid','javascript:run']) {
  assert.ok(!first.includes(executable), executable);
}
assert.ok(first.includes('&#60;script&#62;'));
assert.ok(first.includes('&#35; invented heading'));
assert.ok(first.includes('&#33;&#91;image&#93;'));
assert.ok(first.includes('\\n\\n'));
""")


if __name__ == "__main__":
    unittest.main()
