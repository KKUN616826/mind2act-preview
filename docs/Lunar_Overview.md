# Lunar overview maintenance

The scene is an inline SVG with JavaScript-generated rankings and animation, not a bitmap.

Edit `data/lunar-preview.json` to change model names and the three scores (`mind`, `act`, `coupling`). Scores use a 0–100 scale. Run `python -X utf8 scripts/build.py` to regenerate the website. No graphic editing is required.

Each track sorts independently. Positions are calculated from the actual SVG paths using score height. The illustration currently contains fictional preview values; do not publish them as benchmark results. Update the visible preview label and mode when verified scores are available.

The ascent runs when the section enters view. Replay restarts it. Selecting a model highlights that model on all tracks. Reduced-motion settings disable motion.

`research_intro.html` owns the scene; `lunar.js` owns the ranking and animation; `research.css` owns its appearance.
