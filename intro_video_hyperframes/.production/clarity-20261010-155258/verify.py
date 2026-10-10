from pathlib import Path
import hashlib, json, subprocess, re

run = Path(__file__).resolve().parent
root = run.parent.parent
ffprobe = '/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe'
provenance = json.loads((run / 'provenance.json').read_text())
hashes = {}
media = []
for item in provenance['records']:
    source = item['source']
    if source not in hashes:
        hashes[source] = hashlib.sha256((root / source).read_bytes()).hexdigest()
    assert hashes[source] == item['source_sha256'], source
    output = root / item['enhanced_path']
    info = json.loads(subprocess.check_output([ffprobe, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate,nb_frames,duration', '-of', 'json', str(output)]))['streams'][0]
    assert info['r_frame_rate'] == '30/1', output
    duration = item.get('output_duration', item.get('duration'))
    assert int(info['nb_frames']) == round(duration * 30), output
    media.append({'path': item['enhanced_path'], **info})
active = sorted(set(re.findall(r'assets/generated/clarity[^\s\"\x27<>]+\.mp4', '\n'.join(p.read_text() for p in (root / 'compositions').glob('*.html')))))
assert len(active) == 11, active
for path in active:
    assert (root / path).is_file(), path
report = {'created_at': '2026-10-10T15:52:58+08:00', 'source_hashes_match': True, 'original_sources_verified': len(hashes), 'restored_excerpts': len(media), 'active_restored_assets': active, 'media': media}
(run / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'media'}, indent=2))
