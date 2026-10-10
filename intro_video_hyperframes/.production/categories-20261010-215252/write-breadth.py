from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
prefix='assets/generated/categories-20261010-215252/'
groups=[('Mind','#bdd9cc',[('E','Entity memory'),('F','Button rules'),('P','Order memory'),('S','Spatial memory'),('M','Integrated memory')]),('Act','#aac4d9',[('FR1','Moving targets'),('FR2','Timed response'),('PR1','Resistance control'),('PR2','Voltage control'),('PR3','Curve tracing')]),('Mind2Act','#f0d57e',[('CP01','Moving meal orders'),('CP02','Cake assembly'),('CP03','Moving rack loading'),('CP04','Recipe execution'),('CP05','Sequence replay')])]
css="""@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:400;src:url('assets/fonts/SpaceGrotesk-400.ttf') format('truetype')}@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:600;src:url('assets/fonts/SpaceGrotesk-600.ttf') format('truetype')}@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;src:url('assets/fonts/IBMPlexMono-400.ttf') format('truetype')}
#root{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}.scale-surface{position:absolute;inset:0;background:#090e13;color:#faf9f4;font-family:'Space Grotesk',sans-serif;overflow:hidden}.scale-abs{position:absolute}.scale-grid-title{left:72px;top:62px;font-size:96px;font-weight:600;line-height:1.04;letter-spacing:-3px}.scale-grid-meta{left:855px;top:91px;font-size:36px;color:#bdd9cc}.scale-group{position:absolute;top:224px;width:560px;font-size:44px;font-weight:600;line-height:1.1}.scale-group-rule{position:absolute;left:0;right:0;top:62px;height:2px;background:#30424e}.scale-task{position:absolute;width:560px;height:126px;background:#111c25;border-radius:4px;overflow:hidden}.scale-thumb{position:absolute;left:0;top:0;width:240px;height:126px;overflow:hidden;background:#101820}.scale-thumb video{position:absolute;width:100%;height:100%;object-fit:cover}.scale-taskcode{position:absolute;left:264px;top:19px;font:18px 'IBM Plex Mono',monospace;color:#bccbd5}.scale-taskname{position:absolute;left:264px;top:47px;width:282px;font-size:30px;line-height:1.13;font-weight:600}.scale-hero{position:absolute;inset:0;background:#090e13;overflow:hidden}.scale-hero-media{position:absolute;left:0;top:39px;width:1920px;height:1002px;overflow:hidden;transform-origin:0 0}.scale-hero-media video{width:100%;height:100%;object-fit:contain}.scale-hero-bar{position:absolute;left:0;right:0;bottom:0;height:158px;background:#090e13;display:flex;align-items:center;padding:0 72px;gap:48px}.scale-hero-type{font-size:96px;font-weight:600;letter-spacing:-3px;line-height:1}.scale-hero-name{font-size:36px;color:#c6d3df}.scale-f-outline{position:absolute;left:70px;top:447px;width:564px;height:130px;border:2px solid #f0d57e;border-radius:5px;box-sizing:border-box;pointer-events:none}"""
html=['<!doctype html><html lang="en"><head><meta charset="UTF-8"></head><body><template><style>'+css+'</style>','<div id="root" data-composition-id="scale" data-width="1920" data-height="1080" data-duration="12.471852"><div id="scale-surface" class="scale-surface">','<div id="scale-wall" class="scale-abs" style="inset:0"><div id="scale-grid-title" class="scale-abs scale-grid-title">15 Tasks.</div><div id="scale-grid-meta" class="scale-abs scale-grid-meta">Three categories.</div>']
for gi,(name,color,tasks) in enumerate(groups):
 x=72+gi*608
 html.append(f'<div id="scale-group-{gi}" class="scale-group" style="left:{x}px;color:{color}">{name}<div class="scale-group-rule"></div></div>')
 for ri,(code,label) in enumerate(tasks):
  y=312+ri*137
  html.append(f'<div id="scale-task-{code}" class="scale-task" style="left:{x}px;top:{y}px"><div class="scale-thumb">')
  if code!='F':html.append(f'<video id="scale-video-{code}" class="clip" src="{prefix}{code.lower()}-wall.mp4" data-start="5.05" data-duration="7.421852" data-track-index="{gi+2}" data-hf-media-start-basis="local" muted playsinline></video>')
  html.append(f'</div><div class="scale-taskcode">{code}</div><div class="scale-taskname">{label}</div></div>')
