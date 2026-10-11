from pathlib import Path
import json,subprocess
base=Path(__file__).resolve().parent
run=json.loads((base/'export.json').read_text())
out=base/'rendered';out.mkdir(exist_ok=True)
ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
for t in [3.5,9,20.5,28.6,33.1,39.2,42.25,43.9,45.25,47.8,52.7,53.95,54.6,55.2,55.95,56.5,57.15,57.9,58.6,59.2,60.4,62.9,64.7,70,73.5]:
 subprocess.run([ff,'-v','error','-ss',str(t),'-i',run['master'],'-frames:v','1','-q:v','2','-y',str(out/f"frame-{str(t).replace('.', '-')}.jpg")],check=True)
for name,start,dur,fps in [('montage',41.7,6,1.3333333),('easy-action',54.1,1.6,5),('medium-action',56.1,1.6,5),('hard-action',57.7,2.4,3.3333333)]:
 subprocess.run([ff,'-v','error','-ss',str(start),'-i',run['master'],'-t',str(dur),'-vf',f'fps={fps},scale=640:360,tile=4x2','-frames:v','1','-q:v','2','-y',str(out/(name+'-sheet.jpg'))],check=True)
subprocess.run([ff,'-v','error','-i',run['master'],'-vf','fps=1/8.3,scale=640:360,tile=3x3','-frames:v','1','-q:v','2','-y',str(out/'contact-sheet.jpg')],check=True)
print(out)
