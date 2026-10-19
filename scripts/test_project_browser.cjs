/* Same optional Playwright environment as test_hero_browser.cjs. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.CHROMIUM_EXECUTABLE ? {executablePath:process.env.CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']} : {})});
  const url=process.env.HERO_PREVIEW_URL || 'http://127.0.0.1:8765/';
  try {
    const page=await browser.newPage({reducedMotion:'reduce'}),errors=[],requests=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('request',r=>{if(/\/media\/task-(?:demos|previews)\/.*\.mp4/.test(r.url()))requests.push(r.url());});
    await page.route('**/*.mp4',r=>r.abort());
    await page.goto(url,{waitUntil:'networkidle'});
    await page.evaluate(()=>document.fonts.ready);
    assert.equal(requests.length,0,'No offscreen task video requests');
    assert.equal(await page.locator('#tasks video[poster]').count(),15);
    assert.equal(await page.locator('.community-badge').count(),3);
    assert.equal(await page.locator('.community-badge a,.community-badge button').count(),0,'No fake invitation links');
    assert.ok(await page.locator('.community-badge img,.project-institution img').evaluateAll(imgs=>imgs.every(i=>i.complete&&i.naturalWidth>0)));
    assert.deepEqual(await page.locator('.project-author').allTextContents(),['Yuzhi Huang1*§','Junchao Lin1*','Jiazhen Huang1*','Ziyi Xiong1*','Yuankun Lü1*']);
    assert.match(await page.locator('.project-contributions').textContent(),/Co-first Authors.*Project Lead/);
    assert.equal(await page.locator('#introduction>p').count(),3);
    assert.equal(await page.locator('#introduction').evaluate(e=>e.children[2].classList.contains('intro-overview')),true);
    assert.ok(await page.locator('a[href="benchmark.html"]').count()>0);
    for(const width of [320,390,820,1440,1920]) {
      await page.setViewportSize({width,height:1000});
      const g=await page.evaluate(()=>{
        const selectors=['.project-institution','.project-identity','.academic-project-meta','#introduction','.intro-overview','.version-status','#research-motivation','#research-overview','#top-ten'];
        const rects=selectors.map(s=>{const r=document.querySelector(s).getBoundingClientRect();return {s,x:r.x,width:r.width};});
        const body=getComputedStyle(document.querySelector('#introduction>p'));
        return {overflow:document.documentElement.scrollWidth>innerWidth,rects,title:getComputedStyle(document.querySelector('.paper-project')).fontFamily,body:body.fontFamily,size:parseFloat(body.fontSize),loaded:document.fonts.check('21px "Source Serif 4"'),clipped:[...document.querySelectorAll('.project-author,.project-resources>a,.community-badge')].some(e=>{const r=e.getBoundingClientRect();return r.left<0||r.right>innerWidth;})};
      });
      assert.equal(g.overflow,false,JSON.stringify(g));assert.equal(g.clipped,false);
      const expected=Math.min(920,width-(width<=700?32:48));
      for(const item of g.rects){assert.ok(Math.abs(item.width-expected)<1,JSON.stringify({viewport:width,...item,expected}));assert.ok(Math.abs(item.x-(width-expected)/2)<1,JSON.stringify(item));}
      assert.match(g.title,/Sora/);assert.match(g.body,/Source Serif 4/);assert.equal(g.size,width<=700?18:21);assert.equal(g.loaded,true);
      if(process.env.HERO_SCREENSHOTS){
        fs.mkdirSync(process.env.HERO_SCREENSHOTS,{recursive:true});
        for(const [name,selector] of [['title','.project-identity'],['authors','.academic-project-meta'],['intro','#introduction']])await page.locator(selector).screenshot({path:path.join(process.env.HERO_SCREENSHOTS,`academic-${name}-${width}.png`)});
      }
      console.log('PASS: formal cover, author markers, typography and alignment',width);
    }
    // Use the current share destination; collaborators may update the preview URL.
    const shareURL = new URL(await page.locator('a[aria-label="Share on X"]').getAttribute('href')).searchParams.get('url');
    // Test both clipboard success and its existing manual-copy fallback.
    await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.__copied=text}}));
    await page.locator('#copy-project-link').click();
    assert.equal(await page.evaluate(()=>window.__copied),shareURL);
    assert.equal(await page.locator('#copy-feedback').textContent(),'Link copied');
    await page.evaluate(()=>navigator.clipboard.writeText=async()=>{throw Error('Clipboard unavailable');});
    await page.setViewportSize({width:320,height:900});
    await page.locator('#copy-project-link').click();
    assert.match(await page.locator('#copy-feedback').textContent(),/https:\/\//);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
    await page.locator('.project-resources>a').first().focus();
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').getAttribute('href'),'leaderboard.html');
    await page.locator('#tasks').scrollIntoViewIfNeeded();await page.waitForTimeout(200);
    assert.equal(requests.length,0,'Reduced motion keeps posters without fetching videos');
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.waitForFunction(()=>[...document.querySelectorAll('#tasks source')].some(s=>s.hasAttribute('src')));
    await page.waitForTimeout(200);assert.ok(new Set(requests).size>0 && new Set(requests).size<15);
    await page.locator('.demo-motion-toggle').click();assert.ok(await page.locator('#tasks video').evaluateAll(v=>v.every(x=>x.paused)));
    assert.deepEqual(errors,[]);
    const fallback=await browser.newPage({viewport:{width:390,height:900},reducedMotion:'reduce'});
    await fallback.route(/\.(woff2?|ttf)(\?|$)/,r=>r.abort());await fallback.route('**/*.mp4',r=>r.abort());
    await fallback.goto(url,{waitUntil:'networkidle'});
    assert.equal(await fallback.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
    assert.ok(await fallback.locator('.project-title,#project-title').isVisible());
    assert.ok(await fallback.locator('#introduction>p').first().isVisible());
    await fallback.close();console.log('PASS: share, keyboard access, preview loading and font fallback');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
