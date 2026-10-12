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
  function presentationAt(data, time) {
    const t = Math.max(0, Math.min(data.presentation.duration, time));
    const segment = data.presentation.segments.find(s => t < s.end - 0.000001) || data.presentation.segments.at(-1);
    // Media seeks are quantized to microseconds; snap only edit boundaries.
    const elapsed = Math.max(0, t - segment.start);
    const legacy = segment.phase === 'focus' ? data.media.actStart - 0.000001 : segment.legacyStart + elapsed;
    const state = stateAt(data, legacy);
    const transition = data.presentation.transition;
    const sceneOpacity = Math.min(...transition.boundaries.map(boundary => {
      const distance = t - boundary;
      const progress = Math.min(1, Math.abs(distance) / (distance < 0 ? transition.fadeOut : transition.fadeIn));
      return progress * progress * (3 - 2 * progress);
    }));
    return { ...state, phase: segment.phase, presentationTime: t, localTime: elapsed,
      sceneOpacity,
      sourceTime: segment.sourceStart + elapsed * segment.speed,
      sourceSpeed: segment.speed,
      focusConfirmed: segment.phase === 'focus' && elapsed >= data.actDetail.trigger,
      focusReleased: segment.phase === 'focus' && elapsed >= data.actDetail.release };
  }
  const api = { stateAt, sourceTime, presentationAt };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.Mind2ActDemo = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
