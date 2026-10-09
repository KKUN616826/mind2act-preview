/* Optional browser regression: NODE_PATH=/path/to/node_modules node scripts/test_hero_browser.cjs
 * Start scripts/preview.py first. Playwright/Chromium are QA dependencies only.
 */
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const { chromium } = require('playwright');
const data = require('../data/hero-demo.json');
const { stateAt } = require('./hero-demo-data.js');
const base = process.env.HERO_PREVIEW_URL || 'http://127.0.0.1:8765/';

async function open(browser, width, height, motion = 'reduce', fallback = false) {
  const page = await browser.newPage({ viewport: { width, height }, reducedMotion: motion });
  page.errors = [];
  page.on('pageerror', error => page.errors.push(error.message));
  // Inspect after the player's callback, rather than before it in a competing
  // callback queue (which would incorrectly report a one-frame delay).
  await page.addInitScript(() => {
    const native = HTMLVideoElement.prototype.requestVideoFrameCallback;
    if (!native) return;
    HTMLVideoElement.prototype.requestVideoFrameCallback = function(callback) {
      const video = this;
      return native.call(video, (now, metadata) => {
        callback(now, metadata);
        if (video.id === 'hero-demo-video' && window.heroFrameAudit) {
          window.heroFrameAudit.push({ time: metadata.mediaTime, completed: document.querySelectorAll('.demo-card[data-completed="true"]').length });
        }
      });
    };
  });
  // Other task videos are unrelated to this player and expensive to decode together.
  await page.route('**/media/videos/**', route => route.request().url().includes('CP05_hero_hard_1080p') ? route.continue() : route.abort());
  if (fallback) await page.addInitScript(() => {
    delete HTMLVideoElement.prototype.requestVideoFrameCallback;
    delete HTMLVideoElement.prototype.cancelVideoFrameCallback;
  });
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => {
    const video = document.querySelector('.demo-video');
    return video.readyState >= 2 && video.seekable.length && video.seekable.end(0) > 19 && !document.querySelector('.demo-play').disabled;
  });
  return page;
}

async function seek(page, time) {
  await page.evaluate(time => new Promise(resolve => {
    const video = document.querySelector('.demo-video');
    video.pause();
    video.addEventListener('seeked', resolve, { once: true });
    video.currentTime = time;
  }), time);
}

async function inspect(page, time) {
  const actual = await page.evaluate(() => ({
    captured: [...document.querySelectorAll('.demo-card')].filter(card => !card.hidden).length,
    completed: document.querySelectorAll('.demo-card[data-completed="true"]').length,
    active: [...document.querySelectorAll('.demo-card')].findIndex(card => card.dataset.active === 'true'),
    dots: [...document.querySelectorAll('.demo-event-dot')].filter(dot => dot.style.display !== 'none').length,
    complete: document.querySelector('.demo-hero').dataset.complete === 'true',
    phase: document.querySelector('.demo-hero').dataset.phase,
    overflow: document.documentElement.scrollWidth > innerWidth,
  }));
  const expected = stateAt(data, time);
  for (const key of ['captured', 'completed', 'active', 'complete']) assert.equal(actual[key], expected[key], key + ' at ' + time);
  assert.equal(actual.dots, expected.completed);
  assert.equal(actual.phase, expected.acting ? 'reproduce' : 'observe');
  assert.equal(actual.overflow, false);
}

