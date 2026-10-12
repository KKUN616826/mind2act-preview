(() => {
  const frame = document.querySelector('.lunar-worlds-frame');
  if (!frame) return;
  let observer, scheduled;
  function fit() {
    const doc = frame.contentDocument, main = doc && doc.querySelector('main');
    if (!main) return;
    const desktop = innerWidth >= 1024;
    doc.documentElement.dataset.embeddedFit = String(desktop);
    doc.documentElement.style.overflowY = doc.body.style.overflowY = 'hidden';
    let height;
    if (desktop) {
      const header = document.querySelector('.header').getBoundingClientRect().height;
      height = Math.max(440, Math.floor((window.visualViewport?.height || innerHeight) - header - 32));
      doc.documentElement.style.setProperty('--lunar-panel-height', height + 'px');
    } else {
      doc.documentElement.style.removeProperty('--lunar-panel-height');
      const style = frame.contentWindow.getComputedStyle(main);
      height = Math.ceil(main.getBoundingClientRect().height + parseFloat(style.marginTop) + parseFloat(style.marginBottom) + 8);
    }
    if (frame.style.height !== height + 'px') frame.style.setProperty('height', height + 'px', 'important');
  }
  function schedule() { cancelAnimationFrame(scheduled); scheduled = requestAnimationFrame(fit); }
  function initialize() {
    observer?.disconnect();
    const main = frame.contentDocument?.querySelector('main');
    if (!main) return;
    observer = new ResizeObserver(schedule); observer.observe(main); fit();
  }
  frame.addEventListener('load', initialize);
  addEventListener('resize', schedule);
  window.visualViewport?.addEventListener('resize', schedule);
  if (frame.contentDocument?.readyState === 'complete') initialize();
})();
