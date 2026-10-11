# Actual export review: breadth and difficulty

**Verdict: PASS; no blocking issue, no edit required.**

Reviewed master: `renders/mind2act-world-promo-1080p-20261010-221251.mp4`
SHA256: `8ea3b7ca838692a605603f4939c0f51e19f43a0688a327fd2d6f1810e45a855e`

## Actual exported pixels

Inspected the actual-export `rendered/breadth-motion.jpg`, `rendered/difficulty-motion.jpg` and their full-resolution key frames. These are decoded from the final MP4, not browser snapshots.

- Full-size FR1, CP02 and F clips visibly advance. Footer labels do not cover the conveyor pickup/drop area, cake assembly surface, or F button array.
- The F clip continuously shrinks into the correct Mind/F card. Grid card labels and category headers settle and remain readable; no blank card or wrong category detected.
- All 15 unique tasks appear, five in each category; P retains the selected blue-cup excerpts. No task-performance counters or invented outcomes appear.
- Difficulty heroes Easy, Medium and Hard are clearly separated, with about2.1s between entrance cues. The brief overlapped typography visible during replacement is a transition, not a persistent state.
- Easy has1D track and2buttons; Medium3x3 and4buttons; Hard4x4 and4buttons. Full grid and button controls remain visible.
- Three comparison rows settle without clipping and retain moving real footage. The actual MP4 shows arm/contact motion in all three rows.
- Formula and45configuration payoff are readable and held. The label accurately reads Task-difficulty configurations.

## Pixel evidence for moving footage

Decoded frames at49,50,51,52s and compared only inner video ROIs, excluding labels/borders. Every one of15tiles has strong visual changes across at least one interval; none is an accidental frozen thumbnail. Changes are consistent with visible robot/object movement in the contact sheet.

| Task | Largest mean RGB difference (0–255) | Largest fraction of pixels changing >8 |
|---|---:|---:|
| E | 10.78 | 12.7% |
| F | 32.80 | 32.0% |
| P | 27.34 | 39.9% |
| S | 28.52 | 28.4% |
| M | 10.66 | 11.4% |
| FR1 | 30.55 | 34.6% |
| FR2 | 20.89 | 21.1% |
| PR1 | 26.17 | 20.9% |
| PR2 | 26.16 | 33.7% |
| PR3 | 16.04 | 17.2% |
| CP01 | 21.29 | 19.0% |
| CP02 | 5.47 | 7.1% |
| CP03 | 12.41 | 23.4% |
| CP04 | 6.49 | 7.2% |
| CP05 | 16.67 | 17.8% |

Comparison rows at60.7→61.3→62.2s:

| Difficulty | Mean differences |
|---|---|
| Easy | 20.7012, 18.9653 |
| Medium | 26.1646, 24.0427 |
| Hard | 25.2111, 12.2103 |

All six row comparisons are non-identical, with mean differences12.21–26.16/255. This corroborates the visually observed advancing footage. Pixel metrics alone are not used to infer task success.

Detailed ROIs and interval values: `export-review-breadth-metrics.json`. No source/composition modification made during export review.
