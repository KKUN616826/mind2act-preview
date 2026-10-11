from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,shutil
root=Path.cwd(); base=Path(__file__).resolve().parent; rel=str(base.relative_to(root))
read=lambda p:json.loads(Path(p).read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=read(base/'before/delivery.json'); new=read(base/'delivery-candidate.json')
assert read(base/'check-final.json')['ok']
assert read(base/'exported-visual-review.json')['passed']
expected=(base/'before/compositions/02-motivation.html').read_text().replace('Remember. Reason. Decide.','Choose the next action.').replace('Act with physical precision.','Execute actions reliably.')
assert Path('compositions/02-motivation.html').read_text()==expected
for file,digest in old['source_hashes'].items():
    if file!='compositions/02-motivation.html': assert sha(file)==digest,file
for kind in ['master','web']: assert sha(old[kind])==old['files'][kind]['sha256']
ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg';fp='/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe'
audio=[]
for label,file in [('previous',old['master']),('master',new['master']),('web',new['web'])]:
    a=subprocess.run([ff,'-v','error','-i',file,'-map','0:a:0','-c:a','copy','-f','adts','-'],capture_output=True,check=True).stdout
    b=subprocess.run([fp,'-v','error','-select_streams','a:0','-show_packets','-show_entries','packet=pts,dts,duration,size,flags,side_data_list','-of','json',file],capture_output=True,check=True).stdout
    audio.append({'label':label,'file':file,'adts_sha256':hashlib.sha256(a).hexdigest(),'timing_sha256':hashlib.sha256(b).hexdigest()})
assert len({r['adts_sha256'] for r in audio})==1
assert len({r['timing_sha256'] for r in audio})==1
(base/'audio-preservation.json').write_text(json.dumps({'passed':True,'files':audio,'previous_audit':old['checks']['audio_preservation'],'manual_listening':False},indent=2)+'\n')
stamp=new['id'].removeprefix('mind2act-world-promo-'); oldstamp=old['id'].removeprefix('mind2act-world-promo-')
new['local_preview']=f'renders/preview-{stamp}.html'
Path(new['local_preview']).write_text(Path(old['local_preview']).read_text().replace(oldstamp,stamp))
new['category_preview']=f'renders/mind2act-world-categories-{stamp}.jpg'
shutil.copy2(base/'rendered/frame-9.jpg',new['category_preview'])
new['checks'].update({'exported_visual':f'{rel}/exported-visual-review.json','audio_preservation':f'{rel}/audio-preservation.json','review':f'{rel}/QA.md','unchanged_motion_verified':True,'unchanged_other_compositions_verified':True,'previous_delivery':f'renders/delivery-{oldstamp}.json'})
new['source_hashes']={file:sha(file) for file in old['source_hashes']}
new['revision']='Use parallel action-oriented sentences for Mind, Act and Mind2Act: Choose the next action. / Execute actions reliably. / Coordinate the whole task. Text substitutions only; all styling, motion, timing, footage and audio retained.'
new['narrative']=old['narrative']
new['audio_verification']='AAC packet content and packet timing are identical to the preceding verified export.'
new['verified_at']=datetime.now(timezone.utc).isoformat()
payload=json.dumps(new,indent=2)+'\n'
for dest in ['renders/delivery.json',f'renders/delivery-{stamp}.json',base/'delivery-final.json']:Path(dest).write_text(payload)
Path('renders/README.md').write_text(f'''# Mind2Act World promotional film

Latest: 75 seconds, 1920×1080, 30 fps, H.264/AAC.

- Master: {new['master']}
- Web: {new['web']}
- Local player: {new['local_preview']}
- Category frame: {new['category_preview']}
- Editable preview: {new['preview_url']}

The category captions now share one format: “Choose the next action.” / “Execute actions reliably.” / “Coordinate the whole task.” Only those words changed. The verified two-way pulse, M→FR1→CP04 montage, complete CP02 difficulty section, audio and 75-second timing are retained.

Checks: HyperFrames runtime/layout/contrast, actual encoded category frame, full file decoding, identical AAC content and timing. Earlier exports remain preserved. Verification: {rel}/.
''')
m=read(base/'manifest.json');m.update(status='complete',history_id='9e13f7d8',master=new['master'],web=new['web'],verified_at=new['verified_at']);(base/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({k:new[k] for k in ['master','web','local_preview','category_preview']}))
