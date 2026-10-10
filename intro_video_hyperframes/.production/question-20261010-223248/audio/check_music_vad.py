"""Independent detector check. No automated detector is a human listening certificate."""
from pathlib import Path
import json
import numpy as np
from faster_whisper.audio import decode_audio
from faster_whisper.vad import get_speech_timestamps
work=Path(__file__).resolve().parent
manifest=json.loads((work/'audio-integration.json').read_text())
rate=16000
rows=[]
for name, path, interval in [
 ('full_bgm',manifest['music_input'],[0,manifest['duration']]),
 ('coverage_fullmix',manifest['audio_path'],manifest['statistics_music_only']),
 ('numeric_payoff_fullmix',manifest['audio_path'],manifest['music_only_intervals'][1]),
]:
 audio=decode_audio(path,sampling_rate=rate)
 segment=audio[round(interval[0]*rate):round(interval[1]*rate)]
 chunks=get_speech_timestamps(segment,sampling_rate=rate)
 detected=[{'start':c['start']/rate+interval[0],'end':c['end']/rate+interval[0]} for c in chunks]
 item={'name':name,'path':path,'interval':interval,'speech_intervals':detected,'detected':bool(detected)}
 rows.append(item);print(json.dumps(item),flush=True)
(work/'music-vad-report.json').write_text(json.dumps({'engine':'faster-whisper bundled Silero VAD default threshold 0.5','manual_listening':False,'checks':rows},indent=2)+'\n')
