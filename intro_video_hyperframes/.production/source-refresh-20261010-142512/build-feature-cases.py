from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[2]
REFRESH_DIR = ROOT / ".production/source-refresh-20261010-142512"
OUT = ROOT / "assets/generated/source-refresh-20261010-142512/cases"
FFMPEG = "/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_ffmpeg(args: list[str]) -> None:
    result = subprocess.run(
        [FFMPEG, "-nostdin", "-hide_banner", "-loglevel", "error", "-y", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr[-4000:])


def source_record(audit: dict, fragment: str) -> dict:
    matches = [video for video in audit["videos"] if fragment in video["path"]]
    if len(matches) != 1:
        raise ValueError(f"Expected one source matching {fragment!r}; got {len(matches)}")
    record = matches[0]
    digest = hashlib.sha256((ROOT / record["path"]).read_bytes()).hexdigest()
    if digest != record["sha256"]:
        raise ValueError(f"Source hash changed after audit: {record['path']}")
    return record


def render_clip(
    name: str,
    source: dict,
    start: float,
    duration: float,
    speed: float,
    crop: str,
    size: tuple[int, int] = (1920, 1080),
) -> dict:
    output = OUT / f"{name}.mp4"
    filters = [f"setpts=(PTS-STARTPTS)/{speed}", crop, "fps=30"]
    run_ffmpeg(
        [
            "-threads", "1", "-ss", f"{start:.6f}", "-i", str(ROOT / source["path"]),
            "-vf", ",".join(filters), "-an", "-t", f"{duration:.6f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-g", "30", "-keyint_min", "30",
            "-pix_fmt", "yuv420p", "-threads", "1", "-movflags", "+faststart",
            str(output),
        ]
    )
    return {
        "name": name,
        "path": str(output.relative_to(ROOT)),
        "source": source["path"],
        "source_sha256": source["sha256"],
        "source_start": start,
        "source_end": start + duration * speed,
        "output_duration": duration,
        "playback_rate": speed,
        "crop_filter": crop,
        "resolution": list(size),
        "fps": 30,
    }


def render_still(name: str, source: dict, time: float, crop: str, size: tuple[int, int]) -> dict:
    output = OUT / f"{name}.png"
    filters = f"{crop},scale={size[0]}:{size[1]}:flags=lanczos,setsar=1"
    run_ffmpeg(
        [
            "-threads", "1", "-ss", f"{time:.6f}", "-i", str(ROOT / source["path"]),
            "-vf", filters, "-frames:v", "1", "-update", "1", str(output),
        ]
    )
    return {
        "path": str(output.relative_to(ROOT)),
        "source": source["path"],
        "source_sha256": source["sha256"],
        "source_time": time,
        "crop_filter": crop,
        "resolution": list(size),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    audit = read_json(ROOT / ".production/source-refresh-audit.json")
    p = source_record(audit, "Mind/P/P__P_hard_general_012.mp4")
    pr3 = source_record(audit, "Act/PR3/PR3__PR3_Hard_head_reference_20260919.mp4")
    cp05 = source_record(audit, "Mind2Act/CP05/CP05__CP05_Medium_")

    clips = [
        render_clip("p-intro", p, 2.5, 1.85, 1.0, "crop=640:360:0:0,scale=1920:1080:flags=lanczos"),
        render_clip("p-action1", p, 5.3, 2.61, 2.25, "crop=640:360:0:0,scale=1920:1080:flags=lanczos"),
        render_clip("p-action2", p, 39.5, 2.325926, 2.1, "crop=640:360:0:0,scale=1920:1080:flags=lanczos"),
        render_clip("act-wide", pr3, 0.2, 1.3, 1.0, "crop=640:360:0:20,scale=1920:1080:flags=lanczos"),
        render_clip("act-draw", pr3, 17.0, 5.395926, 1.0, "crop=640:360:0:20,scale=1920:1080:flags=lanczos"),
        render_clip(
            "act-detail", pr3, 17.0, 5.395926, 1.0,
            "crop=240:135:205:70,scale=548:308:flags=lanczos", (548, 308)
        ),
        render_clip("piano-setup", cp05, 24.0, 1.48, 4.05, "crop=640:360:0:0,scale=1920:1080:flags=lanczos"),
        render_clip("piano-demo", cp05, 30.0, 1.48, 2.7, "crop=640:360:0:0,scale=1920:1080:flags=lanczos"),
        render_clip("piano-play", cp05, 44.0, 3.582963, 2.82, "crop=640:360:0:0,scale=1920:1080:flags=lanczos"),
    ]
    stills = {
        "p-order-green-crop": render_still("p-order-green-crop", p, 3.0, "crop=190:108:225:0", (668, 373)),
        "pr3-target-crop": render_still("pr3-target-crop", pr3, 0.2, "crop=240:135:205:70", (548, 308)),
    }
    for index, time in enumerate((25.25, 27.5, 29.5), start=1):
        stills[f"piano-memory-{index}"] = render_still(
            f"piano-memory-{index}", cp05, time, "crop=395:115:120:100", (1060, 308)
        )

    provenance = {
        "generated_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
        "raw_sources_modified": False,
        "source_audit": ".production/source-refresh-audit.json",
        "source_count_verified": len(audit["videos"]),
        "clips": clips,
        "stills": stills,
        "notes": [
            "All featured crops use the refreshed 640x480 sources.",
            "CP05 Medium contains no cover reveal; piano-setup is an uncovered keyboard establishing beat.",
            "The P order card is captured at the matching green-cup order screen; the first and second action clips follow its two listed items.",
            "Piano memory cards use three real blue-key observation frames before replay, without synthetic marks.",
        ],
    }
    (REFRESH_DIR / "case-media-provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
