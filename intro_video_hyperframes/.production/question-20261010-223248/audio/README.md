# Opening question audio revision — 2026-10-10 22:32:48 +08:00

User-approved one-line edit: “Can reasoning and action work together?” replaces “Can strong parts make a reliable whole?” at5.75s. Same Kokoro `am_michael` voice, en-us, synthesis speed1.03. Only that line is newly synthesized. Its subtitle uses exact requested wording. The other nine raw voice files reuse prior caches, and processed voice identity is checked by SHA256 after rebuilding.

All scene timings, other narration text, instrumental music input, selected song offset, SFX placements, spectral carve parameters, fades and mastering target stay the same as categories-20261010-215252. The same frozen Demucs `no_vocals.wav` is reused; no new source separation is needed and no VO is ever sent through vocal removal. The provenance report reuses prior BGM analysis; only changed narration requires fresh ASR. Counts/coverage41.481481–53.333333 and numericpayoff62.6–65.185185 remain VO-free.

Artifacts: `audio-integration.json`, `narration-asr-report.json`, `reused-voice-integrity.json`. Final WAV/SRT/VTT/stems are under `assets/generated/audio/question-20261010-223248/`. Generic `audit_render_audio.py` is copied into this audio revision for auditing the newly exported MP4, including cue correlation/gain, loudness/truepeak, duration and silent narration windows.

Reproduce using existing local environment from project root:

```bash
.production/audio/venv/bin/python .production/question-20261010-223248/audio/build_audio.py voice
.production/audio/venv/bin/python .production/question-20261010-223248/audio/build_audio.py mix --bed .production/categories-20261010-215252/audio/separated/htdemucs/music-source-cut/no_vocals.wav
.production/audio/venv/bin/python .production/question-20261010-223248/audio/audit_render_audio.py /absolute/path/to/final.mp4
```

No root composition or project documentation edited by this audio subtask. Human listening is not claimed; automated evidence and review WAVs are supplied.

## Verification

New motivation cue5.75–8.061167s, duration2.311167s, -17.05LUFS/-4.78dBTP before common master gain. Independent medium.en ASR (no supplied expected text) returned the exact requested sentence; no-speech probability0.000934. All9other processed VO files have identical SHA256 to categories-20261010-215252. FinalWAV74.074083s, -16.00LUFS/-2.42dBTP. Every configured narration-free interval remains exactlyzero in narrationstem. Existingthree difficulty files unchanged, loudness spread0.05LU.

Final deliveredMP4 audit remains the responsibility of the root export step using the copied generic audit script; this audio subtask did not render or inspect a newMP4.
