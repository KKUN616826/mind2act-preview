import json, re
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
MODELS={'astra':'GPT-6 Astra','claude':'Claude','gemini':'Gemini','deepseek':'DeepSeek','qwen':'Qwen'}
def build_rollouts(titles):
 records=json.loads((ROOT/'data/showcase-cases.json').read_text(encoding='utf-8'))
 out=ROOT/'rollouts';out.mkdir(exist_ok=True)
 css="""*{box-sizing:border-box}body{margin:0;background:#faf8ef;color:#192d43;font-family:Arial,sans-serif}a{color:inherit;text-decoration:none}header{border-bottom:1px solid #d2d9ce;background:#faf8ef}nav,main{max-width:1160px;margin:auto;padding:26px 32px}nav{display:flex;justify-content:space-between;align-items:center}nav b{font-size:21px}main{padding-top:50px}h1{font-size:42px;letter-spacing:-1.4px;margin:15px 0 28px}.crumb{font-size:14px;color:#315e73}.tag{display:inline-block;font-size:12px;padding:6px 10px;background:#e9eee5;border-radius:4px;margin-bottom:24px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}.card{background:#faf8ef;border:1px solid #d2d9ce;border-radius:4px;overflow:hidden;transition:background .2s,border-color .2s}.card:hover{border-color:#315e73;background:#eef1e8}.card img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}.card .text{padding:18px}.card h2{font-size:17px;line-height:1.45;margin:8px 0 18px;min-height:49px}.meta{display:flex;justify-content:space-between;font-size:13px;color:#315e73}.id{font-size:12px;letter-spacing:.08em}video{width:100%;aspect-ratio:4/3;display:block;background:#142a3a}.run{background:#faf8ef;border:1px solid #d2d9ce;border-radius:4px;overflow:hidden}.run h2{font-size:18px;padding:0 18px}.run p{padding:24px 18px;min-height:130px}.summary{display:flex;gap:45px;margin-bottom:35px}.summary b{font-size:25px}.summary span{display:block;font-size:12px;margin-top:8px;color:#315e73}.back{display:inline-block;margin:35px 0;padding-bottom:5px;border-bottom:1px solid #315e73}@media(max-width:800px){.grid{grid-template-columns:repeat(2,1fr)}h1{font-size:32px}}@media(max-width:560px){.grid{grid-template-columns:1fr}nav,main{padding-left:20px;padding-right:20px}.summary{gap:25px}}"""
 def page(title,body):return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+' · Mind2Act</title><style>'+css+'</style><header><nav><a href="../index.html"><b>MIND2ACT WORLD</b></a><a href="../index.html#top-ten">Leaderboard ↗</a></nav></header><main>'+body+'</main></html>'
 for slug,name in MODELS.items():
  cards=[]
  for c in records:
   cid=c['id'];clips=[a for a in c['media'] if a['kind']=='video'];asset=clips[0] if clips else None
   img='<img loading="lazy" src="../'+escape(asset['poster'])+'" alt="'+escape(titles[cid])+'">' if asset else ''
   cards.append('<a class="card" href="'+slug+'-'+cid+'.html">'+img+'<div class="text"><span class="id">'+cid+'</span><h2>'+escape(titles[cid])+'</h2><div class="meta"><span>View demonstrations ↗</span><b>XX%</b></div></div></a>')
   runs=[];used=set()
   for level in ['Easy','Medium','Hard']:
    a=next((a for a in clips if re.match(level+r"(?:\s|$)",a['label'],re.I)),None)
    if a:used.add(a['path'])
    media='<video controls playsinline preload="none" poster="../'+escape(a['poster'])+'" src="../'+escape(a['path'])+'"></video>' if a else '<p>Video pending</p>'
    runs.append('<article class="run"><h2>'+level+' <span style="float:right">XX%</span></h2>'+media+'</article>')
   other=[a for a in clips if a['path'] not in used]
   extras=''
   if other:extras='<h2>Demonstrations · difficulty unspecified</h2><div class="grid">'+''.join('<article class="run"><video controls playsinline preload="none" src="../'+escape(a['path'])+'" poster="../'+escape(a['poster'])+'"></video></article>' for a in other)+'</div>'
   body='<div class="crumb"><a href="../index.html#top-ten">Leaderboard</a> / <a href="'+slug+'.html">'+name+'</a> / '+cid+'</div><h1>'+escape(titles[cid])+'</h1><span class="tag">Demonstration preview · model results pending</span><div class="grid">'+''.join(runs)+'</div>'+extras+'<a class="back" href="'+slug+'.html">← All '+name+' tasks</a>'
   (out/(slug+'-'+cid+'.html')).write_text(page(name+' · '+cid,body),encoding='utf-8')
  body='<div class="crumb"><a href="../index.html#top-ten">Leaderboard</a> / '+name+'</div><h1>'+name+'</h1><div class="summary"><div><b>XX%</b><span>Mind</span></div><div><b>XX%</b><span>Act</span></div><div><b>XX%</b><span>Mind2Act</span></div></div><span class="tag">Demonstration preview · model results pending</span><div class="grid">'+''.join(cards)+'</div>'
  (out/(slug+'.html')).write_text(page(name,body),encoding='utf-8')
