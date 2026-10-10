"""Check actual delivered AAC: difficulty cues and voice-free showcase intervals."""
from pathlib import Path
import json
import sys
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from faster_whisper.vad import get_speech_timestamps
import soundfile as sf

work=Path(__file__).resolve().parent/'audio'
manifest=json.loads((work/'audio-integration.json').read_text())
video=Path(sys.argv[1]).resolve()
rate=16000
actual=decode_audio(str(video),sampling_rate=rate)
rows=[]
for name,interval in [('coverage',manifest['statistics_music_only']),('numeric_payoff',manifest['music_only_intervals'][1])]:
 segment=actual[round(interval[0]*rate):round(interval[1]*rate)]
 chunks=get_speech_timestamps(segment,sampling_rate=rate)
 rows.append({'name':name,'interval':interval,'speech_intervals':[{'start':c['start']/rate+interval[0],'end':c['end']/rate+interval[0]} for c in chunks]})
 sf.write(work/f'{video.stem}-{name}-actual-aac.wav',segment,rate,subtype='PCM_24')
print(json.dumps({'vad':rows}),flush=True)
model=WhisperModel('medium.en',device='cpu',compute_type='int8',cpu_threads=6,download_root=str(Path.home()/'.cache/hyperframes/faster-whisper'))
cues=[]
for cue in manifest['voice']:
 if cue['id'] != 'motivation':continue
 start=max(0,cue['start']-.08);end=cue['end']+.08
 segment=actual[round(start*rate):round(end*rate)]
 wav=work/f'{video.stem}-{cue["id"]}-actual-aac.wav';sf.write(wav,segment,rate,subtype='PCM_24')
 segments,_=model.transcribe(str(wav),language='en',beam_size=5,vad_filter=False,condition_on_previous_text=False,temperature=0,word_timestamps=True)
 found=[{'start':s.start,'end':s.end,'text':s.text,'no_speech_prob':s.no_speech_prob,'words':[{'text':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in (s.words or [])]} for s in segments]
 transcript=' '.join(s['text'].strip() for s in found)
 item={'id':cue['id'],'intended':cue['text'],'transcript':transcript,'expected_text_supplied_to_model':False,'sample_start':start,'sample_end':end,'segments':found,'match':transcript.lower().strip(' .!?')==cue['text'].lower().strip(' .!?')}
 cues.append(item);print(json.dumps(item),flush=True)
 report={'video':str(video),'model':'faster-whisper medium.en int8 CPU','vad_model':'bundled Silero threshold0.5','vad_checks':rows,'question_cue':cues,'manual_listening':False,'pass':not any(x['speech_intervals'] for x in rows) and all(x['match'] for x in cues)}
 (work/f'{video.stem}-actual-speech-audit.json').write_text(json.dumps(report,indent=2)+'\n')
