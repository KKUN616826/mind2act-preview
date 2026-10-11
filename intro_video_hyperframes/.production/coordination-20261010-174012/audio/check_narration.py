"""Independent ASR cue verification; expected text is not supplied to the model."""
from pathlib import Path
import json
import re
from faster_whisper import WhisperModel

work = Path(__file__).resolve().parent
manifest = json.loads((work / "audio-integration.json").read_text())
model = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=6, download_root=str(Path.home() / ".cache/hyperframes/faster-whisper"))
checks = []
for cue in manifest["voice"]:
    segments, _ = model.transcribe(cue["path"], language="en", beam_size=5, vad_filter=False, condition_on_previous_text=False, temperature=0)
    rows = [{"start": float(segment.start), "end": float(segment.end), "text": segment.text, "no_speech_prob": float(segment.no_speech_prob)} for segment in segments]
    transcript = " ".join(row["text"].strip() for row in rows)
    normalize = lambda text: re.sub(r"[^a-z0-9]", "", text.lower())
    item = {"id": cue["id"], "expected": cue["text"], "transcript": transcript, "segments": rows, "exact_normalized_match": normalize(transcript) == normalize(cue["text"])}
    checks.append(item)
    print(json.dumps(item), flush=True)
    (work / "narration-asr-report.json").write_text(json.dumps({"model": "faster-whisper medium.en int8 CPU", "expected_text_not_supplied_to_model": True, "cues": checks}, indent=2) + "\n")
