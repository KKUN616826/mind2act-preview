(() => {
  const hero = document.querySelector('.demo-hero');
  const payload = document.getElementById('heroDemoData');
  if (!hero || !payload || !window.Mind2ActDemo) return;
  const data = JSON.parse(payload.textContent);
  const { stateAt, sourceTime } = window.Mind2ActDemo;
  const find = selector => hero.querySelector(selector);
  const video = find('video'), scene = find('.demo-scene');
  const seek = find('.demo-seek'), play = find('.demo-play');
  const chapters = [...hero.querySelectorAll('[data-demo-chapter]')];
  const cards = [...hero.querySelectorAll('.demo-card')];
  const viewport = find('.demo-memory-window'), strip = find('.demo-memory-strip');
  const focus = find('.demo-key-focus'), connection = find('.demo-connection');
  const motion = find('.demo-motion');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const samples = data.motion.samples;
  const plot = { left: 40, right: 346, top: [20, 93], height: 48 };
  const span = data.media.duration - data.media.actStart;
  const xAt = time => plot.left + (time - data.media.actStart) / span * (plot.right - plot.left);
  const yAt = (height, arm) => plot.top[arm] + plot.height * (1 - (height - data.motion.range[0]) / (data.motion.range[1] - data.motion.range[0]));
  const svg = (tag, attrs, text) => {
    const element = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.entries(attrs).forEach(([key, value]) => element.setAttribute(key, value));
    if (text !== undefined) element.textContent = text;
    return element;
  };
  const grid = find('.demo-chart-grid');
  for (let arm = 0; arm < 2; arm++) {
    for (const height of [data.motion.range[0], data.motion.range[1]]) {
      const y = yAt(height, arm);
      grid.append(svg('line', { x1: plot.left, x2: plot.right, y1: y, y2: y }));
      grid.append(svg('text', { x: 32, y: y + 3, 'text-anchor': 'end' }, String(height)));
    }
    grid.append(svg('text', { x: 4, y: plot.top[arm] + 27, class: 'demo-arm-label demo-arm-' + arm }, arm ? 'R' : 'L'));
    const path = samples.map((sample, index) => (index ? 'L' : 'M') + xAt(sample[0]).toFixed(2) + ',' + yAt(sample[arm + 1], arm).toFixed(2)).join(' ');
    find(arm ? '.demo-trace-right' : '.demo-trace-left').setAttribute('d', path);
  }
  for (const time of [data.media.actStart, data.media.actStart + span / 2, data.media.duration]) {
    grid.append(svg('text', { x: xAt(time), y: 157, 'text-anchor': time === data.media.actStart ? 'start' : time === data.media.duration ? 'end' : 'middle' }, sourceTime(data, time).toFixed(1)));
  }
  const eventDots = data.events.map(event => {
    const arm = event.arm === 'Left' ? 0 : 1;
    const dot = svg('circle', { cx: xAt(event.trigger), cy: yAt(event.triggerHeights[arm], arm), r: 3.4, class: 'demo-event-dot demo-arm-' + arm });
    dot.append(svg('title', {}, event.label + ' registered · ' + event.sourceTrigger.toFixed(2) + ' s'));
    find('.demo-chart-events').append(dot);
    return dot;
  });
  const reveal = find('#demo-motion-reveal rect'), cursor = find('.demo-chart-cursor');
  const heads = [...hero.querySelectorAll('.demo-chart-head')];
  let ready = false, failed = false, inView = true, wantsPlay = !reduced.matches;
  let frameId = null, lastSignature = '', geometry = null, lastTime = 0;
  const format = seconds => String(Math.floor(seconds / 60)).padStart(2, '0') + ':' + String(Math.floor(seconds % 60)).padStart(2, '0');

  function measure() {
    const box = scene.getBoundingClientRect(), root = hero.getBoundingClientRect();
    const sourceWidth = video.videoWidth || data.media.width, sourceHeight = video.videoHeight || data.media.height;
    const css = getComputedStyle(video);
    const scale = (css.objectFit === 'contain' ? Math.min : Math.max)(box.width / sourceWidth, box.height / sourceHeight);
    const position = css.objectPosition.split(' ').map(value => parseFloat(value) / 100);
    geometry = { scale, x: (box.width - sourceWidth * scale) * position[0], y: (box.height - sourceHeight * scale) * position[1],
      sceneX: box.left - root.left, sceneY: box.top - root.top };
    connection.setAttribute('viewBox', '0 0 ' + root.width + ' ' + root.height);
    focus.style.setProperty('--focus-size', Math.max(18, 70 * scale) + 'px');
  }

  function connect(state) {
    if (!geometry) return;
    const event = state.acting ? data.events[state.active] : data.events.find(item => state.time >= item.observe && state.time < item.observeEnd);
    focus.dataset.active = String(Boolean(event));
    connection.dataset.active = String(Boolean(state.acting && event));
    if (!event) return;
    const target = { x: geometry.x + event.target[0] * geometry.scale, y: geometry.y + event.target[1] * geometry.scale };
    focus.style.left = target.x + 'px'; focus.style.top = target.y + 'px';
    if (!state.acting) return;
    const root = hero.getBoundingClientRect(), card = cards[state.active].getBoundingClientRect(), windowBox = viewport.getBoundingClientRect();
    if (card.right <= windowBox.left || card.left >= windowBox.right) {
      connection.dataset.active = 'false'; return;
    }
    const x1 = Math.max(windowBox.left + 8, Math.min(card.left + card.width / 2, windowBox.right - 8)) - root.left;
    const y1 = card.top - root.top - 3, x2 = target.x + geometry.sceneX, y2 = target.y + geometry.sceneY;
    const bend = y1 - Math.max(24, (y1 - y2) * 0.45);
    find('.demo-connection-line').setAttribute('d', 'M' + x1 + ',' + y1 + ' C' + x1 + ',' + bend + ' ' + x2 + ',' + bend + ' ' + x2 + ',' + y2);
    const origin = find('.demo-connection-origin'), end = find('.demo-connection-target');
    origin.setAttribute('cx', x1); origin.setAttribute('cy', y1);
    end.setAttribute('cx', x2); end.setAttribute('cy', y2);
  }

  function heightsAt(time) {
    let low = 0, high = samples.length - 1;
    while (low < high) {
      const middle = Math.floor((low + high) / 2);
      if (samples[middle][0] < time) low = middle + 1; else high = middle;
    }
    const next = samples[low], previous = samples[Math.max(0, low - 1)];
    const weight = Math.max(0, Math.min(1, (time - previous[0]) / (next[0] - previous[0] || 1)));
    return [1, 2].map(arm => previous[arm] + weight * (next[arm] - previous[arm]));
  }

  function capture(state) {
    const ghost = find('.demo-capture');
    const index = state.captured - 1, event = data.events[index];
    const age = event ? (state.time - event.observe) / 0.32 : -1;
    ghost.hidden = reduced.matches || state.acting || age < 0 || age >= 1;
    if (ghost.hidden || !geometry) return;
    const root = hero.getBoundingClientRect();
    const card = cards[index].querySelector('img').getBoundingClientRect();
    const [cx, cy, cw, ch] = data.keyboard.snapshotCrop;
    const from = [geometry.sceneX + geometry.x + cx * geometry.scale, geometry.sceneY + geometry.y + cy * geometry.scale, cw * geometry.scale, ch * geometry.scale];
    const to = [card.left - root.left, card.top - root.top, card.width, card.height];
    const progress = age * age * (3 - 2 * age);
    if (ghost.getAttribute('src') !== event.snapshot) ghost.src = event.snapshot;
    ['left', 'top', 'width', 'height'].forEach((property, i) => ghost.style[property] = (from[i] + (to[i] - from[i]) * progress) + 'px');
    ghost.style.opacity = String(Math.min(1, (1 - age) * 8));
  }

  function updateChart(state) {
    const x = Math.max(plot.left, Math.min(plot.right, xAt(state.time)));
    reveal.setAttribute('width', x - plot.left);
    cursor.setAttribute('x1', x); cursor.setAttribute('x2', x);
    heightsAt(state.time).forEach((height, arm) => { heads[arm].setAttribute('cx', x); heads[arm].setAttribute('cy', yAt(height, arm)); });
    eventDots.forEach((dot, index) => dot.style.display = state.acting && data.events[index].trigger <= state.time ? '' : 'none');
  }

  function sync(time = video.currentTime, force = false) {
    if (failed) return;
    const state = stateAt(data, time);
    const signature = [state.acting, state.captured, state.completed, state.released].join(':');
    if (signature !== lastSignature || force) {
      lastSignature = signature;
      hero.dataset.phase = state.acting ? 'reproduce' : 'observe';
      hero.dataset.registered = String(state.registered);
      hero.dataset.complete = String(state.complete);
      motion.hidden = !state.acting;
      const active = data.events[state.active];
      find('.demo-stage').firstChild.textContent = state.acting ? 'ACT ' : 'MIND ';
      find('.demo-title').textContent = state.complete ? 'Sequence complete.' : state.acting ? 'From memory to movement.' : 'Remember the order.';
      find('.demo-count').textContent = (state.acting ? state.completed : state.captured) + ' / ' + data.events.length;
      find('.demo-step').textContent = state.acting ? state.complete ? 'Completed 12 / 12' : 'Step ' + (state.active + 1) + ' / 12 · ' + active.label : state.captured ? 'Remembered · ' + state.captured + ' / 12' : 'Watch · Remember';
      find('.demo-feedback').textContent = state.complete ? 'Every key confirmed' : state.registered ? '✓ Registered · release' : state.acting ? (active.arm === 'Left' ? 'L' : 'R') + ' · Next target' : state.captured ? 'Keep the order. Keep repeats.' : 'Watch a key light up.';
      find('.demo-memory-empty').hidden = state.captured > 0;
      cards.forEach((card, index) => {
        card.hidden = index >= state.captured;
        card.dataset.completed = String(index < state.completed);
        card.dataset.active = String(index === state.active);
        card.dataset.capturing = String(!state.acting && index === state.captured - 1);
        card.setAttribute('aria-current', index === state.active ? 'step' : 'false');
        card.querySelector('.demo-card-status').textContent = index < state.completed ? '✓' : index === state.active ? 'NEXT' : String(index + 1).padStart(2, '0');
        card.setAttribute('aria-label', 'Step ' + (index + 1) + ', ' + data.events[index].label + (index < state.completed ? ', confirmed' : index === state.active ? ', current target' : ''));
      });
      const selected = state.acting ? Math.min(state.released, cards.length - 1) : state.captured - 1;
      if (selected >= 0) {
        const card = cards[selected];
        viewport.scrollLeft = Math.max(0, card.offsetLeft - strip.offsetLeft - (viewport.clientWidth - card.offsetWidth) / 2);
      } else viewport.scrollLeft = 0;
      chapters.forEach(button => button.setAttribute('aria-current', String((button.dataset.demoChapter === 'reproduce') === state.acting)));
      find('.demo-phase-status').textContent = (state.acting ? 'Act' : 'Mind') + ' · ' + find('.demo-step').textContent + ' · ' + find('.demo-feedback').textContent;
      measure();
    }
    // Entry is media-timed too: pause, reverse seeks and loop resets stay exact.
    cards.forEach((card, index) => {
      const age = Math.max(0, Math.min(1, (state.time - data.events[index].observe) / 0.24));
      card.style.setProperty('--entry', reduced.matches ? 1 : age);
    });
    connect(state);
    capture(state);
    updateChart(state);
    seek.value = String(state.time);
    seek.style.setProperty('--played', (100 * state.time / data.media.duration) + '%');
    seek.setAttribute('aria-valuetext', format(state.time / video.playbackRate) + ' of ' + format(Math.ceil(data.media.duration / video.playbackRate)) + ', ' + (state.acting ? 'Act' : 'Mind'));
    find('.demo-speed').textContent = ((state.acting ? 4 : 3) * video.playbackRate).toFixed(2).replace(/\.?0+$/, '') + '× source speed';
    play.setAttribute('aria-label', video.paused ? 'Play demo' : 'Pause demo');
    play.setAttribute('aria-pressed', String(!video.paused));
    lastTime = state.time;
  }
  function cancelFrame() {
    if (frameId !== null) {
      if ('cancelVideoFrameCallback' in video) video.cancelVideoFrameCallback(frameId);
      else cancelAnimationFrame(frameId);
      frameId = null;
    }
  }
  function scheduleFrame() {
    if (frameId !== null || video.paused || video.ended) return;
    const tick = (_, metadata) => { frameId = null; sync(metadata ? metadata.mediaTime : video.currentTime); scheduleFrame(); };
    frameId = 'requestVideoFrameCallback' in video ? video.requestVideoFrameCallback(tick) : requestAnimationFrame(tick);
  }
  async function resume() {
    if (!ready || failed || !wantsPlay || !inView || document.hidden) return;
    try { await video.play(); } catch { wantsPlay = false; sync(); }
  }
  function initialize() {
    if (ready || failed) return;
    ready = true;
    video.defaultPlaybackRate = data.media.playbackRate;
    video.playbackRate = data.media.playbackRate;
    seek.max = String(Math.min(data.media.duration, video.duration));
    seek.disabled = play.disabled = false;
    chapters.forEach(button => button.disabled = false);
    sync(video.currentTime, true);
    resume();
  }
  play.addEventListener('click', () => { wantsPlay = video.paused; if (wantsPlay) resume(); else video.pause(); });
  seek.addEventListener('input', () => { video.currentTime = Number(seek.value); sync(video.currentTime, true); });
  chapters.forEach(button => button.addEventListener('click', () => {
    video.currentTime = button.dataset.demoChapter === 'observe' ? 0 : data.media.actStart;
    sync(video.currentTime, true);
  }));
  video.addEventListener('loadedmetadata', initialize);
  video.addEventListener('seeking', () => { cancelFrame(); sync(video.currentTime, true); });
  video.addEventListener('seeked', () => { sync(video.currentTime, true); scheduleFrame(); });
  video.addEventListener('play', () => { sync(); scheduleFrame(); });
  video.addEventListener('pause', () => { cancelFrame(); sync(); });
  video.addEventListener('timeupdate', () => { if (frameId === null || video.paused || video.currentTime < lastTime) sync(); });
  video.addEventListener('ratechange', () => sync());
  video.addEventListener('error', () => {
    failed = true; wantsPlay = false; cancelFrame();
    seek.disabled = play.disabled = true;
    chapters.forEach(button => button.disabled = true);
    find('.demo-title').textContent = 'Demo unavailable.';
    find('.demo-feedback').textContent = 'Open the full demonstration in Tasks below.';
    find('.demo-phase-status').textContent = 'Demo unavailable. Open the full demonstration in Tasks below.';
    connection.dataset.active = focus.dataset.active = 'false';
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); else resume(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting; if (!inView) video.pause(); else resume();
  }).observe(hero);
  reduced.addEventListener('change', () => { if (reduced.matches) { wantsPlay = false; video.pause(); } sync(); });
  viewport.addEventListener('scroll', () => connect(stateAt(data, lastTime)), { passive: true });
  if ('ResizeObserver' in window) new ResizeObserver(() => { measure(); sync(video.currentTime, true); }).observe(hero);
  else window.addEventListener('resize', () => { measure(); sync(video.currentTime, true); });
  if (video.readyState >= 1) initialize(); else { measure(); sync(0, true); }
})();
