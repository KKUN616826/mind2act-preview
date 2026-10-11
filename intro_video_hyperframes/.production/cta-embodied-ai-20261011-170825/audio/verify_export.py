"""Verify delivered AAC against the exact soundtrack and independently transcribe key cues."""
from pathlib import Path
import argparse
import datetime
import json
import subprocess

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[2]
ASR_PYTHON = ROOT / ".production/coordination-20261010-174012/audio/separation-venv/bin/python"
AUDIO_PYTHON = ROOT / ".production/audio/venv/bin/python"

parser = argparse.ArgumentParser()
parser.add_argument("video", type=Path)
parser.add_argument("--report", type=Path, required=True)
args = parser.parse_args()
video = args.video.resolve()
subprocess.run([str(AUDIO_PYTHON), str(WORK / "audit_render_audio.py"), str(video)], check=True, cwd=ROOT)
subprocess.run([str(ASR_PYTHON), str(WORK / "check_rendered_speech.py"), str(video)], check=True, cwd=ROOT)
levels_path = WORK / f"{video.stem}-aac-audit.json"
speech_path = WORK / f"{video.stem}-actual-speech-audit.json"
levels = json.loads(levels_path.read_text())
speech = json.loads(speech_path.read_text())
preservation = json.loads((WORK / "preservation.json").read_text())
voice = json.loads((WORK / "narration-asr-report.json").read_text())
report = {
    "video": str(video),
    "created_at": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec="seconds"),
    "audio_integration": str(WORK / "audio-integration.json"),
    "aac_report": str(levels_path),
    "speech_report": str(speech_path),
    "source_preservation_report": str(WORK / "preservation.json"),
    "loudness_lufs": levels["loudness_lufs"],
    "true_peak_dbtp": levels["true_peak_dbtp"],
    "master_vs_aac_correlation": levels["master_vs_aac_correlation"],
    "all_cue_levels_match": all(x["passed"] for x in levels["cue_checks"]),
    "source_unchanged_before_ending": preservation["passed"],
    "standalone_ending_asr_match": voice["exact_normalized_match"],
    "exported_cues": [{"id": x["id"], "intended": x["intended"], "transcript": x["transcript"], "match": x["match"]} for x in speech["difficulty_cues"]],
    "music_only_intervals_have_no_detected_speech": not any(x["speech_intervals"] for x in speech["vad_checks"]),
    "manual_listening": False,
    "passed": levels["passed"] and speech["pass"] and preservation["passed"] and voice["exact_normalized_match"],
}
args.report.parent.mkdir(parents=True, exist_ok=True)
args.report.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2), flush=True)
if not report["passed"]:
    raise SystemExit("Export audio verification failed")
