from pathlib import Path
import json, subprocess, shutil, hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

run=Path(__file__).resolve().parent
root=run.parent.parent
ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
fp='/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe'
stamp='20261010-163109'
master=root/f'renders/mind2act-world-promo-1080p-{stamp}.mp4'
web=root/f'renders/mind2act-world-promo-web-{stamp}.mp4'
subprocess.run([ff,'-nostdin','-v','error','-i',str(master),'-c:v','libx264','-crf','18','-preset','medium','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(web)],check=True)
for t,name in [(15,'restored-mind.png'),(13,'restored-order.png')]:
 subprocess.run([ff,'-nostdin','-v','error','-ss',str(t),'-i',str(master),'-frames:v','1',str(run/name)],check=True)
delivery=root/'renders/delivery.json'
shutil.copy2(delivery,root/'renders/delivery-20261010-160400.json')
data=json.loads(delivery.read_text())
data['created_at']=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
data['id']=f'mind2act-world-promo-{stamp}'
for role,file in [('master',master),('web',web)]:
 subprocess.run([ff,'-nostdin','-v','error','-i',str(file),'-f','null','-'],check=True)
 p=json.loads(subprocess.check_output([fp,'-v','error','-show_streams','-show_format','-of','json',str(file)]))
 v=next(s for s in p['streams'] if s['codec_type']=='video')
 a=next(s for s in p['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
 assert abs(float(p['format']['duration'])-47.433333)<0.01
 data[role]=str(file.relative_to(root))
 data['files'][role]={'path':data[role],'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'duration':float(p['format']['duration']),'video_codec':v['codec_name'],'pixel_format':v['pix_fmt'],'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'audio_codec':a['codec_name'],'audio_sample_rate':a['sample_rate'],'audio_channels':a['channels']}
data['meal_packing_restore']={'run':str(run.relative_to(root)),'manifest':str((run/'manifest.json').relative_to(root)),'scope':'First-version meal-packing spotlight and matching order still; timeline unchanged'}
data['clarity_restoration']['scope']='Act and Mind2Act featured cases, six-tile intro and rapid montage; meal-packing spotlight now restored to first-version footage'
delivery.write_text(json.dumps(data,indent=2)+'\n')
readme=root/'renders/README.md'
text=readme.read_text().replace('promo-1080p-20261010-160400','promo-1080p-'+stamp).replace('promo-web-20261010-160400','promo-web-'+stamp)
text+='\n## First-version meal-packing restoration\n\nThe meal-packing spotlight uses its three original first-version clips and matching blue-cup order still. Timing and animation match the archived first version exactly. Other scenes retain the latest approved footage. The previous clarity-restored export remains available under timestamp 20261010-160400. Change manifest: `.production/restore-p-first-20261010-163109/manifest.json`.\n'
readme.write_text(text)
(run/'verification.json').write_text(json.dumps({'check':'pass; see check.log','master_decode':'pass','web_decode':'pass','files':data['files']},indent=2)+'\n')
print(json.dumps(data['files'],indent=2))
