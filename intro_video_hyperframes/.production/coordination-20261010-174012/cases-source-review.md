# Cases and CP05 visual evidence audit

Author: review_narrative subagent. Read-only examination of source media; composition changes restricted to 03-mind, 04-act and 05-mind2act.

## Preserved sources

- P keeps `assets/generated/cases/p-intro.mp4`, `p-action1.mp4`, `p-action2.mp4` and `p-order-blue-crop.png`. This is the user-selected original blue-cup take, not the later green-cup refresh.
- PR3 keeps the current `assets/generated/clarity-20261010-155258/cases/act-wide.mp4` and `act-draw.mp4` picture/timing. The evidence is visible target curve and actual ink; no accuracy score or online correction is inferred.
- CP05 keeps current `piano-setup.mp4`, `piano-demo.mp4`, `piano-play.mp4` in that clarity directory. Two display states describe observed demonstration versus replay, not measured internal model states. The word Excerpt stays visible. No cover removal, rhythm matching, complete-sequence result, or invented recovery is asserted.

## CP05 green-key event audit

Original source: `assets/videos/Mind2Act/CP05/CP05__CP05_Medium_双臂揭罩_8次复奏_20260923.mp4`, 640×480, 30 fps, 72.666667 s. Source identity is recorded in `.production/clarity-20261010-155258/provenance.json` (SHA-256 `79edf926914d8cff010b2d5ce7d813442dfbe8f4a5c4a2e3e0415ca269780971`). Its historical filename does not prove a cover-removal event in the chosen excerpt.

Direct frame inspection found these first visible green-response frames (one-frame precision, not latent task-state evidence):

| Source first green | Prior unlit frame | Visible location | Local time in a source-44s 1× excerpt |
| --- | --- | --- | --- |
| 48.366667 s | 48.333333 s | Left half of the keyboard; left stick | 4.366667 s |
| 50.933333 s | 50.900000 s | Right half of the keyboard; right stick | 6.933333 s |
| 53.533333 s | 53.500000 s | Right half, nearer the center; right stick | 9.533333 s |

Evidence images in this directory: `piano-source-left-onset.png` starts at source 48.2 s, `piano-source-right-onset.png` at 50.8 s, and `piano-source-third-onset.png` at 53.3 s. Each is six columns by three rows at the original 30 fps; frame labels show offset from the stated source start. The wider `piano-source-feedback.png` begins at source 47.6 s and samples every 0.2 s. The first derivative overview `piano-play-quarter-second.png` is only a coarse cross-check; do not use its fps-resampled labels for source onset precision.

The existing retimed `piano-play.mp4` provenance uses source start 44 s and playback rate 2.82. The first two source onsets correspond approximately to derivative times 1.5485 s and 2.4586 s, before output-frame rounding. Do not attach note names, full-sequence indices or success scores: they are not established by these visible frames.

## Closed-loop illustration boundary

The proposed three task mappings are task semantics: delivered items change remaining demand; actual ink changes the remaining path; a valid key response allows sequence progression. Editorial arrows can explain those dependencies after a real observed result. They do not establish the demonstrator's internal state, a specific feedback controller, recovery, or model evaluation performance. A return pulse must start after its corresponding green-response frame. Forward motion for the second event should finish before local 6.933333 s.
