# Lunar overview maintenance

The scene is an inline SVG with JavaScript-generated rankings and animation, not a bitmap.

Edit `data/lunar-preview.json` to change model names and the three scores (`mind`, `act`, `coupling`). Scores use a 0–100 scale. Run `python -X utf8 scripts/build.py` to regenerate the website. No graphic editing is required.

Each track sorts independently. Positions are calculated from each capability score: the central column uses score height; the side clusters use distance and angle relative to their star-group target. The illustration currently contains fictional preview values; do not publish them as benchmark results. Update the visible preview label and mode when verified scores are available.

The ascent runs on page initialization. Continuous floating motion runs independently of score coordinates. Replay restarts it. Selecting a model highlights that model on all tracks. Reduced-motion settings disable motion.

`research_intro.html` owns the scene; `lunar.js` owns the ranking and animation; `research.css` owns its appearance.

The current density preview contains 11 representative model families (33 markers), not an exhaustive market inventory. Brand SVGs are embedded during build from `media/icons/`, so the page has no dependency on a remote icon service. Sources: https://github.com/simple-icons/simple-icons/tree/develop/icons ; OpenAI icon from tag 13.21.0. Codex uses its provider OpenAI emblem. Rankings and scores remain fictional.

Scale labels sit outside the marker field. Crowded markers keep their exact score height and move horizontally with a leader to the trajectory. Model names and numeric scores appear on hover, focus, or click.


## Score display
Permanent ticks removed. Hover, focus or click a marker to show its score and arithmetic mean of the three illustrative scores. Preview values remain fictional. The moon and Earth use the original vector artwork.


## Accepted star-cluster composition (2026-10-03)
The academic page reads `data/lunar-preview.json` at build time. `mind`, `act`, and `coupling` each control their own model placement. The scores remain illustrative, not measured benchmark results. Continuous inner-group motion is independent of score coordinates and never changes rank. The Moon and warm/cool atmospheric fields animate continuously. Reduced-motion preferences disable ambient animation.
Runtime integration: `window.Mind2ActLunar.getScores()` reads current records; `updateScores(records)` validates numeric scores from 0 to 100 and rebuilds the visualization. Existing model IDs inherit their icons; new IDs require `icon_svg`. File edits require rebuilding with `python scripts/build.py`. The static site does not poll a server by itself.
