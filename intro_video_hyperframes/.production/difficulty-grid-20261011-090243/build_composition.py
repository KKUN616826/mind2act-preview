from pathlib import Path
import re
ROOT=Path.cwd()
WORK=ROOT/'.production/difficulty-grid-20261011-090243'
source=(WORK/'before/compositions/09-difficulty.html').read_text()
# Retain all hero CSS, media and entrance choreography for the first 6.3s.
css=source.split('<style>',1)[1].split('</style>',1)[0]
extra='''
.difficulty-grid{position:absolute;inset:0;pointer-events:none}
.difficulty-grid-title{position:absolute;left:72px;top:65px;font-size:64px;line-height:1.08;font-weight:600;letter-spacing:-1.5px}
.difficulty-grid-row{position:absolute;left:60px;width:1800px;height:220px;background:#111c25;border:2px solid #30424e;border-radius:6px;box-sizing:border-box;overflow:hidden}
.difficulty-grid-label{position:absolute;left:22px;top:0;width:350px;height:216px;display:flex;flex-direction:column;justify-content:center;gap:16px}
.difficulty-grid-category{font-size:26px;line-height:1.1;font-weight:400;color:#c6d3df}
.difficulty-grid-caption{font-size:42px;line-height:1.12;font-weight:600;color:#faf9f4;max-width:342px}
.difficulty-grid-cell{position:absolute;top:-2px;width:448px;height:220px;overflow:hidden;background:#101820}
.difficulty-grid-cell img,.difficulty-grid-cell video{display:block;width:100%;height:100%;object-fit:cover}
.difficulty-cake-count{position:absolute;left:12px;top:12px;min-width:49px;height:49px;display:flex;align-items:center;justify-content:center;background:#090e13;color:#faf9f4;font-size:34px;font-weight:600;line-height:1;border-radius:4px;padding:0 9px}
.difficulty-cover-film{position:absolute;inset:0;background:#101820}
'''
body=source.split('<div id="root"',1)[1].split('<script>',1)[0]
body='<div id="root"'+body
body=body.replace('data-duration="12.471852"','data-duration="13.371852"',1)
body=re.sub(r'<div id="difficulty-row-(?:easy|medium|hard)"[^>]*></div>\n?','',body)
body=re.sub(r'<div id="difficulty-note-(?:easy|medium|hard)".*?</div></div>','',body)
# New comparison remains a single stable spatial layout.
assets='assets/generated/difficulty-grid-20261011-090243/'
grid=['<div id="difficulty-grid" class="difficulty-grid"><div id="difficulty-grid-title" class="difficulty-grid-title">Three levels. Rising demands.</div>']
for row,top,category,caption,color in [('f',280,'Mind','Rules &amp; routes','#bdd9cc'),('pr3',516,'Act','Tighter turns','#aac4d9'),('cp02',752,'Mind2Act','More pieces &amp; steps','#f0d57e')]:
 grid.append(f'<div id="difficulty-grid-{row}" class="difficulty-grid-row" style="top:{top}px"><div class="difficulty-grid-label"><div class="difficulty-grid-category" style="color:{color}">{category}</div><div class="difficulty-grid-caption">{caption}</div></div>')
 for i,lv in enumerate(['easy','medium','hard']):
  # Column content begins at x456,928,1400 in composition space.
  grid.append(f'<div id="difficulty-cell-{row}-{lv}" class="difficulty-grid-cell" style="left:{394+i*472}px">')
  if row=='f':
   grid.append(f'<video id="difficulty-nav-{lv}" class="clip" src="{assets}f-{lv}-navigation.mp4" data-start="6.40" data-duration="4.33" data-track-index="{4+i}" data-hf-media-start-basis="local" muted playsinline></video>')
  else:
   grid.append(f'<img id="difficulty-image-{row}-{lv}" src="{assets}{row}-{lv}.png" alt="{category} {lv} '+('reference path' if row=='pr3' else 'reference cake to remember')+'">')
  if row=='cp02':
   if lv=='hard':
    grid.append(f'<div id="difficulty-cover-film" class="difficulty-cover-film"><video id="difficulty-cover-video" class="clip" src="{assets}cp02-hard-cover.mp4" data-start="9.05" data-duration="1.68" data-track-index="8" data-hf-media-start-basis="local" muted playsinline></video></div>')
   grid.append(f'<div id="difficulty-cake-count-{lv}" class="difficulty-cake-count">{4 if lv=="easy" else 6}</div>')
  grid.append('</div>')
 grid.append('</div>')
