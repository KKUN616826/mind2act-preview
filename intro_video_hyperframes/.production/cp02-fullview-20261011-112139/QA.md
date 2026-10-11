# Restore CP02 source-camera width

The previous reference crop began at source x128 and the cover crop at x32. Both removed left-side source content. All CP02 reference images and cover footage now use the original main camera region x0–639, y0–333. Output1280×668 preserves its aspect. The separate lower wrist-camera panel is excluded. No horizontal source columns are discarded.

The original camera itself meets/truncates the Medium/Hard tray at its extreme left boundary. This edit restores all recorded content; it does not invent content outside the camera. Delivery wording must say full original main-camera width, not promise a complete tray beyond the source boundary.

Only CP02 asset paths changed in the composition. CSS, motion, scene timing, audio and all other compositions are verified unchanged. Existing contain fitting displays the complete derived image in both the large hero and comparison cells. The hero continues to contract into the bottom-right CP02 cell.

Source and output hashes, frame/clip ranges and crop geometry are in media-provenance.json. Root and independent source review inspected native and derived frames. Runtime/layout/contrast checks and actual encoded hero/grid/cover frame review are required before promotion. Lint's repeated-image warnings describe intentional hero/comparison reuse and the existing Act reference reuse.

Final master and compact MP4 are fully decoded and probed. Actual audio packets are compared with the110436 master, carrying forward its earlier verified cue/Hard/transcription/loudness/VAD evidence when byte-identical. Historical exports are retained and their hashes rechecked. No manual listening claim.

See check-final.json, independent-visual-review.json, exported-visual-review.json, audio-preservation.json and the rendered frame evidence.
