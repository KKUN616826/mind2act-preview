# Coordination audio revision — 2026-10-10 17:40:12 +08:00

The authored soundtrack is `assets/generated/audio/coordination-20261010-174012/soundtrack-coordination-20261010-174012.wav`, relative to the original project root. The complete integration manifest is `audio-integration.json` beside this file. The original project audio and historical renders are retained.

The ten new narration cues use the same local Kokoro `am_michael` voice. Cache keys include narration text, speed, language, provider version, and SHA-256 hashes of the model and voice bank. The two former statistics narration cues are absent. The narration stem is exactly zero from 40.740741 through 48.680700 seconds, including the new 45.00–48.55 statistics display.

The old short-cue two-pass normalization caused very quiet statistics phrases and Hard. The new chain trims only edge silence, applies the same high-pass/compression to narration, then uses measured static gain and a bounded limiter. Every final cue is measured again. Difficulty cues measure -17.01, -17.02, and -17.06 LUFS before the common master gain; their spread is 0.05 LU. No narration was sent through vocal separation.

The original song is retained at source offset 11.9877 seconds for 62.222222 seconds. Demucs 4.0.1 `htdemucs` separated this BGM-only cut on CPU. The no-vocals stem is the music input. Separation outputs are under `separated/htdemucs/music-source-cut/`. The classified vocal component was already very low: -57.41 dBFS RMS overall and -61.75 dBFS in 40.7407–48.6807 seconds. These measurements do not prove that the component is human speech.

Independent faster-whisper 1.2.1 `medium.en`, int8 CPU, checked the original music and both separator outputs. The original music produced a repetitive, implausible tail transcript with no-speech probabilities 0.949–0.964. The separated no-vocals bed produced only tail tokens “Oh” and “You” with no-speech probabilities 0.948–0.959 and word probabilities 0.014/0.140. No speech tokens were returned for the 40.7407–48.6807 music interval. These results support no detected intelligible lyrics, but are not a listening certification. `bgm-asr-report.json` records the separator-output checks; `separation-measurement.json` records interval measurements. Review WAV samples are provided for listening. No actual human listening has been claimed.

Music is adaptively carved only under the complete narration bus, with 1 kHz/2.5 kHz dips and 6 dB ducking, 160 ms anticipation, and 400 ms release. Music, narration and SFX remain separate stems. A common master gain preserves their exact sum. Final WAV: -15.99 LUFS, -2.66 dBTP, 62.222229 seconds at 48 kHz.

Reproduce from the project root:

```bash
.production/audio/venv/bin/python .production/coordination-20261010-174012/audio/build_audio.py voice
.production/audio/venv/bin/python .production/coordination-20261010-174012/audio/build_audio.py source
OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 .production/coordination-20261010-174012/audio/separation-venv/bin/python -m demucs --two-stems=vocals -n htdemucs -d cpu --float32 --shifts 1 --jobs 1 -o .production/coordination-20261010-174012/audio/separated assets/generated/audio/coordination-20261010-174012/music-source-cut.wav
.production/audio/venv/bin/python .production/coordination-20261010-174012/audio/build_audio.py mix --bed .production/coordination-20261010-174012/audio/separated/htdemucs/music-source-cut/no_vocals.wav
.production/audio/venv/bin/python .production/coordination-20261010-174012/audio/audit_render_audio.py /absolute/path/to/final.mp4
```

`narration.srt` and `narration.vtt` use final clip timing and contain no obsolete statistics phrases. The AAC audit verifies decoded duration, loudness and true peak, each cue's correlation and gain relative to the approved WAV, and the zero-narration statistics interval; it emits a JSON result and short rendered difficulty samples. It does not substitute for listening.

Independent `medium.en` ASR also checked all ten processed narration cues without receiving expected text as a prompt. All ten transcripts match their intended text after ignoring case and punctuation, including Hard. Evidence: `narration-asr-report.json`. The first coordination sentence occupies approximately 30.04–32.84 seconds; the second occupies 32.84–37.743667 seconds. Subtitle clip boundaries come from the authored audio, because ASR segment endpoints on short isolated words can exceed the actual file duration.
