"""Versioned local voice generation and independently processed audio stems."""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import math
import shutil
import subprocess

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent
SPEC = json.loads((WORK / "narration.json").read_text())
OUT = ROOT / "assets/generated/audio" / SPEC["version"]
FFMPEG = "/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg"
MODEL = Path("/home/xzy/.cache/hyperframes/tts/models/kokoro-v1.0.onnx")
VOICES = Path("/home/xzy/.cache/hyperframes/tts/voices/voices-v1.0.bin")
SFX = Path("/home/xzy/.claude/plugins/cache/hyperframes/hyperframes/0.8.143/skills/media-use/audio/assets/sfx")
SR = SPEC["sample_rate"]
N = round(SPEC["duration"] * SR)


def ff(args):
    return subprocess.run([FFMPEG, "-nostdin", "-hide_banner", "-y", *map(str, args)], capture_output=True, text=True, check=True)


def digest(path):
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def loudness(path):
    result = ff(["-i", path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=10:print_format=json", "-f", "null", "-"])
    data, _ = json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind("{"):])
    return {key: float(data[key]) for key in ("input_i", "input_tp", "input_lra", "input_thresh")}


def save(path, samples):
    sf.write(path, samples, SR, subtype="PCM_24")


def generate():
    import kokoro_onnx
    from kokoro_onnx.config import EspeakConfig
    import espeakng_loader
    import onnxruntime as ort

    OUT.mkdir(parents=True, exist_ok=True)
    short_data = Path("/home/xzy/.cache/mind2act-espeak-ng-data")
    if not short_data.exists():
        shutil.copytree(espeakng_loader.get_data_path(), short_data)
    options = ort.SessionOptions()
    options.intra_op_num_threads = 4
    options.inter_op_num_threads = 2
    session = ort.InferenceSession(str(MODEL), sess_options=options, providers=["CPUExecutionProvider"])
    model = kokoro_onnx.Kokoro.from_session(session, str(VOICES), espeak_config=EspeakConfig(data_path=str(short_data)))
    provenance = {
        "provider": SPEC["provider"], "provider_version": importlib.metadata.version("kokoro-onnx"),
        "model_sha256": digest(MODEL), "voices_sha256": digest(VOICES),
        "voice": SPEC["voice"], "language": SPEC["language"]
    }
    cache = []
    for cue in SPEC["lines"]:
        key_data = {**provenance, "text": cue["text"], "speed": cue["speed"]}
        key = hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
        raw = OUT / f"vo-{cue['id']}-{key[:16]}-raw.wav"
        if not raw.exists():
            samples, rate = model.create(cue["text"], voice=SPEC["voice"], speed=cue["speed"], lang=SPEC["language"])
            sf.write(raw, samples, rate, subtype="PCM_24")
        samples, rate = sf.read(raw)
        cache.append({**cue, "cache_key": key, "cache_parameters": key_data, "raw_path": str(raw), "raw_duration": len(samples) / rate})
        print(cue["id"], f"{len(samples) / rate:.3f}s", flush=True)
    (WORK / "voice-cache.json").write_text(json.dumps(cache, indent=2) + "\n")


def source():
    OUT.mkdir(parents=True, exist_ok=True)
    ff(["-ss", SPEC["music_source_offset"], "-i", ROOT / "assets/audio/The Midnight - The Equaliser (Not Alone).mp3", "-t", SPEC["duration"], "-ar", SR, "-ac", 2, "-c:a", "pcm_s24le", OUT / "music-source-cut.wav"])


def subtitles(cues):
    def stamp(value, separator):
        ms = round(value * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02}{separator}{ms % 1000:03}"
    srt, vtt = [], ["WEBVTT\n"]
    for index, cue in enumerate(cues, 1):
        srt.append(f"{index}\n{stamp(cue['start'], ',')} --> {stamp(cue['end'], ',')}\n{cue.get('caption', cue['text'])}\n")
        vtt.append(f"{stamp(cue['start'], '.')} --> {stamp(cue['end'], '.')}\n{cue.get('caption', cue['text'])}\n")
    (OUT / "narration.srt").write_text("\n".join(srt))
    (OUT / "narration.vtt").write_text("\n".join(vtt))


