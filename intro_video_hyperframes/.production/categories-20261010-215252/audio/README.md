# Audio revision — categories-20261010-215252

Same selected music identity and Kokoro `am_michael` voice. One changed cue: CP05 now names sequence memory plus valid key presses, distinguishing that category demonstration from the following abstract coordination definition. All nine unchanged processed cues are SHA-256 identical to the earlier approved revision; their previous independent ASR checks remain valid. The new cue was independently transcribed without expected text and matches exactly after punctuation normalization.

The source song remains `assets/audio/The Midnight - The Equaliser (Not Alone).mp3`, source offset 11.9877 seconds. This cut was extended naturally to 74.074074 seconds; its beat grid is unchanged at 81 BPM. Demucs 4.0.1 `htdemucs`, CPU, separated this BGM-only cut into vocals/no_vocals. The no-vocals track is the only music input. Narration was never sent to source separation. Music is adaptively carved against the complete narration bus and faded to silence at the ending. Narration, music and SFX remain separate stems.

Final authored WAV: **74.074083 s, 48 kHz stereo PCM24, -16.00 LUFS, -2.42 dBTP**. Difficulty cue integrated loudness before common master gain: Easy -17.01, Medium -17.02, Hard -17.06 LUFS (spread 0.05 LU). Measured static gain avoids the prior short-word normalization bug.

Narration is exactly zero throughout coverage 41.481481–53.333333 and the numeric payoff 62.6–65.185185. The complete separated BGM and both final-mix silent-narration intervals produce no speech segments under Silero VAD at the default 0.5 threshold. Unprompted medium.en ASR produced low-confidence tail artifacts on music: “Oh” at ~58.6 s (word probability 0.014, no-speech 0.95) and an end-of-file “Thanks for watching” artifact (initial probability 0.007, no-speech 0.80, later tokens zero-duration at file end). No intelligible speech was detected in the coverage interval. These are detector checks, not a human listening certification. Review WAVs are delivered.

## Cue timing

| Cue | Start | End | Display text |
|---|---:|---:|---|
| intro | 0.280000 | 4.477458 | Mind2Act World. Reasoning and action, evaluated together. |
| motivation | 5.750000 | 8.035625 | Can strong parts make a reliable whole? |
| mind | 12.220000 | 15.472792 | Mind tracks the task through observations and history. |
| act | 18.120000 | 21.209000 | Act must make the intended physical result happen. |
| mind2act | 24.030000 | 27.839750 | Mind2Act links sequence memory with valid key presses. |
| coordination-loop | 30.040000 | 37.743667 | Intent guides physically valid action. Actual outcomes update what remains, when to act, and which phase comes next. |
| scale-easy | 53.683333 | 54.403333 | Easy. |
| scale-medium | 55.783333 | 56.576042 | Medium. |
| scale-hard | 57.883333 | 58.576958 | Hard. |
| ending | 65.881852 | 70.777021 | Build the benchmark. Test your agents. Let's take the next giant leap together. |

## Artifacts

- `audio-integration.json`: paths, source hashes, cue timing, loudness, stems and mixing parameters.
- `reused-voice-integrity.json`: unchanged processed-cue hashes.
- `narration-asr-report.json`: independent new CP05 cue check.
- `bgm-asr-report.json` and `music-vad-report.json`: independent music checks.
- `narrative-review.md`: category and claim audit against reference positioning.
- Output assets: `assets/generated/audio/categories-20261010-215252/`.
- `narration.srt` and `narration.vtt`: final authored clip timing; display spelling Mind2Act, spoken spelling Mind to Act.

Reproduce from the project root using the existing local voice/separation environments. The local voice is retained for continuity, as already selected for the film; no provider change or credential flow is needed.

```bash
.production/audio/venv/bin/python .production/categories-20261010-215252/audio/build_audio.py voice
.production/audio/venv/bin/python .production/categories-20261010-215252/audio/build_audio.py source
OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 .production/coordination-20261010-174012/audio/separation-venv/bin/python -m demucs --two-stems=vocals -n htdemucs -d cpu --float32 --shifts 1 --jobs 1 -o .production/categories-20261010-215252/audio/separated assets/generated/audio/categories-20261010-215252/music-source-cut.wav
.production/audio/venv/bin/python .production/categories-20261010-215252/audio/build_audio.py mix --bed .production/categories-20261010-215252/audio/separated/htdemucs/music-source-cut/no_vocals.wav
.production/audio/venv/bin/python .production/categories-20261010-215252/audio/audit_render_audio.py /absolute/path/to/final.mp4
```

The render audit compares the decoded final AAC against the WAV, including per-cue correlation/gain, final loudness and true peak, duration and zero-VO intervals. It must run on the final delivered render; current WAV verification does not establish final render correctness.

## Final actual-export verification

`renders/mind2act-world-promo-1080p-20261010-221251.mp4` actual AAC passed audit. Decoded audio74.090667s versus authoredWAV74.074083s (AAC padding16.6ms), -16.10LUFS, -2.45dBTP. Fullmix correlation with WAV0.996799; all10cuewindows pass, per-cue gain deviation within0.107dB and per-cue correlation≥0.9972. Hard specifically: correlation0.997466, gain deviation-0.0854dB, so no short-cue muting occurred on export.

Unprompted independent `medium.en` ASR correctly returned Easy, Medium and Hard from their actual mixedAAC excerpts. Hard wordprobability0.485 (the final mix includes music), transcript “Hard.”; this supports rendered intelligibility but is not an assertion of human listening. Actual AAC coverage41.481481–53.333333 and numericpayoff62.6–65.185185 each yielded noSileroVAD speech intervals. Narrationstem is exactlyzero there. No manual-listening certification is claimed.

Evidence: `mind2act-world-promo-1080p-20261010-221251-aac-audit.json`, `mind2act-world-promo-1080p-20261010-221251-actual-speech-audit.json`; actual mixed short review WAVs beside these reports.
