from pathlib import Path
import json, subprocess
work=Path(__file__).resolve().parent
run=json.loads((work/'export.json').read_text())
out=work/'rendered';out.mkdir(exist_ok=True)
ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
for time in [6.2,8.5,11.5]:
 subprocess.run([ff,'-v','error','-ss',str(time),'-i',run['master'],'-frames:v','1','-q:v','2','-y',str(out/f"frame-{str(time).replace('.', '-')}.jpg")],check=True)
subprocess.run([ff,'-v','error','-i',run['master'],'-vf','fps=1/8.23,scale=640:360,tile=3x3','-frames:v','1','-q:v','2','-y',str(out/'contact-sheet.jpg')],check=True)
print(out)
