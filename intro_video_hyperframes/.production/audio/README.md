# Mind2Act World audio production

Final composition media: `assets/generated/audio/soundtrack.wav`. Place at timeline zero, unity gain. The file is already mixed and mastered; do not apply additional ducking or normalization.

- Duration: 47.407417 seconds (64 beats at 81 BPM).
- Provided music: The Midnight — The Equaliser (Not Alone), source offset 11.9877 seconds.
- Measured master: −15.9 LUFS, −1.5 dBTP; 48 kHz stereo PCM 24 bit.
- Narrator: local Kokoro-82M, `am_michael`, generated from new English copy for this project. The same model/voices used by HyperFrames TTS were used directly after the CLI exposed eSpeak's path-length limit inside the deeply nested project. The reproducible Python generator supplies a short eSpeak cache path.
- Music: 6 dB speech duck, 2 dB presence-band carve, beat-aligned transition accents, final musical fade.
- Sound effects: HyperFrames bundled Pixabay assets; credits copied alongside final audio.
- `audio-timing.json`: source/scene timing, all 11 spoken cues, processing metadata and verified master measurements.
- `narration.srt`: sentence/short-cue subtitles aligned to final processed takes. No artificial word timestamps.
- `soundtrack-preview.m4a`: compact AAC preview of the final master.
- `narration-stem.wav`, `music-stem.wav`, `sfx-stem.wav`: individual premaster stems, for further editing.

To regenerate, use the dedicated `.production/audio/venv/bin/python` and run `generate_voice.py`, `mix_audio.py`, and `export_captions.py` from the project root. Rendering the completed video does not require this Python environment. Exclude the venv, raw takes, premaster and temporary EQ file from a distribution package unless source-production intermediates are wanted.
