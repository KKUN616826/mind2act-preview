from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NEW_CASES = "assets/generated/source-refresh-20261010-142512/cases/"
NEW_MONTAGE = "assets/generated/source-refresh-20261010-142512/montage/"


def update_file(name: str, replacements: dict[str, str]) -> dict:
    path = ROOT / "compositions" / name
    original = path.read_text(encoding="utf-8")
    content = original
    counts = {}
    for old, new in replacements.items():
        count = content.count(old)
        if count == 0:
            if new in content:
                counts[old] = "already updated"
                continue
            raise ValueError(f"{name}: cannot find old or new value for {old!r}")
        content = content.replace(old, new)
        counts[old] = count
    path.write_text(content, encoding="utf-8")
    return {"composition": str(path.relative_to(ROOT)), "replacements": counts}


def main() -> None:
    changes = [
        update_file(
            "01-intro.html",
            {
                "assets/generated/cases/piano-play.mp4": NEW_CASES + "piano-play.mp4",
                "assets/generated/montage/six-cases-mosaic.mp4": NEW_MONTAGE + "six-cases-mosaic.mp4",
                "assets/generated/montage/all-cases-mosaic.mp4": NEW_MONTAGE + "all-cases-mosaic.mp4",
            },
        ),
        update_file(
            "03-mind.html",
            {
                "assets/generated/cases/p-intro.mp4": NEW_CASES + "p-intro.mp4",
                "assets/generated/cases/p-action1.mp4": NEW_CASES + "p-action1.mp4",
                "assets/generated/cases/p-action2.mp4": NEW_CASES + "p-action2.mp4",
                "assets/generated/cases/p-order-blue-crop.png": NEW_CASES + "p-order-green-crop.png",
                NEW_CASES + "p-order-current-crop.png": NEW_CASES + "p-order-green-crop.png",
            },
        ),
        update_file(
            "04-act.html",
            {
                "assets/generated/cases/act-wide.mp4": NEW_CASES + "act-wide.mp4",
                "assets/generated/cases/act-draw.mp4": NEW_CASES + "act-draw.mp4",
                "assets/generated/cases/act-detail.mp4": NEW_CASES + "act-detail.mp4",
                "assets/generated/cases/pr3-target-crop.png": NEW_CASES + "pr3-target-crop.png",
            },
        ),
        update_file(
            "05-mind2act.html",
            {
                'id="piano-reveal"': 'id="piano-setup"',
                "assets/generated/cases/piano-cover.mp4": NEW_CASES + "piano-setup.mp4",
                "assets/generated/cases/piano-demo.mp4": NEW_CASES + "piano-demo.mp4",
                "assets/generated/cases/piano-play.mp4": NEW_CASES + "piano-play.mp4",
                "assets/generated/cases/piano-memory-1.png": NEW_CASES + "piano-memory-1.png",
                "assets/generated/cases/piano-memory-2.png": NEW_CASES + "piano-memory-2.png",
                "assets/generated/cases/piano-memory-3.png": NEW_CASES + "piano-memory-3.png",
                "> Reveal</div>": "> Prepare</div>",
            },
        ),
        update_file(
            "06-scale.html",
            {
                "assets/generated/montage/fast-montage.mp4": NEW_MONTAGE + "fast-montage.mp4",
                "assets/generated/montage/all-cases-mosaic.mp4": NEW_MONTAGE + "all-cases-mosaic.mp4",
            },
        ),
    ]
    report = {
        "scope": "Updated generated video and still-image references to the refreshed case source render set.",
        "compositions": changes,
    }
    output = ROOT / ".production/source-refresh-20261010-142512/composition-refresh.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
