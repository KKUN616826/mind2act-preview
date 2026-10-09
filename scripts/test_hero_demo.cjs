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
