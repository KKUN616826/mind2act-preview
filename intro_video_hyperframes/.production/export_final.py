from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess,json,hashlib,shutil
p=Path.cwd();r=p/'renders';ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg';fp='/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe'
check=json.loads((p/'qa/check-order-refinement.json').read_text());assert check['ok'],check
now=datetime.now(ZoneInfo('Asia/Shanghai'));tag=now.strftime('%Y%m%d-%H%M%S')
master=r/f'mind2act-world-promo-1080p-{tag}.mp4';web=r/f'mind2act-world-promo-web-{tag}.mp4'
run={'created_at':now.isoformat(),'id':'mind2act-world-promo-'+tag,'master':str(master.relative_to(p)),'web':str(web.relative_to(p))}
(p/'.production/export.json').write_text(json.dumps(run,indent=2));print('export',tag,flush=True)
with (p/'qa/render-final.log').open('w') as log:
 subprocess.run(['bash','scripts/hyperframes.sh','render','--quality','delivery','--fps','30','--workers','4','--gpu','--output',str(master.relative_to(p))],stdout=log,stderr=subprocess.STDOUT,check=True)
print('master complete',flush=True)
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(master),'-c:v','libx264','-preset','slow','-crf','23','-pix_fmt','yuv420p','-threads','8','-c:a','aac','-b:a','160k','-movflags','+faststart',str(web)],check=True)
print('web complete',flush=True)
files={}
for label,src in [('master',master),('web',web)]:
 j=json.loads(subprocess.check_output([fp,'-v','error','-show_format','-show_streams','-of','json',str(src)]));streams=j['streams']
 v=next(x for x in streams if x['codec_type']=='video');a=next(x for x in streams if x['codec_type']=='audio')
 assert v['width']==1920 and v['height']==1080 and v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
 assert a['codec_name']=='aac' and a['channels']==2
 assert abs(float(j['format']['duration'])-47.433333)<.04
 files[label]={'path':str(src.relative_to(p)),'bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'duration':float(j['format']['duration']),'video_codec':v['codec_name'],'pixel_format':v['pix_fmt'],'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'audio_codec':a['codec_name'],'audio_sample_rate':a['sample_rate'],'audio_channels':a['channels']}
 (p/f'qa/rendered/ffprobe-{label}-final.json').write_text(json.dumps(j,indent=2))
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss','3.5','-i',str(master),'-frames:v','1','-q:v','2',str(r/'mind2act-world-poster.jpg')],check=True)
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss','13.12','-i',str(master),'-frames:v','1',str(p/'qa/rendered/order-final.png')],check=True)
subprocess.run([ff,'-hide_banner','-v','error','-i',str(master),'-f','null','-'],check=True,stderr=open(p/'qa/rendered/decode-final.txt','w'))
subprocess.run([ff,'-hide_banner','-v','error','-i',str(web),'-f','null','-'],check=True,stderr=open(p/'qa/rendered/decode-web-final.txt','w'))
delivery={**run,'framework':'HyperFrames 0.8.143','authored_duration':47.4074074074,'files':files,'poster':'renders/mind2act-world-poster.jpg','subtitles':['renders/mind2act-world-narration.srt','renders/mind2act-world-narration.vtt'],'preview_url':'http://localhost:3052/#project/mind2act-hyperframes-blank-20261010-111117','checks':{'composition':'qa/check-final.json','order_refinement':'qa/check-order-refinement.json','animation_map':'qa/animation-map/animation-map.json','visual_contact_sheets':['qa/rendered/contact-sheet-1.jpg','qa/rendered/contact-sheet-2.jpg'],'final_order_frame':'qa/rendered/order-final.png','decode_master':'pass','decode_web':'pass'},'music_source':'assets/audio/The Midnight - The Equaliser (Not Alone).mp3','bpm':81,'music_source_start':11.9877}
(r/'delivery.json').write_text(json.dumps(delivery,indent=2,ensure_ascii=False))
readme=r/'README.md';text=readme.read_text().replace('20261010-125815',tag);readme.write_text(text)
# Keep earlier review encodes out of the delivery directory.
review=p/'qa/review-encodes';review.mkdir(exist_ok=True)
for old in r.glob('*.mp4'):
 if old not in [master,web]:shutil.move(str(old),str(review/old.name))
print(json.dumps(delivery,ensure_ascii=False),flush=True)
