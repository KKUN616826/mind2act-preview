from pathlib import Path
import json
r=json.loads(Path('.production/audio/audio-timing.json').read_text())
wrap={
'intro':'Introducing Mind2Act World.\nReasoning and action, evaluated together.',
'motivation':'When robots fail, is it the decision,\nthe execution, or how they work together?',
'mind':'Mind tracks progress, understands rules,\nand decides what comes next.',
'act':'Act turns intent into precise motion,\nthrough geometry, contact, and timing.',
'mind2act':'Mind2Act closes the loop.\nExecution reshapes the plan, step by step.',
'ending':'Contribute new tasks. Evaluate agents.\nMind2Act World.'}
def tc(t):
 ms=round(t*1000);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60)
 return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
rows=[]
for i,l in enumerate(r['voice'],1):
 rows.append(f"{i}\n{tc(l['start'])} --> {tc(l['end'])}\n{wrap.get(l['id'],l['text'])}\n")
Path('assets/generated/audio/narration.srt').write_text('\n'.join(rows))
Path('assets/generated/audio/narration.txt').write_text('\n\n'.join(wrap.get(l['id'],l['text']).replace('\n',' ') for l in r['voice'])+'\n')
