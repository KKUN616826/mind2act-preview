from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,json,concurrent.futures
root=Path('.')
audit=root/'.production/audit'
inv=json.loads((audit/'video-inventory.json').read_text())
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
def frame(p,t,w=384):
 raw=subprocess.check_output(['ffmpeg','-loglevel','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf',f'scale={w}:-1','-f','image2pipe','-vcodec','mjpeg','-threads','1','-'])
 from io import BytesIO
 return Image.open(BytesIO(raw)).convert('RGB')
def sheet(name,items,cols,w=384,h=288):
 out=Image.new('RGB',(cols*w,((len(items)+cols-1)//cols)*(h+42)),(8,12,18)); d=ImageDraw.Draw(out)
 def get(item):
  p,t,label=item
  im=frame(p,t,w); im.thumbnail((w,h)); return im
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  ims=list(pool.map(get,items))
 for i,(im,item) in enumerate(zip(ims,items)):
  x=(i%cols)*w;y=(i//cols)*(h+42)
  out.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))
  d.text((x+6,y+h+3),item[2],fill='white',font=font)
  d.text((x+6,y+h+22),f'{item[1]:.2f} sec',fill=(80,205,235),font=font)
 out.save(audit/name)
heroes=[v for v in inv if ('/Mind/P/P_' in v['path'] or '/Act/PR3/' in v['path'] or '/Mind2Act/CP05/' in v['path'] or '/reference-videos/' in v['path'])]
for v in heroes:
 stem=Path(v['path']).stem
 times=[(v['duration']-1)*i/11 for i in range(12)]
 sheet(stem+'.jpg',[(v['path'],t,stem[:40]) for t in times],4)
all_items=[]
for v in inv:
 if '/reference-videos/' in v['path']:continue
 label='/'.join(Path(v['path']).parts[2:])
 all_items.append((v['path'],v['duration']*.4,label[:40]))
for i in range(0,len(all_items),15):
 sheet(f'all-cases-{i//15+1}.jpg',all_items[i:i+15],5,320,240)
print('Saved',len(heroes)+3,'contact sheets')
