from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[2]
old = 'assets/generated/source-refresh-20261010-142512'
new = 'assets/generated/clarity-20261010-155258'
before = Path(__file__).parent / 'before'
before.mkdir(exist_ok=True)
for path in (root / 'compositions').glob('*.html'):
    shutil.copy2(path, before / path.name)
    content = path.read_text()
    for media in (root / new).rglob('*.mp4'):
        relative = media.relative_to(root / new).as_posix()
        content = content.replace(f'{old}/{relative}', f'{new}/{relative}')
    path.write_text(content)
