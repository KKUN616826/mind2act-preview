from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
p=Path.cwd();ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg';fp='/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe';src=p/'renders/mind2act-world-promo-1080p-20261010-125815.mp4'
o=p/'qa/rendered';o.mkdir(exist_ok=True)
times=[0.13,.9,1.8,3.4,8.7,10.5,12.9,15.3,18.3,21.9,25.8,27.8,31.5,35.8,38.4,40.9,45.1,46.7]
for i,t in enumerate(times):
 subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(src),'-frames:v','1','-vf','scale=640:360',str(o/f'{i:02d}.jpg')],check=True)
for offset in [0,9]:
 sheet=Image.new('RGB',(1920,1170),'#101820');d=ImageDraw.Draw(sheet)
 for i in range(offset,min(offset+9,len(times))):
  x=((i-offset)%3)*640;y=((i-offset)//3)*390;sheet.paste(Image.open(o/f'{i:02d}.jpg'),(x,y));d.text((x+14,y+365),f'{times[i]:.2f}s',fill='#e4e6d2')
 sheet.save(o/f'contact-sheet-{offset//9+1}.jpg',quality=92)
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss','3.5','-i',str(src),'-frames:v','1','-q:v','2',str(p/'renders/mind2act-world-poster.jpg')],check=True)
j=json.loads(subprocess.check_output([fp,'-v','error','-show_format','-show_streams','-of','json',str(src)]));(o/'ffprobe-master.json').write_text(json.dumps(j,indent=2))
r=subprocess.run([ff,'-hide_banner','-v','error','-i',str(src),'-f','null','-'],capture_output=True,text=True);(o/'decode-check.txt').write_text('exit_code='+str(r.returncode)+'\n'+r.stderr);print('decode',r.returncode)
subprocess.run([ff,'-hide_banner','-i',str(src),'-vf','blackdetect=d=0.10:pix_th=0.12','-an','-f','null','-'],stderr=open(o/'blackdetect.txt','w'),stdout=subprocess.DEVNULL)
print('master',j['format']['duration'],j['format']['size']);print('sheets ready')
