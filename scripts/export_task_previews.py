#!/usr/bin/env python3
"""Export homepage-only previews; never overwrite task detail originals.

Requires ffmpeg / ffprobe with libx264 and libwebp. Run again to verify sources
and reuse matching exports; --force re-encodes them with the recorded recipe.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/task-previews.json'
RECIPE = {'version': 1, 'codec': 'libx264', 'preset': 'slow', 'crf': 22,
          'fallbackCrf': 20, 'threads': 2, 'keyframeInterval': 60,
          'pixelFormat': 'yuv420p', 'faststart': True, 'posterSeconds': 1,
          'posterQuality': 85, 'minimumSSIM': .98}

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout

def probe(path):
    data = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                          '-show_entries', 'stream=width,height,r_frame_rate,nb_frames:format=duration',
                          '-of', 'json', str(path)]))
    return {**data['streams'][0], 'duration': float(data['format']['duration'])}

def export(source, previous, force):
    src = ROOT / source
    source_hash = digest(src)
    if not force and previous and previous['sourceSha256'] == source_hash:
        if all((ROOT / previous[key]).is_file() and digest(ROOT / previous[key]) == previous[key + 'Sha256']
               for key in ('preview', 'poster')):
            print('Verified cached preview:', source, flush=True)
            return previous
    info = probe(src)
    assert (info['width'], info['height'], info['r_frame_rate']) == (640, 480, '30/1'), info
    task, filename = Path(source).parts[-2:]
    folder = ROOT / 'media/task-previews' / task
    folder.mkdir(parents=True, exist_ok=True)
    dst, poster = folder / filename, folder / Path(filename).with_suffix('.webp')
    score = 0
    crf = RECIPE['crf']
    for crf in (RECIPE['crf'], RECIPE['fallbackCrf']):
        run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-an', '-c:v', 'libx264',
             '-preset', RECIPE['preset'], '-crf', str(crf), '-threads', '2', '-g', '60',
             '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(dst)])
        measured = subprocess.run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', str(src),
             '-threads', '2', '-i', str(dst), '-lavfi', '[0:v][1:v]ssim',
             '-filter_complex_threads', '2', '-an', '-f', 'null', '-'],
             check=True, capture_output=True, text=True)
        score = float(re.findall(r'All:([0-9.]+)', measured.stderr)[-1])
        if score >= RECIPE['minimumSSIM']:
            break
    preview = dst if score >= RECIPE['minimumSSIM'] and dst.stat().st_size < src.stat().st_size else src
    if preview == src:
        dst.unlink()  # Discard only our unused encode, never the original.
    encoded = probe(preview)
    assert encoded == info, (source, info, encoded)
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(min(1, info['duration'] / 2)), '-i', str(src),
         '-frames:v', '1', '-c:v', 'libwebp', '-quality', '85', '-threads', '2', str(poster)])
    assert digest(src) == source_hash
    result = {'source': source, 'sourceSha256': source_hash,
              'preview': str(preview.relative_to(ROOT)), 'previewSha256': digest(preview),
              'poster': str(poster.relative_to(ROOT)), 'posterSha256': digest(poster),
              'sourceBytes': src.stat().st_size, 'previewBytes': preview.stat().st_size,
              'video': info, 'crf': crf if preview == dst else None,
              'ssim': score if preview == dst else 1.0,
              'candidateSSIM': score, 'usesOriginal': preview == src}
    print(f'{source}: {score:.6f} SSIM, {100 * result["previewBytes"] / result["sourceBytes"]:.1f}% original size', flush=True)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    # The homepage now shows only Medium; keep all 30 exports reproducible.
    cases = json.loads((ROOT / 'data/showcase-cases.json').read_text())
    sources = sorted(f'media/task-demos/{case["id"]}/{level}.mp4'
                     for case in cases for level in ('easy', 'medium'))
    assert len(sources) == 30
    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    previous = {x['source']: x for x in old.get('previews', [])} if old.get('recipe') == RECIPE else {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda src: export(src, previous.get(src), args.force), sources))
    payload = {'recipe': RECIPE, 'encoder': run(['ffmpeg', '-version']).splitlines()[0], 'previews': results}
    MANIFEST.write_text(json.dumps(payload, indent=2) + '\n')
    print(f'Exported {len(results)} homepage previews; originals retained.')

if __name__ == '__main__':
    main()
