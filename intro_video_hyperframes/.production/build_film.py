from pathlib import Path
import json,html
P=Path.cwd(); C=P/'compositions';C.mkdir(exist_ok=True)
D=47.4074074074; B=60/81
starts=[0,7*B,16*B,24*B,32*B,40*B,57*B,D]
logo='assets/logos/Mind2Act-三个Logo-高清透明版/03-Mind2Act-1254x1254.png'
media_root='assets/generated/source-refresh-20261010-142512'
common='''
*{box-sizing:border-box} .scene-surface{position:absolute;inset:0;overflow:hidden;background:#090e13;color:#faf9f4;font-family:'Space Grotesk',sans-serif} .abs{position:absolute}.clip{position:absolute}.mono{font-family:'IBM Plex Mono',monospace;font-weight:400;letter-spacing:2px}.label{font-size:22px;line-height:1.3;letter-spacing:3px}.mint{color:#bdd9cc}.gold{color:#f0d57e}.steel{color:#9fb2c8}.moon{color:#e4e6d2}.hairline{height:1px;background:rgba(189,217,204,.32)} .fill{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.case-title{font-size:82px;font-weight:600;letter-spacing:-4px;line-height:1}.case-sub{font-size:22px;letter-spacing:3px}.case-top{position:absolute;left:64px;top:56px;display:flex;gap:24px;align-items:center}.case-mark{width:74px;height:74px;object-fit:contain}.case-meta{position:absolute;right:64px;top:63px;text-align:right}.case-header-bg{position:absolute;left:0;right:0;top:0;height:245px;background:linear-gradient(#090e13ec 0%,#090e13d9 68%,transparent 100%)}.case-panel{position:absolute;right:58px;top:240px;width:324px;padding:26px;background:rgba(9,14,19,.85);border:1px solid rgba(189,217,204,.32);border-radius:4px}.panel-title{font-size:21px;line-height:1.4;letter-spacing:2px}.panel-big{font-size:34px;line-height:1.17;letter-spacing:-1px;margin-top:15px}.case-bottom{position:absolute;left:0;right:0;bottom:0;height:76px;background:rgba(9,14,19,.90);display:flex;align-items:center;justify-content:space-between;padding:0 64px;font-family:'IBM Plex Mono',monospace;font-size:18px;letter-spacing:1.4px}.corner{position:absolute;width:24px;height:24px;border-top:2px solid #bdd9cc;border-left:2px solid #bdd9cc}.wipe-edge{position:absolute;right:0;top:0;width:5px;height:100%;background:#bdd9cc}.tag{display:inline-block;font-size:20px;border:1px solid #9fb2c860;padding:10px 15px;background:#102134d9}.accent-rule{height:3px;background:#f0d57e;transform-origin:left center}.step-row{padding:18px 0;border-top:1px solid #e4e6d230;font-size:25px;line-height:1.2}.step-row small{display:block;font-family:'IBM Plex Mono',monospace;font-size:16px;margin-bottom:6px;letter-spacing:1px;color:#9fb2c8} svg{overflow:visible} .footage-camera{position:absolute;inset:0;transform-origin:center center}.case-outline{position:absolute;inset:22px;border:1px solid rgba(228,230,210,.18);pointer-events:none}
'''
fonts='\n'.join(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};src:url('assets/fonts/{fn}-{w}.ttf') format('truetype')}}" for fam,fn,ws in [('Space Grotesk','SpaceGrotesk',[400,500,600,700]),('IBM Plex Mono','IBMPlexMono',[400,500])] for w in ws)
def video(id,src,start,dur,cls='fill',extra=''):
 return f'<video id="{id}" class="clip {cls}" src="{media_root}/{src}" data-start="{start:.6f}" data-duration="{dur:.6f}" data-track-index="1" data-hf-media-start-basis="local" muted playsinline {extra}></video>'
def scene(i,name,body,css,js):
 dur=starts[i+1]-starts[i]
 s=f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"></head><body><template>
