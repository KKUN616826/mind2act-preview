#!/usr/bin/env python3
"""Build the model site; reuse only the Bench visual template."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from content import COMMIT, MODULES, REPO, SOURCES, MODEL_NAME, MODEL_SUBTITLE
from presentation import ALIGNMENT, FIGURES, STATES

ROOT = Path(__file__).resolve().parents[1]

e = lambda value: html.escape(str(value), quote=True)
dump = lambda value: json.dumps(value, ensure_ascii=False, indent=2)
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
SOURCE_DATA = [dict(id=sid, title=title, path=path, line=line, description=description,
                    url=f'{REPO}/blob/{COMMIT}/{path}#L{line}') for sid, title, path, line, description in SOURCES]
SOURCE_BY_ID = {s['id']: s for s in SOURCE_DATA}

def module_html(m):
    pending = ' pending' if m['id'] in {'vla', 'experience'} else ''
    return f'<div><span class="state{pending}">{e(m["state"])}</span><h3>{e(m["name"])}</h3><p>{e(m["body"])}</p></div><div><dl><dt>INPUT</dt><dd>{e(m["inputs"])}</dd><dt>OUTPUT</dt><dd>{e(m["outputs"])}</dd></dl><p class="boundary">{e(m["boundary"])}</p><div class="small-links">' + ''.join(f'<a href="#source-{s}">{e(SOURCE_BY_ID[s]["title"])} ↗</a>' for s in m['sources']) + '</div></div>'

def state_html(w):
    return '<h3>' + e(w['title']) + '</h3><div class="state-columns">' + ''.join(f'<article><h4>{label}</h4><p>{e(w[key])}</p></article>' for key, label in [('cognitive', 'Cognitive'), ('reactive', 'Reactive'), ('runtime', 'Runtime')]) + '</div><p class="boundary">' + e(w['evidence']) + '</p>'

def figure_html(f):
    return f'<figure class="model-figure" id="figure-{f["id"]}"><a class="figure-open" href="{f["path"]}" data-figure="{f["id"]}" aria-label="放大：{e(f["title"])}" target="_blank"><img src="{f["path"]}" alt="{e(f["description"])}" width="1536" height="1024" loading="lazy"></a><figcaption><span>{e(f["description"])}</span><a href="{f["path"]}" download title="下载原图" aria-label="下载：{e(f["title"])}">↓</a></figcaption></figure>'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench-link", default="../index.html")
    args = parser.parse_args()
    bench_link = args.bench_link
    modules = [{k: v for k, v in m.items() if k != 'cases'} for m in MODULES]
    payload = dict(model=MODEL_NAME, subtitle=MODEL_SUBTITLE, implementation='EvoMemHarness / Cognitive–Reactive', commit=COMMIT, modules=modules, sources=SOURCE_DATA, states=STATES, alignment=ALIGNMENT, figures=FIGURES)
    (ROOT / 'data/model.json').write_text(dump(payload) + '\n')
    template = ROOT / 'scripts/base.css'
    css = template.read_text()
    safe_data = dump(payload).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    substitutions = {
        '__BENCH_CSS__': css, '__BENCH_LINK__': bench_link, '__MODEL_NAME__': MODEL_NAME, '__MODEL_SUBTITLE__': MODEL_SUBTITLE, '__REPO__': REPO, '__SHA__': COMMIT, '__SHORT_SHA__': COMMIT[:12], '__DATA__': safe_data,
        '__ARCHITECTURE_FIGURE__': figure_html(FIGURES[0]), '__EXPERIENCE_FIGURE__': figure_html(FIGURES[1]),
        '__INITIAL_MODULE__': module_html(modules[0]), '__INITIAL_STATE__': state_html(STATES['ongoing']),
        '__MODULE_BUTTONS__': ''.join(f'<button data-module="{m["id"]}" aria-pressed="{str(i == 0).lower()}">{e(m["name"])}</button>' for i, m in enumerate(modules)),
        '__ALIGNMENT__': ''.join('<tr>' + ''.join(f'<td>{e(cell)}</td>' for cell in row) + '</tr>' for row in ALIGNMENT),
        '__SOURCES__': '\n'.join(f'<article class="source-item" id="source-{s["id"]}"><a href="{e(s["url"])}" target="_blank" rel="noreferrer">{e(s["title"])} ↗</a><p>{e(s["description"])}</p><code>{e(s["path"])}:{s["line"]}</code></article>' for s in SOURCE_DATA),
    }
    page = (ROOT / 'scripts/model.html').read_text()
    for key, value in substitutions.items():
        page = page.replace(key, value)
    assert not re.search(r'__[A-Z_]+__', page)
    (ROOT / 'index.html').write_text(page)
    provenance = dict(repo=REPO, branch='evomemharness', commit=COMMIT, revision='mindaccord-v3', base_stylesheet_sha256=digest(template), stylesheet_reuse='Bundled stylesheet snapshot plus model overrides', image_generation='Architecture: editable SVG; lifecycle: original ImageGen; docs/Figure_Notes.md', figures=[f | dict(sha256=digest(ROOT / f['path'])) for f in FIGURES], claims='Architecture explanation; no Bench cases reproduced; no new robot evaluations.')
    (ROOT / 'data/provenance.json').write_text(dump(provenance) + '\n')
    md = [f'# {MODEL_NAME}', '', MODEL_SUBTITLE, '', f'实现基础：[EvoMemHarness]({REPO}/tree/{COMMIT})。', '', '当前原生路径为 Cognitive–Reactive + 固定控制器；VLA 接口已经定义，checkpoint 接入待完成。', '', '## 总体架构', '', '![双层 Agent 架构](../media/mindaccord-architecture.svg)', '', 'Cognitive 通过 Subgoal Contract 授权 Reactive；Reactive 经 Runtime 派发动作。Notes 与 Perceive 服务两个角色，但不持有物理执行权。环境观察和动作回执回到双方。', '', '## 模块职责', '']
    for m in modules:
        md += [f'### {m["name"]}', '', f'**状态：** {m["state"]}', '', m['body'], '', f'- 输入：{m["inputs"]}', f'- 输出：{m["outputs"]}', f'- 边界：{m["boundary"]}', '', '代码依据：' + '；'.join(f'[{SOURCE_BY_ID[s]["title"]}]({SOURCE_BY_ID[s]["url"]})' for s in m['sources']), '']
    md += ['## 执行反馈', '']
    for w in STATES.values():
        md += [f'### {w["title"]}', '', f'- Cognitive：{w["cognitive"]}', f'- Reactive：{w["reactive"]}', f'- Runtime：{w["runtime"]}', '', w['evidence'], '']
    md += ['## 双层经验', '', '![跨局经验生命周期](../media/experience-lifecycle-v2.png)', '', '局内 notes 按 Episode 隔离，正文由 Agent 主动读写。跨局经验从开发 Record 开始，每三条触发离线 Critic，形成认知或运动候选。只有验证通过后才能发布冻结快照供后续 Episode 使用。', '', '当前原生候选缺少 paired native replay / regression validator，暂不晋升；RGB 原生入口只接受空经验快照。SEM-Memory 效果后验与自动回滚属于后续设计。', '', '## 与 Bench 的能力对应', '', '| 维度 | 模块 | 能力 | 证据 |', '|---|---|---|---|']
    md += ['| ' + ' | '.join(row) + ' |' for row in ALIGNMENT]
    md += ['', f'[任务定义与演示见 MindActWorld]({"../" + bench_link})。迁移是附加协议，不是新增任务套件。', '', '## 来源', '']
    md += [f'- [{s["title"]}]({s["url"]})：{s["description"]}' for s in SOURCE_DATA]
    (ROOT / 'docs/PhysCo_Model_Architecture.md').write_text('\n'.join(md) + '\n')
    print(dump(dict(output=str(ROOT / 'index.html'), modules=len(modules), figures=2, case_cards=0)))

if __name__ == '__main__':
    main()
