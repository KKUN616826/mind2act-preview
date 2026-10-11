"""Capture evidence from the actual encoded delivery, not browser snapshots."""
from pathlib import Path
import json
import subprocess

work = Path(__file__).resolve().parent
run = json.loads((work/'export.json').read_text())
out = work/'rendered'
out.mkdir(exist_ok=True)
ff = '/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
for time in [3.5, 8.5, 54.3, 56.5, 58.8, 59.8, 59.95, 60.08, 60.4, 61.4, 62.3, 63.2, 64.7, 67.2, 73.8]:
    subprocess.run([ff, '-v', 'error', '-ss', str(time), '-i', run['master'], '-frames:v', '1', '-q:v', '2', '-y', str(out/f"frame-{str(time).replace('.', '-')}.jpg")], check=True)
subprocess.run([ff, '-v', 'error', '-i', run['master'], '-vf', 'fps=1/8.3,scale=640:360,tile=3x3', '-frames:v', '1', '-q:v', '2', '-y', str(out/'contact-sheet.jpg')], check=True)
subprocess.run([ff, '-v', 'error', '-ss', '59.55', '-i', run['master'], '-t', '1', '-vf', 'fps=8,scale=640:360,tile=4x2', '-frames:v', '1', '-q:v', '2', '-y', str(out/'handoff-sheet.jpg')], check=True)
subprocess.run([ff, '-v', 'error', '-ss', '62.33', '-i', run['master'], '-t', '1.6', '-vf', 'fps=5,scale=640:360,tile=4x2', '-frames:v', '1', '-q:v', '2', '-y', str(out/'cover-sheet.jpg')], check=True)
subprocess.run([ff, '-v', 'error', '-ss', '60.4', '-i', run['web'], '-frames:v', '1', '-vf', 'scale=960:540', '-q:v', '2', '-y', str(out/'comparison-web-960.jpg')], check=True)
print(out)
