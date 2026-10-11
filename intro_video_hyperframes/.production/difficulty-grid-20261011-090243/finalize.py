"""Promote the verified difficulty-grid delivery; preserve all previous exports."""
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
stem = Path(delivery['master']).stem
audit_path = BASE/'audio'/f'{stem}-aac-audit.json'
speech_path = BASE/'audio'/f'{stem}-actual-speech-audit.json'
audit, speech = read(audit_path), read(speech_path)
assert read(BASE/'check-final.json')['ok']
assert audit['passed'] and speech['pass']
assert len(speech['difficulty_cues']) == 4
assert read(BASE/'exported-visual-review.json')['passed']
for kind in ['master', 'web']:
    assert sha(previous[kind]) == previous['files'][kind]['sha256']
for file, digest in previous['source_hashes'].items():
    if file not in ['index.html', 'compositions/09-difficulty.html']:
        assert sha(file) == digest, f'Unexpected composition change: {file}'
def audio_hash(file):
    data = subprocess.run([FF, '-v', 'error', '-i', file, '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', '-'], capture_output=True, check=True).stdout
    return hashlib.sha256(data).hexdigest()
aac = {kind: audio_hash(delivery[kind]) for kind in ['master', 'web']}
assert aac['master'] == aac['web']
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
    'aac': str(audit_path.relative_to(ROOT)),
    'rendered_difficulty_asr': str(speech_path.relative_to(ROOT)),
    'web_aac_identical': True,
    'aac_hashes': aac,
    'review': f'{REL}/QA.md',
    'exported_visual': f'{REL}/exported-visual-review.json',
    'animation_review': f'{REL}/animation-review.json',
    'unchanged_compositions_verified': True,
    'previous_delivery': f'renders/delivery-{old_stamp}.json',
})
delivery['source_hashes'] = {file: sha(file) for file in previous['source_hashes']}
delivery['verified_at'] = datetime.now(timezone.utc).isoformat()
delivery['revision'] = 'Retained Easy/Medium/Hard hero sequence. Added Mind F navigation, Act PR3 reference paths, and Mind2Act CP02 4/6/6 reference cakes with real Hard cover action, in a stable 3-by-3 grid. One new narration sentence; 45 reveal and outro shifted by 0.9 seconds.'
delivery['narrative'] = 'Question and three distinct categories → representative Mind/Act/Mind2Act cases → bidirectional coordination and three-logo triangle → 15 real task videos in 3 categories → Easy/Medium/Hard → three tasks across three levels → 45 task-difficulty configurations → collective moonshot invitation.'
delivery['audio_verification'] = 'Actual exported AAC independently transcribed for Easy, Medium, Hard and the new difficulty sentence; waveform/loudness and speech-free interval checks passed. Ten prior voice cues byte-identical. No manual listening claim.'
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

Preserved the Easy/Medium/Hard hero sequence. The next page compares F, PR3 and CP02 at all three levels, with Rules & routes / Tighter turns / More pieces & steps. Cake reference images show 4/6/6 decorations; Hard switches to real cover placement. Added “More rules. Tighter turns. More to remember—and do.” Original 45 reveal follows, and the film is 0.9 seconds longer.

Checks: HyperFrames composition check; actual export frames at normal player size; transition and cover motion strips; full master/web decoding; identical AAC streams in master and web; independent transcription of all four difficulty cues. Audio {audit['loudness_lufs']:.2f} LUFS / {audit['true_peak_dbtp']:.2f} dBTP. No manual listening certification.

Production record: {REL}/. Historical exports remain in renders/.
''')
manifest = read(BASE/'manifest.json')
manifest.update(status='complete', delivery=delivery['master'], web=delivery['web'], verified_at=delivery['verified_at'], history_id='1a833163')
(BASE/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({key: delivery[key] for key in ['master', 'web', 'local_preview', 'difficulty_excerpt', 'difficulty_preview']}))
