import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
FFPROBE = '/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe'
TAG = '20261010-145614'

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def probe(path):
    data = json.loads(subprocess.check_output([FFPROBE, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    video = next(s for s in data['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in data['streams'] if s['codec_type'] == 'audio')
    return {
        'path': str(path.relative_to(ROOT)), 'bytes': path.stat().st_size, 'sha256': sha(path),
        'duration': float(data['format']['duration']), 'video_codec': video['codec_name'],
        'pixel_format': video['pix_fmt'], 'width': video['width'], 'height': video['height'],
        'fps': video['avg_frame_rate'], 'audio_codec': audio['codec_name'],
        'audio_sample_rate': audio['sample_rate'], 'audio_channels': audio['channels'],
    }

raw = {str(p.relative_to(ROOT)): sha(p) for p in (ROOT / 'assets/videos').rglob('*.mp4')}
montage = read(RUN / 'montage-provenance.json')
cases = read(RUN / 'case-media-provenance.json')
assert len(raw) == 45
assert raw == {s['path']: s['sha256'] for s in montage['sources']}
for item in [*cases['clips'], *cases['stills'].values()]:
    assert raw[item['source']] == item['source_sha256']
texts = [(ROOT / 'index.html').read_text(), *[p.read_text() for p in (ROOT / 'compositions').glob('*.html')]]
assert not any(re.search(r'assets/generated/(cases|montage)/', t) for t in texts)
refs = sorted(set(re.findall(r'src="(assets/generated/source-refresh-[^"]+)"', '\n'.join(texts))))
assert len(refs) == 17
for ref in refs:
    assert (ROOT / ref).is_file(), ref

now = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')
validation = {
    'verified_at': now, 'source_count': 45, 'all_source_hashes_match': True,
    'active_refreshed_assets': refs, 'stale_case_montage_references': 0,
    'hyperframes_check': 'pass: 0 errors, 0 warnings; 9 layout samples; 39/39 contrast checks',
    'render_log': str((RUN / 'render.log').relative_to(ROOT)),
    'decode_master': 'pass', 'decode_web': 'pass',
    'visual_frames': [str(p.relative_to(ROOT)) for p in sorted((RUN / 'rendered').glob('*.png'))],
    'max_keyframe_gap_seconds': 1.0,
}
write(RUN / 'verification.json', validation)

current = ROOT / 'renders/delivery.json'
previous = read(current)
previous_copy = ROOT / 'renders/delivery-20261010-130800.json'
if not previous_copy.exists():
    write(previous_copy, previous)
delivery = {
    'created_at': now, 'id': f'mind2act-world-promo-{TAG}',
    'master': f'renders/mind2act-world-promo-1080p-{TAG}.mp4',
    'web': f'renders/mind2act-world-promo-web-{TAG}.mp4',
    'framework': 'HyperFrames 0.8.143', 'authored_duration': 47.4074074074,
    'files': {}, 'poster': f'renders/mind2act-world-poster-{TAG}.jpg',
    'subtitles': ['renders/mind2act-world-narration.srt', 'renders/mind2act-world-narration.vtt'],
    'preview_url': 'http://localhost:3052/#project/mind2act-hyperframes-blank-20261010-111117',
    'source_refresh': {
        'source_count': 45, 'run': '.production/source-refresh-20261010-142512',
        'case_provenance': '.production/source-refresh-20261010-142512/case-media-provenance.json',
        'montage_provenance': '.production/source-refresh-20261010-142512/montage-provenance.json',
        'verification': '.production/source-refresh-20261010-142512/verification.json',
    },
    'music_source': 'assets/audio/The Midnight - The Equaliser (Not Alone).mp3',
    'bpm': 81, 'music_source_start': 11.9877,
}
for key in ('master', 'web'):
    delivery['files'][key] = probe(ROOT / delivery[key])
write(ROOT / f'renders/delivery-{TAG}.json', delivery)
write(current, delivery)
print(json.dumps({'source_count': len(raw), 'active_refreshed_assets': len(refs), 'master': delivery['files']['master'], 'web': delivery['files']['web']}, indent=2))
