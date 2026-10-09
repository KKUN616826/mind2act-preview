(() => {
  const hero = document.querySelector('.demo-hero');
  if (!hero) return;
  const video = hero.querySelector('video');
  const seek = hero.querySelector('.demo-seek');
  const play = hero.querySelector('.demo-play');
  const title = hero.querySelector('.demo-title');
  const status = hero.querySelector('.demo-phase-status');
  const stage = hero.querySelector('.demo-stage');
  const chapters = [...hero.querySelectorAll('[data-demo-chapter]')];
  const focus = hero.querySelector('.demo-key-focus');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');

  // CP05 Hard, CP05-1080p.mp4 (1920×1080, 30 fps): source 36.5–60.5s at 3×, then 60.5–105.5s at 4×.
  // Times below refer to the exported approximately 19.25-second hero edit, not the full demo.
  const passage = { start: 0, reproduce: 8, end: 19.25 };
  const phases = {
    observe: { stage: 'MIND', title: 'Remember the key sequence.', status: 'Mind · Remember the key sequence.' },
    reproduce: { stage: 'ACT', title: 'Strike the keys precisely.', status: 'Act · Strike the keys precisely.' }
  };
  // Measured from visible blue display / green contact frames in this edit.
  // Coordinates refer to the original 1920×1080 image, before object-fit cropping.
  const keyCues = [{"s":0.1,"e":0.3667,"x":1318.1},{"s":0.7667,"e":1.0333,"x":989.9},{"s":1.4333,"e":1.7,"x":1251.0},{"s":2.1,"e":2.3667,"x":1052.0},{"s":2.7667,"e":3.0333,"x":927.7},{"s":3.4333,"e":3.7,"x":576.2},{"s":4.1,"e":4.3667,"x":500.2},{"s":4.7667,"e":5.0333,"x":1318.1},{"s":5.4333,"e":5.7,"x":576.0},{"s":6.1,"e":6.3667,"x":1383.9},{"s":6.7667,"e":7.0333,"x":531.3},{"s":7.4333,"e":7.7,"x":1401.6},{"s":9.0667,"e":9.1333,"x":1315.1},{"s":9.8,"e":9.8667,"x":989.4},{"s":10.5667,"e":10.6333,"x":1248.6},{"s":11.2667,"e":11.3667,"x":1050.4},{"s":12.0,"e":12.0667,"x":928.5},{"s":12.9,"e":12.9333,"x":579.9},{"s":14.3,"e":14.3667,"x":503.3},{"s":15.2333,"e":15.2667,"x":1314.4},{"s":16.4333,"e":16.5,"x":579.6},{"s":17.0667,"e":17.1333,"x":1380.5},{"s":17.7333,"e":17.7667,"x":534.7},{"s":18.3667,"e":18.4333,"x":1398.2}];
  let geometry = { scale: 1, x: 0, y: 0 };
  function layoutFocus() {
    const width = hero.clientWidth, height = hero.clientHeight;
    const sourceWidth = video.videoWidth || 1920, sourceHeight = video.videoHeight || 1080;
    const scale = Math.max(width / sourceWidth, height / sourceHeight);
    const position = getComputedStyle(video).objectPosition.split(' ').map(value => parseFloat(value) / 100);
    geometry = { scale, x: (width - sourceWidth * scale) * (position[0] || .5), y: (height - sourceHeight * scale) * (position[1] || .3) };
    hero.style.setProperty('--piano-x', `${geometry.x + 960 * scale}px`);
    hero.style.setProperty('--piano-y', `${geometry.y + 330 * scale}px`);
    hero.style.setProperty('--piano-rx', `${760 * scale}px`);
    hero.style.setProperty('--piano-ry', `${255 * scale}px`);
    focus.style.setProperty('--focus-size', `${104 * scale}px`);
    sync();
  }
  function highlightKey(time) {
    const cue = keyCues.find(cue => time >= cue.s && time < cue.e + .28);
    focus.dataset.active = String(Boolean(cue));
    if (!cue) return;
    const age = time - cue.s;
    const progress = Math.min(1, age / (cue.e - cue.s + .28));
    focus.style.left = `${geometry.x + cue.x * geometry.scale}px`;
    focus.style.top = `${geometry.y + 399 * geometry.scale}px`;
    focus.style.setProperty('--pulse-scale', reduced.matches ? '1' : String(.72 + progress * .9));
    focus.style.setProperty('--echo-scale', reduced.matches ? '1.2' : String(1 + progress * .95));
    focus.style.setProperty('--pulse-opacity', String(reduced.matches ? 1 : 1 - progress * .6));
  }
  let lastPhase = '';
  let ready = false;
  let wantsPlay = !reduced.matches;
  let inView = true;
  let framePending = false;

  const format = seconds => `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
  function sync() {
    const time = Math.min(passage.end, Math.max(passage.start, video.currentTime));
    const phase = time < passage.reproduce ? 'observe' : 'reproduce';
    if (phase !== lastPhase) {
      lastPhase = phase;
      hero.dataset.phase = phase;
      stage.textContent = phases[phase].stage;
      title.textContent = phases[phase].title;
      status.textContent = phases[phase].status;
      chapters.forEach(button => button.setAttribute('aria-current', String(button.dataset.demoChapter === phase)));
    }
    highlightKey(time);
    seek.value = String(time);
    seek.style.setProperty('--played', `${100 * (time - passage.start) / (passage.end - passage.start)}%`);
    seek.setAttribute('aria-valuetext', `${format(time - passage.start)} of ${format(Math.ceil(passage.end - passage.start))}, ${phases[phase].status}`);
    play.setAttribute('aria-label', video.paused ? 'Play demo' : 'Pause demo');
    play.setAttribute('aria-pressed', String(!video.paused));
  }
  async function resume() {
    if (!ready || !wantsPlay || !inView || document.hidden) return;
    try { await video.play(); } catch { wantsPlay = false; sync(); }
  }
  function tick() {
    framePending = false;
    sync();
    if (!video.paused && !video.ended) scheduleFrame();
  }
  function scheduleFrame() {
    if (framePending) return;
    framePending = true;
    if ('requestVideoFrameCallback' in video) video.requestVideoFrameCallback(tick);
    else requestAnimationFrame(tick);
  }
  function initialize() {
    if (ready) return;
    ready = true;
    layoutFocus();
    passage.end = Math.min(passage.end, video.duration);
    seek.min = String(passage.start);
    seek.max = String(passage.end);
    seek.disabled = false;
    play.disabled = false;
    chapters.forEach(button => { button.disabled = false; });
    video.currentTime = passage.start;
    sync();
    resume();
  }
  play.addEventListener('click', () => {
    wantsPlay = video.paused;
    if (wantsPlay) resume(); else video.pause();
  });
  seek.addEventListener('input', () => { video.currentTime = Number(seek.value); sync(); });
  chapters.forEach(button => button.addEventListener('click', () => {
    video.currentTime = button.dataset.demoChapter === 'observe' ? passage.start : passage.reproduce;
    sync();
  }));
  video.addEventListener('loadedmetadata', initialize);
  video.addEventListener('seeked', sync);
  video.addEventListener('play', () => { sync(); scheduleFrame(); });
  video.addEventListener('pause', sync);
  video.addEventListener('timeupdate', () => {
    sync();
  });
  video.addEventListener('error', () => {
    wantsPlay = false;
    status.textContent = 'Demo unavailable · Open the full demonstration below';
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) video.pause(); else resume();
  });
  if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting;
    if (!inView) video.pause(); else resume();
  }, { threshold: 0 }).observe(hero);
  reduced.addEventListener('change', () => {
    if (reduced.matches) { wantsPlay = false; video.pause(); }
  });
  if ('ResizeObserver' in window) new ResizeObserver(layoutFocus).observe(hero);
  else window.addEventListener('resize', layoutFocus);
  if (video.readyState >= 1) initialize();
  sync();
})();
