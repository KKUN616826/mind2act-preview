const assert = require('node:assert/strict');
const test = require('node:test');
const data = require('../data/hero-demo.json');
const { stateAt, sourceTime } = require('./hero-demo-data.js');

test('initial frame and every demonstration boundary accumulate one independent memory', () => {
  assert.equal(stateAt(data, 0).captured, 0);
  data.events.forEach((event, i) => {
    assert.equal(stateAt(data, event.observe - 0.0001).captured, i);
    assert.equal(stateAt(data, event.observe).captured, i + 1);
    assert.equal(stateAt(data, event.observe).completed, 0);
  });
  assert.equal(data.events[0].keyId, data.events[7].keyId);
  assert.notEqual(data.events[0].snapshot, data.events[7].snapshot);
});

test('a trigger confirms only its card; next target waits for recorded release', () => {
  data.events.forEach((event, i) => {
    const before = stateAt(data, event.trigger - 0.0001);
    assert.equal(before.completed, i);
    assert.equal(before.active, i);
    const hit = stateAt(data, event.trigger);
    assert.equal(hit.completed, i + 1);
    assert.equal(hit.active, i);
    assert.equal(hit.registered, true);
    assert.equal(stateAt(data, event.release - 0.0001).active, i);
    assert.equal(stateAt(data, event.release).active, i === 11 ? -1 : i + 1);
  });
});

test('jump to Act restores all memory; reverse seeks and loop reset erase future effects', () => {
  const time = data.events[5].trigger;
  const reference = stateAt(data, time);
  for (const other of [19, 0, 18, 4, 12]) stateAt(data, other);
  assert.deepEqual(stateAt(data, time), reference);
  const act = stateAt(data, 8);
  assert.equal(act.captured, 12);
  assert.equal(act.completed, 0);
  assert.equal(act.active, 0);
  assert.equal(stateAt(data, data.media.duration).complete, true);
  assert.equal(stateAt(data, 0).complete, false);
  assert.equal(stateAt(data, 0).completed, 0);
});

test('different playback rates do not change source time or confirmation semantics', () => {
  assert.equal(sourceTime(data, 0), 36.5);
  assert.equal(sourceTime(data, 8), 60.5);
  for (const event of data.events) {
    assert.ok(Math.abs(sourceTime(data, event.trigger) - event.sourceTrigger) < 0.000003);
  }
});

const { presentationAt } = require('./hero-demo-data.js');
const [mind, focus, coupling] = data.presentation.segments;
test('isolated Act shows contact and release without consuming the full sequence', () => {
  for (const local of [0, 1, data.actDetail.trigger, data.actDetail.release, 4.49]) {
    const state = presentationAt(data, focus.start + local);
    assert.equal(state.phase, 'focus');
    assert.equal(state.completed, 0);
    assert.equal(state.active, -1);
    assert.equal(state.focusConfirmed, local >= data.actDetail.trigger);
    assert.equal(state.focusReleased, local >= data.actDetail.release);
  }
  const state = presentationAt(data, coupling.start);
  assert.equal(state.phase, 'reproduce');
  assert.equal(state.captured, 12);
  assert.equal(state.completed, 0);
  assert.equal(state.active, 0);
  assert.equal(state.sourceTime, 60.5);
});
test('all 12 trigger and release boundaries survive the new edit clock', () => {
  for (const [i, event] of data.events.entries()) {
    const trigger = coupling.start + event.trigger - 8;
    const release = coupling.start + event.release - 8;
    assert.equal(presentationAt(data, trigger - 0.0001).completed, i);
    assert.equal(presentationAt(data, trigger + 0.0001).completed, i + 1);
    assert.equal(presentationAt(data, release - 0.0001).active, i);
    assert.equal(presentationAt(data, release + 0.0001).active, i === 11 ? -1 : i + 1);
  }
});
test('seeks and loops reconstruct scene state, with microsecond edit-boundary precision', () => {
  for (const segment of data.presentation.segments) {
    const state = presentationAt(data, segment.start);
    presentationAt(data, data.presentation.duration);
    assert.deepEqual(presentationAt(data, segment.start), state);
    assert.equal(presentationAt(data, Math.floor(segment.start * 1e6) / 1e6).phase, segment.phase);
  }
  assert.equal(presentationAt(data, 0).completed, 0);
  assert.equal(presentationAt(data, data.presentation.duration).complete, true);
  assert.ok(Math.abs(data.presentation.duration / data.presentation.playbackRate - 25.289) < 0.001);
  assert.equal(focus.end - focus.start, 4.5);
});

test('the short dip hides the source-time jump without masking a contact event', () => {
  const boundary = coupling.start;
  for (const [offset, opacity] of [[-0.3, 1], [-0.2, 1], [-0.1, 0.5], [0, 0], [0.1, 0.5], [0.2, 1], [0.3, 1]]) {
    const state = presentationAt(data, boundary + offset);
    assert.ok(Math.abs(state.sceneOpacity - opacity) < 1e-9);
    assert.equal(state.completed, 0);
    if (offset < 0) assert.equal(state.focusReleased, true);
  }
  for (const time of [focus.start + data.actDetail.trigger, focus.start + data.actDetail.release,
    ...data.events.flatMap(event => [coupling.start + event.trigger - 8, coupling.start + event.release - 8])]) {
    assert.equal(presentationAt(data, time).sceneOpacity, 1, 'Contact and release stay fully visible');
  }
  const paused = presentationAt(data, boundary - 0.1);
  for (const time of [boundary, boundary + 0.1, 18, 0]) presentationAt(data, time);
  assert.deepEqual(presentationAt(data, boundary - 0.1), paused);
  assert.equal(presentationAt(data, 0).sceneOpacity, 1);
});
