/* Same optional Playwright environment and preview URL as test_hero_browser.cjs. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({headless: true, ...(process.env.CHROMIUM_EXECUTABLE ? {executablePath: process.env.CHROMIUM_EXECUTABLE, args: ['--no-sandbox', '--disable-dev-shm-usage']} : {})});
  try {
    const page = await browser.newPage({reducedMotion: 'reduce'});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.route('**/*.mp4', route => route.abort());
    await page.goto(process.env.HERO_PREVIEW_URL || 'http://127.0.0.1:8765/', {waitUntil: 'domcontentloaded'});
    const frame = page.frameLocator('.lunar-worlds-frame');
    await frame.locator('.node').first().waitFor();
    const tableHeaders = await page.locator('#top-ten th').allTextContents();
    assert.ok(tableHeaders.includes('Generalization') && tableHeaders.includes('Memory'));
    for (const [width, height] of [[1440,900], [1920,1080], [1440,768], [1920,700], [820,1100], [390,900], [320,900], [1440,900]]) {
      await page.setViewportSize({width,height});
      await page.locator('.lunar-worlds-frame').scrollIntoViewIfNeeded();
      await page.waitForTimeout(150);
      const layout = await page.locator('.lunar-worlds-frame').evaluate(frame => {
        const doc = frame.contentDocument, svg = doc.querySelector('#scene');
        const main = doc.querySelector('main').getBoundingClientRect();
        const stage = doc.querySelector('.stage').getBoundingClientRect();
        const nodes = [...doc.querySelectorAll('.node')].map(n => n.getBoundingClientRect());
        return {height: frame.offsetHeight, expected: Math.max(440, Math.floor(innerHeight - document.querySelector('.header').offsetHeight - 32)), main: main.height,
          overflow: document.documentElement.scrollWidth > innerWidth, childOverflow: doc.documentElement.scrollWidth > frame.clientWidth,
          ratio: svg.getBoundingClientRect().width / svg.viewBox.baseVal.width / (svg.getBoundingClientRect().height / svg.viewBox.baseVal.height),
          nodesInStage: nodes.every(n => n.left >= stage.left && n.right <= stage.right && n.top >= stage.top && n.bottom <= stage.bottom),
          legendFits: doc.querySelector('.legend').getBoundingClientRect().bottom <= frame.offsetHeight,
          natural: doc.documentElement.dataset.embeddedFit === 'false'};
      });
      assert.equal(layout.overflow, false); assert.equal(layout.childOverflow, false);
      assert.equal(layout.legendFits, true);
      if (width >= 1024) {
        assert.ok(Math.abs(layout.height - layout.expected) <= 1, JSON.stringify(layout));
        assert.ok(Math.abs(layout.ratio - 1) < 0.001, 'Keep SVG icons undistorted');
        assert.equal(layout.nodesInStage, true);
      } else assert.equal(layout.natural, true);
      for (const [key, image, background] of [
        ['mind', 'mind-moon-upper.png', 'url(#day)'],
        ['act', 'act-moon-lower.png', 'url(#sky)'],
        ['coupling', 'lunar-ranking-moon.png', 'url(#daynight)'],
      ]) {
        await frame.locator(`button[data-world="${key}"]`).click();
        assert.equal(await frame.locator(`button[data-world="${key}"]`).getAttribute('aria-selected'), 'true');
        assert.equal(await frame.locator('#scene > image').getAttribute('href'), 'media/images/' + image);
        assert.equal(await frame.locator('#scene > rect').getAttribute('fill'), background);
        assert.equal(await frame.locator(`button[data-world="${key}"] img`).evaluate(img => img.complete && img.naturalWidth > 0), true);
        // The latest comprehensive table keeps all capability columns visible.
        assert.equal(await page.locator('#top-ten th.selected-dimension').count(), 0);
        assert.deepEqual(await page.locator('#top-ten th').allTextContents(), tableHeaders);
        await frame.locator('.node').first().focus();
        assert.match(await frame.locator('.tooltip').textContent(), /illustrative/);
        if (process.env.HERO_SCREENSHOTS && [390,1440,1920].includes(width)) {
          fs.mkdirSync(process.env.HERO_SCREENSHOTS, {recursive: true});
          await page.screenshot({path: path.join(process.env.HERO_SCREENSHOTS, `board-${width}-${height}-${key}.png`)});
        }
      }
      await frame.locator('button[data-world="mind"]').focus();
      await page.keyboard.press('ArrowRight');
      assert.equal(await frame.locator('button[data-world="act"]').getAttribute('aria-selected'), 'true');
      console.log('PASS: lunar sizing, logos, themes, model tooltips and table linkage:', width, height);
    }
    await page.locator('#model-search').fill('gpt');
    const visible = await page.locator('#top-ten tbody tr:visible').allTextContents();
    assert.ok(visible.length > 0 && visible.every(text => /gpt/i.test(text)));
    await page.locator('#model-search').fill('no such model');
    assert.equal(await page.locator('#top-ten tbody tr:visible').count(), 0);
    await page.locator('#model-search').fill('');
    assert.ok(await page.locator('#top-ten tbody tr:visible').count() > 1);
    assert.ok(await page.locator('#top-ten a[href^="rollouts/"]').count() > 0);
    assert.match(await page.locator('.leader-status').textContent(), /pending validation.*unreported result/);
    await page.locator('.full-leader-link a').click();
    await page.waitForURL('**/leaderboard.html');
    assert.ok(await page.locator('table tbody tr').count() > 0);
    assert.deepEqual(errors, []);
    console.log('PASS: model search, case links and full leaderboard');
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