(async () => {
  const options = { headless: true };
  if (process.env.CHROMIUM_EXECUTABLE) {
    options.executablePath = process.env.CHROMIUM_EXECUTABLE;
    options.args = ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'];
  }
  const browser = await chromium.launch(options);
  try {
    for (const [name, width, height] of [['desktop', 1440, 1000], ['tablet', 820, 1100], ['mobile', 390, 1100], ['narrow', 320, 900]]) {
      const page = await open(browser, width, height);
      assert.equal(await page.locator('.demo-video').evaluate(v => v.paused), true, 'Reduced motion disables autoplay');
      for (const time of [8, 12.08, 3, 18.8, 0, 7.5, 8.4]) {
        await seek(page, time); await inspect(page, time);
      }
      await seek(page, 12.08);
      const alignment = await page.evaluate(() => {
        const h = document.querySelector('.demo-hero').getBoundingClientRect();
        const s = document.querySelector('.demo-scene').getBoundingClientRect();
        const t = document.querySelector('.demo-connection-target');
        const x = h.left + Number(t.getAttribute('cx')), y = h.top + Number(t.getAttribute('cy'));
        const card = document.querySelector('.demo-card[data-active="true"]').getBoundingClientRect();
        const windowBox = document.querySelector('.demo-memory-window').getBoundingClientRect();
        return { targetInVideo: x >= s.left && x <= s.right && y >= s.top && y <= s.bottom,
          cardVisible: card.left >= windowBox.left - 1 && card.right <= windowBox.right + 1 };
      });
      assert.equal(alignment.targetInVideo, true); assert.equal(alignment.cardVisible, true);
      if (process.env.HERO_SCREENSHOTS) {
        fs.mkdirSync(process.env.HERO_SCREENSHOTS, { recursive: true });
        await page.screenshot({ path: path.join(process.env.HERO_SCREENSHOTS, name + '-act.png') });
        await seek(page, 3);
        await page.screenshot({ path: path.join(process.env.HERO_SCREENSHOTS, name + '-mind.png') });
      }
      assert.deepEqual(page.errors, []);
      await page.close();
      console.log('PASS: responsive layout, seeks and target mapping:', name);
    }
    const page = await open(browser, 1440, 1000);
    for (const event of data.events) {
      for (const time of [event.observe - 0.0001, event.observe + 0.0001, event.trigger - 0.0001, event.trigger + 0.0001, event.release - 0.0001, event.release + 0.0001]) {
        await seek(page, time); await inspect(page, time);
      }
    }
    await page.locator('.demo-hero').getByRole('button', { name: 'Mind', exact: true }).click(); await inspect(page, 0);
    await page.locator('.demo-hero').getByRole('button', { name: 'Act', exact: true }).click(); await inspect(page, 8);
    await page.locator('.demo-seek').focus(); await page.keyboard.press('End');
    await page.waitForFunction(() => document.querySelector('.demo-hero').dataset.complete === 'true');
    await page.keyboard.press('Home'); await inspect(page, 0);
    for (let i = 0; i < 2; i++) {
      await seek(page, data.media.duration - 0.1);
      await page.getByRole('button', { name: 'Play demo', exact: true }).click();
      await page.waitForFunction(() => document.querySelector('.demo-video').currentTime < 0.5 && document.querySelectorAll('.demo-card[data-completed="true"]').length === 0);
      assert.equal(await page.locator('.demo-card[data-completed="true"]').count(), 0);
      await page.getByRole('button', { name: 'Pause demo', exact: true }).click();
    }
    await seek(page, 8.9);
    await page.evaluate(() => { window.heroFrameAudit = []; });
    await page.getByRole('button', { name: 'Play demo', exact: true }).click();
    await page.waitForFunction(() => document.querySelector('.demo-video').currentTime > 9.3);
    await page.getByRole('button', { name: 'Pause demo', exact: true }).click();
    const frames = await page.evaluate(() => window.heroFrameAudit);
    const confirmed = frames.find(frame => frame.completed === 1);
    assert.ok(confirmed && confirmed.time >= data.events[0].trigger - 1e-6);
    assert.ok(confirmed.time - data.events[0].trigger <= 1 / 30 + 1e-6, JSON.stringify(frames));
    const pausedTime = await page.locator('.demo-video').evaluate(v => v.currentTime);
    await page.waitForTimeout(200);
    assert.equal(await page.locator('.demo-video').evaluate(v => v.currentTime), pausedTime);
    await page.getByRole('button', { name: 'Play demo', exact: true }).click();
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForFunction(() => document.querySelector('.demo-video').paused);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForFunction(() => !document.querySelector('.demo-video').paused);
    for (const hidden of [true, false]) {
      await page.evaluate(hidden => {
        Object.defineProperty(document, 'hidden', { configurable: true, value: hidden });
        document.dispatchEvent(new Event('visibilitychange'));
      }, hidden);
      await page.waitForFunction(hidden => document.querySelector('.demo-video').paused === hidden, hidden);
    }
    await page.getByRole('button', { name: 'Pause demo', exact: true }).click();
    await page.evaluate(() => { document.querySelector('.demo-video').dispatchEvent(new Event('error')); });
    assert.equal(await page.locator('.demo-play').isDisabled(), true);
    assert.equal(await page.locator('.demo-title').textContent(), 'Demo unavailable.');
    assert.deepEqual(page.errors, []);
    await page.close();
    console.log('PASS: all event boundaries, keyboard controls, loops, frame synchronization, pause/visibility and error handling');
    const fallback = await open(browser, 1280, 900, 'no-preference', true);
    await fallback.waitForFunction(() => document.querySelector('.demo-video').currentTime > 0.2);
    await seek(fallback, 16.5); await inspect(fallback, 16.5);
    assert.deepEqual(fallback.errors, []); await fallback.close();
    console.log('PASS: muted autoplay and requestAnimationFrame fallback');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
