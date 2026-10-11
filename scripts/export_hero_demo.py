#!/usr/bin/env python3
"""Export the CP05 hero from one recorded run; never run the simulator.

Requires numpy, h5py, Pillow and ffmpeg. The site build only needs the exported
JSON/images, not these dependencies or access to the private recording.
"""
import argparse
from bisect import bisect_left
import hashlib
import io
import json
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN = Path('/root/share/physco/campaigns/CP05-hard-hd-replay-20261009')
SEGMENTS = [
    dict(editStart=0, editEnd=8, sourceStart=36.5, sourceEnd=60.5, speed=3),
    dict(editStart=8, editEnd=19.233333, sourceStart=60.5, sourceEnd=105.433332, speed=4),
]
CROP = (430, 180, 1050, 390)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def edit_time(source):
    segment = SEGMENTS[0] if source < 60.5 else SEGMENTS[1]
    return round(segment['editStart'] + (source - segment['sourceStart']) / segment['speed'], 6)


def main():
    import h5py
    import numpy as np
    from PIL import Image

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, default=DEFAULT_RUN)
    parser.add_argument('--output', type=Path, default=ROOT)
    args = parser.parse_args()
    run, output = args.run, args.output
    replay = run / 'replay'
    read = lambda name: json.loads((replay / name).read_text())
    trajectory, control, result = read('trajectory.json'), read('control_trace.json'), read('integrated_result.json')
    plan = json.loads((run / 'plan.json').read_text())
    clock = np.load(replay / 'collection/control.npz')
    steps, stamps = clock['source_step'], clock['world_time']
    assert np.all(np.diff(steps) == 1)
    assert np.allclose(np.diff(stamps), 1 / 120, atol=1e-6, rtol=0)
    assert [row['step'] for row in trajectory] == steps.tolist()
    with h5py.File(replay / 'collection/native_rgb/rgb.h5', 'r') as frames:
        frame_stamps, frame_steps = frames['world_time_s'][:], frames['physics_step'][:]
    assert np.all(np.diff(frame_steps) == 4)
    assert np.allclose(np.diff(frame_stamps), 1 / 30, atol=1e-6, rtol=0)
    assert abs(float(frame_stamps[0]) - float(stamps[0])) < 1e-6
    origin = float(frame_stamps[0])
    source_time = lambda step: float(stamps[int(step - steps[0])]) - origin
    tool_rows = [row for row in trajectory if 'tools' in row]
    tool_steps = [row['step'] for row in tool_rows]
    assert all(b - a == 4 for a, b in zip(tool_steps, tool_steps[1:]))
    def trigger_heights(step):
        # Events are logged at 120 Hz; tool poses at 30 Hz. Interpolate only the
        # marker's plotted height, never its confirmation timestamp.
        at = bisect_left(tool_steps, step)
        before, after = tool_rows[max(0, at - 1)], tool_rows[at]
        weight = (step - before['step']) / (after['step'] - before['step']) if after['step'] != before['step'] else 0
        return [round((before['tools'][side]['tip'][2] * (1 - weight) + after['tools'][side]['tip'][2] * weight) * 100, 4) for side in ('Left', 'Right')]
    observe_step = next(row['step'] for row in trajectory if row['phase'] == 'observe')
    sequence = plan['spec']['levels']['hard']['sequence']
    hits = [event for event in result['key_events'] if event['phase'] == 'replay']
    assert len(sequence) == 12 and [hit['key'] for hit in hits] == sequence
    assert result['replay_contact_success'] and all(len(hit['tip_contacts']) == 1 for hit in hits)
    image_dir = output / 'media/images/hero-memory'
    image_dir.mkdir(parents=True, exist_ok=True)
    events = []
    for index, hit in enumerate(hits):
        key = hit['key']
        demo_step = observe_step + index * 240
        # Take a real frame inside this event's blue illumination, including repeats.
        shot_time = source_time(demo_step) + 0.32
        png = subprocess.check_output([
            'ffmpeg', '-v', 'error', '-ss', f'{shot_time:.8f}', '-i',
            str(run / 'CP05-Hard-1080p.mp4'), '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-',
        ])
        image = Image.open(io.BytesIO(png)).convert('RGB')
        # The keyboard ROI excludes the blue background/other scene objects.
        pixels = np.asarray(image)[350:426, 460:1450].astype(float)
        mask = (pixels[:, :, 2] > 1.4 * pixels[:, :, 0]) & (pixels[:, :, 2] > 1.2 * pixels[:, :, 1]) & (pixels[:, :, 2] > 70)
        ys, xs = np.nonzero(mask)
        assert len(xs) > 30, f'No demonstrated blue key at {shot_time}'
        target = [round(float(np.median(xs)) + 460, 2), 399]
        asset = f'media/images/hero-memory/step-{index + 1:02d}.webp'
        x, y, width, height = CROP
        image.crop((x, y, x + width, y + height)).resize((420, 156), Image.Resampling.LANCZOS).save(output / asset, quality=88, method=6)
        release_row = next(row for row in control if row['step'] > hit['step'] and row['phase'] == 'replay' and row['key_depths'][str(key)] < 0.002)
        events.append(dict(
            step=index + 1, keyId=key, label=f'K{key + 1:02d}', arm=hit['tip_contacts'][0],
            observe=edit_time(source_time(demo_step)), observeEnd=edit_time(source_time(demo_step + 90)),
            trigger=edit_time(source_time(hit['step'])), release=edit_time(source_time(release_row['step'])),
            observeStep=demo_step, triggerStep=hit['step'], releaseStep=release_row['step'],
            sourceObserve=round(source_time(demo_step), 6), sourceTrigger=round(source_time(hit['step']), 6),
            sourceRelease=round(source_time(release_row['step']), 6), snapshot=asset,
            snapshotSourceTime=round(shot_time, 6), target=target,
            triggerHeights=trigger_heights(hit['step']),
        ))
    # Keep every recorded 30 Hz tool-pose sample, without synthetic resampling.
    samples = []
    for row in tool_rows:
        t = source_time(row['step'])
        if 60.5 - 1 / 30 <= t <= SEGMENTS[-1]['sourceEnd'] + 1 / 30:
            samples.append([round(8 + (t - 60.5) / 4, 6)] + [round(row['tools'][side]['tip'][2] * 100, 4) for side in ('Left', 'Right')])
    heights = [value for sample in samples for value in sample[1:]]
    required = ['trajectory.json', 'control_trace.json', 'integrated_result.json', 'collection/control.npz', 'collection/metadata.json', 'collection/recording_report.json']
    data = dict(
        version=1,
        provenance=dict(run=run.name, publicEpisode='CP05/hard/episode_0002',
                        recording='Simulation demonstration', memory='Illustrative memory overlay',
                        motion='Recorded simulation state; tip position computed from actual tool pose.',
                        acceptedExpertEpisode=False, fullWorkflowClaim=False,
                        sourceVideoSha256=digest(run / 'CP05-Hard-1080p.mp4'),
                        files={name: digest(replay / name) for name in required}),
        media=dict(path='media/videos/CP05_hero_hard_1080p.mp4', duration=19.233333, actStart=8,
                   width=1920, height=1080, fps=30, playbackRate=0.75, segments=SEGMENTS,
                   sha256=digest(ROOT / 'media/videos/CP05_hero_hard_1080p.mp4')),
        clock=dict(physicsHz=120, videoHz=30, sourceStepOrigin=int(steps[0]),
                   worldTimeOrigin=origin, nativeFrameCount=len(frame_stamps),
                   nativeClockVerified=True, releaseSamplePeriodSeconds=10 / 120),
        keyboard=dict(labelConvention='K01–K29: white keys left to right; not musical pitches.',
                      whiteKeyCount=29, snapshotCrop=list(CROP)),
        events=events,
        motion=dict(title='Stick-tip height', unit='cm', referenceFrame='simulation world',
                    columns=['editTime', 'Left', 'Right'], sampleHz=30, triggerHeightInterpolation='linear between recorded tool poses',
                    range=[math.floor(min(heights)), math.ceil(max(heights))], samples=samples),
    )
    (output / 'data').mkdir(parents=True, exist_ok=True)
    (output / 'data/hero-demo.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'Exported {len(events)} event screenshots and {len(samples)} real motion samples.')


if __name__ == '__main__':
    main()
