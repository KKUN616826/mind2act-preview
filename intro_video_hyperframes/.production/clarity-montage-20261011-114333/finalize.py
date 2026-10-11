from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess
ROOT=Path.cwd()
BASE=Path(__file__).resolve().parent
REL=str(BASE.relative_to(ROOT))
read=lambda p:json.loads(Path(p).read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
delivery=read(BASE/'delivery-candidate.json')
previous=read(BASE/'before/delivery.json')
stamp=delivery['id'].removeprefix('mind2act-world-promo-')
old_stamp=previous['id'].removeprefix('mind2act-world-promo-')
assert read(BASE/'check-final.json')['ok']
assert read(BASE/'exported-visual-review.json')['passed']
assert read(BASE/'animation-review.json')['passed']
for kind in ['master','web']:
    assert sha(previous[kind])==previous['files'][kind]['sha256']
allowed={'compositions/'+n+'.html' for n in ['02-motivation','04-act','05-mind2act','06-scale','08-coordination']}
for file,digest in previous['source_hashes'].items():
    if file not in allowed: assert sha(file)==digest, f'Unexpected change: {file}'
ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
fp='/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe'
audios=[]
for name,file in [('previous',previous['master']),('master',delivery['master']),('web',delivery['web'])]:
    data=subprocess.run([ff,'-v','error','-i',file,'-map','0:a:0','-c:a','copy','-f','adts','-'],capture_output=True,check=True).stdout
    packets=subprocess.run([fp,'-v','error','-select_streams','a:0','-show_packets','-show_entries','packet=pts,dts,duration,size,flags,side_data_list','-of','json',file],capture_output=True,check=True).stdout
    audios.append({'name':name,'path':file,'adts_bytes':len(data),'adts_sha256':hashlib.sha256(data).hexdigest(),'packet_timing_sha256':hashlib.sha256(packets).hexdigest()})
assert len({r['adts_sha256'] for r in audios})==1
assert len({r['packet_timing_sha256'] for r in audios})==1
(BASE/'audio-preservation.json').write_text(json.dumps({'passed':True,'files':audios,'method':'AAC packetstream and packet timing hashes match previous verified export exactly.','prior_audit':'.production/cp02-fullview-20261011-112139/audio-preservation.json','manual_listening':False},indent=2)+'\n')
delivery['local_preview']=f'renders/preview-{stamp}.html'
Path(delivery['local_preview']).write_text(Path(previous['local_preview']).read_text().replace(old_stamp,stamp))
delivery['contact_sheet']=f'renders/mind2act-world-contact-{stamp}.jpg'
shutil.copy2(BASE/'rendered/contact-sheet.jpg',delivery['contact_sheet'])
delivery['difficulty_preview']=f'renders/mind2act-world-difficulty-{stamp}.jpg'
shutil.copy2(BASE/'rendered/frame-60-4.jpg',delivery['difficulty_preview'])
delivery['category_preview']=f'renders/mind2act-world-categories-{stamp}.jpg'
shutil.copy2(BASE/'rendered/frame-10.jpg',delivery['category_preview'])
delivery['checks'].update({'audio_preservation':f'{REL}/audio-preservation.json','exported_visual':f'{REL}/exported-visual-review.json','animation_review':f'{REL}/animation-review.json','montage_review':f'{REL}/montage-review.json','review':f'{REL}/QA.md','unchanged_difficulty_verified':True,'unchanged_timing_verified':True,'previous_delivery':f'renders/delivery-{old_stamp}.json'})
delivery['source_hashes']={file:sha(file) for file in previous['source_hashes']}
delivery['verified_at']=datetime.now(timezone.utc).isoformat()
delivery['revision']='Correct continuous fractional SVG highlight motion in both directions, unify category description baselines, compact Act and piano panel text, order fullscreen montage M / Mind -> FR1 / Act -> CP04 / Mind2Act with continuous CP04 landing in taxonomy wall and CP02 bridge into latest difficulty section.'
delivery['narrative']='Question and three categories -> P / PR3 / CP05 representative cases -> two-way coordination and three-logo triangle -> M / FR1 / CP04 fullscreen montage -> 15 tasks in three categories -> CP02 Easy / Medium / Hard -> three-task difficulty comparison -> 45 configurations -> moonshot invitation.'
delivery['audio_verification']='Master and web AAC packets and timing match the prior verified 112801 export. Existing voiceover, Hard, music and subtitle timing are preserved.'
payload=json.dumps(delivery,indent=2)+'\n'
for dest in [f'renders/delivery-{stamp}.json','renders/delivery.json',BASE/'delivery-final.json']:Path(dest).write_text(payload)
Path('renders/README.md').write_text(f'''# Mind2Act World promotional film

Latest: **75 seconds, 1920×1080, 30 fps, H.264/AAC**.

- Master: {delivery['master']}
- Web preview: {delivery['web']}
- Local player: {delivery['local_preview']}
- English subtitles: {', '.join(delivery['subtitles'])}
- Editable preview: {delivery['preview_url']}

This revision fixes the Act-to-Mind highlight motion, aligns the three category descriptions, compacts the Act and piano floating-panel text, and uses M / Mind → FR1 / Act → CP04 / Mind2Act for the fullscreen task montage. CP04 continuously lands in its taxonomy card; CP02 is highlighted before the difficulty scene.

The latest difficulty section is retained in full: CP02 Easy/Medium/Hard with 4/6/6 reference cakes and real Hard cover placement, full-width main-camera framing, then F/PR3/CP02 comparison and the 45-configuration payoff. The Easy/Medium/Hard typography and narration retain their timing.

Checks: HyperFrames runtime/layout/contrast, actual exported frame/motion review, full master/web decoding, identical AAC streams and packet timing. Previous exports are preserved. Production record: {REL}/.
''')
m=read(BASE/'manifest.json');m.update(status='complete',delivery=delivery['master'],web=delivery['web'],verified_at=delivery['verified_at'],history_id='d05a762b');(BASE/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({k:delivery[k] for k in ['master','web','local_preview','category_preview']}))
