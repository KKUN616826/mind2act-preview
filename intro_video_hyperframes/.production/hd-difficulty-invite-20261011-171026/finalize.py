from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,shutil
root=Path.cwd();base=Path(__file__).resolve().parent;rel=str(base.relative_to(root))
read=lambda p:json.loads(Path(p).read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=read(base/'before/delivery.json');new=read(base/'delivery-candidate.json')
for report in ['check-final.json','exported-visual-review.json','exported-audio-review.json','animation-review.json']:
 j=read(base/report);assert j.get('passed',j.get('ok')),report
assert read(base/'animation-review.json')['actual_encoded_review']['passed'] is True
allowed={'index.html','compositions/06-scale.html','compositions/07-outro.html','compositions/09-difficulty.html'}
for file,digest in old['source_hashes'].items():
 if file not in allowed:assert sha(file)==digest,file
for kind in ['master','web']:assert sha(old[kind])==old['files'][kind]['sha256']
ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
checks=[]
for kind in ['master','web']:
 data=subprocess.run([ff,'-v','error','-i',new[kind],'-map','0:a:0','-c:a','copy','-f','adts','-'],capture_output=True,check=True).stdout
 checks.append({'kind':kind,'sha256':hashlib.sha256(data).hexdigest()})
assert checks[0]['sha256']==checks[1]['sha256']
stamp=new['id'].removeprefix('mind2act-world-promo-');oldstamp=old['id'].removeprefix('mind2act-world-promo-')
new['local_preview']=f'renders/preview-{stamp}.html'
Path(new['local_preview']).write_text(Path(old['local_preview']).read_text().replace(oldstamp,stamp))
for field,file,label in [('contact_sheet','contact-sheet.jpg','contact'),('difficulty_preview','frame-54-6.jpg','difficulty'),('montage_preview','frame-45-25.jpg','montage')]:
 new[field]=f'renders/mind2act-world-{label}-{stamp}.jpg';shutil.copy2(base/'rendered'/file,new[field])
new['difficulty_excerpt']=f'renders/mind2act-world-difficulty-review-{stamp}.mp4'
subprocess.run([ff,'-v','error','-ss','53.333333','-i',new['web'],'-t','12.752','-c:v','libx264','-preset','medium','-crf','20','-threads','6','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-n',new['difficulty_excerpt']],check=True)
new['checks'].update({'exported_visual':f'{rel}/exported-visual-review.json','exported_audio':f'{rel}/exported-audio-review.json','animation_review':f'{rel}/animation-review.json','review':f'{rel}/QA.md','master_web_aac_identical':checks,'unchanged_other_compositions_verified':True,'previous_delivery':f'renders/delivery-{oldstamp}.json'})
new['source_hashes']={f:sha(f) for f in old['source_hashes']}
new['revision']='Replace fullscreen M/FR1/CP04 montage with supplied native 1080p hard-task sources and parallel category captions. Show CP02 Easy placement, Medium button/opening and Hard cover actions with brief count/action cues. Broaden ending text and narration to embodied AI systems.'
new['narrative']=old['narrative'].replace('CP02 Easy / Medium / Hard','CP02 Easy placement / Medium press and open / Hard cover').replace('moonshot invitation','inclusive embodied AI moonshot invitation')
new['audio_verification']='Only the ending speech cue was regenerated. Earlier narration and music preservation checked against prior soundtrack; new encoded ending speech and captions reviewed.'
new['verified_at']=datetime.now(timezone.utc).isoformat()
payload=json.dumps(new,indent=2)+'\n'
for dest in ['renders/delivery.json',f'renders/delivery-{stamp}.json',base/'delivery-final.json']:Path(dest).write_text(payload)
Path('renders/README.md').write_text(f'''# Mind2Act World promotional film

Latest: 75 seconds, 1920×1080, 30 fps, H.264/AAC.

- Master: {new['master']}
- Web preview: {new['web']}
- Local player: {new['local_preview']}
- Difficulty excerpt: {new['difficulty_excerpt']}
- English subtitles: {', '.join(new['subtitles'])}
- Editable preview: {new['preview_url']}

The three fullscreen cases use the supplied 1080p M/FR1/CP04 recordings with original aspect ratio. Their captions describe the categories: Choose the next action. / Execute actions reliably. / Coordinate the whole task.

CP02 Easy/Medium/Hard retains the large typography and narration, with brief count/action cues and real placement, button/opening, and cover-placement clips. The three-task comparison and 45-configuration page remain. Ending screen and voiceover invite evaluation of embodied AI systems, covering models, hybrid systems and agents.

Checks: HyperFrames runtime/layout/contrast, actual exported picture and audio review, full file decoding, preservation of earlier edits and historical exports. Production evidence: {rel}/.
''')
m=read(base/'manifest.json');m.update(status='complete',history_id='38ec7cb7',master=new['master'],web=new['web'],verified_at=new['verified_at']);(base/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({k:new[k] for k in ['master','web','local_preview','difficulty_excerpt']}))
