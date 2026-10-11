from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

ROOT = Path.cwd()
BASE = Path(__file__).resolve().parent
REL = str(BASE.relative_to(ROOT))
FF = '/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
read = lambda p: json.loads(Path(p).read_text())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
delivery = read(BASE/'delivery-candidate.json')
previous = read(BASE/'before/renders/delivery.json')
stamp = delivery['id'].removeprefix('mind2act-world-promo-')
assert read(BASE/'check-final.json')['ok']
assert read(BASE/'exported-visual-review.json')['passed']
assert read(BASE/'audio-preservation.json')['passed']
for kind in ['master', 'web']:
    assert sha(previous[kind]) == previous['files'][kind]['sha256']
for file, digest in previous['source_hashes'].items():
    if file != 'compositions/09-difficulty.html':
        assert sha(file) == digest, f'Unexpected composition change: {file}'
def audio_hash(file):
    data = subprocess.run([FF, '-v', 'error', '-i', file, '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', '-'], capture_output=True, check=True).stdout
    return hashlib.sha256(data).hexdigest()
aac = {kind: audio_hash(delivery[kind]) for kind in ['master', 'web']}
aac['previous'] = audio_hash(previous['master'])
assert len(set(aac.values())) == 1
old_stamp = previous['id'].removeprefix('mind2act-world-promo-')
delivery['local_preview'] = f'renders/preview-{stamp}.html'
Path(delivery['local_preview']).write_text(Path(previous['local_preview']).read_text().replace(old_stamp, stamp))
delivery['contact_sheet'] = f'renders/mind2act-world-contact-{stamp}.jpg'
shutil.copy2(BASE/'rendered/contact-sheet.jpg', delivery['contact_sheet'])
delivery['difficulty_preview'] = f'renders/mind2act-world-difficulty-{stamp}.jpg'
shutil.copy2(BASE/'rendered/frame-60-4.jpg', delivery['difficulty_preview'])
delivery['difficulty_excerpt'] = f'renders/mind2act-world-difficulty-review-{stamp}.mp4'
subprocess.run([FF, '-v', 'error', '-ss', '53.333333', '-i', delivery['web'], '-t', '12.752', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-threads', '6', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-n', delivery['difficulty_excerpt']], check=True)
delivery['checks'].update({
    'audio_preservation': f'{REL}/audio-preservation.json',
    'web_and_previous_aac_identical': True,
    'aac_hashes': aac,
    'review': f'{REL}/QA.md',
    'exported_visual': f'{REL}/exported-visual-review.json',
    'animation_review': f'{REL}/animation-review.json',
    'unchanged_compositions_verified': True,
    'previous_delivery': f'renders/delivery-{old_stamp}.json',
})
delivery['source_hashes'] = {file: sha(file) for file in previous['source_hashes']}
delivery['verified_at'] = datetime.now(timezone.utc).isoformat()
delivery['revision'] = 'Restore the full 640-pixel width of the original CP02 main camera in all hero and comparison views, including cover footage. Extract only the top 640x334 main view; no horizontal crop. Preserve native aspect with contain fitting. Layout, motion, timing, soundtrack and other scenes unchanged.'
delivery['narrative'] = previous['narrative'].replace('→ Easy/Medium/Hard →', '→ CP02 Easy/Medium/Hard →')
delivery['audio_verification'] = 'New master and compact MP4 AAC packet streams are byte-identical to the previously verified 110436 master. Prior full narration, Hard, loudness, ASR and VAD evidence applies without a new listening claim.'
payload = json.dumps(delivery, indent=2)+'\n'
for dest in [f'renders/delivery-{stamp}.json', 'renders/delivery.json', BASE/'delivery-final.json']:
    Path(dest).write_text(payload)
Path('renders/README.md').write_text(f'''# Mind2Act World promotional film

Latest: **75 seconds, 1920×1080, 30 fps, H.264/AAC**.

- Master: {delivery['master']}
- Web preview: {delivery['web']}
- Local player: {delivery['local_preview']}
- Difficulty excerpt: {delivery['difficulty_excerpt']}
- Difficulty frame: {delivery['difficulty_preview']}
- English subtitles: {', '.join(delivery['subtitles'])}
- Editable preview: {delivery['preview_url']}

The difficulty hero now uses CP02: Easy 4 pieces, Medium 6 pieces, Hard 6 pieces + cover. Remember. Recreate. introduces the task. The existing Easy/Medium/Hard typography and narration remain, with unchanged timing. All CP02 images and cover footage retain the original main-camera width, including its left edge and tray. Only the separate bottom wrist-camera panel is excluded. Native640x334 aspect is preserved with contain fitting. The hero picture contracts into the bottom-right comparison cell.

Checks: HyperFrames runtime/layout/contrast; independent actual export frame and motion-strip review; full master/web decoding; identical AAC streams in prior and current masters and web export. Historical exports remain in renders/. Production record: {REL}/.
''')
manifest = read(BASE/'manifest.json')
manifest.update(status='complete', delivery=delivery['master'], web=delivery['web'], verified_at=delivery['verified_at'], history_id='67d19058')
(BASE/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({key: delivery[key] for key in ['master', 'web', 'local_preview', 'difficulty_excerpt', 'difficulty_preview']}))
