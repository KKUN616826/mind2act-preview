#!/usr/bin/env python3
"""Build the static site and task documents from public, versioned content."""
import json
import re
from pathlib import Path
from render_cases import card, case_md, cover, e
from leaderboard import render as render_leaderboard

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
    page = page.replace('__RESEARCH_INTRO__', (ROOT / 'scripts/research_intro.html').read_text())
    page = page.replace('__RESEARCH_CSS__', (ROOT / 'scripts/research.css').read_text())
    page = page.replace('__LEADERBOARD__', render_leaderboard(records))
    page = page.replace('__LEADERBOARD_JS__', (ROOT / 'scripts/leaderboard.js').read_text())
    by_id = {c['id']: c for c in records}
    for cid in ['P', 'PR3', 'CP02']:
        c = by_id[cid]
        a = next(a for a in c['media'] if a['kind'] == 'video' and ('Medium' in a['label'] or cid == 'P'))
        demo = f'<figure class="article-demo"><video controls preload="none" playsinline poster="{e(a["poster"])}" aria-label="观点演示 {cid}"><source src="{e(a["path"])}" type="video/mp4"></video><figcaption><b>{cid} · {e(c["title"])} · {e(a["label"])}</b><span>任务运控演示；不代表模型评测结果。</span><a href="#case-{cid}">任务定义与全部档位 →</a></figcaption></figure>'
        page = page.replace('__POINT_DEMO_' + cid + '__', demo)
    highlights = [('CP01', '历史订单 → 动态取料', '实际入盘才更新剩余需求'), ('CP02', '局部位置 → 运动目标', '落位与停稳决定后续操作'), ('CP04', '空间计划 → 真实占用', '场景图；完整执行视频待补')]
    previews = {'CP01': 'media/posters/CP01__research_overview.jpg'}
    media = ''.join(f'<a href="#case-{cid}"><figure><img src="{e(previews.get(cid) or cover(by_id[cid]))}" alt="{e(by_id[cid]["title"])}" loading="eager"><figcaption><b>{cid} · {e(title)}</b><span>{e(note)}</span></figcaption></figure></a>' for cid, title, note in highlights)
    for key, value in {'INSIGHT_MEDIA': media, 'CASES': '\n'.join(card(c) for c in records), 'PUBLIC_DATA': payload, 'VIDEO_COUNT': str(videos), 'IMAGE_COUNT': str(images)}.items():
        page = page.replace('__' + key + '__', value)
    assert not re.search(r'__[A-Z_]+__', page)
    (ROOT / 'index.html').write_text(page)
    print(f'Built {len(records)} cases, {videos} videos, {images} images.')

if __name__ == '__main__':
    main()
