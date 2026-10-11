from pathlib import Path
import json, subprocess
import numpy as np
from scipy.signal import find_peaks, stft, correlate
p=Path('assets/audio/The Midnight - The Equaliser (Not Alone).mp3')
sr=22050
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar',str(sr),'-f','f32le','-'])
y=np.frombuffer(raw,dtype=np.float32)
f,t,z=stft(y,sr,nperseg=1024,noverlap=768)
a=np.abs(z)
flux=np.maximum(np.diff(a,axis=1),0)
# Focus on kick and snare onset energies rather than pads
bands=[(20,150),(150,2500),(2500,8000)]
ons=[]
for lo,hi in bands:
 x=flux[(f>=lo)&(f<hi)].sum(axis=0)
 x=x/np.quantile(x,.99)
 ons.append(x)
onset=.65*ons[0]+.25*ons[1]+.1*ons[2]
dt=t[1]-t[0]
c=correlate(onset-onset.mean(),onset-onset.mean(),mode='full')[len(onset)-1:]
lo=int(60/180/dt); hi=int(60/70/dt)
peak,_=find_peaks(c[lo:hi]); candidates=sorted([(c[k+lo],60/((k+lo)*dt)) for k in peak],reverse=True)[:8]
period=60/candidates[0][1]
peaks,_=find_peaks(onset,height=np.quantile(onset,.72),distance=int(.22/dt))
pt=t[1:][peaks]
energy=[]
for start in range(0,int(len(y)/sr),4):
 sy=y[start*sr:(start+4)*sr]
 energy.append([start,float(np.sqrt(np.mean(sy*sy)))])
out={'duration':len(y)/sr,'tempo_candidates':[[float(a),float(b)] for a,b in candidates],'energy_by_4s':energy,'strong_onsets':pt.tolist()}
Path('.production/audio/bgm-analysis.json').write_text(json.dumps(out,indent=2))
print('tempo candidates:', candidates)
print('energy:',energy[:28])
print('onsets 0-55:',pt[pt<55])
# Direct grid likelihood avoids FFT-lag quantization.
tt=t[1:]
mask=(tt>12)&(tt<100)
best=(-1,None,None)
for bpm in np.linspace(79.5,82.0,501):
 per=60/bpm
 phases=np.mod(tt[mask],per)
 hist=np.zeros(180)
 np.add.at(hist,(phases/per*180).astype(int),onset[mask])
 smooth=np.convolve(np.r_[hist[-5:],hist,hist[:5]],np.ones(7)/7,'same')[5:-5]
 idx=int(np.argmax(smooth));score=float(smooth[idx])
 if score>best[0]:best=(score,bpm,idx*per/180)
print('BEST GRID',best)
out['grid']={'bpm':best[1],'phase_seconds':best[2]}
Path('.production/audio/bgm-analysis.json').write_text(json.dumps(out,indent=2))
