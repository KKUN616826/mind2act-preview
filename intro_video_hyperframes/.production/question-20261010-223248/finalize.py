"""Promote the checked opening-question revision, preserving earlier deliveries."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone

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
assert read(BASE/'exported-visual-review.json')['passed']
for kind in ['master', 'web']:
    assert sha(previous[kind]) == previous['files'][kind]['sha256']
for file, digest in previous['source_hashes'].items():
    if file not in ['index.html', 'compositions/02-motivation.html']:
        assert sha(file) == digest, f'Unexpected composition change: {file}'
def audio_hash(file):
    data = subprocess.run([FF, '-v', 'error', '-i', file, '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', '-'], capture_output=True, check=True).stdout
    return hashlib.sha256(data).hexdigest()
aac = {kind: audio_hash(delivery[kind]) for kind in ['master', 'web']}
assert aac['master'] == aac['web']
delivery['local_preview'] = f'renders/preview-{stamp}.html'
old_stamp = previous['id'].removeprefix('mind2act-world-promo-')
Path(delivery['local_preview']).write_text(Path(previous['local_preview']).read_text().replace(old_stamp, stamp))
delivery['contact_sheet'] = f'renders/mind2act-world-contact-{stamp}.jpg'
shutil.copy2(BASE/'rendered/contact-sheet.jpg', delivery['contact_sheet'])
delivery['title_preview'] = f'renders/mind2act-world-question-{stamp}.jpg'
shutil.copy2(BASE/'rendered/frame-8-5.jpg', delivery['title_preview'])
delivery['checks'].update({
    'aac': str(audit_path.relative_to(ROOT)),
    'rendered_question_asr': str(speech_path.relative_to(ROOT)),
    'web_aac_identical': True,
    'aac_hashes': aac,
    'review': f'{REL}/QA.md',
    'exported_visual': f'{REL}/exported-visual-review.json',
    'unchanged_compositions_verified': True,
    'previous_delivery': f'renders/delivery-{old_stamp}.json',
})
delivery['source_hashes'] = {file: sha(file) for file in previous['source_hashes']}
delivery['verified_at'] = datetime.now(timezone.utc).isoformat()
delivery['revision'] = 'Opening title and matching voiceover/subtitles: Can reasoning and action work together? White first line, gold second line, existing motion retained.'
delivery['narrative'] = previous['narrative']
delivery['audio_verification'] = 'Final AAC question independently transcribed; waveform/loudness checks passed. Nine other voice cues are byte-identical to previous sources. No manual listening claim.'
payload = json.dumps(delivery, indent=2)+'\n'
for dest in [f'renders/delivery-{stamp}.json', 'renders/delivery.json', BASE/'delivery-final.json']:
    Path(dest).write_text(payload)
Path('renders/README.md').write_text(f'''# Mind2Act World promotional film

Latest: **74.1 seconds, 1920×1080, 30 fps, H.264/AAC**.

- Master: {delivery['master']}
- Web preview: {delivery['web']}
- Local player: {delivery['local_preview']}
- Title frame: {delivery['title_preview']}
- English subtitles: {', '.join(delivery['subtitles'])}
- Editable preview: {delivery['preview_url']}

Opening question: **Can reasoning and action work together?** The title keeps its white/gold two-line treatment and existing entrance motion; voiceover and subtitles match. Previous delivery and every other composition are retained unchanged.

Checks: complete HyperFrames composition gate; actual exported title frame review; full master/web decoding; final AAC comparison and independent question transcription. Audio {audit['loudness_lufs']:.2f} LUFS / {audit['true_peak_dbtp']:.2f} dBTP. No manual listening certification.

Production record: {REL}/. Historical deliveries remain in renders/.
''')
manifest = read(BASE/'manifest.json')
manifest.update(status='complete', delivery=delivery['master'], web=delivery['web'], verified_at=delivery['verified_at'], history_id='371a6abe')
(BASE/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({key: delivery[key] for key in ['master', 'web', 'local_preview', 'title_preview']}))
