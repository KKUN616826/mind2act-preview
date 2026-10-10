from pathlib import Path
import json,subprocess,concurrent.futures,time
root=Path('.'); out=root/'assets/generated/montage'; out.mkdir(parents=True,exist_ok=True)
inv=json.loads((root/'.production/audit/video-inventory.json').read_text()); vids=[v for v in inv if '/videos/' in v['path']]
# Every task family and all three difficulty variants appear in the wall.
def task(v): return Path(v['path']).parts[3]
def start(v):
 p=v['path']; t=task(v);d=v['duration']
 if t=='P': return 17.0 if 'hard' in p else 15.5
 if t=='PR3': return 23.0
 if t=='CP05': return 34.0 if 'Easy' in p else (70.0 if 'Medium' in p else 96.0)
 if t=='CP02': return 41.0 if 'easy' in p else (59.0 if 'medium' in p else 81.0)
 return min(d-6,max(1,d*.4))
def run(args):
 p=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y']+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-4000:])
def base(p,s): return ['-threads','1','-ss',str(s),'-i',p]
def encode(v,path,w,h,duration,speed=1,grid=False,start_override=None):
 s=start(v) if start_override is None else start_override
 vf=[]
 if task(v)=='CP02':vf.append('crop=iw:ih-64:0:64')
 if task(v)=='CP03':vf.append('crop=iw:ih-36:0:36')
 # 16:9 crop stays high enough to keep the tabletop and useful arm motion.
 if w/h>1.6: vf.append('crop=iw:iw*9/16:0:ih*0.05')
 if speed!=1:vf.append(f'setpts=(PTS-STARTPTS)/{speed}')
 else:vf.append('setpts=PTS-STARTPTS')
 tw,th=(w-2,h-2) if grid else (w,h)
 vf += [f'scale={tw}:{th}:force_original_aspect_ratio=increase:flags=lanczos',f'crop={tw}:{th}', 'setsar=1','fps=30']
 if grid:vf.append(f'pad={w}:{h}:0:0:color=0x060911')
 run(base(v['path'],s)+['-vf',','.join(vf),'-t',str(duration),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','1','-movflags','+faststart',str(path)])
 return {'source':v['path'],'source_start':s,'source_end':s+duration*speed,'speed':speed,'duration':duration,'path':str(path),'width':w,'height':h}
records=[]
def cell(args):
 i,v=args;p=out/f'cell-{i:02d}-{task(v).lower()}.mp4';r=encode(v,p,240,180,5.5,grid=True)
 print(f'cell {i+1}/45 {task(v)}',flush=True);return r
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: records=list(pool.map(cell,enumerate(vids)))
# Interleave families/difficulties so adjacent tiles look diverse.
idx=[]
for level in range(3):
 for family in range(15):idx.append(family*3+level)
idx+= [24,13,43]
layout='|'.join(f'{(i%8)*240}_{(i//8)*180}' for i in range(48))
args=[]
for i in idx: args += ['-threads','1','-i',records[i]['path']]
filt=''.join(f'[{i}:v]' for i in range(48))+f'xstack=inputs=48:layout={layout}:fill=0x060911[v]'
run(args+['-filter_complex_threads','1','-filter_complex',filt,'-map','[v]','-t','5.5','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','4','-movflags','+faststart',str(out/'all-cases-mosaic.mp4')])
print('ALL CASES MOSAIC READY',flush=True)
# Six distinct actions span three axes, not six similar variants.
six_fams=['P','PR3','CP05','E','CP02','CP04'];six=[]
for fam in six_fams:
 candidates=[v for v in vids if task(v)==fam]
 v=next((v for v in candidates if ('hard' in v['path'] if fam=='P' else 'Medium' in v['path'] if fam=='CP05' else 'easy' in v['path'] or 'Easy' in v['path'])),candidates[0])
 six.append(encode(v,out/f'six-{fam.lower()}.mp4',640,540,1.5,grid=True))
args=[]
for r in six:args += ['-threads','1','-i',r['path']]
layout='|'.join(f'{(i%3)*640}_{(i//3)*540}' for i in range(6))
filt=''.join(f'[{i}:v]' for i in range(6))+f'xstack=inputs=6:layout={layout}:fill=0x060911[v]'
run(args+['-filter_complex_threads','1','-filter_complex',filt,'-map','[v]','-t','1.5','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','4','-movflags','+faststart',str(out/'six-cases-mosaic.mp4')])
print('SIX CASES MOSAIC READY',flush=True)
# 12 complementary task families: 3 MIND, 4 ACT, 4 MIND2ACT plus the remaining MIND.
quick_fams=['E','FR1','CP02','F','PR1','CP03','M','FR2','CP04','S','PR2','CP01']
quick=[]
for fam in quick_fams:
 candidates=[v for v in vids if task(v)==fam]
 v=next((v for v in candidates if ('hard' in v['path'] if fam=='F' else ('Hard' in v['path'] if fam=='CP03' else ('easy' in v['path'] or 'Easy' in v['path'])))),candidates[0])
 quick.append((v,out/f'quick-{fam.lower()}.mp4'))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: quick_records=list(pool.map(lambda x:encode(x[0],x[1],1280,720,1.1,speed=2),quick))
# 0.37037s is half a beat at 81 BPM. Set boundaries to nearest 30fps frame; total 134f=4.4667s.
args=[]
for r in quick_records:args+=['-threads','1','-i',r['path']]
frame_counts=[11]*10+[12]*2
filt=';'.join(f'[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS[q{i}]' for i,n in enumerate(frame_counts))+';'+''.join(f'[q{i}]' for i in range(12))+'concat=n=12:v=1:a=0[v]'
run(args+['-filter_complex_threads','1','-filter_complex',filt,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-threads','4','-movflags','+faststart',str(out/'fast-montage.mp4')])
prov={'generated_at':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'raw_sources_modified':False,'fps':30,'mosaic_all':{'path':str(out/'all-cases-mosaic.mp4'),'duration':5.5,'resolution':[1920,1080],'layout':[8,6],'source_count':45,'slots':48,'slot_source_indices':idx,'cells':records},'mosaic_six':{'path':str(out/'six-cases-mosaic.mp4'),'duration':1.5,'resolution':[1920,1080],'cells':six},'fast_reel':{'path':str(out/'fast-montage.mp4'),'duration':sum(frame_counts)/30,'resolution':[1280,720],'task_order':quick_fams,'frames_per_cut':frame_counts,'cuts':quick_records}}
(root/'.production/montage-provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2))
print('ALL ASSETS READY',flush=True)
