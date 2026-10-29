const {chromium} = require('playwright');
const fs = require('node:fs');
const assert = require('node:assert/strict');

(async () => {
  const [base, output, seedPath] = process.argv.slice(2);
  const seed = JSON.parse(fs.readFileSync(seedPath));
  const browser = await chromium.launch({headless:true});
  const page = await browser.newPage({viewport:{width:1440,height:1000}});
  const errors = [];
  page.on('pageerror', e => errors.push(e.stack || e.message));
  try {
    await page.goto(base + '/#study/' + seed.study + '/observe');
    await page.locator('#run-select').selectOption(seed.run);
    await page.locator('.tag').filter({hasText:/^text$/}).waitFor();
    await page.getByRole('button',{name:'分析',exact:true}).click();
    await page.locator('#analysis-title').fill('相似表面不等于相同用途');
    await page.locator('#analysis-text').fill('同样是整理资料，当前目的已经改变。旧口吻的延续尚不能证明方法适用。');
    await page.locator('#analysis-alternatives').fill('可能是当前指令不足，也可能是采用环节仍读了旧方法。');
    await page.locator('#analysis-limits').fill('作者合成观察；没有模型执行。\n不能推论长期 memory 效果。');
    await page.locator('.evidence-open[data-id="'+seed.observation+'"]').click();
    await page.locator('#evidence-field').selectOption('text');
    await page.locator('#evidence-relation').selectOption('challenges');
    await page.locator('#evidence-note').fill('当前目的改变后，响应仍沿用旧语气。');
    await page.locator('#evidence-quote').fill('这次仍沿用了旧的语气。');
    await page.locator('#evidence-add').click();
    await page.locator('.analysis-citation blockquote').getByText('这次仍沿用了旧的语气。',{exact:true}).waitFor();
    await page.locator('.evidence-open[data-id="'+seed.review+'"]').click();
    await page.locator('#evidence-relation').selectOption('context');
    await page.locator('#evidence-note').fill('保留最初的不同解释。');
    await page.locator('#evidence-add').click();
    await page.waitForFunction(()=>document.querySelector('#analysis-save-status').textContent==='分析草稿已保存');
    await page.reload();
    await page.locator('#analysis-text').waitFor();
    assert.match(await page.locator('#analysis-text').inputValue(),/当前目的已经改变/);
    assert.equal(await page.locator('.analysis-citation').count(),2);
    // Continue typing while a navigation-triggered save is held at the HTTP boundary.
    const draftUrl = page.url();
    let releaseSave, beginSave, held = false;
    const gate = new Promise(resolve=>{releaseSave=resolve;});
    const began = new Promise(resolve=>{beginSave=resolve;});
    await page.route('**/api/command',async route=>{
      const request = route.request().postDataJSON();
      if(!held && request.name==='working.save' && request.payload.name.startsWith('analysis-draft:')){
        held=true;beginSave();await gate;
      }
      await route.continue();
    });
    await page.locator('#analysis-text').fill('当前目的已经改变；保存中的第一版。');
    await page.getByRole('link',{name:/01 研究桌/}).click();
    await began;
    await page.locator('#analysis-text').fill('当前目的已经改变；导航等待期间补写的末句。');
    releaseSave();
    await page.getByRole('heading',{name:'让一个问题，继续生长。',exact:true}).waitFor();
    await page.unroute('**/api/command');
    await page.goto(draftUrl);
    await page.locator('#analysis-text').waitFor();
    assert.match(await page.locator('#analysis-text').inputValue(),/导航等待期间补写的末句/);
    await page.locator('#analysis-freeze').click();
    await page.waitForURL(/\/analysis\/[^/]+\/1$/);
    await page.locator('#analysis-revision').waitFor();
    const firstUrl = page.url();
    const analysisId = firstUrl.split('/').at(-2);
    await page.screenshot({path:output+'/analysis-desktop.png',fullPage:true});

    // A real author-side amendment changes review context, not the saved analysis.
    await page.getByRole('button',{name:'评审',exact:true}).click();
    await page.locator('.judge').click();
    await page.locator('[name=reviewer]').fill('synthetic-reviewer');
    await page.locator('[name=observation]').selectOption(seed.observation);
    await page.locator('[name=mapping]').selectOption('ambiguous');
    await page.locator('[name=rationale]').fill('新解释：同样的现象也可能来自当前任务指令不足。');
    await page.locator('#modal-form button[type=submit]').click();
    await page.getByText('新解释：同样的现象也可能来自当前任务指令不足。',{exact:true}).waitFor();
    await page.goto(firstUrl);
    await page.locator('#analysis-review-warning').waitFor();
    await page.getByText('引用的是历史判断 · 已有同人修订',{exact:true}).waitFor();
    await page.locator('#analysis-text').fill('修订解释：已有两个机制可能产生同一响应，当前观察无法区分。');
    await page.locator('#analysis-freeze').click();
    await page.waitForURL(/\/2$/);
    await page.locator('#analysis-revision').waitFor();
    assert.equal(await page.locator('#analysis-review-warning').count(),0);
    await page.locator('#analysis-revision').selectOption('1');
    await page.waitForURL(/\/1$/);
    await page.locator('#analysis-current').waitFor();
    await page.locator('#analysis-review-warning').waitFor();
    assert.match(await page.locator('#analysis-text').inputValue(),/当前目的已经改变/);
    assert(await page.locator('#analysis-text').evaluate(el=>el.readOnly));

    await page.locator('#analysis-claim').click();
    await page.locator('[name=title]').fill('用途改变时，重新检查经验的适用范围');
    await page.locator('[name=text]').fill('表面相似不能独立决定经验是否适用。');
    await page.locator('[name=limits]').fill('作者解释；私人分析在公开投影中不可验证。');
    await page.locator('[name=public]').check();
    await page.locator('#modal-form button[type=submit]').click();
    await page.waitForURL(/#library$/);
    await page.locator('#publication-selection label').filter({hasText:'用途改变时，重新检查经验的适用范围'}).locator('input').check();
    await page.locator('#preview').click();
    const [publication] = await Promise.all([page.waitForEvent('download'),page.locator('#download-public').click()]);
    await publication.saveAs(output+'/analysis-publication.json');
    const bundle = JSON.parse(fs.readFileSync(output+'/analysis-publication.json'));
    const raw = JSON.stringify(bundle);
    assert(!raw.includes(seed.observation));
    assert(!raw.includes(analysisId));
    assert(!raw.includes('这次仍沿用了旧的语气。'));
    assert(bundle.objects[0].refs.some(r=>r.withheld));
    await page.locator('#freeze-edition').click();
    await page.getByText('Edition 已固定，可从作品列表重新打开。',{exact:true}).waitFor();

    // Return link chooses the cited run even if another run was selected later.
    await page.goto(base+'/#study/'+seed.study+'/observe');
    await page.locator('#run-select').selectOption(seed.otherRun);
    await page.goto(base+'/#library');
    await page.locator('.library-sources summary').click();
    await page.getByRole('link',{name:'查看所引用的分析 · r1 ↗',exact:true}).click();
    await page.locator('#analysis-current').waitFor();
    assert.match(await page.locator('#analysis-text').inputValue(),/当前目的已经改变/);
    await page.locator('#analysis-current').click();
    await page.locator('#analysis-freeze').waitFor();

    for (const width of [1024,390]) {
      await page.setViewportSize({width,height:900});
      if(width===390){
        await page.getByRole('button',{name:'查材料',exact:true}).click();
        await page.locator('.evidence-open[data-id="'+seed.empty+'"]').click();
        await page.getByText('此区域原文为空。空返回本身可以成为证据，无须编造引文。',{exact:true}).waitFor();
        await page.locator('#evidence-note').fill('空正文不能补出内部原因。');
        await page.locator('#evidence-add').click();
        await page.getByRole('button',{name:'写分析',exact:true}).press('Tab');
      }
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
      await page.screenshot({path:output+'/analysis-'+width+'.png',fullPage:true});
    }
    await page.setViewportSize({width:1440,height:1000});
    const [transfer] = await Promise.all([page.waitForEvent('download'),page.locator('#transfer').click()]);
    await transfer.saveAs(output+'/analysis-transfer.zip');
    fs.writeFileSync(output+'/analysis-result.json',JSON.stringify({analysisId,firstUrl,errors}));
    assert.deepEqual(errors,[]);
    console.log('Authored analysis browser journey: PASS');
  } catch(e) {
    await page.screenshot({path:output+'/analysis-failure.png',fullPage:true});
    console.error('PAGE_ERRORS',errors);
    console.error((await page.locator('body').innerText()).slice(-3500));
    throw e;
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
