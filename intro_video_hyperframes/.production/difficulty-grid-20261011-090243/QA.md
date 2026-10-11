# Difficulty comparison revision

The current edit preserves the Easy / Medium / Hard hero typography, source clips, narration and cuts for the first 6.34 seconds of the difficulty scene. The comparison then opens into three stable task rows under shared difficulty headers. The original 45 reveal follows 0.9 seconds later; the final film is 75 seconds at 1920×1080, 30 fps.

## Evidence and factual checks

- F uses real navigation footage, with the goal, slider and control buttons retained. Common crop preserves relative track and grid size.
- PR3 uses unobstructed source reference frames at a common crop and scale. No synthetic paths or reconstructed performance traces.
- CP02 uses the initial examples to remember. Counts are 4 / 6 / 6. The Hard cell switches to source footage of the real cover lowering, with landing visible before the statistics transition. No completion badges or performance scores.
- `media-provenance.json` records source files, hashes, times, crops, and derived file hashes.
- All eight unrelated composition files match the previous delivery SHA-256 values. Existing ten voice cues are byte-identical. Only the new difficulty sentence was synthesized.

## Visual review

- Full-project runtime/layout/contrast check passed; after the final small label-timing fix, focused transition/grid/cover/statistics checks also passed.
- The only inherited lint warning concerns intentional duplicate PR3 reference-image roles in the Act composition.
- Independent snapshot review found brief text overlaps in the handoff. Final choreography sequences titles, moves only the active Hard hero, places hidden Easy/Medium at final positions, and introduces row labels after the moving word has cleared them.
- Actual encoded transition and cover sequences reviewed in `rendered/handoff-sheet.jpg` and `rendered/cover-sheet.jpg`.
- Actual web output reviewed at 960×540 in `rendered/comparison-web-960.jpg`: track/grid differences, three reference curves, cake quantities and captions remain visible.
- `animation-review.json` explains animation-map parent/child collision flags, duplicate timeline enumeration, intended fades and existing holds.
- Source photographic media retained its original color treatment; cropping and scale supply the requested clarity without invented details.

## Audio and delivery checks

- Actual exported AAC measures −16.10 LUFS and −2.63 dBTP. All eleven cues correlate with the independently prepared WAV; maximum cue gain difference is under 0.083 dB.
- Independent unprompted transcription correctly recognizes Easy, Medium, Hard and “More rules. Tighter turns. More to remember—and do.”
- No VAD speech intervals in the actual encoded coverage showcase or numerical payoff. The narration stem is exactly silent in those intervals.
- Master and compact web MP4 fully decoded without errors. Both are H.264, yuv420p, 1920×1080, 30 fps, stereo AAC, 75 seconds.
- Export audio verification uses transcription, waveform, loudness and VAD checks; it does not claim manual listening.
- Promotion verifies that historical master/web SHA-256 values remain unchanged, and that master and compact web share identical AAC packet streams.

See `exported-visual-review.json`, `check-final.json`, `check-before-label-timing.json`, `audio/*-aac-audit.json` and `audio/*-actual-speech-audit.json` for detailed results.
