import cv2, numpy as np, torch, json, time, subprocess, math, hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

RUN=Path(__file__).resolve().parent
ROOT=RUN.parent.parent
OUT=ROOT/'assets/generated/clarity-20261010-155258'
FF='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg'
torch.set_num_threads(4)
torch.backends.cudnn.benchmark=True
scope={}
code=(RUN/'models/srvgg_arch.py').read_text().replace('from basicsr.utils.registry import ARCH_REGISTRY','').replace('@ARCH_REGISTRY.register()','')
exec(compile(code,'official_srvgg_arch.py','exec'),scope)
model=scope['SRVGGNetCompact'](num_conv=32).cuda().half().eval()
a=torch.load(RUN/'models/realesr-general-x4v3.pth',map_location='cpu',weights_only=True)['params']
b=torch.load(RUN/'models/realesr-general-wdn-x4v3.pth',map_location='cpu',weights_only=True)['params']
model.load_state_dict({k:a[k]*.35+b[k]*.65 for k in a})

@torch.inference_mode()
def enhance(frame,size):
    rgb=np.ascontiguousarray(frame[:,:,::-1])
    x=torch.from_numpy(rgb).permute(2,0,1).unsqueeze(0).cuda().half()/255
    y=model(x).clamp_(0,1)
    result=(y[0].permute(1,2,0).float().cpu().numpy()*255).round().astype('uint8')[:,:,::-1]
    result=cv2.resize(result,size,interpolation=cv2.INTER_AREA)
    base=cv2.resize(frame,size,interpolation=cv2.INTER_LANCZOS4)
    return cv2.addWeighted(result,.8,base,.2,0)

def frame_at(path,t):
    cap=cv2.VideoCapture(str(path));cap.set(cv2.CAP_PROP_POS_MSEC,t*1000)
    ok,f=cap.read();cap.release()
    if not ok:raise RuntimeError(path)
    return f

def sample():
    p=ROOT/'assets/videos/Mind/P/P__P_hard_general_012.mp4'
    f=frame_at(p,5.3)[:360]
    t=time.time();after=enhance(f,(1920,1080));print('inference sec',time.time()-t,flush=True)
    before=cv2.resize(f,(1920,1080),interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(str(RUN/'qa/before.png'),before)
    cv2.imwrite(str(RUN/'qa/after.png'),after)
    # same 3x cup crop, side by side; no additional resampling
    parts=[before[315:705,420:1440],after[315:705,420:1440]]
    sheet=np.zeros((450,2040,3),np.uint8)
    for i,part in enumerate(parts):
        sheet[60:,i*1020:(i+1)*1020]=part
        cv2.putText(sheet,['BEFORE / LANCZOS','AFTER / RESTORED'][i],(i*1020+25,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    cv2.imwrite(str(RUN/'qa/comparison.png'),sheet)

def encode(source,start,duration,speed,crop,size,dest,grid=False):
    dest.parent.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(source));fps=cap.get(cv2.CAP_PROP_FPS)
    count=round(duration*30)
    enc=subprocess.Popen([FF,'-nostdin','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{size[0]}x{size[1]}','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','14','-preset','medium','-threads','4','-g','30','-keyint_min','30','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE)
    current=-1;frame=None
    for i in range(count):
        target=round((start+i/30*speed)*fps)
        if current<0:cap.set(cv2.CAP_PROP_POS_FRAMES,target);current=target-1
        while current<target:
            ok,f=cap.read()
            if not ok:raise RuntimeError(f'Source exhausted {source}')
            frame=f;current+=1
        x,y,w,h=crop;f=frame[y:y+h,x:x+w]
        if grid:
            tw,th=size[0]-2,size[1]-2
            ratio=tw/th
            if f.shape[1]/f.shape[0]>ratio:
                cw=round(f.shape[0]*ratio);cx=(f.shape[1]-cw)//2;f=f[:,cx:cx+cw]
            else:
                ch=round(f.shape[1]/ratio);cy=(f.shape[0]-ch)//2;f=f[cy:cy+ch]
            out=np.zeros((size[1],size[0],3),np.uint8);out[:th,:tw]=enhance(f,(tw,th))
        else:out=enhance(f,size)
        enc.stdin.write(np.ascontiguousarray(out).tobytes())
    cap.release();enc.stdin.close()
    if enc.wait():raise RuntimeError('Encoder failed')
    print('done',dest.name,count,flush=True)

def build():
    old=ROOT/'.production/source-refresh-20261010-142512'
    cases=json.loads((old/'case-media-provenance.json').read_text())
    montage=json.loads((old/'montage-provenance.json').read_text())
    records=[]
    for c in cases['clips']:
        vals=c['crop_filter'].split(',')[0].split('=')[1].split(':');w,h,x,y=map(int,vals)
        dest=OUT/'cases'/Path(c['path']).name
        encode(ROOT/c['source'],c['source_start'],c['output_duration'],c['playback_rate'],(x,y,w,h),tuple(c['resolution']),dest)
        records.append({**c,'enhanced_path':str(dest.relative_to(ROOT))})
    for group,grid in [('mosaic_six',True),('fast_reel',False)]:
        cells=montage[group].get('cells',montage[group].get('cuts'))
        for c in cells:
            crop=(0,24,640,360) if not grid else (0,0,640,480)
            dest=OUT/'montage'/Path(c['path']).name
            encode(ROOT/c['source'],c['source_start'],c['duration'],c['speed'],crop,(c['width'],c['height']),dest,grid)
            records.append({**c,'enhanced_path':str(dest.relative_to(ROOT))})
    inputs=[]
    for c in montage['mosaic_six']['cells']:inputs+=['-i',str(OUT/'montage'/Path(c['path']).name)]
    graph=''.join(f'[{i}:v]' for i in range(6))+'xstack=inputs=6:layout=0_0|640_0|1280_0|0_540|640_540|1280_540[v]'
    common=['-an','-c:v','libx264','-crf','14','-preset','medium','-threads','4','-g','30','-pix_fmt','yuv420p','-movflags','+faststart']
    subprocess.run([FF,'-nostdin','-v','error','-y',*inputs,'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]',*common,str(OUT/'montage/six-cases-mosaic.mp4')],check=True)
    inputs=[]
    for c in montage['fast_reel']['cuts']:inputs+=['-i',str(OUT/'montage'/Path(c['path']).name)]
    frames=montage['fast_reel']['frames_per_cut']
    graph=';'.join(f'[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS[q{i}]' for i,n in enumerate(frames))+';'+''.join(f'[q{i}]' for i in range(len(frames)))+f'concat=n={len(frames)}:v=1:a=0[v]'
    subprocess.run([FF,'-nostdin','-v','error','-y',*inputs,'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-r','30',*common,str(OUT/'montage/fast-montage.mp4')],check=True)
    (RUN/'provenance.json').write_text(json.dumps({'created_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),'model':'Real-ESRGAN realesr-general-x4v3 + wdn','model_mix': [.35,.65],'restored_blend':.8,'source_blend':.2,'originals_modified':False,'records':records,'excluded':'Order, target-line and piano-note stills retain source pixels; 45-case mosaic already downscales and is unchanged.'},indent=2,ensure_ascii=False))

if __name__=='__main__':
    import sys
    if '--build' in sys.argv:build()
    else:sample()