def mix(bed_path):
    OUT.mkdir(parents=True, exist_ok=True)
    voice = np.zeros((N, 2), dtype=np.float64)
    activity = np.zeros(N)
    cues = []
    cache = json.loads((WORK / "voice-cache.json").read_text())
    for cue in cache:
        raw, rate = sf.read(cue["raw_path"])
        active = np.flatnonzero(np.abs(raw) > max(0.001, np.max(np.abs(raw)) * 0.005))
        if not len(active):
            raise ValueError(f"Silent source: {cue['id']}")
        lo = max(0, active[0] - round(0.035 * rate))
        hi = min(len(raw), active[-1] + round(0.065 * rate))
        duration = (hi - lo) / rate
        tempo = max(1.0, duration / cue["max_duration"])
        if tempo > 1.18:
            raise ValueError(f"VO needs rewrite rather than excessive acceleration: {cue['id']} {tempo}")
        clean = OUT / f"vo-{cue['id']}-clean.wav"
        ff(["-i", cue["raw_path"], "-af", f"atrim=start={lo / rate}:end={hi / rate},asetpts=PTS-STARTPTS,atempo={tempo:.9f},highpass=f=75,acompressor=threshold=0.0630957:ratio=3:attack=3:release=70:knee=2.828:makeup=1,alimiter=limit=0.2511886:attack=2:release=50:level=false:latency=true,afade=t=in:st=0:d=0.012", "-ar", SR, "-ac", 1, "-c:a", "pcm_s24le", clean])
        before = loudness(clean)
        # A static measured gain avoids the old short-cue loudnorm failure.
        gain_db = -17.0 - before["input_i"]
        final = OUT / f"vo-{cue['id']}.wav"
        for _ in range(4):
            ff(["-i", clean, "-af", f"volume={gain_db:.8f}dB,alimiter=limit=0.562341:attack=3:release=65:level=false:latency=true", "-ar", SR, "-ac", 1, "-c:a", "pcm_s24le", final])
            after = loudness(final)
            if abs(after["input_i"] + 17.0) < 0.15:
                break
            gain_db += -17.0 - after["input_i"]
        samples, _ = sf.read(final)
        start = round(cue["start"] * SR)
        end = start + len(samples)
        if end > N:
            raise ValueError(f"VO extends beyond composition: {cue['id']}")
        voice[start:end] += samples[:, None]
        attack = max(0, start - round(0.16 * SR))
        release = min(N, end + round(0.4 * SR))
        activity[attack:start] = np.maximum(activity[attack:start], np.linspace(0, 1, start - attack))
        activity[start:end] = 1
        activity[end:release] = np.maximum(activity[end:release], np.linspace(1, 0, release - end))
        cues.append({**cue, "path": str(final), "trim_start": lo / rate, "trim_end": hi / rate, "atempo": tempo, "gain_db": gain_db, "end": end / SR, "final_duration": len(samples) / SR, "before_gain": before, "measurement": loudness(final)})
        print(cue["id"], cues[-1]["measurement"], flush=True)

    gap_start, gap_end = (round(t * SR) for t in SPEC["statistics_music_only"])
    if np.max(np.abs(voice[gap_start:gap_end])) != 0:
        raise ValueError("Statistics interval contains narration")
    for interval in SPEC["music_only_intervals"]:
        lo, hi = (round(t * SR) for t in interval)
        if np.max(np.abs(voice[lo:hi])) != 0:
            raise ValueError(f"Music-only interval contains narration: {interval}")
    words = [cue["measurement"]["input_i"] for cue in cues if cue["id"] in ("scale-easy", "scale-medium", "scale-hard")]
    if max(words) - min(words) > 2:
        raise ValueError(f"Difficulty VO loudness mismatch: {words}")

    music, music_rate = sf.read(bed_path)
    if music_rate != SR or music.ndim != 2 or music.shape[1] != 2:
        resampled = OUT / "music-bed-resampled.wav"
        ff(["-i", bed_path, "-ar", SR, "-ac", 2, "-c:a", "pcm_s24le", resampled])
        music, _ = sf.read(resampled)
    music = np.pad(music[:N], ((0, max(0, N - len(music))), (0, 0)))
    clean_bed = OUT / "music-bed-clean.wav"
    save(clean_bed, music)
    # Only the music is carved, against the full narration bus envelope.
    carved_path = OUT / "music-bed-carved.wav"
    ff(["-i", clean_bed, "-af", "equalizer=f=1000:t=q:w=0.8:g=-2,equalizer=f=2500:t=q:w=0.8:g=-4", "-ar", SR, "-c:a", "pcm_s24le", carved_path])
    carved, _ = sf.read(carved_path)
    music = music * (1 - activity[:, None]) + carved * activity[:, None]
    music *= np.power(10, (-8.5 - 6 * activity[:, None]) / 20)
    fade = np.ones(N)
    fin, fout = round(0.07 * SR), round(1.3 * SR)
    fade[:fin] = np.linspace(0, 1, fin)
    fade[-fout:] = np.linspace(1, 0, fout) ** 1.25
    music *= fade[:, None]

    sfx = np.zeros_like(voice)
    placements = SPEC["sfx_placements"]
    for name, start, level in placements:
        result = subprocess.run([FFMPEG, "-v", "error", "-i", str(SFX / (name + ".mp3")), "-ar", str(SR), "-ac", "2", "-f", "f32le", "-"], capture_output=True, check=True)
        samples = np.frombuffer(result.stdout, np.float32).reshape(-1, 2).astype(np.float64)
        samples *= 10 ** (level / 20) / (np.sqrt(np.mean(samples ** 2)) + 1e-9)
        at = round(start * SR)
        length = min(len(samples), N - at)
        sfx[at:at + length] += samples[:length]
    premaster = OUT / "soundtrack-premaster.wav"
    save(premaster, voice + music + sfx)
    measured = loudness(premaster)
    master_gain = min(-16.0 - measured["input_i"], -1.65 - measured["input_tp"])
    factor = 10 ** (master_gain / 20)
    stems = {"narration": voice, "music": music, "sfx": sfx}
    for name, samples in stems.items():
        save(OUT / (name + "-stem.wav"), samples * factor)
    master = OUT / f"soundtrack-{SPEC['version']}.wav"
    save(master, (voice + music + sfx) * factor)
    final_measurement = loudness(master)
    if abs(final_measurement["input_i"] + 16) > 0.6 or final_measurement["input_tp"] > -1.5:
        raise ValueError(f"Master out of bounds: {final_measurement}")
    subtitles(cues)
    shutil.copy(SFX / "CREDITS.md", OUT / "SFX-CREDITS.md")
    for name, start, duration, src in [("statistics-music-only", 41.481482, 11.851851, master), ("difficulty-vo", 53.333333, 6.5, OUT / "narration-stem.wav"), ("difficulty-fullmix", 53.333333, 11.851852, master), ("coordination-loop", 29.62963, 11.851852, master), ("closing", 65.185185, 8.888889, master), ("bgm-only", 0, SPEC["duration"], OUT / "music-stem.wav")]:
        ff(["-ss", start, "-i", src, "-t", duration, "-c:a", "pcm_s24le", OUT / f"review-{name}.wav"])
    report = {
        **SPEC, "audio_path": str(master), "stems": {name: str(OUT / (name + "-stem.wav")) for name in stems},
        "subtitles": {"srt": str(OUT / "narration.srt"), "vtt": str(OUT / "narration.vtt")},
        "voice": cues, "music_input": str(bed_path), "music_source_sha256": digest(ROOT / "assets/audio/The Midnight - The Equaliser (Not Alone).mp3"),
        "music_processing": {"source_offset": SPEC["music_source_offset"], "source_end": SPEC["music_source_offset"] + SPEC["duration"], "vocal_separation": "Demucs 4.0.1 htdemucs vocals/no_vocals, BGM only" if "no_vocals" in str(bed_path) else "none", "voice_processed_by_separator": False, "asr_report": str(WORK / "bgm-asr-report.json"), "manual_listening": False},
        "carve": {"source": "narration bus only", "bed_only": True, "bands_hz": [1000, 2500], "max_cut_db": [-2, -4], "duck_db": 6, "anticipation_seconds": 0.16, "release_seconds": 0.4},
        "sfx": placements, "mastering": {"target_lufs": -16, "ceiling_dbtp": -1.5, "premaster": measured, "static_gain_db": master_gain, "final": final_measurement},
        "qa": {"statistics_narration_peak": 0, "difficulty_lufs_spread": max(words) - min(words), "difficulty_lufs": words, "authored_sample_count": N, "sample_rate": SR, "actual_duration": N / SR, "manual_listening": False},
        "review_samples": [str(path) for path in sorted(OUT.glob("review-*.wav"))]
    }
    (WORK / "audio-integration.json").write_text(json.dumps(report, indent=2) + "\n")
    print("COMPLETE", master, final_measurement, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["voice", "source", "mix"])
    parser.add_argument("--bed", type=Path)
    args = parser.parse_args()
    if args.stage == "voice":
        generate()
    elif args.stage == "source":
        source()
    else:
        mix(args.bed or OUT / "music-source-cut.wav")