<style>{fonts}\n#root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;}}\n{common}\n{css}</style>
<div id="root" data-composition-id="{name}" data-width="1920" data-height="1080" data-duration="{dur:.6f}"><div class="scene-surface" id="{name}-surface">{body}</div></div>
<script>(function(){{const tl=gsap.timeline({{paused:true}});{js}\nwindow.__timelines['{name}']=tl;}})();</script>
</template></body></html>'''
 (C/f'{i+1:02d}-{name}.html').write_text(s)
def in_(sel,at,params='y:40',dur=.6,ease='power3.out'):
 return f"tl.fromTo('{sel}',{{opacity:0,{params}}},{{opacity:1,x:0,y:0,scale:1,rotation:0,duration:{dur},ease:'{ease}'}},{at});\n"
def casetop(n,label,sub,code):
 case_logo={'mind':'assets/logos/Mind2Act-三个Logo-高清透明版/01-Mind-1308x1203.png','act':'assets/logos/Mind2Act-三个Logo-高清透明版/02-Act-1268x1241.png'}.get(n,logo)
 return f'<div class="case-header-bg"></div><div class="case-top" id="{n}-top"><img class="case-mark" src="{case_logo}"><div><div class="case-title">{label}</div><div class="case-sub mono mint">{sub}</div></div></div><div class="case-meta mono" id="{n}-meta"><div class="label">{code}</div><div style="font-size:18px;margin-top:12px;color:#d8dfdd">TASK SPOTLIGHT</div></div>'
def panel(n,label,big,rows):
 return f'<div class="case-panel" id="{n}-panel"><div class="panel-title mono mint">{label}</div><div class="panel-big">{big}</div><div class="accent-rule" style="margin:22px 0"></div>'+''.join(f'<div class="step-row" id="{n}-step{k}"><small>0{k+1}</small>{v}</div>' for k,v in enumerate(rows))+'</div>'
# 1 — footage → mosaic → brand
body=f'''<div class="abs" style="inset:0" id="intro-one">{video('intro-source','cases/piano-play.mp4',0,1.5)}</div>
<div class="abs" style="inset:0" id="intro-six">{video('intro-sixvid','montage/six-cases-mosaic.mp4',0,1.5)}</div>
<div class="abs" style="inset:0" id="intro-all" data-layout-allow-overflow>{video('intro-allvid','montage/all-cases-mosaic.mp4',0,5.185185)}</div>
<div id="intro-shade" class="abs" style="inset:0;background:#090e13"></div>
<div class="abs intro-orbit" id="intro-orbit" data-layout-ignore><svg width="680" height="680" viewBox="0 0 680 680"><circle cx="340" cy="340" r="312" fill="none" stroke="#bdd9cc" stroke-opacity=".3" stroke-width="1"/><circle cx="340" cy="340" r="327" fill="none" stroke="#9fb2c8" stroke-opacity=".28" stroke-dasharray="2 18"/><path d="M 42 340 H 86 M 594 340 H 638" stroke="#f0d57e" stroke-width="2"/></svg></div>
<img id="intro-logo" class="abs" src="{logo}" style="left:778px;top:140px;width:364px;height:364px">
<div class="abs mono label mint" id="intro-eyebrow" style="top:568px;left:0;width:100%;text-align:center">A NEW WORLD OF EMBODIED INTELLIGENCE</div>
<div class="abs" id="intro-name" style="top:600px;width:100%;text-align:center;font-size:128px;font-weight:600;letter-spacing:-7px">Mind2Act <span class="moon" style="font-weight:400">World</span></div>
<div id="intro-rule" class="abs accent-rule" style="left:730px;top:777px;width:460px;height:2px"></div>
<div class="abs" id="intro-tagline" style="top:820px;left:340px;width:1240px;text-align:center;font-size:34px;line-height:1.4;color:#e4e6d2">Evaluating reasoning–acting coordination in robotic manipulation.</div>
<div class="abs mono" id="intro-edge" style="left:65px;bottom:42px;font-size:18px;letter-spacing:2px">MIND / ACT / MIND2ACT</div>'''
css='#intro-six,#intro-all,#intro-shade{opacity:0}.intro-orbit{left:620px;top:-17px;width:680px;height:680px} '
js="""
tl.fromTo('#intro-one',{scale:1.08},{scale:1,duration:.55,ease:'power2.out'},0);
tl.fromTo('#intro-six',{opacity:0,scale:1.8},{opacity:1,scale:1,duration:.45,ease:'expo.out'},.37);
tl.fromTo('#intro-all',{opacity:0,scale:2.5},{opacity:1,scale:1.015,duration:.82,ease:'power3.inOut'},1.02);
tl.to('#intro-shade',{opacity:.82,duration:.8,ease:'power2.out'},1.30);
tl.fromTo('#intro-logo',{opacity:0,scale:.60,rotation:-12},{opacity:1,scale:1,rotation:0,duration:.80,ease:'expo.out'},1.30);
tl.fromTo('#intro-orbit',{opacity:0,scale:.6,rotation:-55},{opacity:1,scale:1,rotation:8,duration:1.25,ease:'power2.out'},1.42);
tl.to('#intro-orbit',{rotation:22,duration:2.5,ease:'none'},2.67);
"""+in_('#intro-eyebrow',1.90,'y:18',.45)+in_('#intro-name',2.06,'y:65',.64,'expo.out')+"tl.fromTo('#intro-rule',{scaleX:0},{scaleX:1,duration:.7,ease:'power2.inOut'},2.28);"+in_('#intro-tagline',2.48,'y:24',.65,'sine.out')+in_('#intro-edge',2.7,'x:-20',.5)
scene(0,'intro',body,css,js)
# 2 — question / lunar logic
body=f'''<div class="abs motive-grid" id="motive-grid" data-layout-ignore></div>
<div id="motivation-head" class="abs" style="left:80px;top:75px"><div class="mono label mint">THE QUESTION BEHIND THE BENCHMARK</div><div style="font-size:78px;font-weight:500;letter-spacing:-3px;margin-top:18px">When robots fail, what breaks down?</div></div>
<div class="abs" id="motivation-orbit" style="left:555px;top:275px;width:810px;height:620px" data-layout-ignore><svg width="810" height="620"><ellipse cx="405" cy="310" rx="400" ry="205" stroke="#9fb2c8" stroke-opacity=".35" fill="none"/><path id="motive-link" d="M20 310 H185 M625 310 H790" stroke="#f0d57e" stroke-width="3" fill="none"/></svg></div>
<img id="motivation-bright" class="abs" src="{logo}" style="left:735px;top:340px;width:450px;height:450px;clip-path:polygon(0 0,100% 0,100% 3%,3% 100%,0 100%)">
<div id="motivation-dark" class="abs" style="background-image:url('{logo}');background-size:contain;background-repeat:no-repeat;left:735px;top:340px;width:450px;height:450px;clip-path:polygon(100% 3%,100% 100%,3% 100%)"></div>
<div class="abs" id="motivation-mind" style="left:120px;top:408px;width:410px"><div class="mono label mint">01 / TASK REASONING</div><div style="font-size:108px;letter-spacing:-6px;margin:16px 0">Mind</div><div style="font-size:36px;color:#e4e6d2">The decision.</div></div>
<div class="abs" id="motivation-act" style="left:1420px;top:408px;width:410px"><div class="mono label steel">02 / PHYSICAL EXECUTION</div><div style="font-size:108px;letter-spacing:-6px;margin:16px 0">Act</div><div style="font-size:36px;color:#e4e6d2">The execution.</div></div>
<div class="abs" id="motivation-coord" style="left:430px;top:882px;width:1060px;text-align:center"><span class="gold" style="font-size:45px;letter-spacing:-1px">Or their coordination?</span><div class="mono" style="font-size:18px;margin-top:17px;color:#a8bacb;letter-spacing:3px">REASON → ACT → UPDATE</div></div>
<div class="abs hairline" style="left:80px;right:80px;bottom:52px"></div>'''
css='.motive-grid{inset:0;background-image:linear-gradient(#9fb2c80b 1px,transparent 1px),linear-gradient(90deg,#9fb2c80b 1px,transparent 1px);background-size:110px 110px}'
js="tl.fromTo('#motivation-surface',{clipPath:'circle(0% at 50% 30%)'},{clipPath:'circle(100% at 50% 30%)',duration:.6,ease:'power3.inOut'},0);"+in_('#motivation-head',.15,'y:30',.75)+in_('#motivation-bright',.12,'scale:.82',.6)+in_('#motivation-dark',.12,'scale:.82',.6)+"tl.to('#motivation-bright',{x:-130,y:-28,duration:1.15,ease:'power3.inOut'},1.1);tl.to('#motivation-dark',{x:130,y:28,duration:1.15,ease:'power3.inOut'},1.1);"+in_('#motivation-mind',1.20,'x:75',.70,'expo.out')+in_('#motivation-act',2.14,'x:-75',.75,'power2.out')+in_('#motivation-orbit',2.65,'scale:.90',.65,'sine.out')+in_('#motivation-coord',3.75,'y:38',.75)+"tl.to('#motivation-bright',{x:-55,y:-12,duration:1.2,ease:'power2.inOut'},4.65);tl.to('#motivation-dark',{x:55,y:12,duration:1.2,ease:'power2.inOut'},4.65);tl.fromTo('#motive-grid',{x:-14,y:-12},{x:12,y:9,duration:6.66,ease:'none'},0);"
scene(1,'motivation',body,css,js)
# 3 — P retained order
body=f'''<div class="footage-camera" data-layout-allow-overflow id="mind-camera">{video('mind-establish','cases/p-intro.mp4',0,1.85)}{video('mind-grasp','cases/p-action1.mp4',1.70,2.61)}{video('mind-place','cases/p-action2.mp4',4.22,2.325926)}</div>{casetop('mind','Mind','TASK-LEVEL REASONING','P / MEAL PACKING')}
<div id="mind-order" class="abs" style="left:610px;top:186px;width:700px;background:#101c28;border:2px solid #bdd9cc;padding:14px;transform-origin:top left;box-shadow:0 15px 60px #0008"><div class="mono mint" style="font-size:24px;letter-spacing:2px;padding:4px 8px 16px">REMEMBER THE ORDER</div><img src="assets/generated/cases/p-order-blue-crop.png" style="display:block;width:668px;height:373px;object-fit:cover"><div id="mind-order-highlight" class="abs" style="left:80px;top:237px;width:500px;height:130px;border:4px solid #f0d57e"></div></div>
{panel('mind','AFTER THE PROMPT','The task state persists.',['Read the order','Keep the goal','Choose the next item'])}
<div class="case-bottom" id="mind-bottom"><span>P / MEAL PACKING</span><span class="mint">HISTORY + CURRENT STATE → NEXT ACTION</span></div>'''
css=''
js="tl.fromTo('#mind-surface',{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.36,ease:'power3.inOut'},0);tl.fromTo('#mind-camera',{scale:1.025},{scale:1,duration:1.2,ease:'power2.out'},0);"+in_('#mind-top',.15,'y:-30',.55)+in_('#mind-meta',.30,'x:35',.5)+in_('#mind-order',.52,'scale:.42,y:-100',.65,'expo.out')+"tl.fromTo('#mind-order-highlight',{opacity:0,scale:1.15},{opacity:1,scale:1,duration:.27,ease:'power2.out'},1.0);tl.to('#mind-order',{x:-550,y:575,scale:.48,duration:.75,ease:'power3.inOut'},1.36);"+in_('#mind-panel',2.02,'x:70',.6)+in_('#mind-bottom',.4,'y:20',.5)+"tl.fromTo('#mind-step0',{color:'#faf9f4'},{color:'#bdd9cc',duration:.3},2.25);tl.fromTo('#mind-step1',{color:'#faf9f4'},{color:'#f0d57e',duration:.3},3.12);tl.fromTo('#mind-step2',{color:'#faf9f4'},{color:'#f0d57e',duration:.3},4.38);"
scene(2,'mind',body,css,js)
# 4 — line tracing, target vs executed from actual pixels
body=f'''<div class="footage-camera" data-layout-allow-overflow id="act-camera">{video('act-target-video','cases/act-wide.mp4',0,1.3)}{video('act-drawing','cases/act-draw.mp4',1.15,5.395926)}</div>{casetop('act','Act','CONSTRAINT-AWARE EXECUTION','PR3 / LINE TRACING')}
<div class="abs" id="act-target-focus" data-layout-allow-overflow style="left:610px;top:305px;width:650px;height:320px;border:2px solid #e4e6d2"><div class="mono" style="position:absolute;left:0;top:-42px;font-size:24px;background:#102134e6;padding:6px 12px">TARGET CURVE</div><div style="width:100%;height:100%;background-image:url('assets/generated/cases/pr3-target-crop.png');background-size:cover;background-position:center"></div></div>
<div id="act-compare" class="abs" style="left:58px;top:755px;width:590px;height:222px;background:#090e13ec;border:1px solid #9fb2c8;padding:14px"><div class="mono" style="display:flex;justify-content:space-between;font-size:18px;padding:0 6px 12px"><span class="moon">TARGET</span><span class="mint">EXECUTED TRACE</span></div><div style="position:absolute;left:14px;top:48px;width:274px;height:153px;overflow:hidden"><img src="assets/generated/cases/pr3-target-crop.png" style="width:100%;height:100%;object-fit:cover"></div><div style="position:absolute;left:300px;top:48px;width:274px;height:153px;overflow:hidden">{video('act-inset-video','cases/act-detail.mp4',1.15,5.395926)}</div></div>
{panel('act','FROM INTENT TO MOTION','Precision under constraints.',['Follow geometry','Maintain contact','Control the motion'])}<div class="case-bottom" id="act-bottom"><span>PR3 / LINE TRACING</span><span class="mint">GEOMETRY + CONTACT + TIMING</span></div>'''
css=''
js="tl.fromTo('#act-surface',{clipPath:'inset(0% 0% 100% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.38,ease:'power3.inOut'},0);"+in_('#act-top',.12,'y:-35',.5)+in_('#act-meta',.3,'x:35',.5)+in_('#act-target-focus',.22,'scale:.9',.45,'sine.out')+"tl.to('#act-target-focus',{opacity:0,duration:.18},1.10);tl.to('#act-camera',{scale:1.38,x:90,y:75,duration:.8,ease:'power3.inOut'},1.18);tl.to('#act-camera',{scale:1.17,x:40,y:22,duration:2.8,ease:'sine.inOut'},2.45);"+in_('#act-compare',1.72,'x:-70',.55,'expo.out')+in_('#act-panel',2.05,'x:70',.6)+in_('#act-bottom',.42,'y:20',.5)
scene(3,'act',body,css,js)
# 5 — observed sequence / memory / replay
body=f'''<div class="footage-camera" data-layout-allow-overflow id="mind2act-camera">{video('piano-reveal','cases/piano-cover.mp4',0,1.48)}{video('piano-observe','cases/piano-demo.mp4',1.481481,1.48)}{video('piano-replay','cases/piano-play.mp4',2.962963,3.582963)}</div>{casetop('mind2act','Mind2Act','REASONING–ACTING COORDINATION','CP05 / PIANO REPLAY')}
<div class="case-panel" id="mind2act-panel" style="top:178px;right:48px;width:286px;padding:20px"><div class="mono panel-title gold">MEMORY → MOVEMENT</div><div class="panel-big">Keep the sequence. Play it back.</div><div class="accent-rule" style="margin:22px 0"></div><div class="piano-stage" id="piano-stage0"><span>01</span> Reveal</div><div class="piano-stage" id="piano-stage1"><span>02</span> Observe</div><div class="piano-stage" id="piano-stage2"><span>03</span> Replay</div><div class="mono" style="font-size:16px;margin-top:24px;letter-spacing:1px;line-height:1.7;color:#c6d3df">EXECUTION UPDATES WHAT COMES NEXT</div></div>
<div class="abs" id="piano-memory" style="left:64px;top:795px;width:925px;height:182px;background:#090e13e8;border:1px solid #f0d57e66;padding:22px"><div class="mono gold" style="font-size:19px;letter-spacing:2px">OBSERVED SEQUENCE · EXCERPT</div><div style="display:flex;gap:12px;margin-top:18px">'''+''.join(f'<div id="memory-frame{k}" style="width:280px;height:90px;overflow:hidden;border:2px solid #9fb2c8;position:relative"><img src="assets/generated/cases/piano-memory-{k+1}.png" style="width:100%;height:100%;object-fit:cover"><span class="mono" style="position:absolute;top:0;left:0;background:#102134;color:#f0d57e;font-size:16px;padding:2px 6px">0{k+1}</span></div>' for k in range(3))+f'''</div></div>
<div class="case-bottom" id="mind2act-bottom"><span>CP05 / PIANO REPLAY</span><span class="gold">REASON → ACT → UPDATE → REPEAT</span></div>'''
css='.piano-stage{font-size:26px;border-top:1px solid #e4e6d230;padding:13px 0;color:#c6d3df}.piano-stage span{font-family:"IBM Plex Mono",monospace;font-size:17px;margin-right:20px;color:#9fb2c8}'
js="tl.fromTo('#mind2act-surface',{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.4,ease:'power3.inOut'},0);"+in_('#mind2act-top',.12,'y:-35',.5)+in_('#mind2act-meta',.3,'x:35',.5)+in_('#mind2act-panel',.60,'x:60',.65)+in_('#piano-memory',1.50,'y:48',.6)+in_('#mind2act-bottom',.40,'y:20',.5)+"tl.to('#piano-stage0',{color:'#f0d57e',duration:.18},.74);tl.to('#piano-stage1',{color:'#f0d57e',duration:.18},1.6);tl.to('#piano-stage2',{color:'#f0d57e',duration:.18},3.08);tl.to('#mind2act-camera',{scale:1.07,x:30,y:18,duration:2.92,ease:'sine.out'},2.97);"
for k,t in [(0,1.60),(1,2.22),(2,2.81)]:
 js+=in_(f'#memory-frame{k}',t,'y:24',.32,'power3.out')
js+="tl.to('#piano-memory',{borderColor:'#f0d57e',duration:.3},3.2);"
scene(4,'mind2act',body,css,js)
# 6 — breadth, scale, difficulty
body=f'''<div id="scale-reel" class="abs" style="inset:0">{video('scale-fastmontage','montage/fast-montage.mp4',0,4.444444)}</div>
<div id="scale-reel-shade" class="abs" style="inset:0;background:#090e13;opacity:.38"></div>
<div class="abs" id="scale-label" style="left:74px;top:60px"><span class="mono label mint">BEYOND A SINGLE TASK</span></div>
<div class="abs" id="scale-word0" style="left:72px;top:690px;font-size:152px;letter-spacing:-7px;font-weight:600">Reason.</div><div class="abs" id="scale-word1" style="left:72px;top:690px;font-size:152px;letter-spacing:-7px;font-weight:600">Control.</div><div class="abs" id="scale-word2" style="left:72px;top:690px;font-size:152px;letter-spacing:-7px;font-weight:600">Coordinate.</div>
<div id="scale-stats" class="abs" style="inset:0;background:#102134"><div class="abs" style="left:0;right:0;bottom:0;height:330px;overflow:hidden;opacity:.3">{video('scale-mosaic','montage/all-cases-mosaic.mp4',4.35,5.2)}</div><div class="abs mono label mint" id="scale-stats-label" style="left:80px;top:82px">ONE BENCHMARK. THREE CAPABILITY SUITES.</div><div id="stat15" class="abs" style="left:105px;top:236px"><div class="stat-number moon">15</div><div class="stat-caption">Robotic tasks</div><div class="mono" style="font-size:20px;margin-top:24px;color:#9fb2c8">5 TASKS IN EACH SUITE</div></div><div class="abs" id="stat45" style="left:995px;top:236px"><div class="stat-number gold">45</div><div class="stat-caption">Task–difficulty configurations</div><div class="mono" style="font-size:20px;margin-top:24px;color:#c6d3df">MIND / ACT / MIND2ACT</div></div><div class="abs" id="stat-divider" style="left:915px;top:250px;height:475px;width:1px;background:#bdd9cc60"></div></div>
<div id="difficulty" class="abs" style="inset:0;background:#090e13"><div class="abs mono label mint" style="left:80px;top:74px" id="difficulty-label">THREE LEVELS. RISING DEMANDS.</div><div class="abs" style="left:78px;top:245px" id="difficulty-easy"><div class="difficulty-word moon">Easy</div><div class="difficulty-sub">Establish the fundamentals.</div></div><div class="abs" style="left:78px;top:245px" id="difficulty-medium"><div class="difficulty-word mint">Medium</div><div class="difficulty-sub">Raise the task demands.</div></div><div class="abs" style="left:78px;top:245px" id="difficulty-hard"><div class="difficulty-word gold">Hard</div><div class="difficulty-sub">Push memory, timing and control.</div></div><div class="abs" id="difficulty-bars" style="left:1160px;top:255px;width:665px"><div class="mono" style="font-size:20px;display:flex;justify-content:space-around;color:#c6d3df"><span>EASY</span><span>MEDIUM</span><span>HARD</span></div><div class="mono" style="font-size:19px;letter-spacing:1px;color:#9fb2c8;margin-top:45px">P / ITEMS TO DELIVER</div><div style="display:flex;justify-content:space-around;margin-top:16px;font-size:90px;color:#e4e6d2"><span id="delivery0">4</span><span id="delivery1">5</span><span id="delivery2">7</span></div><div class="hairline" style="margin-top:28px"></div><div class="mono" style="font-size:19px;letter-spacing:1px;color:#9fb2c8;margin-top:28px">CP05 / CANDIDATE KEYS</div><div style="display:flex;justify-content:space-around;margin-top:16px;font-size:90px;color:#bdd9cc"><span id="keys0">7</span><span id="keys1">14</span><span id="keys2">21</span></div></div><div class="abs" id="difficulty-axes" style="left:80px;right:80px;top:840px;display:flex;gap:32px"><span class="tag">MEMORY LOAD</span><span class="tag">PHASE DEPENDENCIES</span><span class="tag">PRECISION + CONTACT</span><span class="tag">RESPONSE WINDOWS</span></div><div class="abs mono steel" style="left:80px;top:977px;font-size:17px;letter-spacing:2px">EASY / MEDIUM / HARD</div></div>'''
css='.stat-number{font-size:300px;font-weight:500;line-height:1;letter-spacing:-18px;font-variant-numeric:tabular-nums}.stat-plus{font-size:95px;margin-left:70px;vertical-align:middle}.stat-caption{font-size:37px;margin-top:32px;letter-spacing:-1px}.difficulty-word{font-size:208px;line-height:1.1;font-weight:500;letter-spacing:-10px}.difficulty-sub{font-size:35px;color:#c6d3df;margin-top:30px}.levelbar{width:140px;transform-origin:bottom center;position:relative}.levelbar:after{content:"";position:absolute;inset:14px;border:1px solid #10213433}'
js="tl.fromTo('#scale-surface',{clipPath:'inset(0% 0% 0% 100%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.3,ease:'power3.inOut'},0);"+in_('#scale-label',.20,'x:-35',.5)+in_('#scale-word0',.23,'y:110',.40,'expo.out')+"tl.set('#scale-word0',{opacity:0},1.48);"+in_('#scale-word1',1.48,'y:100',.38,'expo.out')+"tl.set('#scale-word1',{opacity:0},2.96);"+in_('#scale-word2',2.96,'y:100',.4,'expo.out')+"tl.fromTo('#scale-stats',{clipPath:'inset(100% 0% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.45,ease:'power3.inOut'},4.15);"+in_('#scale-stats-label',4.4,'y:24',.5)+in_('#stat15',4.5,'y:160,scale:.9',.65,'expo.out')+in_('#stat45',5.12,'y:160,scale:.9',.65,'expo.out')+"tl.fromTo('#stat-divider',{scaleY:0},{scaleY:1,duration:.7,ease:'power2.out'},5.0);tl.fromTo('#difficulty',{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.45,ease:'power3.inOut'},7.77);"+in_('#difficulty-label',7.95,'y:20',.5)+in_('#difficulty-easy',8.1,'y:100',.4,'expo.out')+"tl.set('#difficulty-easy',{opacity:0},9.45);"+in_('#difficulty-medium',9.45,'y:100',.4,'expo.out')+"tl.set('#difficulty-medium',{opacity:0},10.81);"+in_('#difficulty-hard',10.81,'y:100',.4,'expo.out')+in_('#difficulty-axes',8.30,'y:40',.5)+"tl.fromTo('#difficulty-bars',{opacity:0,x:80},{opacity:1,x:0,duration:.6,ease:'expo.out'},8.15);tl.to(['#delivery0','#keys0'],{color:'#f0d57e',duration:.2},8.2);tl.to(['#delivery1','#keys1'],{color:'#f0d57e',duration:.2},9.5);tl.to(['#delivery2','#keys2'],{color:'#f0d57e',duration:.2},10.85);"
scene(5,'scale',body,css,js)
# 7 — open call
body=f'''<div class="abs" id="outro-linefield" style="inset:0" data-layout-ignore><svg width="1920" height="1080"><ellipse cx="960" cy="442" rx="760" ry="290" fill="none" stroke="#9fb2c8" stroke-opacity=".22"/><ellipse cx="960" cy="442" rx="660" ry="390" fill="none" stroke="#bdd9cc" stroke-opacity=".12"/><path d="M0 1000 L1920 200 M0 830 L1920 30" stroke="#9fb2c8" stroke-opacity=".1"/></svg></div>
<img id="outro-logo" class="abs" src="{logo}" style="left:829px;top:62px;width:262px;height:262px">
<div id="outro-brand" class="abs" style="left:0;right:0;top:335px;text-align:center;font-size:88px;font-weight:500;letter-spacing:-4px">Mind2Act <span class="moon">World</span></div>
<div id="outro-call" class="abs" style="left:190px;top:490px;width:1540px;text-align:center;font-size:69px;font-weight:500;letter-spacing:-2px">Call for <span class="mint">contributors</span> &amp; <span class="gold">evaluations</span>.</div>
<div id="outro-sub" class="abs" style="left:0;right:0;top:615px;text-align:center;font-size:32px;color:#c6d3df">Contribute new tasks. Evaluate your agents. Build with us.</div>
<div id="outro-rule" class="abs accent-rule" style="left:635px;top:718px;width:650px;height:2px"></div>
<div id="outro-url" class="abs mono" style="left:0;right:0;top:775px;text-align:center;font-size:32px;letter-spacing:0;color:#e4e6d2">kkun616826.github.io/mind2act-preview</div>
<div class="abs mono" id="outro-footer" style="left:0;right:0;top:960px;text-align:center;font-size:20px;letter-spacing:4px;color:#9fb2c8">REASONING AND ACTION. EVALUATED TOGETHER.</div>'''
css=''
js="tl.fromTo('#outro-surface',{clipPath:'circle(0% at 50% 30%)'},{clipPath:'circle(100% at 50% 30%)',duration:.62,ease:'power3.inOut'},0);"+in_('#outro-logo',.12,'scale:.70,rotation:-12',.9,'expo.out')+in_('#outro-brand',.40,'y:35',.65)+in_('#outro-call',.72,'y:75',.7,'expo.out')+in_('#outro-sub',1.04,'y:25',.6,'sine.out')+"tl.fromTo('#outro-rule',{scaleX:0},{scaleX:1,duration:.7,ease:'power2.inOut'},1.24);"+in_('#outro-url',1.35,'y:24',.6)+in_('#outro-footer',1.55,'y:20',.65)+"tl.fromTo('#outro-linefield',{scale:.88,rotation:-5},{scale:1.05,rotation:3,duration:5.18,ease:'sine.inOut'},0);tl.to('#outro-surface',{opacity:0,duration:.40,ease:'power2.in'},4.785185);"
scene(6,'outro',body,css,js)
# Keep image references and renamed CP05 copy aligned with refreshed derivatives.
refresh_refs={
 'assets/generated/cases/p-order-blue-crop.png':f'{media_root}/cases/p-order-green-crop.png',
 'assets/generated/cases/pr3-target-crop.png':f'{media_root}/cases/pr3-target-crop.png',
 'assets/generated/cases/piano-memory-':f'{media_root}/cases/piano-memory-',
 f'{media_root}/cases/piano-cover.mp4':f'{media_root}/cases/piano-setup.mp4',
 'id="piano-reveal"':'id="piano-setup"',
 '> Reveal</div>':'> Prepare</div>',
}
for composition in C.glob('*.html'):
 html_text=composition.read_text()
 for old,new in refresh_refs.items():
  html_text=html_text.replace(old,new)
 for enhanced in (P/'assets/generated/clarity-20261010-155258').rglob('*.mp4'):
  relative=enhanced.relative_to(P/'assets/generated/clarity-20261010-155258').as_posix()
  html_text=html_text.replace(f'{media_root}/{relative}',f'assets/generated/clarity-20261010-155258/{relative}')
 # User-selected first-version meal-packing footage, preserving the existing timeline.
 if composition.name=='03-mind.html':
  for name in ['p-intro','p-action1','p-action2']:
   html_text=html_text.replace(f'assets/generated/clarity-20261010-155258/cases/{name}.mp4',f'assets/generated/cases/{name}.mp4')
  html_text=html_text.replace(f'{media_root}/cases/p-order-green-crop.png','assets/generated/cases/p-order-blue-crop.png')
 composition.write_text(html_text)
# root scene windows overlap by outgoing tail so incoming masks have a full image underneath
names=['intro','motivation','mind','act','mind2act','scale','outro']
rootfonts=fonts.replace("assets/","assets/")
hosts=''
for i,name in enumerate(names):
 dur=starts[i+1]-starts[i]
 if i<len(names)-1:dur+=.62
 hosts+=f'<div id="scene-{name}" class="clip" data-composition-id="{name}" data-composition-src="compositions/{i+1:02d}-{name}.html" data-start="{starts[i]:.6f}" data-duration="{dur:.6f}" data-track-index="{i+1}" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:{i+1}"></div>\n'
# audio inserted after audio agent has delivered; add automatically when present
track=''
for candidate in ['assets/generated/audio/soundtrack.wav','assets/generated/audio/master.wav','assets/generated/audio/final-mix.wav']:
 if (P/candidate).exists():
  track=f'<audio id="soundtrack" class="clip" src="{candidate}" data-start="0" data-duration="{D:.6f}" data-track-index="20" data-volume="1"></audio>';break
index=f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080"><title>Mind2Act World — Reasoning into action</title><script src="assets/lib/gsap.min.js"></script><style>{rootfonts} *{{box-sizing:border-box}}html,body{{margin:0;width:1920px;height:1080px;background:#090e13;overflow:hidden}}#root{{position:relative;width:100%;height:100%;overflow:hidden}}</style></head><body><div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="{D:.6f}" data-fps="30">{hosts}{track}</div><script>const tl=gsap.timeline({{paused:true}});tl.to({{progress:0}},{{progress:1,duration:{D},ease:'none'}},0);window.__timelines['main']=tl;</script></body></html>'''
(P/'index.html').write_text(index)
(P/'.production/edit-timing.json').write_text(json.dumps(dict(duration=D,bpm=81,scenes=[dict(id=n,start=starts[i],end=starts[i+1]) for i,n in enumerate(names)]),indent=2))
print('Created',len(names),'scenes',D)
