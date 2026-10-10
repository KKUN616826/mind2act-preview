from pathlib import Path
import json,subprocess,shutil
import numpy as np
import soundfile as sf
from scipy.ndimage import uniform_filter1d
spec=json.loads(Path('.production/audio/narration.json').read_text());out=Path('assets/generated/audio');sr=48000;n=round(spec['duration']*sr)
voice=np.zeros((n,2),dtype=np.float64);activity=np.zeros(n,dtype=np.float64)
report=[]
def ff(cmd):return subprocess.run(['ffmpeg','-nostdin','-hide_banner','-y',*cmd],capture_output=True,text=True,check=True)
def norm(src,dst,filters,target=-17):
 af=','.join(filters+[f'loudnorm=I={target}:TP=-2:LRA=9:print_format=json'])
 r=ff(['-i',str(src),'-af',af,'-f','null','-']);s=r.stderr[r.stderr.rfind('{'):];m=json.loads(s)
 af=','.join(filters+[f"loudnorm=I={target}:TP=-2:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"])
 ff(['-i',str(src),'-af',af,'-ar',str(sr),'-ac','1','-c:a','pcm_s24le',str(dst)])
 return m
for line in spec['lines']:
 src=out/f"vo-{line['id']}-raw.wav";raw,rs=sf.read(src)
 # Remove only true leading/trailing silence; keep natural internal pauses.
 nz=np.flatnonzero(np.abs(raw)>max(.001,np.max(np.abs(raw))*.005))
 lo=max(0,nz[0]-round(.035*rs));hi=min(len(raw),nz[-1]+round(.065*rs))
 dur=(hi-lo)/rs;tempo=max(1.0,dur/line['max_duration'])
 dst=out/f"vo-{line['id']}.wav"
 m=norm(src,dst,[f'atrim=start={lo/rs}:end={hi/rs}','asetpts=PTS-STARTPTS',f'atempo={tempo:.8f}','highpass=f=75','afade=t=in:st=0:d=0.012'])
 y,_=sf.read(dst);st=round(line['start']*sr);end=min(st+len(y),n)
 voice[st:end,:]+=y[:end-st,None]
 # Short anticipatory duck, sustain across phrase, slow musical release.
 a=max(0,st-round(.16*sr));r=min(n,end+round(.40*sr));activity[a:st]=np.maximum(activity[a:st],np.linspace(0,1,st-a));activity[st:end]=1;activity[end:r]=np.maximum(activity[end:r],np.linspace(1,0,r-end))
 report.append({**line,'path':str(dst),'original_duration':len(raw)/rs,'trimmed_duration':dur,'atempo':tempo,'final_duration':len(y)/sr,'end':end/sr})
 print(report[-1],flush=True)
sf.write(out/'narration-stem.wav',voice,sr,subtype='PCM_24')
# Music occupies the stereo field, with a restrained carve in the speech-presence band.
ff(['-i',str(out/'music-source-cut.wav'),'-af','equalizer=f=1800:t=q:w=0.65:g=-2','-ar',str(sr),'-c:a','pcm_s24le',str(out/'music-eq.wav')])
music,_=sf.read(out/'music-eq.wav');music=music[:n];music=np.pad(music,((0,n-len(music)),(0,0)))
# The supplied mastered source measures -10.27 LUFS.
# -8.5 dB gaps; -14.5 dB speech => approximately -19 / -25 LUFS.
gain_db=-8.5-6.0*activity;music*=np.power(10,gain_db[:,None]/20)
fades=np.ones(n);fin=round(.07*sr);fout=round(1.3*sr);fades[:fin]=np.linspace(0,1,fin);fades[-fout:]=np.linspace(1,0,fout)**1.25;music*=fades[:,None]
sf.write(out/'music-stem.wav',music,sr,subtype='PCM_24')
# Bundled, licensed, understated accents, placed on scene and logo landings.
sfx=np.zeros_like(voice);sfxdir=Path('/home/xzy/.claude/plugins/cache/hyperframes/hyperframes/0.8.143/skills/media-use/audio/assets/sfx')
placements=[('impact-bass-1',1.48148,-24),('whoosh-short',4.98,-24),('whoosh-short',11.65,-24),('whoosh-short',17.57,-27),('whoosh-short',23.50,-27),('whoosh-cinematic',29.08,-25),('impact-bass-1',42.22222,-24)]
for name,start,level in placements:
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(sfxdir/(name+'.mp3')),'-ar',str(sr),'-ac','2','-f','f32le','-'])
 y=np.frombuffer(raw,np.float32).reshape(-1,2).astype(np.float64);y*=10**(level/20)/(np.sqrt(np.mean(y*y))+1e-9)
 st=round(start*sr);length=min(len(y),n-st);sfx[st:st+length]+=y[:length]
sf.write(out/'sfx-stem.wav',sfx,sr,subtype='PCM_24')
sf.write(out/'soundtrack-premaster.wav',voice+music+sfx,sr,subtype='PCM_24')
# Two-pass EBU R128 master to web-friendly integrated loudness.
r=ff(['-i',str(out/'soundtrack-premaster.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=10:print_format=json','-f','null','-']);m=json.loads(r.stderr[r.stderr.rfind('{'):])
flt=f"loudnorm=I=-16:TP=-1.5:LRA=10:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
ff(['-i',str(out/'soundtrack-premaster.wav'),'-af',flt,'-ar',str(sr),'-c:a','pcm_s24le',str(out/'soundtrack.wav')])
shutil.copy(sfxdir/'CREDITS.md',out/'SFX-CREDITS.md')
report={'bpm':spec['bpm'],'duration':spec['duration'],'source_offset':spec['music_source_offset'],'scene_boundaries':spec['scene_boundaries'],'voice_provider':'Local Kokoro-82M (same HyperFrames TTS engine), am_michael','voice':report,'sfx':placements,'mastering':{'target_lufs':-16,'true_peak_ceiling':-1.5,'pre_master_measurement':m}}
Path('.production/audio/audio-timing.json').write_text(json.dumps(report,indent=2))
print('MASTER COMPLETE',flush=True)
