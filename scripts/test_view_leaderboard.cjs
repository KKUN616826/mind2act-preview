/* NODE_PATH and CHROMIUM_EXECUTABLE follow test_hero_browser.cjs. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {chromium} = require('playwright');
const data = require('../data/view-leaderboard.json');
(async () => {
 const browser = await chromium.launch({headless:true, ...(process.env.CHROMIUM_EXECUTABLE ? {executablePath:process.env.CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']} : {})});
 const base = process.env.HERO_PREVIEW_URL || 'http://127.0.0.1:8765/';
 try {
  for (const path of ['', 'leaderboard.html']) {
   const page = await browser.newPage({reducedMotion:'reduce'});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.route('**/*.mp4',r=>r.abort());
   await page.goto(new URL(path,base).href,{waitUntil:'domcontentloaded'});
   const board=page.locator('.view-leaderboard');
   await board.scrollIntoViewIfNeeded();
   assert.deepEqual(await board.locator('[role=tab]').allTextContents(),['Mind','Act','Mind2Act']);
   assert.deepEqual(await board.locator('thead th').allTextContents(),['Rank','Model','Paradigm','Score 0–100','Success %','Demos']);
   for(const view of data.views){
    await board.locator(`[data-board-view="${view.key}"]`).click();
    assert.equal(await board.locator('h3').textContent(),view.label);
    assert.deepEqual(await board.locator('.board-task-links a').allTextContents(),view.tasks);
    for(const paradigm of ['all',...Object.keys(data.paradigms)]){
     await board.locator('select').selectOption(paradigm);
     const expected=data.models.filter(m=>paradigm==='all'||m.paradigm===paradigm);
     assert.equal(await board.locator('tbody tr:visible').count(),expected.length);
     assert.ok(await board.locator('tbody tr:visible').evaluateAll(rows=>rows.every(row=>[0,3,4].every(i=>row.cells[i].textContent==='—'))));
     await board.locator('input').fill('  '+expected[0].name.toUpperCase()+'  ');
     assert.equal(await board.locator('tbody tr:visible').count(),1);
     await board.locator('input').fill('no such model');
     assert.equal(await board.locator('tbody tr:visible').count(),0);
     assert.equal(await board.locator('.board-empty').isVisible(),true);
     await board.locator('input').fill('');
    }
   }
   await board.locator('select').selectOption('all');
   for(const width of [320,390,820,1440,1920]){
    await page.setViewportSize({width,height:900});
    await board.scrollIntoViewIfNeeded();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`${path} ${width}: page overflow`);
    assert.ok(await board.locator('.board-tabs button,.board-tools label').evaluateAll(els=>els.every(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth})),`${path} ${width}: clipped controls`);
    if(process.env.HERO_SCREENSHOTS){fs.mkdirSync(process.env.HERO_SCREENSHOTS,{recursive:true});await board.screenshot({path:`${process.env.HERO_SCREENSHOTS}/views-${path?'full':'home'}-${width}.png`});}
   }
   await board.locator('[data-board-view="mind"]').focus();await page.keyboard.press('ArrowRight');
   assert.equal(await board.locator('[aria-selected="true"]').getAttribute('data-board-view'),'act');
   await page.keyboard.press('End');assert.equal(await board.getAttribute('data-view'),'coupling');
   if(!path){
    await page.locator('.lunar-worlds-frame').scrollIntoViewIfNeeded();
    const scene=page.frameLocator('.lunar-worlds-frame');await scene.locator('.node').first().waitFor();
    await board.locator('[data-board-view="act"]').click();
    await page.waitForFunction(()=>document.querySelector('.lunar-worlds-frame').contentDocument.querySelector('.stage').dataset.world==='act');
    await scene.locator('[data-world="coupling"][role="tab"]').click();
    await page.waitForFunction(()=>document.querySelector('.view-leaderboard').dataset.view==='coupling');
    await board.locator('select').selectOption('coding');await board.locator('input').fill('gpt');
    await page.locator('.full-leader-link a').click();await page.waitForURL('**/leaderboard.html?**');
    assert.equal(await page.locator('.view-leaderboard').getAttribute('data-view'),'coupling');
    assert.equal(await page.locator('#board-paradigm').inputValue(),'coding');
    assert.equal(await page.locator('#model-search').inputValue(),'gpt');
    assert.equal(await page.locator('tbody tr:visible').count(),1);
   }
   assert.deepEqual(errors,[]);
   await page.close();console.log('PASS:',path||'homepage','three views, pending values, combined filters, empty state, keyboard, responsive layout and links');
  }
  const deep=await browser.newPage({reducedMotion:'reduce'});
  await deep.route('**/*.mp4',r=>r.abort());
  await deep.goto(new URL('?view=act&paradigm=end-to-end',base).href,{waitUntil:'domcontentloaded'});
  await deep.locator('.lunar-worlds-frame').scrollIntoViewIfNeeded();
  await deep.frameLocator('.lunar-worlds-frame').locator('.node').first().waitFor();
  await deep.waitForFunction(()=>document.querySelector('.lunar-worlds-frame').contentDocument.querySelector('.stage').dataset.world==='act');
  assert.equal(await deep.locator('.view-leaderboard').getAttribute('data-view'),'act');
  assert.equal(await deep.locator('#board-paradigm').inputValue(),'end-to-end');
  await deep.close();
  const page=await browser.newPage();await page.goto(new URL('leaderboard.html?view=bad&paradigm=bad&q=%3Cimg%20src=x%3E',base).href);
  assert.equal(await page.locator('.view-leaderboard').getAttribute('data-view'),'mind');
  assert.equal(await page.locator('#board-paradigm').inputValue(),'all');
  assert.equal(await page.locator('tbody tr:visible').count(),0);
  assert.equal(await page.locator('img[src="x"]').count(),0);
  await page.close();
  const nojs=await browser.newPage({javaScriptEnabled:false});await nojs.goto(new URL('leaderboard.html',base).href);
  assert.equal(await nojs.locator('tbody tr').count(),data.models.length);await nojs.close();
  console.log('PASS: invalid query handling and readable static fallback');
 } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1});
