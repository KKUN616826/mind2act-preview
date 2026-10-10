from pathlib import Path
from PIL import Image,ImageChops,ImageStat
import io,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
MASTER=ROOT/'renders/mind2act-world-promo-1080p-20261010-221251.mp4'
OUT=ROOT/'.production/categories-20261010-215252'
def frame(t):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(MASTER),'-frames:v','1','-f','image2pipe','-vcodec','png','-']);return Image.open(io.BytesIO(b)).convert('RGB')
def stats(a,b,roi):
 a=a.crop(roi);b=b.crop(roi);dif=ImageChops.difference(a,b);grey=dif.convert('L');h=grey.histogram();return {'mean_abs_difference':round(sum(ImageStat.Stat(dif).mean)/3,4),'fraction_pixels_diff_gt8':round(sum(h[9:])/sum(h),5),'identical':a.tobytes()==b.tobytes()}
times=[49,50,51,52];frames=[frame(t) for t in times]
groups=[['E','F','P','S','M'],['FR1','FR2','PR1','PR2','PR3'],['CP01','CP02','CP03','CP04','CP05']]
tiles={}
for g,codes in enumerate(groups):
 for r,c in enumerate(codes):
  x=72+g*608;y=312+r*137;roi=(x+4,y+4,x+236,y+122)
  s=[stats(frames[i],frames[i+1],roi) for i in range(len(frames)-1)]
  tiles[c]={'roi':roi,'comparisons':[{'from':times[i],'to':times[i+1],**s[i]}for i in range(len(s))]}
times2=[60.7,61.3,62.2];frames2=[frame(t) for t in times2];rows={}
for i,c in enumerate(['Easy','Medium','Hard']):
 x=614;y=254+i*239;roi=(x+5,y+5,x+427,y+221)
 rows[c]={'roi':roi,'comparisons':[{'from':times2[j],'to':times2[j+1],**stats(frames2[j],frames2[j+1],roi)}for j in range(len(frames2)-1)]}
res={'master':str(MASTER.relative_to(ROOT)),'sha256':hashlib.sha256(MASTER.read_bytes()).hexdigest(),'method':'Actual decoded MP4 RGB crop differences; only video image ROI, excluding text/borders/label animations. Mean 0..255. Nonzero difference alone does not prove semantic motion; contact sheets also visually inspected.','wall':tiles,'difficulty':rows}
json.dump(res,open(OUT/'export-review-breadth-metrics.json','w'),indent=2)
for name,vals in [('wall',tiles),('difficulty',rows)]:
 for c,v in vals.items():print(name,c,[(z['mean_abs_difference'],z['fraction_pixels_diff_gt8']) for z in v['comparisons']])
