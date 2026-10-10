"""Compare the final decoded AAC with the independently verified WAV master."""
from pathlib import Path
import argparse
import json
import subprocess
import numpy as np
import soundfile as sf

FFMPEG = "/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg"
parser = argparse.ArgumentParser()
parser.add_argument("video", type=Path)
args = parser.parse_args()
work = Path(__file__).resolve().parent
manifest = json.loads((work / "audio-integration.json").read_text())
sample_rate = manifest["sample_rate"]
result = subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-i", str(args.video), "-map", "0:a:0", "-ar", str(sample_rate), "-ac", "2", "-f", "f32le", "-"], capture_output=True, check=True)
actual = np.frombuffer(result.stdout, np.float32).reshape(-1, 2)
expected, _ = sf.read(manifest["audio_path"])
count = min(len(actual), len(expected))
decoded_path = work / f"{args.video.stem}-decoded-aac.wav"
sf.write(decoded_path, actual, sample_rate, subtype="PCM_24")
measurement = subprocess.run([FFMPEG, "-nostdin", "-hide_banner", "-i", str(decoded_path), "-af", "loudnorm=I=-16:TP=-1.5:LRA=10:print_format=json", "-f", "null", "-"], capture_output=True, text=True, check=True)
metrics, _ = json.JSONDecoder().raw_decode(measurement.stderr[measurement.stderr.rfind("{"):])
rows = []
for cue in manifest["voice"]:
    start, end = (round(value * sample_rate) for value in (cue["start"], cue["end"]))
    reference = expected[start:min(end, count)].ravel()
    decoded = actual[start:min(end, count)].ravel()
    correlation = float(np.corrcoef(reference, decoded)[0, 1])
    ratio = float(np.sqrt(np.mean(decoded ** 2)) / np.sqrt(np.mean(reference ** 2)))
    error_db = 20 * float(np.log10(max(ratio, 1e-12)))
    rows.append({"id": cue["id"], "start": cue["start"], "end": cue["end"], "master_vs_aac_correlation": correlation, "gain_error_db": error_db, "expected_vo_lufs": cue["measurement"]["input_i"], "passed": correlation > 0.99 and abs(error_db) < 0.3})
    if cue["id"].startswith("scale-"):
        sf.write(work / f"review-rendered-{cue['id']}.wav", actual[max(0, start - round(0.08 * sample_rate)):min(len(actual), end + round(0.08 * sample_rate))], sample_rate, subtype="PCM_24")
gap_start, gap_end = (round(value * sample_rate) for value in manifest["statistics_music_only"])
narration, _ = sf.read(manifest["stems"]["narration"])
report = {
    "video": str(args.video.resolve()), "decoded_audio": str(decoded_path), "master": manifest["audio_path"],
    "master_vs_aac_correlation": float(np.corrcoef(expected[:count].ravel(), actual[:count].ravel())[0, 1]),
    "wav_duration": len(expected) / sample_rate, "decoded_aac_duration": len(actual) / sample_rate,
    "loudness_lufs": float(metrics["input_i"]), "true_peak_dbtp": float(metrics["input_tp"]),
    "cue_checks": rows, "statistics_narration_peak": float(np.max(np.abs(narration[gap_start:gap_end]))),
    "difficulty_lufs_spread": manifest["qa"]["difficulty_lufs_spread"],
    "manual_listening": False, "bgm_listening_sample": manifest["review_samples"],
}
report["passed"] = all(row["passed"] for row in rows) and abs(report["loudness_lufs"] + 16) < 0.6 and report["true_peak_dbtp"] <= -1.5 and abs(report["decoded_aac_duration"] - report["wav_duration"]) < 0.08 and report["statistics_narration_peak"] == 0
(work / f"{args.video.stem}-aac-audit.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({key: report[key] for key in ("video", "master_vs_aac_correlation", "loudness_lufs", "true_peak_dbtp", "passed")}, indent=2))
if not report["passed"]:
    raise SystemExit(1)
