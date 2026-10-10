import json,hashlib,subprocess,concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/generated/categories-20261010-215252';OUT.mkdir(exist_ok=True,parents=True)
AUD=json.load(open(ROOT/'.production/source-refresh-audit.json'))
med={Path(v['path']).parts[3]:v for v in AUD['videos'] if 'medium' in v['path'].lower()}
starts={'E':43,'F':1,'P':0,'S':38,'M':51,'FR1':13,'FR2':7,'PR1':1,'PR2':9,'PR3':12,'CP01':58,'CP02':49,'CP03':84,'CP04':65,'CP05':44}
recs=[]
def make(args):
 task,st=args;v=med[task];src=ROOT/v['path'];out=OUT/(task.lower()+'-wall.mp4')
 if task=='P':
  files=['assets/generated/cases/p-intro.mp4','assets/generated/cases/p-action1.mp4','assets/generated/cases/p-action2.mp4'];lst=OUT/'p-inputs.txt';lst.write_text(''.join("file '"+str(ROOT/f)+"'\n" for f in files));cmd=['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-vf','scale=640:360:flags=lanczos,setsar=1','-an','-c:v','libx264','-crf','19','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(out)];r={'task':task,'source':files,'source_sha256':[hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files],'note':'Selected historical blue-cup excerpts preserved at their prior edited speeds; concatenate, no repeats, no event labels.','output':str(out.relative_to(ROOT))}
 else:
  cmd=['ffmpeg','-v','error','-y','-ss',str(st),'-i',str(src),'-t','8','-vf','crop=640:334:0:0,setsar=1','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
  r={'task':task,'source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'start':st,'end':st+8,'speed':1,'crop':'Full source width, first334rows: main camera; wrist strips excluded.','output':str(out.relative_to(ROOT))}
 subprocess.run(cmd,check=True);return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:recs=list(ex.map(make,starts.items()))
for lv in ['easy','medium','hard']:
 src=ROOT/f'assets/videos/Mind/F/F__F_{lv}.mp4';out=OUT/f'f-{lv}-probe.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-ss','0.5','-i',str(src),'-t','10','-vf','crop=640:334:0:0,scale=1280:668:flags=lanczos,setsar=1','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 recs.append({'task':'F','level':lv,'source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'start':.5,'end':10.5,'speed':1,'crop':'640x334 at0,0; entire platform and button array preserved; wrist strips excluded.','phase':'Initial exploration of the fixed unknown button mapping, samephase across3levels; no navigation/progress outcomes authored.','output':str(out.relative_to(ROOT))})
json.dump(recs,open(ROOT/'.production/categories-20261010-215252/breadth-difficulty-provenance.json','w'),indent=2,ensure_ascii=False)
