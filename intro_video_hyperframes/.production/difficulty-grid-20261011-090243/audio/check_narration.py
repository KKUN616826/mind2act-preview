"""Independent unprompted ASR verification and word timing for new difficulty cue."""
from pathlib import Path
import json,re
from faster_whisper import WhisperModel
work=Path(__file__).resolve().parent
manifest=json.loads((work/'audio-integration.json').read_text())
cue=next(x for x in manifest['voice'] if x['id']=='difficulty-explanation')
model=WhisperModel('medium.en',device='cpu',compute_type='int8',cpu_threads=6,download_root=str(Path.home()/'.cache/hyperframes/faster-whisper'))
segments,_=model.transcribe(cue['path'],language='en',beam_size=5,vad_filter=False,condition_on_previous_text=False,temperature=0,word_timestamps=True)
rows=[{'start':s.start,'end':s.end,'text':s.text,'no_speech_prob':s.no_speech_prob,'words':[{'text':w.word,'start':w.start,'end':w.end,'global_start':w.start+cue['start'],'global_end':w.end+cue['start'],'difficulty_local_start':w.start+cue['start']-53.3333333333,'difficulty_local_end':w.end+cue['start']-53.3333333333,'probability':w.probability} for w in (s.words or [])]} for s in segments]
transcript=' '.join(r['text'].strip() for r in rows)
normalize=lambda x:re.sub(r'[^a-z0-9]','',x.lower())
report={'model':'faster-whisper medium.en int8 CPU','expected_text_not_supplied_to_model':True,'id':cue['id'],'expected':cue['text'],'transcript':transcript,'segments':rows,'exact_normalized_match':normalize(transcript)==normalize(cue['text']),'manual_listening':False}
(work/'narration-asr-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
if not report['exact_normalized_match']:raise SystemExit('Independent ASR did not match')
