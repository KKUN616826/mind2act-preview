/* Uses the same optional Playwright environment as test_hero_browser.cjs. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.CHROMIUM_EXECUTABLE ? {executablePath:process.env.CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']} : {})});
  try {
    const page = await browser.newPage({reducedMotion:'reduce'}), errors = [], requests = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('request', r => {if (/\/media\/task-(?:demos|previews)\/.*\.mp4/.test(r.url())) requests.push(r.url());});
    await page.route('**/*.mp4', r => r.abort());
    await page.goto(process.env.HERO_PREVIEW_URL || 'http://127.0.0.1:8765/', {waitUntil:'networkidle'});
    await page.evaluate(() => document.fonts.ready);
    assert.equal(requests.length, 0, 'No offscreen task video requests on initial load');
    assert.equal(await page.locator('#benchmark video[poster], #tasks video[poster]').count(), 30);
    for (const width of [320,390,820,1440,1920]) {
      await page.setViewportSize({width,height:900});
      const geometry = await page.evaluate(() => {
        const selectors=['.project-identity','.academic-project-meta','#introduction','.intro-overview','.version-status','#research-motivation','#research-overview','#top-ten'];
        return {overflow:document.documentElement.scrollWidth>innerWidth, items:selectors.map(s=>{const r=document.querySelector(s).getBoundingClientRect();return {s,x:r.x,width:r.width};}),
          font:getComputedStyle(document.querySelector('.paper-project')).fontFamily,
          brand:getComputedStyle(document.querySelector('.paper-project')).fontWeight,
          tagline:getComputedStyle(document.querySelector('.project-tagline')).fontWeight,
          status:getComputedStyle(document.querySelector('.version-status')).backgroundColor};
      });
      assert.equal(geometry.overflow,false,JSON.stringify(geometry));
      const expected=Math.min(1200,width-(width<=700?28:48));
      for (const item of geometry.items) {
        assert.ok(Math.abs(item.width-expected)<1, JSON.stringify({width,...item,expected}));
        assert.ok(Math.abs(item.x-(width-expected)/2)<1, JSON.stringify({width,...item}));
      }
      assert.match(geometry.font,/Space Grotesk/);assert.equal(geometry.brand,'700');assert.equal(geometry.tagline,'500');
      assert.equal(geometry.status,'rgb(232, 239, 234)');
      if(process.env.HERO_SCREENSHOTS) {
        fs.mkdirSync(process.env.HERO_SCREENSHOTS,{recursive:true});
        for(const [name,selector] of [['title','.project-identity'],['why','#research-motivation'],['status','.version-status']])
          await page.locator(selector).screenshot({path:path.join(process.env.HERO_SCREENSHOTS,`project-${name}-${width}.png`)});
      }
      console.log('PASS: aligned project layout and typography',width);
    }
    await page.locator('#benchmark').scrollIntoViewIfNeeded();
    await page.waitForTimeout(250);
    await page.locator('#tasks').scrollIntoViewIfNeeded();
    await page.waitForTimeout(250);
    assert.equal(requests.length,0,'Reduced motion retains posters without fetching previews');
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.waitForFunction(()=>[...document.querySelectorAll('#tasks source')].some(s=>s.hasAttribute('src')));
    await page.waitForTimeout(250);
    const fetched = new Set(requests);
    assert.ok(fetched.size>0 && fetched.size<30,`Only visible previews hydrate: ${fetched.size} unique requests`);
    await page.locator('.demo-motion-toggle').click();
    assert.ok(await page.locator('#tasks video').evaluateAll(videos=>videos.every(v=>v.paused)));
    assert.deepEqual(errors,[]);
    console.log('PASS: preview posters, deferred loading and reduced-motion controls');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
