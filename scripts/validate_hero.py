"""Validate exported evidence, assets and the assembled hero, without private logs."""
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate_hero(content=None):
    data = json.loads((ROOT / 'data/hero-demo.json').read_text())
    if content is None:
        content = (ROOT / 'index.html').read_text()
    embedded = re.search(r'<script id="heroDemoData" type="application/json">(.*?)</script>', content, re.S)
    assert embedded and json.loads(embedded[1]) == data, 'Hero HTML differs from exported evidence'
    events = data['events']
    assert len(events) == 12 and [event['step'] for event in events] == list(range(1, 13))
    assert [event['keyId'] for event in events] == [25, 15, 23, 17, 13, 2, 0, 25, 2, 27, 1, 28]
    assert len({event['snapshot'] for event in events}) == 12, 'Repeated keys need independent screenshots'
    assert len(re.findall(r'class="demo-card"', content)) == 12
    for i, event in enumerate(events):
        assert event['label'] == f'K{event["keyId"] + 1:02d}'
        assert (ROOT / event['snapshot']).is_file()
        assert event['snapshot'] in content
        assert 0 <= event['observe'] < event['observeEnd'] < data['media']['actStart']
        assert data['media']['actStart'] < event['trigger'] < event['release'] < data['media']['duration']
        assert event['arm'] in ('Left', 'Right')
        assert event['triggerStep'] < event['releaseStep']
        assert 0 < event['target'][0] < 1920 and 0 < event['target'][1] < 1080
        assert abs(event['trigger'] - (8 + (event['sourceTrigger'] - 60.5) / 4)) < 1e-6
        if i:
            assert events[i - 1]['observeEnd'] < event['observe']
            assert events[i - 1]['release'] < event['trigger']
    motion = data['motion']
    assert motion['sampleHz'] == 30 and motion['unit'] == 'cm' and motion['referenceFrame'] == 'simulation world'
    assert data['clock']['physicsHz'] == 120 and data['clock']['nativeClockVerified'] is True
    assert data['clock']['releaseSamplePeriodSeconds'] == 10 / 120
    assert data['provenance']['acceptedExpertEpisode'] is False
    assert data['provenance']['fullWorkflowClaim'] is False
    samples = motion['samples']
    assert samples[0][0] <= 8 and samples[-1][0] >= data['media']['duration']
    for index, sample in enumerate(samples):
        assert len(sample) == 3 and all(math.isfinite(value) for value in sample)
        assert all(motion['range'][0] <= height <= motion['range'][1] for height in sample[1:])
        if index:
            assert abs(sample[0] - samples[index - 1][0] - 1 / 120) < 2e-6
    with (ROOT / data['media']['path']).open('rb') as video:
        assert hashlib.file_digest(video, 'sha256').hexdigest() == data['media']['sha256']
    assert 'Simulation demonstration' in content and 'Illustrative memory overlay' in content
    assert 'Source time · s' in content and 'World height · cm' in content
    print('PASS: 12 independent screenshots, recorded 30 Hz heights, 120 Hz triggers, release ordering and embedded hero data')


if __name__ == '__main__':
    validate_hero()
