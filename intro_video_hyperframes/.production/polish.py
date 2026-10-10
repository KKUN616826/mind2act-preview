from pathlib import Path
p=Path('.production/build_film.py');s=p.read_text()
s=s.replace('When robots fail, where does it break?','When robots fail, what breaks down?')
s=s.replace('100% 34%,34% 100%','100% 3%,3% 100%').replace('100% 33%,100% 100%,33% 100%','100% 3%,100% 100%,3% 100%')
s=s.replace('<span class="stat-plus gold">×</span>','')
s=s.replace('Add dependencies and precision.','Raise the task demands.')
s=s.replace("def casetop(n,label,sub,code):\n return", "def casetop(n,label,sub,code):\n case_logo={'mind':'assets/logos/Mind2Act-三个Logo-高清透明版/01-Mind-1308x1203.png','act':'assets/logos/Mind2Act-三个Logo-高清透明版/02-Act-1268x1241.png'}.get(n,logo)\n return")
s=s.replace('class="case-mark" src="{logo}"','class="case-mark" src="{case_logo}"')
# Shrink piano side panel and keep the keyboard and mallets clear.
s=s.replace('style="top:222px;width:338px"','style="top:178px;right:48px;width:286px;padding:20px"')
s=s.replace('.piano-stage{font-size:29px;', '.piano-stage{font-size:26px;').replace('padding:20px 0;color:#c6d3df','padding:13px 0;color:#c6d3df')
s=s.replace('left:64px;top:808px;width:835px;height:135px','left:64px;top:795px;width:925px;height:182px')
s=s.replace('OBSERVE → RETAIN → REPLAY</div><div style="display:flex;gap:12px;margin-top:18px">','OBSERVED SEQUENCE · EXCERPT</div><div style="display:flex;gap:12px;margin-top:18px">')
a=s.index("'''+''.join(f'<div id=\"memory-key")
b=s.index("+f'''</div></div>",a)
s=s[:a]+"'''+''.join(f'<div id=\"memory-frame{k}\" style=\"width:280px;height:90px;overflow:hidden;border:2px solid #9fb2c8;position:relative\"><img src=\"assets/generated/cases/piano-memory-{k+1}.png\" style=\"width:100%;height:100%;object-fit:cover\"><span class=\"mono\" style=\"position:absolute;top:0;left:0;background:#102134;color:#f0d57e;font-size:16px;padding:2px 6px\">0{k+1}</span></div>' for k in range(3))"+s[b:]
a=s.index('for k,t in [(2,1.72)');b=s.index("scene(4,'mind2act'",a)
s=s[:a]+'''for k,t in [(0,1.60),(1,2.22),(2,2.81)]:
 js+=in_(f'#memory-frame{k}',t,'y:24',.32,'power3.out')
js+="tl.to('#piano-memory',{borderColor:'#f0d57e',duration:.3},3.2);"
'''+s[b:]
# Replace generic difficulty bars with verified task-specific quantities.
a=s.index('<div class="abs" id="difficulty-bars"');b=s.index('<div class="abs" id="difficulty-axes"',a)
s=s[:a]+'''<div class="abs" id="difficulty-bars" style="left:1160px;top:255px;width:665px"><div class="mono" style="font-size:20px;display:flex;justify-content:space-around;color:#c6d3df"><span>EASY</span><span>MEDIUM</span><span>HARD</span></div><div class="mono" style="font-size:19px;letter-spacing:1px;color:#9fb2c8;margin-top:45px">P / ITEMS TO DELIVER</div><div style="display:flex;justify-content:space-around;margin-top:16px;font-size:90px;color:#e4e6d2"><span id="delivery0">4</span><span id="delivery1">5</span><span id="delivery2">7</span></div><div class="hairline" style="margin-top:28px"></div><div class="mono" style="font-size:19px;letter-spacing:1px;color:#9fb2c8;margin-top:28px">CP05 / CANDIDATE KEYS</div><div style="display:flex;justify-content:space-around;margin-top:16px;font-size:90px;color:#bdd9cc"><span id="keys0">7</span><span id="keys1">14</span><span id="keys2">21</span></div></div>'''+s[b:]
a=s.index("tl.fromTo('#levelbar0'");b=s.index('"\nscene(5',a)
s=s[:a]+"tl.fromTo('#difficulty-bars',{opacity:0,x:80},{opacity:1,x:0,duration:.6,ease:'expo.out'},8.15);tl.to(['#delivery0','#keys0'],{color:'#f0d57e',duration:.2},8.2);tl.to(['#delivery1','#keys1'],{color:'#f0d57e',duration:.2},9.5);tl.to(['#delivery2','#keys2'],{color:'#f0d57e',duration:.2},10.85);"+s[b:]
# Keep last case pictures alive underneath incoming wipe.
s=s.replace('4.22,1.705926','4.22,2.325926').replace('1.15,4.775926','1.15,5.395926').replace('2.962963,2.962963','2.962963,3.582963')
p.write_text(s)
