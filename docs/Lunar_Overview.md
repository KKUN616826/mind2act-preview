# Lunar overview maintenance

The scene is an inline SVG with JavaScript-generated rankings and animation, not a bitmap.

Edit `data/lunar-preview.json` to change model names and the three scores (`mind`, `act`, `coupling`). Scores use a 0–100 scale. Run `python -X utf8 scripts/build.py` to regenerate the website. No graphic editing is required.

Each track sorts independently. Positions are calculated from the actual SVG paths using score height. The illustration currently contains fictional preview values; do not publish them as benchmark results. Update the visible preview label and mode when verified scores are available.

The ascent runs when the section enters view. Replay restarts it. Selecting a model highlights that model on all tracks. Reduced-motion settings disable motion.

`research_intro.html` owns the scene; `lunar.js` owns the ranking and animation; `research.css` owns its appearance.

The current density preview contains 11 representative model families (33 markers), not an exhaustive market inventory. Brand SVGs are embedded during build from `media/icons/`, so the page has no dependency on a remote icon service. Sources: https://github.com/simple-icons/simple-icons/tree/develop/icons ; OpenAI icon from tag 13.21.0. Codex uses its provider OpenAI emblem. Rankings and scores remain fictional.

Scale labels sit outside the marker field. Crowded markers keep their exact score height and move horizontally with a leader to the trajectory. Model names and numeric scores appear on hover, focus, or click.
