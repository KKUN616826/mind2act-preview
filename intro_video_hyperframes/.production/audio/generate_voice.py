import json, os, shutil
from pathlib import Path
import kokoro_onnx, soundfile as sf
from kokoro_onnx.config import EspeakConfig
import espeakng_loader
import onnxruntime as ort
spec=json.loads(Path('.production/audio/narration.json').read_text())
# eSpeak has a native path-length limit; the nested project path exceeds it.
# Use a short cache path, while keeping all generated project assets local.
short_data=Path('/home/xzy/.cache/mind2act-espeak-ng-data')
if not short_data.exists():shutil.copytree(espeakng_loader.get_data_path(),short_data)
opts=ort.SessionOptions();opts.intra_op_num_threads=4;opts.inter_op_num_threads=2
session=ort.InferenceSession('/home/xzy/.cache/hyperframes/tts/models/kokoro-v1.0.onnx',sess_options=opts,providers=['CPUExecutionProvider'])
model=kokoro_onnx.Kokoro.from_session(session,'/home/xzy/.cache/hyperframes/tts/voices/voices-v1.0.bin',espeak_config=EspeakConfig(data_path=str(short_data)))
for l in spec['lines']:
 p=Path('assets/generated/audio')/f"vo-{l['id']}-raw.wav"
 if p.exists():continue
 samples,sr=model.create(l['text'],voice=spec['voice'],speed=l['speed'],lang='en-us')
 sf.write(p,samples,sr)
 print(l['id'],len(samples)/sr,flush=True)
