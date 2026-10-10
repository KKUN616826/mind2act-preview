from __future__ import annotations

import concurrent.futures
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[2]
REFRESH_DIR = ROOT / ".production/source-refresh-20261010-142512"
OUT = ROOT / "assets/generated/source-refresh-20261010-142512/montage"
FFMPEG = "/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def task_family(video: dict) -> str:
    return Path(video["path"]).parts[3]


def run_ffmpeg(args: list[str]) -> None:
    result = subprocess.run(
        [FFMPEG, "-nostdin", "-hide_banner", "-loglevel", "error", "-y", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr[-4000:])


def retimed_start(old_cell: dict, video: dict, source_span: float) -> tuple[float, dict]:
    old_duration = float(video["old"]["duration"])
    new_duration = float(video["duration"])
    old_start = float(old_cell["source_start"])
    proportional = old_start / old_duration * new_duration if old_duration else 0.0
    max_start = max(0.0, new_duration - source_span)
    start = min(proportional, max_start)
    return start, {
        "old_source_start": old_start,
        "old_source_duration": old_duration,
        "new_source_duration": new_duration,
        "proportional_source_start": proportional,
        "source_start": start,
        "source_end": start + source_span,
        "clamped": start != proportional,
    }


def encode(
    video: dict,
    old_cell: dict,
    output: Path,
    width: int,
    height: int,
    duration: float,
    speed: float = 1.0,
    grid: bool = False,
) -> dict:
    source_span = duration * speed
    start, selection = retimed_start(old_cell, video, source_span)
    filters = []

    # The refreshed CP02/CP03 files no longer include the HUD strip removed by
    # the previous generator, so keep their complete 640x480 frame.
    if width / height > 1.6:
        filters.append("crop=iw:iw*9/16:0:ih*0.05")
    filters.append(f"setpts=(PTS-STARTPTS)/{speed}" if speed != 1 else "setpts=PTS-STARTPTS")
    target_width, target_height = (width - 2, height - 2) if grid else (width, height)
    filters.extend(
        [
            f"scale={target_width}:{target_height}:force_original_aspect_ratio=increase:flags=lanczos",
            f"crop={target_width}:{target_height}",
            "setsar=1",
            "fps=30",
        ]
    )
    if grid:
        filters.append(f"pad={width}:{height}:0:0:color=0x060911")

    source = ROOT / video["path"]
    run_ffmpeg(
        [
            "-threads", "1", "-ss", f"{start:.6f}", "-i", str(source),
            "-vf", ",".join(filters), "-t", f"{duration:.6f}", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-g", "30", "-keyint_min", "30",
            "-pix_fmt", "yuv420p", "-threads", "1", "-movflags", "+faststart",
            str(output),
        ]
    )
    return {
        "source": video["path"],
        "source_sha256": video["sha256"],
        **selection,
        "speed": speed,
        "duration": duration,
        "path": str(output.relative_to(ROOT)),
        "width": width,
        "height": height,
        "fps": 30,
        "crop": "16:9, full source width, y = source height * 0.05" if width / height > 1.6 else "none",
    }


def make_stack(records: list[dict], output: Path, width: int, height: int, cols: int, duration: float) -> None:
    inputs = []
    for record in records:
        inputs.extend(["-threads", "1", "-i", str(ROOT / record["path"])])
    count = len(records)
    layout = "|".join(f"{(i % cols) * width}_{(i // cols) * height}" for i in range(count))
    graph = "".join(f"[{i}:v]" for i in range(count)) + f"xstack=inputs={count}:layout={layout}:fill=0x060911[v]"
    run_ffmpeg(
        [
            *inputs, "-filter_complex_threads", "1", "-filter_complex", graph,
            "-map", "[v]", "-t", f"{duration:.6f}", "-an", "-c:v", "libx264",
            "-preset", "veryfast", "-crf", "18", "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p",
            "-threads", "4", "-movflags", "+faststart", str(output),
        ]
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    old = read_json(ROOT / ".production/montage-provenance.json")
    audit = read_json(ROOT / ".production/source-refresh-audit.json")
    videos = audit["videos"]
    old_cells = old["mosaic_all"]["cells"]
    if len(videos) != 45 or len(old_cells) != 45:
        raise ValueError("Expected the audited 45-source set and 45 prior mosaic cells")
    if [video["path"] for video in videos] != [cell["source"] for cell in old_cells]:
        raise ValueError("Refreshed source order differs from prior montage provenance")

    for video in videos:
        actual = hashlib.sha256((ROOT / video["path"]).read_bytes()).hexdigest()
        if actual != video["sha256"]:
            raise ValueError(f"Source hash changed after audit: {video['path']}")

    def make_cell(item):
        index, video = item
        path = OUT / f"cell-{index:02d}-{task_family(video).lower()}.mp4"
        return encode(video, old_cells[index], path, 240, 180, 5.5, grid=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        cells = list(pool.map(make_cell, enumerate(videos)))

    slot_order = old["mosaic_all"]["slot_source_indices"]
    all_slots = [cells[index] for index in slot_order]
    make_stack(all_slots, OUT / "all-cases-mosaic.mp4", 240, 180, 8, 5.5)

    def find_video(path: str) -> dict:
        return next(video for video in videos if video["path"] == path)

    six = []
    for index, old_cell in enumerate(old["mosaic_six"]["cells"]):
        video = find_video(old_cell["source"])
        six.append(
            encode(video, old_cell, OUT / f"six-{task_family(video).lower()}-{index:02d}.mp4", 640, 540, 1.5, grid=True)
        )
    make_stack(six, OUT / "six-cases-mosaic.mp4", 640, 540, 3, 1.5)

    quick_order = old["fast_reel"]["task_order"]
    quick_records = []
    for index, old_cell in enumerate(old["fast_reel"]["cuts"]):
        video = find_video(old_cell["source"])
        quick_records.append(
            encode(video, old_cell, OUT / f"quick-{quick_order[index].lower()}.mp4", 1280, 720, 1.1, speed=2)
        )
    frame_counts = old["fast_reel"]["frames_per_cut"]
    inputs = []
    for record in quick_records:
        inputs.extend(["-threads", "1", "-i", str(ROOT / record["path"])])
    filter_graph = ";".join(
        f"[{index}:v]trim=end_frame={frames},setpts=PTS-STARTPTS[q{index}]"
        for index, frames in enumerate(frame_counts)
    ) + ";" + "".join(f"[q{index}]" for index in range(len(quick_records))) + f"concat=n={len(quick_records)}:v=1:a=0[v];[v]settb=expr=1/30,setpts=N[final]"
    run_ffmpeg(
        [
            *inputs, "-filter_complex_threads", "1", "-filter_complex", filter_graph,
            "-map", "[final]", "-an", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "17", "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p", "-threads", "4",
            "-movflags", "+faststart", str(OUT / "fast-montage.mp4"),
        ]
    )
    # FFmpeg 7's concat output can carry a one-frame-short track duration
    # despite all 134 frame timestamps being correct. A lossless remux writes
    # the final sample's duration without altering any encoded frames.
    fixed_fast = OUT / "fast-montage-remux.mp4"
    run_ffmpeg([
        "-i", str(OUT / "fast-montage.mp4"), "-c", "copy", "-t", f"{sum(frame_counts) / 30:.6f}",
        "-movflags", "+faststart", str(fixed_fast),
    ])
    fixed_fast.replace(OUT / "fast-montage.mp4")

    provenance = {
        "generated_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
        "raw_sources_modified": False,
        "source_audit": ".production/source-refresh-audit.json",
        "source_count": len(videos),
        "fps": 30,
        "retiming": "old source_start / old source duration * refreshed source duration, clamped to preserve the full requested source span",
        "cp02_cp03_crop": "none; refreshed 640x480 frames inspected and contain no HUD strip",
        "sources": [
            {"path": video["path"], "sha256": video["sha256"], "duration": video["duration"]}
            for video in videos
        ],
        "mosaic_all": {
            "path": str((OUT / "all-cases-mosaic.mp4").relative_to(ROOT)),
            "duration": 5.5,
            "resolution": [1920, 1080],
            "layout": [8, 6],
            "source_count": 45,
            "slots": len(slot_order),
            "slot_source_indices": slot_order,
            "cells": cells,
        },
        "mosaic_six": {
            "path": str((OUT / "six-cases-mosaic.mp4").relative_to(ROOT)),
            "duration": 1.5,
            "resolution": [1920, 1080],
            "cells": six,
        },
        "fast_reel": {
            "path": str((OUT / "fast-montage.mp4").relative_to(ROOT)),
            "duration": sum(frame_counts) / 30,
            "resolution": [1280, 720],
            "task_order": quick_order,
            "frames_per_cut": frame_counts,
            "cuts": quick_records,
        },
    }
    (REFRESH_DIR / "montage-provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
