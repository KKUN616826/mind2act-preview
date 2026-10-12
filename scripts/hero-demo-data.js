/* Pure, source-timed state shared by the player and its regression tests. */
(function (root) {
  function stateAt(data, time) {
    const t = Math.max(0, Math.min(data.media.duration, time));
    const acting = t >= data.media.actStart;
    const captured = data.events.filter(event => event.observe <= t).length;
    const completed = acting ? data.events.filter(event => event.trigger <= t).length : 0;
    const released = acting ? data.events.filter(event => event.release <= t).length : 0;
    const active = acting && released < data.events.length ? released : -1;
    const event = active >= 0 ? data.events[active] : null;
    return { time: t, acting, captured, completed, released, active,
      registered: Boolean(event && t >= event.trigger),
      complete: acting && released === data.events.length };
  }
  function sourceTime(data, time) {
    const segment = data.media.segments.find(s => time < s.editEnd) || data.media.segments.at(-1);
    return segment.sourceStart + (time - segment.editStart) * segment.speed;
  }
  const api = { stateAt, sourceTime };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.Mind2ActDemo = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