html.append('</div>')
for i,(task,name,category,color,start,dur) in enumerate([('fr1','Moving targets','Act.','#aac4d9',0,1.8),('cp02','Cake assembly','Mind2Act.','#f0d57e',1.45,1.9)]):
 html.append(f'<div id="scale-hero-{i}" class="scale-hero"><div class="scale-hero-media" style="left:77px;top:0;width:1766px;height:922px"><video id="scale-hero-video-{i}" class="clip" src="{prefix}{task}-wall.mp4" data-start="{start}" data-duration="{dur}" data-track-index="5" data-hf-media-start-basis="local" muted playsinline></video></div><div class="scale-hero-bar"><div class="scale-hero-type" style="color:{color}">{category}</div><div class="scale-hero-name">{name}</div></div></div>')
html.append(f'<div id="scale-f-hero" class="scale-hero-media"><video id="scale-f-hero-video" class="clip" src="{prefix}f-medium-probe.mp4" data-start="3" data-duration="9.471852" data-track-index="6" data-hf-media-start-basis="local" muted playsinline></video></div><div id="scale-f-bar" class="scale-hero-bar"><div class="scale-hero-type" style="color:#bdd9cc">Mind.</div><div class="scale-hero-name">Learn the button rules.</div></div><div id="scale-f-outline" class="scale-f-outline"></div></div></div>')
js="""(function(){const tl=gsap.timeline({paused:true});
tl.fromTo('#scale-surface',{clipPath:'inset(0% 0% 0% 100%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.38,ease:'power3.inOut'},0);
tl.fromTo('#scale-hero-0 .scale-hero-bar',{y:160},{y:0,duration:.45,ease:'expo.out'},.14);
tl.fromTo('#scale-hero-1',{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.25,ease:'power3.inOut'},1.45);
tl.fromTo('#scale-hero-1 .scale-hero-type',{y:90,opacity:0},{y:0,opacity:1,duration:.4,ease:'expo.out'},1.56);
tl.fromTo('#scale-f-hero',{opacity:0,x:76.8,y:-39,scale:.92},{opacity:1,x:76.8,y:-39,scale:.92,duration:.25,ease:'power2.out'},3);
tl.fromTo('#scale-f-bar',{opacity:0,y:50},{opacity:1,y:0,duration:.32,ease:'power4.out'},3.02);
// The last full-screen F clip is the same element that lands in the F taxonomy card.
tl.to(['#scale-hero-0','#scale-hero-1','#scale-f-bar'],{opacity:0,duration:.3,ease:'power2.inOut'},5.12);
tl.to('#scale-f-hero',{x:72,y:410,scale:.125,duration:1.03,ease:'power3.inOut',transformOrigin:'0 0'},5.12);
tl.fromTo('#scale-wall',{opacity:0},{opacity:1,duration:.28,ease:'power2.out'},5.12);
tl.fromTo('#scale-grid-title',{y:90,opacity:0},{y:0,opacity:1,duration:.6,ease:'expo.out'},5.27);
tl.fromTo('#scale-grid-meta',{x:45,opacity:0},{x:0,opacity:1,duration:.6,ease:'power2.out'},5.56);
[0,1,2].forEach((n)=>tl.fromTo('#scale-group-'+n,{y:35,opacity:0},{y:0,opacity:1,duration:.48,ease:'power3.out'},5.72+n*.07));
const codes=['E','F','P','S','M','FR1','FR2','PR1','PR2','PR3','CP01','CP02','CP03','CP04','CP05'];
codes.forEach((code,i)=>tl.fromTo('#scale-task-'+code,{y:42,opacity:0},{y:0,opacity:1,duration:.58,ease:'power3.out'},5.72+(i%5)*.06+Math.floor(i/5)*.07));
tl.fromTo('#scale-f-outline',{opacity:0},{opacity:1,duration:.3,ease:'sine.out'},10.77);
window.__timelines['scale']=tl;})();"""
html.append('<script>'+js+'</script></template></body></html>');(ROOT/'compositions/06-scale.html').write_text('\n'.join(html))
