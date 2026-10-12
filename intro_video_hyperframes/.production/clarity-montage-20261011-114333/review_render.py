from pathlib import Path
import json, subprocess
work = Path(__file__).resolve().parent
run = json.loads((work/'export.json').read_text())
out = work/'rendered'
out.mkdir(exist_ok=True)
ff = '/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
for time in [3.5,10,14,20.5,26,28.6,31.8,32.55,32.85,33.15,33.45,33.65,36.2,39.2,42.25,43.9,45.25,46.85,47.8,52.7,54.3,56.5,58.8,60.4,62.9,64.7,70,73.8]:
    subprocess.run([ff,'-v','error','-ss',str(time),'-i',run['master'],'-frames:v','1','-q:v','2','-y',str(out/f"frame-{str(time).replace('.', '-')}.jpg")], check=True)
subprocess.run([ff,'-v','error','-i',run['master'],'-vf','fps=1/8.3,scale=640:360,tile=3x3','-frames:v','1','-q:v','2','-y',str(out/'contact-sheet.jpg')], check=True)
for name,start,duration,fps in [('return-arrow',32.45,1.6,5),('montage',41.7,6,1.3333333)]:
    subprocess.run([ff,'-v','error','-ss',str(start),'-i',run['master'],'-t',str(duration),'-vf',f'fps={fps},scale=640:360,tile=4x2','-frames:v','1','-q:v','2','-y',str(out/(name+'-sheet.jpg'))], check=True)
print(out)
