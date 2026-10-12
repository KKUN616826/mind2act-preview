"""Reproducible three-scene edit and controller evidence for the isolated Act view."""
import json
import subprocess
from pathlib import Path


def export_presentation(run, output, data, trajectory, clock, digest):
    import numpy as np

    # Exact output-frame boundaries; the original hero and evidence clock stay intact.
    fps = 30
    segments = [
        dict(phase='observe', start=0, end=97 / fps, sourceStart=42.4, sourceEnd=52.1, speed=3, legacyStart=(42.4 - 36.5) / 3),
        dict(phase='focus', start=97 / fps, end=232 / fps, sourceStart=62.5, sourceEnd=67.0, speed=1),
        dict(phase='reproduce', start=232 / fps, end=569 / fps, sourceStart=60.5, sourceEnd=105.433333, speed=4, legacyStart=8),
    ]
    crop = [0, 0, 1920, 1080]
    path = 'media/videos/CP05_hero_fullframe_act.mp4'
    video = output / path
    video.parent.mkdir(parents=True, exist_ok=True)
    filters = (
        '[0:v]split=3[m][a][c];'
        '[m]trim=start=42.4:end=52.1,setpts=(PTS-STARTPTS)/3,fps=30,trim=end_frame=97,setsar=1[mind];'
        '[a]trim=start=62.5:end=67,setpts=PTS-STARTPTS,fps=30,trim=end_frame=135,setsar=1[act];'
        '[c]trim=start=60.5:end=105.433333,setpts=(PTS-STARTPTS)/4,fps=30,trim=end_frame=337,setsar=1[coupling];'
        '[mind][act][coupling]concat=n=3:v=1:a=0[out]'
    )
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(run / 'CP05-Hard-1080p.mp4'),
                    '-filter_complex_threads', '1', '-filter_complex', filters, '-map', '[out]', '-an',
                    '-c:v', 'libx264', '-threads', '2', '-preset', 'medium', '-crf', '21',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-map_metadata', '-1', str(video)], check=True)
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(video)]))
    assert int(probe['streams'][0]['nb_frames']) == 569
    data['presentation'] = dict(path=path, sha256=digest(video), duration=569 / fps, fps=fps,
                                width=1920, height=1080, playbackRate=0.75, segments=segments,
                                transition=dict(boundary=segments[2]['start'], fadeOut=0.2, fadeIn=0.2))

    steps = clock['source_step']
    times = clock['world_time'] - data['clock']['worldTimeOrigin']
    feedback = json.loads((run / 'replay/feedback82.json').read_text())
    tool_rows = [row for row in trajectory if 'tools' in row]
    tool_steps = np.array([row['step'] for row in tool_rows])
    tool_z = np.array([row['tools']['Right']['tip'][2] * 100 for row in tool_rows])
    samples = []
    for row in feedback:
        if row['side'] != 'Right':
            continue
        at = int(np.searchsorted(steps, row['step']))
        assert steps[at] == row['step']
        time = float(times[at])
        if 62.5 - 1e-5 <= time <= 67.0 + 1e-5:
            # runtime.before logs the target for this tick; collection.sample records
            # its command and post-step observation. measured_tip in feedback82 is
            # PRE-step and must not be substituted for the video's observed state.
            samples.append([round(time - 62.5, 6), round(row['target'][2] * 100, 4),
                            round(float(np.interp(row['step'], tool_steps, tool_z)), 4)] +
                           np.degrees(clock['action'][at, 8:14]).round(3).tolist() +
                           np.degrees(clock['joint_position_after'][at, 8:14].astype(float)).round(3).tolist())
    assert len(samples) == 541
    hit = data['events'][0]
    data['actDetail'] = dict(
        arm='Right', keyId=hit['keyId'], label=hit['label'], sourceStart=62.5, sourceEnd=67.0,
        crop=crop, outputRectangle=crop,
        target=hit['target'], highlightRegion=[1000, 60, 920, 780],
        trigger=round(hit['sourceTrigger'] - 62.5, 6), release=round(hit['sourceRelease'] - 62.5, 6),
        reference='GT target · controller reference', actual='Recorded post-step simulation state',
        alignment='Target issued before tick k; actual joints sampled after tick k. Tool height interpolated from recorded 30 Hz poses; no time shift.',
        sampleHz=120, measuredTipHz=30, heightUnit='cm', jointUnit='deg',
        columns=['time', 'targetHeight', 'actualHeight'] + [f'targetJ{i}' for i in range(1, 7)] + [f'actualJ{i}' for i in range(1, 7)],
        samples=samples,
    )
    data['provenance']['files']['feedback82.json'] = digest(run / 'replay/feedback82.json')
    data['version'] = 3
