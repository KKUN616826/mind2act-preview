from pathlib import Path
import json, hashlib, shutil, subprocess

run = Path(__file__).resolve().parent
root = run.parent.parent
file = root / 'compositions/03-mind.html'
shutil.copy2(file, run / '03-mind-before.html')
replacements = {
    f'assets/generated/clarity-20261010-155258/cases/{name}.mp4': f'assets/generated/cases/{name}.mp4'
    for name in ['p-intro', 'p-action1', 'p-action2']
}
replacements['assets/generated/source-refresh-20261010-142512/cases/p-order-green-crop.png'] = 'assets/generated/cases/p-order-blue-crop.png'
original = file.read_text()
updated = original
records = []
for previous, restored in replacements.items():
    assert updated.count(previous) == 1, previous
    assert (root / restored).is_file(), restored
    updated = updated.replace(previous, restored)
    records.append({'previous': previous, 'restored': restored, 'sha256': hashlib.sha256((root / restored).read_bytes()).hexdigest()})
first = root / '.production/source-refresh-20261010-142512/before/compositions/03-mind.html'
assert updated == first.read_text(), 'Restored scene differs from archived first version'
file.write_text(updated)
(run / 'manifest.json').write_text(json.dumps({'created_at': '2026-10-10T16:31:09+08:00', 'scope': 'Meal-packing spotlight only; first-version excerpts and matching order still; timing and animation unchanged', 'scene_matches_archived_first_version': True, 'assets': records}, indent=2) + '\n')
print('Restored 3 video references and matching order still; exact match to first-version scene.')
