/* Snapshot payloads use the canonical validator/renderers. No imported script,
 * generated SVG or executable field is accepted as rendering authority. */
const fs = require('node:fs');
const {validate, readModels, mermaid, buildComponent} = require('./build.cjs');
const {renderSvg} = require('./render-svg.cjs');

function payload(project, modelFile) {
  const models = readModels();
  models.forEach(validate);
  const model = modelFile ? JSON.parse(fs.readFileSync(modelFile, 'utf8')) : models.find(item => item.id === project);
  if (!model) throw new Error('Unknown Atlas project');
  validate(model);
  if (project && model.id !== project) throw new Error('Model project does not match --project');
  // Keep authored walkthroughs and all conditions; comparisons remain scoped to
  // this snapshot, never substituted from a different commit of the same system.
  let collection = JSON.parse(fs.readFileSync(require('node:path').join(__dirname,'exhibits.json'), 'utf8'));
  collection.exhibits = collection.exhibits.map(exhibit => ({...exhibit,
    comparisons:exhibit.comparisons.filter(item => item.project === model.id &&
      model.views.some(view => view.id === item.view && item.nodes.every(id => view.nodes.some(node => node.id === id))) &&
      item.sources.every(id => model.sources.some(source => source.id === id)))
  })).filter(exhibit => exhibit.comparisons.length);
  // An old model alone cannot establish which authored synthesis existed then.
  // Studio restores saved full payloads to recover historical conditions.
  if (modelFile && JSON.stringify(model) !== JSON.stringify(models.find(item => item.id === model.id))) collection = null;
  const assets = {}, guides = {};
  for (const view of model.views) {
    const key = `${model.id}--${view.id}`;
    assets[key] = renderSvg(model, view);
    guides[key] = mermaid(model, view);
  }
  return {date:'2026-09-22',renderer:'relata-native-svg-1',models:[model],assets,guides,collection};
}
module.exports = {payload};
if (require.main === module) {
  try {
    const args = process.argv.slice(2);
    if (args.length === 1 && args[0] === '--component') process.stdout.write(buildComponent());
    else {
      const options = {};
      for (let i=0; i<args.length; i+=2) {
        if (!['--project','--model-file'].includes(args[i]) || !args[i+1]) throw new Error('Usage: --project ID [--model-file JSON] | --component');
        options[args[i]] = args[i+1];
      }
      if (!options['--project']) throw new Error('--project is required');
      process.stdout.write(JSON.stringify(payload(options['--project'], options['--model-file'])));
    }
  } catch(error) {console.error(error.message);process.exitCode = 1;}
}
