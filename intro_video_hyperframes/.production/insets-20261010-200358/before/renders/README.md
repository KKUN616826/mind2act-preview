# Mind2Act World promotional film

Latest delivery: **62.23 seconds at 1920×1080 / 30 fps**, with English narration and the supplied music treated as a separate instrumental stem. The authored timeline is 62.222222 s; MP4 duration is rounded to a video frame boundary.

- `mind2act-world-promo-1080p-20261010-180033.mp4` — revised delivery master, H.264/AAC, 72.0 MB.
- `mind2act-world-promo-web-20261010-180033.mp4` — website copy with faststart, 10.5 MB. AAC is copied unchanged from the master.
- `mind2act-world-poster-20261010-180033.jpg` — current opening brand frame.
- `mind2act-world-narration-20261010-180033.srt` / `.vtt` — synchronized English captions.
- `preview-20261010-180033.html` — standalone local video player with captions.
- `delivery.json` — actual verified technical details and hashes.

For the website, use the timestamped web MP4, poster and VTT above. The local player provides the same `<video controls playsinline>` setup. Editable HyperFrames preview: http://localhost:3052/#project/mind2act-hyperframes-blank-20261010-111117.

This revision preserves the selected blue-cup meal-packing, drawing and CP05 piano clips, and all historical renders. The independent Mind and Act marks plus three connector dots resolve into the complete original logo. Opening and closing use the supplied pixel wordmark without redrawing its glyphs. A new bidirectional task-logic scene follows the cases; actual green-key responses precede feedback pulses. It does not claim to reveal model internal state, recovery or performance.

The editable project is one directory above, split into eight compositions. Use `bash scripts/hyperframes.sh check` and the pinned HyperFrames 0.8.143 wrapper. Current provenance, audio scripts, render script, final AAC audit and actual exported-frame reviews are in `.production/coordination-20261010-174012/`. Earlier generator scripts are historical and would restore old copy/timing if rerun; edit the current compositions or use this revision's export script. All original supplied files remain in `assets/`.

Statistics have no narration. Easy/Medium/Hard were regenerated and normalized individually; the three voice cues differ by 0.05 LU. The final AAC measures -16.09 LUFS and -2.38 dBTP. Encoded audio, source stems and ASR/VAD were checked; these measurements are not an assertion of manual listening. Detailed limitations are recorded with the audio evidence.

## Clarity restoration

The selected drawing/piano footage, six-tile intro and rapid montage retain the previous conservative Real-ESRGAN restoration. Original sources are unchanged. The added continuous loop excerpt uses a direct Lanczos upscale of the same original CP05 source; it does not synthesize motion. Master uses HyperFrames delivery quality; the compact website copy uses CRF 23. Restoration cannot recover true original HD pixels. Earlier provenance remains in `.production/clarity-20261010-155258/`.

## First-version meal-packing restoration

The meal-packing spotlight preserves its three original first-version clips, matching blue-cup order still and source timing. This revision simplifies the surrounding motion and captions. The previous films remain available under their original timestamps, including 20261010-163109. Historical source manifest: `.production/restore-p-first-20261010-163109/manifest.json`.
