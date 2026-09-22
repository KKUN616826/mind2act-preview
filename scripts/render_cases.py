#!/usr/bin/env python3
"""Build a curated public project site; internal research records are never serialized."""
import html,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SUITES={'cognitive':('任务级推理','Task-Level Reasoning'),'motor':('约束感知执行','Constraint-Aware Execution'),'coupling':('自适应协同','Adaptive Coordination')}
FEATURED={'CP02':'Hard','CP05':'Medium','PR3':'Hard'}
e=lambda x:html.escape(str(x),quote=True)
def ul(values):return '<ul>'+''.join('<li>'+e(v)+'</li>' for v in values)+'</ul>'
def label(n,text):return '<div class="detail-label"><small>'+n+'</small><h4>'+e(text)+'</h4></div>'
def evidence(c):
    names={'high':'高层目标证据','low':'低层物理证据','feedback':'闭环验收与边界'}
    return '<div class="protocol">'+''.join('<div><h4>'+title+'</h4><p>'+e(c['evidence'][key])+'</p></div>' for key,title in names.items())+'</div>'
def cover(c):
    items=c['media']
    if not items:return None
    for a in items:
        if FEATURED.get(c['id']) and FEATURED[c['id']] in a['label']:return a.get('poster',a['path'])
    return items[0].get('poster',items[0]['path'])
def cover_html(c):
    path=cover(c)
    if not path:return '<div class="no-cover"><b>'+e(c['id'])+'</b><span>任务定义 · 可视化素材待补充</span></div>'
    videos=sum(a['kind']=='video' for a in c['media'])
    kind=(str(videos)+' 段演示') if videos else '场景预览'
    return '<div class="cover"><img src="'+e(path)+'" alt="'+e(c['title']+' · 场景预览')+'" loading="lazy"><span class="cover-kind">'+kind+'</span></div>'
def duration(seconds):
    t=int(seconds);return f'{t//60:02d}:{t%60:02d}'
def gallery(c):
    assets=c['media']
    if not assets:return '<p class="media-pending">本任务的视频与场景图待补充。</p>'
    variant=' single' if len(assets)==1 else ' two' if len(assets)==2 else ''
    parts=['<div class="media-grid'+variant+'">']
    for i,a in enumerate(assets,1):
        parts.append('<figure class="media-item">')
        if a['kind']=='video':
            parts.append('<video controls preload="none" playsinline poster="'+e(a['poster'])+'" aria-label="'+e(c['id']+' '+a['label'])+'"><source src="'+e(a['path'])+'" type="video/mp4">请下载视频观看。</video>')
            name=a['label'];time=' · '+duration(a['duration_seconds'])
        else:
            parts.append('<a href="'+e(a['path'])+'" target="_blank"><img src="'+e(a['path'])+'" alt="'+e(c['title']+' 场景图 '+str(i))+'" loading="lazy"></a>');name='场景图 '+str(i);time=''
        parts.append('<figcaption><div>'+e(name)+'<span>'+e(time)+'</span></div><a href="'+e(a['path'])+'" download>下载 ↓</a></figcaption></figure>')
    parts.append('</div>');return '\n'.join(parts)
def table(c):
    d=c['difficulty']
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in d['columns'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(v)+'</td>' for v in r)+'</tr>' for r in d['rows'])+'</tbody></table></div>'
def card(c):
    cid=c['id'];suite=SUITES[c['suite']]
    return '\n'.join([
    f'<details class="case-card" id="case-{cid}" data-id="{cid}" data-suite="{c["suite"]}">',
    '<summary>'+cover_html(c)+'<div class="card-intro"><div class="card-eyebrow"><span class="cid">'+cid+'</span><span>'+e(suite[1])+'</span></div><h3>'+e(c['title'])+'</h3><p>'+e(c['challenge'])+'</p><div class="card-more"><span class="more-label">探索任务</span><span class="sign" aria-hidden="true">+</span></div></div></summary>',
    '<div class="case-body"><p class="description">'+e(c['description'])+'</p>',
    label('01','任务演示'),gallery(c),
    label('02','验证什么能力'),'<div class="detail-columns"><div>'+ul(c['abilities'])+'</div><div><ol class="flow">'+''.join('<li>'+e(x)+'</li>' for x in c['flow'])+'</ol></div></div>',
    evidence(c),label('03','难度设置'),table(c),
    label('04','完成条件与评测指标'),'<div class="success">'+e(c['success'])+'</div><ul class="metric-list">'+''.join('<li>'+e(x)+'</li>' for x in c['metrics'])+'</ul>',
    '<details class="notes"><summary>参数与评测说明</summary>'+ul(c['notes'])+'</details>',
    '<div class="case-footer"><span>'+cid+' · '+e(suite[0])+'</span><span><a href="docs/cases/'+cid+'.md" download>任务说明 ↓</a> · <a href="#case-'+cid+'">任务链接</a></span></div></div></details>'])
def featured(records):
    by_id={c['id']:c for c in records};out=[]
    for cid in FEATURED:
        c=by_id[cid]
        out.append('<a href="#case-'+cid+'"><figure><img src="'+e(cover(c))+'" alt="'+e(c['title'])+'"><figcaption><div><small>'+cid+'</small><b> · '+e(c['title'])+'</b></div><span aria-hidden="true">↗</span></figcaption></figure></a>')
    return '\n'.join(out)
def md_table(c):
    clean=lambda x:str(x).replace('|','／').replace('\n',' / ')
    data=c['difficulty'];return '\n'.join(['| '+' | '.join(map(clean,data['columns']))+' |','|'+'|'.join(['---']*len(data['columns']))+'|']+['| '+' | '.join(map(clean,row))+' |' for row in data['rows']])
def case_md(c,relative):
    lines=[f'# {c["id"]} · {c["title"]}','',SUITES[c['suite']][0],'',c['description'],'','**核心挑战：** '+c['challenge'],'','## 验证能力','']+['- '+x for x in c['abilities']]
    lines+=['','## 高层、低层与闭环证据','', '- 高层目标：'+c['evidence']['high'], '- 低层效果：'+c['evidence']['low'], '- 闭环验收：'+c['evidence']['feedback']]
    lines+=['','## 执行流程','',' → '.join(c['flow']),'','## 难度设置','',md_table(c),'','## 完成条件与指标','',c['success'],'']+['- '+x for x in c['metrics']]
    lines+=['','## 演示素材','']
    if not c['media']:lines+=['视频与场景图待补充。']
    for i,a in enumerate(c['media'],1):
        if a['kind']=='video':lines+=[f'- [{a["label"]} · {duration(a["duration_seconds"])}]({relative+a["path"]})']
        else:lines += [f'![场景图 {i}]({relative+a["path"]})']
    lines+=['','## 参数与评测说明','']+['- '+x for x in c['notes']]+['']
    return '\n'.join(lines)
