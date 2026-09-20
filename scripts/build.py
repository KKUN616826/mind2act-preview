#!/usr/bin/env python3
"""Build the static site and task documents from public, versioned content."""
import json
import re
from pathlib import Path
from render_cases import card, featured, case_md, duration

ROOT = Path(__file__).resolve().parents[1]

def main():
    records = json.loads((ROOT / 'data/showcase-cases.json').read_text())
    assert len(records) == len({c['id'] for c in records}) == 15
    videos = sum(a['kind'] == 'video' for c in records for a in c['media'])
    images = sum(a['kind'] == 'image' for c in records for a in c['media'])
    for c in records:
        for a in c['media']:
            assert (ROOT / a['path']).is_file(), a['path']
            if a.get('poster'):
                assert (ROOT / a['poster']).is_file(), a['poster']
        (ROOT / 'docs/cases' / (c['id'] + '.md')).write_text(case_md(c, '../../'))
    intro = (ROOT / 'docs/PhysCo_Showcase.md').read_text()
    (ROOT / 'docs/PhysCo_Cases.md').write_text(intro + '\n\n---\n\n' + '\n\n---\n\n'.join(case_md(c, '../') for c in records))
    media = ['# PhysCo 演示素材索引', '', f'{videos} 段视频、{images} 张场景图。', '']
    for c in records:
        media += ['## ' + c['id'] + ' · ' + c['title'], '']
        for a in c['media']:
            media.append(f'- [{a["label"]}](../{a["path"]})')
        media += ['']
    (ROOT / 'docs/PhysCo_Media.md').write_text('\n'.join(media))
    payload = json.dumps(records, ensure_ascii=False, separators=(',', ':'))
    for char, escape in [('<', '\\u003c'), ('>', '\\u003e'), ('&', '\\u0026'), ('\u2028', '\\u2028'), ('\u2029', '\\u2029')]:
        payload = payload.replace(char, escape)
    page = (ROOT / 'scripts/showcase.html').read_text()
    for key, value in {'FEATURED': featured(records), 'CASES': '\n'.join(card(c) for c in records), 'PUBLIC_DATA': payload, 'VIDEO_COUNT': str(videos), 'IMAGE_COUNT': str(images)}.items():
        page = page.replace('__' + key + '__', value)
    assert not re.search(r'__[A-Z_]+__', page)
    (ROOT / 'index.html').write_text(page)
    print(f'Built {len(records)} cases, {videos} videos, {images} images.')

if __name__ == '__main__':
    main()