grid.append('</div>')
# New grid is under original hero objects; they become column headings during the handoff.
body=body.replace('<div id="difficulty-word-easy"',''.join(grid)+'\n<div id="difficulty-word-easy"',1)
script=source.split('<script>',1)[1].split('// All three videos',1)[0]
script+='''
// Preserve the large-word sequence until this handoff, then keep a stable 3x3 comparison.
tl.to(['#difficulty-kicker','#difficulty-title'],{opacity:0,duration:.16,ease:'power2.inOut'},6.34);
tl.fromTo('#difficulty-grid-title',{opacity:0,y:22},{opacity:1,y:0,duration:.24,ease:'power3.out'},6.50);
['f','pr3','cp02'].forEach((row)=>{
 tl.fromTo('#difficulty-grid-'+row,{opacity:0,y:22},{opacity:1,y:0,duration:.38,ease:'power3.out'},6.34);
 tl.fromTo('#difficulty-grid-'+row+' .difficulty-grid-label',{opacity:0},{opacity:1,duration:.18,ease:'power2.out'},6.56);
});
levels.forEach((lv,i)=>{
 const x=456+i*472;
 if(lv==='hard'){
  tl.to('#difficulty-word-'+lv,{opacity:1,x:x+20-74,y:187-359,scale:.30,duration:.4,ease:'power3.inOut'},6.34);
  tl.to('#difficulty-film-'+lv,{opacity:1,x:x-690,y:280-275,scale:448/1160,duration:.4,ease:'power3.inOut'},6.34);
  tl.to('#difficulty-film-'+lv,{opacity:0,duration:.15,ease:'power2.out'},6.62);
 }else{
  tl.set('#difficulty-word-'+lv,{opacity:0,x:x+20-74,y:187-359,scale:.30},6.34);
  tl.to('#difficulty-word-'+lv,{opacity:1,duration:.20,ease:'power2.out'},6.54);
 }
 tl.to('#difficulty-desc-'+lv,{opacity:0,duration:.20},6.34);
});
// Speech-aligned emphasis: rules, turns, then memory and the extra physical step.
tl.to('#difficulty-grid-f',{borderColor:'#bdd9cc',backgroundColor:'#1b2b33',duration:.18},6.70);
tl.to('#difficulty-grid-f',{borderColor:'#30424e',backgroundColor:'#111c25',duration:.2},7.66);
tl.to('#difficulty-grid-pr3',{borderColor:'#aac4d9',backgroundColor:'#1b2b33',duration:.18},7.66);
tl.to('#difficulty-grid-pr3',{borderColor:'#30424e',backgroundColor:'#111c25',duration:.2},8.60);
tl.to('#difficulty-grid-cp02',{borderColor:'#f0d57e',backgroundColor:'#242b2c',duration:.18},8.60);
tl.fromTo('#difficulty-cover-film',{opacity:0},{opacity:1,duration:.15,ease:'power2.out'},9.05);
// 45 retains its existing entrance and hold, shifted by 0.90 seconds.
tl.fromTo('#difficulty-stat',{clipPath:'inset(100% 0% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.4,ease:'power3.inOut'},10.33);
tl.fromTo('#difficulty-formula',{opacity:0,y:55},{opacity:1,y:0,duration:.55,ease:'power3.out'},10.49);
tl.fromTo('#difficulty-45',{opacity:0,y:170,scale:.92},{opacity:1,y:0,scale:1,duration:.7,ease:'expo.out'},10.73);
tl.fromTo('#difficulty-config',{opacity:0,x:80},{opacity:1,x:0,duration:.6,ease:'power2.out'},10.96);
window.__timelines['difficulty']=tl;})();'''
Path('compositions/09-difficulty.html').write_text('<!doctype html><html lang="en"><head><meta charset="UTF-8"></head><body><template><style>'+css+extra+'</style>\n'+body+'<script>'+script+'</script></template></body></html>\n')
