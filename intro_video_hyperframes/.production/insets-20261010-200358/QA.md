# Inset and title revision

The existing project and 62.222222-second timeline are retained. Original PNGs, the blue-cup meal footage, source piano/drawing clips and soundtrack are unchanged. All earlier exported films remain in place.

## Requested changes

- Removed the two selected captions above the feedback-loop diagram: `COORDINATION THROUGH THE COMPLETE TASK` and `TASK LOGIC ILLUSTRATION / NOT MODEL INTERNAL STATE`. Task-logic interpretation remains in source comments and production provenance.
- Restored the Act opening target focus plus the lower-left TARGET / EXECUTED TRACE comparison. The actual trace inset starts at local 1.15 seconds, exactly matching the main drawing clip. The short right card reads Follow the curve / Maintain contact / Read the trace and does not present these as completed stages.
- Restored the three original piano demonstration stills, labeled OBSERVED SEQUENCE · EXCERPT, with no invented sequence numbers or cursor. The right card uses Observe / Replay, with only the current excerpt type in gold. No lid opening or rhythm-matching claim was added.
- Used a centered CSS window on the original wordmark image to hide its colon. The visible source x-range is 140–974; the colon at x=980–989 is outside the window. Opening uses the existing 1.2× image size, closing uses 1×. Glyph proportions, original colors, source PNG and all other brand motion remain unchanged.

## Composition review

HyperFrames 0.8.143 full check passed. Zero runtime/layout/contrast errors; 23 of 23 contrast checks passed. The one lint warning is intentional reuse of the target reference image in the temporary center focus and lower-left comparison. Actual snapshots confirm both uses. Informational clipping findings correspond to the opening mosaic push-in and the two requested wordmark crop windows.

Narrative agent inspected four actual snapshots at 18.6, 21.0, 25.9 and 28.4 seconds. Brand agent inspected 3.5 and 59.5 seconds. Root inspected the restored case windows, centered wordmarks and 35-second diagram. No core pen/keyboard contact region is blocked; original three observed key stills remain legible.

Final export `201142.mp4` is 62.233333 seconds at 1920×1080 / 30 fps, H.264/yuv420p and AAC stereo 48 kHz. Master and website MP4 both decode fully without errors. Root inspected a 12-frame sequence from the actual exported cases and full-size frames at the changed title/loop points: restored trace footage advances with the main drawing, piano stills and right cards remain visible, the two selected loop captions are absent, and the opening wordmark has no colon.

The actual final AAC is bit-identical to the previously audited 180033 MP4 (ADTS SHA-256 `bce3f72902e2d25a93f12175b5b75752103c05c26e806c55f8d68b2176787163` for both). No audio regression was introduced, so the prior Hard/statistics/speech/loudness audit remains applicable. Full records are in `delivery-final.json`, `audio-continuity.json` and `rendered/`.

Independent visual agent also reviewed the actual exported film's 3.5/18.5–23/25–29.3/35/59.5-second frames and case sequence: both wordmarks are centered without colons, trace inset updates with the main action, all three piano excerpt stills appear as authored, side cards are readable and core actions remain visible. No substantive visual defect was found.
