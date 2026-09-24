#!/usr/bin/env python3
"""Build the Astra–Jev proposal site; no model or robot execution."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from content import MODEL_NAME, MODEL_SUBTITLE, COMMIT, REPO, MODULES, SOURCES
from presentation import ALIGNMENT, FIGURES, STATES
ROOT = Path(__file__).resolve().parents[1]
e = lambda x: html.escape(str(x), quote=True)
dump = lambda x: json.dumps(x, ensure_ascii=False, indent=2)

def module_html(m):
    return f'<div><small>{e(m["state"])}</small><h3>{e(m["name"])}</h3><p>{e(m["body"])}</p></div><div><dl><dt>输入</dt><dd>{e(m["inputs"])}</dd><dt>输出</dt><dd>{e(m["outputs"])}</dd></dl><p class="note">{e(m["boundary"])}</p></div>'

def state_html(s):
    columns = ''.join(f'<article><h4>{label}</h4><p>{e(s[key])}</p></article>' for key,label in [('cognitive','Astra'),('reactive','Jev harness'),('runtime','Runtime')])
    return f'<h3>{e(s["title"])}</h3><div class="state-columns">{columns}</div><p class="note">{e(s["evidence"])}</p>'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bench-link',default='../index.html');args=ap.parse_args()
    examples={p.stem:json.loads(p.read_text()) for p in sorted((ROOT/'data/examples').glob('*.json'))}
    evidence_path = ROOT/'data/research/case7_development_evidence_20260924.json'
    development_evidence = dict(path=str(evidence_path.relative_to(ROOT)), sha256=hashlib.sha256(evidence_path.read_bytes()).hexdigest(), scope='Historical external Case7 seed034 development runs; not benchmark results or matched comparisons.')
    payload=dict(project="Mind2Act",benchmark="Mind2Act World",model=MODEL_NAME,subtitle=MODEL_SUBTITLE,status='proposal',proposal_version=2,updated_at='2026-09-24',baseline_commit=COMMIT,upstream=dict(name='GPT-6 Astra',api_model_id=None),downstream=dict(name='Jev',version=None),results=None,development_evidence=development_evidence,modules=MODULES,states=STATES,alignment=ALIGNMENT,figures=FIGURES,sources=SOURCES,examples=examples)
    (ROOT/'data/model.json').write_text(dump(payload)+'\n')
    data=dump(payload)
    for a,b in [('<','\\u003c'),('>','\\u003e'),('&','\\u0026'),('\u2028','\\u2028'),('\u2029','\\u2029')]:data=data.replace(a,b)
    replacements={'__CSS__':(ROOT/'scripts/proposal.css').read_text(),'__SUBTITLE__':MODEL_SUBTITLE,'__BENCH_LINK__':args.bench_link,'__DATA__':data,'__INITIAL_MODULE__':module_html(MODULES[0]),'__INITIAL_STATE__':state_html(STATES['ongoing']),'__INITIAL_SCHEMA__':e(dump(examples['subgoal-contract'])),'__MODULE_BUTTONS__':''.join(f'<button data-module="{m["id"]}" aria-pressed="{str(i==0).lower()}">{e(m["name"])}</button>' for i,m in enumerate(MODULES)),'__STATE_BUTTONS__':''.join(f'<button data-state="{key}" aria-pressed="{str(i==0).lower()}">{e(s["label"])}</button>' for i,(key,s) in enumerate(STATES.items())),'__SOURCES__':''.join(f'<article id="source-{s["id"]}"><a href="{e(s["url"])}" target="_blank" rel="noreferrer">{e(s["title"])}</a><p>{e(s["description"])}</p></article>' for s in SOURCES)}
    for f in FIGURES:
        assert (ROOT/f['path']).is_file()
        replacements['__FIGURE_'+f['id']+'__']=f'<figure class="model-figure" id="figure-{f["id"]}"><a href="{e(f["path"])}" data-figure="{f["id"]}" aria-label="放大：{e(f["title"])}"><img src="{e(f["path"])}" width="1480" height="760" loading="lazy" alt="{e(f["description"])}"></a><figcaption>{e(f["description"])}</figcaption></figure>'
    page=(ROOT/'scripts/proposal.html').read_text()
    for key,value in replacements.items():page=page.replace(key,value)
    assert not re.search(r'__[A-Z_a-z]+__',page)
    (ROOT/'index.html').write_text(page)
    # Retain the historical download path while making the current proposal canonical.
    (ROOT/'docs/PhysCo_Model_Architecture.md').write_text((ROOT/'docs/MindAccord_Proposal_v2.md').read_text())
    provenance=dict(revision='mindaccord-astrajev-proposal-v2-20260924',status='proposal',baseline=dict(repo=REPO,commit=COMMIT,scope='prior implementation reference; external Case7 prototype documented separately'),figures=[f|dict(sha256=hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()) for f in FIGURES],results=None,development_evidence=development_evidence,scope='Documentation update using historical external prototype logs; no new model inference or robot experiments. Benchmark results and comparative benefits remain unmeasured.')
    (ROOT/'data/provenance.json').write_text(dump(provenance)+'\n')
    print('Built Mind2Act Harness proposal:',len(MODULES),'modules,',len(FIGURES),'figures; historical development evidence linked, benchmark results remain empty.')
if __name__=='__main__':main()
