# Difficulty grid audio revision

The existing Kokoro `am_michael` voice, music source, and ten narration cue files are retained. `reused-voice-integrity.json` verifies SHA256 equality for all ten existing processed cues, including Easy, Medium and Hard. Only the ending placement moves +0.9 seconds.

The new cue is “More rules. Tighter turns. More to remember—and do.” at global 60.033333–63.261792 seconds. Speed 1.03; no atempo acceleration. `narration-asr-report.json` independently transcribes it without supplying expected text and provides word timestamps. Recommended difficulty-local row emphasis: F6.70, PR3 7.66, CP02 8.60; “and do”9.26–9.74.

The same original song is continuously extracted from source offset11.9877 through86.9617740741 seconds (74.974074 seconds). Demucs4.0.1 `htdemucs`, CPU, processes this music-only cut. No music looping, zero padding or voice source separation. The new instrumental bed is long enough before mixing; mixer rejects insufficient coverage. BGM is spectrally carved at1/2.5kHz and ducked under the narration bus; narration, music and FX remain separate stems.

Master WAV is74.974083 seconds, -15.99 LUFS, -2.60 dBTP. Easy/Medium/Hard loudness spread is0.05dB. Narration is exactly zero at41.481481–53.333333 and63.833333–66.085185 seconds. `music-vad-report.json` detects no speech in the complete BGM or either corresponding final-mix interval. Unprompted full-bed ASR produced repetitive artifacts around57.24–59.84 seconds (no-speech probability0.946, initial token probability0.011, mostly zero-duration words) and a common end-of-file “Thanks for watching” artifact (no-speech0.821, first token probability0.008). No coverage-interval words were returned. These are consistent with music-driven ASR hallucinations and do not indicate detected intelligible vocals. Detector checks are not a human listening certification.

Render-stage checks are ready:

```bash
.production/audio/venv/bin/python .production/difficulty-grid-20261011-090243/audio/audit_render_audio.py RENDERED_MASTER.mp4
.production/coordination-20261010-174012/audio/separation-venv/bin/python .production/difficulty-grid-20261011-090243/audio/check_rendered_speech.py RENDERED_MASTER.mp4
```

Actual exported master `mind2act-world-promo-1080p-20261011-092248.mp4` passed decoded AAC audit: -16.10 LUFS, -2.63dBTP, full WAV/AAC correlation0.997042. All11 cue correlations >0.99 and gain errors <0.3dB. Independent unprompted ASR correctly transcribed Easy, Medium, Hard and the complete new sentence. Both coverage and numeric payoff produce no detected speech in actual AAC. Checks are automated, not manual listening.
