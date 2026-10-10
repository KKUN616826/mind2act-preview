# Breadth and difficulty revision

Owned: `compositions/06-scale.html` (`scale`) and `compositions/09-difficulty.html` (`difficulty`). Both author 12.471852 s including 0.62 s transition tail; root slots remain 11.851852 s. No unrelated scenes, root timing or audio edited by this worker.

## Content and scope

- Full-size real clips FR1 -> CP02 -> F, then the same F video element scales into its task-card position.
- Fifteen unique tasks visibly sorted into Mind (E,F,P,S,M), Act (FR1,FR2,PR1,PR2,PR3), Mind2Act (CP01..CP05). Five tasks per group.
- P alone uses concatenated selected historical blue-cup excerpts; current raw P file is not substituted. Original excerpt edits/speeds preserved.
- Remaining wall video sources use medium demonstrations, 1x playback, crop only to source main camera (640x334, entire width); auxiliary wrist strips omitted.
- Full-size montage framing reserves footer space so buttons/objects are not obscured.
- F difficulty footage: the same initial exploration phase, each sourced from 0.5–10.5 s, 1x speed, same crop. Full grid, all buttons and contact region retained. No success, policy-state, correction, reaction-speed or performance claims added.
- F labels verified against `third_party/physco-bench/upstream/docs/cases/F.md` and source-metadata training-demo manifest: Easy=1D track/2 unmarked buttons; Medium=3x3 grid/4 buttons; Hard=4x4 grid/4 buttons. Larger grid is shown directly. No invented step counts from rendered excerpts.
- Removed old P 4/5/7 and CP05 7/14/21 comparison table.
- Large Easy, Medium, Hard kinetic words retained; three corresponding real videos then settle into three horizontal comparison rows.
- Numeric conclusion: 15 Tasks x 3 Levels, 45 Task-difficulty configurations. Does not conflate 45 with task count.

## Timing (local)

- Scale: FR1 0–1.45, CP02 1.45–3.0, F 3.0–5.12; F-to-grid transformation5.12–6.15. All taxonomy cards settled6.66. F selectionoutline10.77.
- Difficulty word entrances0.12/2.22/4.32, VO cue recommendations0.35/2.45/4.55. Comparison transition6.34–7.14, clearholdto9.43. Statistics reveal9.43–10.66 andholdthroughend.

## Checks

- HyperFrames0.8.143 via project wrapper, lint0errors. Existing intentional duplicatePR3targetimage warning remains outside worker scope.
- Twelve scene snapshots inspected at42.5,44,45.7,47.3,48.6,51.7,54.3,56.5,58.8,60.9,62.2,64.4global. Same F clip identity and correct finalcard verified. Threehero stages, threecomparison rows and45final verified readable.
- Additional4snapshot run verifies correctedfullmaincamera framing at42.5/44/45.7 andgrid48.6.
- Focused `keyframes --selector '#scale-f-hero'` proof created `f-grid-motion.png`.
- Actual full-film export review is performed by the parent after full project integration.

Provenance: `breadth-difficulty-provenance.json`. Builder scripts retained beside this note.

Final copy refinement: label uses `2/4 button rules to learn` (the mapping, rather than the button object, is unknown). Kicker `MIND / F · THREE LEVELS` clearly binds this example to the Mind category. Verified final56.5/60.9snapshots: both hero and comparison captions fit fully without clipping.
