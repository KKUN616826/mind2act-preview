"""Render the same public, three-view leaderboard on both entry points."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load():
    data = json.loads((ROOT / 'data/view-leaderboard.json').read_text())
    assert data['status'] == 'pending'
    assert [v['key'] for v in data['views']] == ['mind', 'act', 'coupling']
    assert len({m['id'] for m in data['models']}) == len(data['models'])
    for model in data['models']:
        assert model['paradigm'] in data['paradigms']
        assert set(model['results']) == {'mind', 'act', 'coupling'}
        assert all(r == {'score': None, 'success': None} for r in model['results'].values())
        for asset in ('icon', 'cases'):
            assert not model[asset] or (ROOT / model[asset]).is_file()
    for view in data['views']:
        assert len(view['tasks']) == 5 and (ROOT / view['icon']).is_file()
        assert all((ROOT / f'tasks/{task}.html').is_file() for task in view['tasks'])
    return data


def render():
    data = load()
    tabs = ''.join(f'<button type="button" role="tab" id="board-tab-{v["key"]}" data-board-view="{v["key"]}" aria-controls="board-panel" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}"><img src="{v["icon"]}" width="24" height="24" alt="">{v["label"]}</button>' for i, v in enumerate(data['views']))
    options = ''.join(f'<option value="{key}">{label}</option>' for key, label in data['paradigms'].items())
    rows = ''
    for model in data['models']:
        icon = f'<img src="{model["icon"]}" width="22" height="22" alt="">' if model['icon'] else '<span aria-hidden="true">' + escape(model['name'][:2]) + '</span>'
        cases = f'<a href="{model["cases"]}">View demos ↗</a>' if model['cases'] else '<span aria-label="Demonstrations not available">—</span>'
        rows += f'<tr data-model-id="{model["id"]}" data-paradigm="{model["paradigm"]}"><td>—</td><th scope="row"><span class="board-model"><span class="board-icon">{icon}</span>{escape(model["name"])}</span></th><td>{data["paradigms"][model["paradigm"]]}</td><td>—</td><td>—</td><td>{cases}</td></tr>'
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    return f'''<div class="view-leaderboard" data-view="mind">
<div class="board-heading"><h2>Leaderboard</h2><span class="board-status">Results pending</span></div>
<div class="board-tabs" role="tablist" aria-label="Evaluation view">{tabs}</div>
<div class="board-tools"><label>Paradigm<select id="board-paradigm">{ '<option value="all">All paradigms</option>' + options}</select></label><label>Search models<input id="model-search" type="search" placeholder="Search models" autocomplete="off"></label></div>
<section id="board-panel" role="tabpanel" aria-labelledby="board-tab-mind" tabindex="0">
<div class="board-summary"><h3 id="board-title">Mind</h3><p id="board-description">{data['views'][0]['description']}</p></div>
<p class="board-count" role="status" aria-live="polite">{len(data['models'])} candidates · All paradigms · Results pending</p>
<div class="board-table-scroll" role="region" aria-label="Leaderboard results; scroll horizontally on small screens" tabindex="0"><table><caption class="sr-only">Mind leaderboard · Results pending</caption><thead><tr><th scope="col">Rank</th><th scope="col">Model</th><th scope="col">Paradigm</th><th scope="col">Score <small>0–100</small></th><th scope="col">Success <small>%</small></th><th scope="col">Demos</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="board-empty" hidden>No matching models. Change the paradigm or search term.</p>
<p class="board-coverage"><span>5 tasks · Easy / Medium / Hard</span><span class="board-task-links">{''.join(f'<a href="tasks/{t}.html">{t}</a>' for t in data['views'][0]['tasks'])}</span></p>
<p class="board-note">Score measures task performance on a 0–100 scale; Success is the final task success rate. — = result not yet published; no ranks are assigned. Results will be reported separately for each evaluation view.</p>
<p class="board-note">Paradigms use different action interfaces and training conditions. Demo links show existing model-family examples, not evidence for leaderboard scores.</p>
</section><noscript><p>Enable JavaScript to switch views and filter candidates. All results are currently pending.</p></noscript>
<script type="application/json" id="viewLeaderboardData">{payload}</script></div>'''
