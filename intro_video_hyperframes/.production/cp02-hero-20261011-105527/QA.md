# CP02 difficulty hero and complete cake framing

Scope: replace the difficulty hero's F footage with CP02 reference cakes and real Hard cover placement. Preserve the Easy/Medium/Hard typography, narration, music, scene duration and other compositions. Repair the cropped cake comparison row.

## Source and framing

All three reference images use the initial0.7-second frame of their original demonstrations. Common crop448×252 at128,66 preserves the complete cake and plinth, with4/6/6 visible pieces. Hard also contains the separate lid. The cover clip uses original95.7–97.9seconds, cropped576×324 at32,0 to retain the full raised lid, cake base and relevant gripper motion. Both stills and cover retain16:9 proportions with contain fitting, no stretching, artificial details or grading. Full source and output hashes are in media-provenance.json.

Hero headings are Remember. Recreate. with4pieces /6pieces /6pieces+cover. No completion count or result badge is added. A brief dissolve marks the change from the memory reference to later actual execution. Landing occurs before the picture contracts. The active Hard picture contracts to the bottom-right CP02 cell; the other two task rows appear at the existing handoff time.

## Verification

- HyperFrames runtime, layout and contrast checks passed at all requested hero, handoff, comparison, cover and statistics moments.
- Lint reports two reviewed warnings: existing Act reference-image reuse, and intentional reuse of CP02 reference images as hero and comparison views. Their wrappers occupy distinct animation phases; snapshots verify visibility.
- Root and independent visual reviews check complete cake bases, raised-lid headroom, undistorted proportions and the correct bottom-right handoff. See snapshots and exported-visual-review.json for final encoded evidence.
- Animation map flags are reviewed in animation-review.json. No new persistent offscreen content or text overlap.
- Unrelated composition files and index.html are SHA-verified unchanged. No audio source or timing edits.
- Master/web format checks and full decodes are performed before promotion. The audio-preservation audit compares actual AAC packets and timing with the previously checked092248 delivery; matching packets preserve earlier voice, Hard, loudness, transcription and speech-free interval evidence.
- Historical master and web file hashes are rechecked during promotion; old outputs remain on disk.

Final delivery remains75seconds,1920×1080,30fps,H.264/yuv420p with stereoAAC. No manual listening claim.
