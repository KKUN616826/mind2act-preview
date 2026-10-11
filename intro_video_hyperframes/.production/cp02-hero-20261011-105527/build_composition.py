from pathlib import Path
import re

base = Path(__file__).resolve().parent
source = (base/'before/compositions/09-difficulty.html').read_text()
assets = 'assets/generated/cp02-hero-20261011-105527/'
source = source.replace('MIND / F · THREE LEVELS', 'MIND2ACT / CP02 · THREE LEVELS')
source = source.replace('Learn the button rules.', 'Remember. Recreate.')
source = source.replace('.difficulty-film video{width:100%;height:100%;object-fit:contain}', '.difficulty-film{background:#101820}.difficulty-film img,.difficulty-film video{display:block;width:100%;height:100%;object-fit:contain}.difficulty-hero-cover{position:absolute;inset:0;background:#101820}')
source = source.replace('</style>', '#difficulty-grid-cp02 .difficulty-grid-cell img,#difficulty-grid-cp02 .difficulty-grid-cell video{object-fit:contain;object-position:center}\n</style>', 1)
for level, count in [('easy', 4), ('medium', 6), ('hard', 6)]:
    source = source.replace(f'assets/generated/difficulty-grid-20261011-090243/cp02-{level}.png', f'{assets}cp02-{level}.png')
    pattern = rf'<div id="difficulty-desc-{level}" class="difficulty-hero-desc">.*?</div></div>'
    caption = f'{count} pieces' + (' + cover' if level=='hard' else '')
    source, n = re.subn(pattern, f'<div id="difficulty-desc-{level}" class="difficulty-hero-desc">{caption}</div>', source, count=1)
    assert n == 1
    pattern = rf'<video id="difficulty-video-{level}".*?</video>'
    media = f'<img id="difficulty-hero-reference-{level}" src="{assets}cp02-{level}.png" alt="{level.capitalize()} initial reference cake to remember: {count} pieces">'
    if level == 'hard':
        media += f'<div id="difficulty-hero-cover" class="difficulty-hero-cover"><video id="difficulty-hero-cover-video" class="clip" src="{assets}cp02-hard-cover.mp4" data-start="4.95" data-duration="1.85" data-track-index="3" data-hf-media-start-basis="local" muted playsinline></video></div>'
    source, n = re.subn(pattern, media, source, count=1)
    assert n == 1
source = source.replace('assets/generated/difficulty-grid-20261011-090243/cp02-hard-cover.mp4', f'{assets}cp02-hard-cover.mp4')
source = source.replace('// Preserve the large-word sequence until this handoff, then keep a stable 3x3 comparison.', "// Clearly cut from the initial reference to the later real cover placement.\ntl.fromTo('#difficulty-hero-cover',{opacity:0},{opacity:1,duration:.12,ease:'power2.out'},4.95);\n// Preserve the large-word sequence; cake footage contracts into its CP02 row.")
source = source.replace("tl.to('#difficulty-film-'+lv,{opacity:1,x:x-690,y:280-275,scale:448/1160,duration:.4,ease:'power3.inOut'},6.34);", "const cakeScale=220/605.375;\n  const cakeX=x+(448-1160*cakeScale)/2;\n  tl.to('#difficulty-film-'+lv,{x:cakeX-690,y:752-275,scale:cakeScale,duration:.4,ease:'power3.inOut'},6.34);")
Path('compositions/09-difficulty.html').write_text(source)
