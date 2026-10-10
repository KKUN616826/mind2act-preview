"""ASR is a check for intelligible lyrics, never proof of absolute vocal absence."""
from pathlib import Path
import json
import sys
from faster_whisper import WhisperModel

model = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=6, download_root=str(Path.home() / ".cache/hyperframes/faster-whisper"))
report = []
for path in map(Path, sys.argv[1:]):
    segments, info = model.transcribe(str(path), language="en", beam_size=5, vad_filter=False, condition_on_previous_text=False, temperature=0, word_timestamps=True)
    rows = []
    for segment in segments:
        row = {"start": segment.start, "end": segment.end, "text": segment.text, "avg_logprob": segment.avg_logprob, "no_speech_prob": segment.no_speech_prob,
               "words": [{"start": word.start, "end": word.end, "text": word.word, "probability": word.probability} for word in (segment.words or [])]}
        rows.append(row)
        print(path.name, row, flush=True)
    report.append({"file": str(path.resolve()), "engine": "faster-whisper 1.2.1 medium.en int8 CPU", "language": info.language, "language_probability": info.language_probability, "segments": rows})
    Path(__file__).with_name("bgm-asr-report.json").write_text(json.dumps(report, indent=2) + "\n")
