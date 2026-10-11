from pathlib import Path
import json, hashlib, subprocess, shutil
from datetime import datetime
from zoneinfo import ZoneInfo

run = Path(__file__).resolve().parent
root = run.parent.parent
ff = '/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
fp = '/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe'
delivery = root / 'renders/delivery.json'
shutil.copy2(delivery, root / 'renders/delivery-20261010-145614.json')
data = json.loads(delivery.read_text())
data['created_at'] = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
data['id'] = 'mind2act-world-promo-20261010-160400'
data['poster'] = 'renders/mind2act-world-poster-20261010-160400.jpg'
for role in ['master', 'web']:
    path = f'renders/mind2act-world-promo-{"1080p" if role == "master" else "web"}-20261010-160400.mp4'
    file = root / path
    subprocess.run([ff, '-nostdin', '-v', 'error', '-i', str(file), '-f', 'null', '-'], check=True)
    probe = json.loads(subprocess.check_output([fp, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(file)]))
    v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    a = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
    assert (v['width'], v['height'], v['r_frame_rate']) == (1920, 1080, '30/1')
    data[role] = path
    data['files'][role] = {'path': path, 'bytes': file.stat().st_size, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest(), 'duration': float(probe['format']['duration']), 'video_codec': v['codec_name'], 'pixel_format': v['pix_fmt'], 'width': v['width'], 'height': v['height'], 'fps': v['r_frame_rate'], 'audio_codec': a['codec_name'], 'audio_sample_rate': a['sample_rate'], 'audio_channels': a['channels']}
data['clarity_restoration'] = {'run': str(run.relative_to(root)), 'created_at': '2026-10-10T15:52:58+08:00', 'source_resolution': '640x480', 'provenance': str((run / 'provenance.json').relative_to(root)), 'verification': str((run / 'verification.json').relative_to(root)), 'master_crf': 16, 'web_crf': 18, 'original_sources_unchanged': True, 'scope': 'featured cases, six-tile intro, rapid montage; source stills and small 45-tile mosaic unchanged'}
delivery.write_text(json.dumps(data, indent=2) + '\n')
verification = json.loads((run / 'verification.json').read_text())
verification.update({'hyperframes_check': '0 errors, 0 warnings; 9 layout samples; 39/39 contrast checks', 'master_decode': 'pass', 'web_decode': 'pass', 'visual_samples': ['qa/rendered-mind.png', 'qa/rendered-act.png', 'qa/rendered-piano.png']})
(run / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
readme = root / 'renders/README.md'
text = readme.read_text().replace('20261010-145614', '20261010-160400').replace('refreshed-source delivery master', 'restored-source delivery master').replace('refreshed-source website-friendly', 'restored-source website-friendly')
text += '\n## Clarity restoration\n\nFeatured case footage, the six-tile intro and rapid montage now use conservative Real-ESRGAN restoration of the replacement 640x480 sources. Source files are unchanged. Order/target/piano-memory stills and the small 45-case mosaic retain their prior source derivatives. Master CRF 16 and web CRF 18 reduce additional compression. Restoration improves perceived detail but cannot recover true original HD pixels. Provenance, before/after images and verification are in `.production/clarity-20261010-155258/`. Earlier refreshed renders and their metadata remain available.\n'
readme.write_text(text)
print(json.dumps(data['files'], indent=2))
