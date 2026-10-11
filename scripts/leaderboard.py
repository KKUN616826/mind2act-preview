"""Render explicit unmeasured leaderboard placeholders; never import other scores."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
esc = lambda value: html.escape(str(value), quote=True)
METRICS = [('overall', '综合分'), ('cognitive', '任务级推理'), ('motor', '约束感知执行'), ('coupling', '推理—执行协同')]

def load(records):
    data = json.loads((ROOT/'data/leaderboard.json').read_text())
    assert data['status'] == 'placeholder'
    assert data['aggregation'] is None, 'Freeze and implement an aggregation protocol before scores'
    ids = {c['id'] for c in records}
    assert len({r['id'] for r in data['candidates']}) == len(data['candidates'])
    for row in data['candidates']:
        assert row['track'] in ('vla', 'coding')
        assert row['status'] == 'pending' and row['rank'] is None
        assert row['protocol_id'] is None and row['episodes'] is None
        assert set(row['scores']) == {m[0] for m in METRICS}
        assert all(v is None for v in row['scores'].values())
        assert set(row['tasks']) == ids and all(v is None for v in row['tasks'].values())
        assert all(v is None for v in row['costs'].values())
    return data

def missing():
    return '<td class="lb-missing"><span aria-label="尚未评测">—</span></td>'

def render(records):
    data = load(records)
    panels = []
    for track, title in [('vla', 'VLA / WAM'), ('coding', 'Coding Agent')]:
        rows = [r for r in data['candidates'] if r['track'] == track]
        # Alphabetical order for the borrowed roster conveys no ranking.
        if track == 'coding': rows.sort(key=lambda r:r['name'].casefold())
        overview, tasks, costs = [], [], []
        for row in rows:
            model = '<th scope="row">'+esc(row['name'])+'</th>'
            attrs = f'data-lb-row data-name="{esc(row["name"].lower())}"'
            state = '<td><span class="lb-pending">待评测</span></td>'
            config = '<td class="lb-config">'+esc(row['harness'] or 'Checkpoint 待固定')+'</td>'
            overview.append(f'<tr {attrs}>'+model+missing()+config+''.join(missing() for _ in METRICS)+state+'</tr>')
            tasks.append(f'<tr {attrs}>'+model+''.join(missing() for _ in records)+state+'</tr>')
            costs.append(f'<tr {attrs}>'+model+''.join(missing() for _ in range(4))+state+'</tr>')
        for view, label, heads, body in [
            ('overview','能力概览', ['模型', '名次', '参考 Harness' if track=='coding' else '版本 / 配置']+[m[1] for m in METRICS]+['状态'],overview),
            ('tasks','逐任务结果', ['模型']+[c['id'] for c in records]+['状态'],tasks),
            ('costs','运行与成本', ['模型','评测回合','端到端时延','任务运行时长','API 成本']+['状态'],costs),
        ]:
            headings = ''.join('<th scope="col">'+(f'<a href="#case-{h}">{h}</a>' if h in {c['id'] for c in records} else esc(h))+'</th>' for h in heads)
            panels.append(f'<div data-lb-panel data-track="{track}" data-view="{view}" class="lb-panel"><div class="table-wrap lb-scroll" role="region" aria-label="{title} · {label}" tabindex="0"><table><caption>{title} · {label} · 计划参评，暂无成绩</caption><thead><tr>'+headings+'</tr></thead><tbody>'+''.join(body)+'</tbody></table></div></div>')
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return (ROOT/'scripts/leaderboard.html').read_text().replace('__LB_PANELS__','\n'.join(panels)) + '\n<script id="leaderboardData" type="application/json">' + payload + '</script>'
