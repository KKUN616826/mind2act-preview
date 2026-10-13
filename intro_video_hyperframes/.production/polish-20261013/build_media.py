"""Polish revision 2026-10-13: derived media for the intro zoom, scale heroes and Hard task wall.

Run from anywhere:  python3 .production/polish-20261013/build_media.py [stage ...]
Stages: wall, heroes, intro, probe (default: all but probe). Originals are never modified.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/generated/polish-20261013"
WORK = Path(__file__).resolve().parent
FF = "/opt/homebrew/bin/ffmpeg"
V = ROOT / "assets/videos"
HD = ROOT / "assets/generated/montage-hd-20261011-170017"

# Hard source + start for every wall card. Starts reuse the audited 45-case
# mosaic selections (same moments, Hard level), except M where the main-camera
# view is shifted down so the cup row and plates stay clear of the top crop.
HARD = {
    "E": ("Mind/E/E__E_hard.mp4", 68.07),
    "F": ("Mind/F/F__F_hard.mp4", 13.25),
    "P": ("Mind/P/P__P_hard_general_012.mp4", 17.09),
    "S": ("Mind/S/S__S_hard.mp4", 28.96),
    "M": ("Mind/M/M__M_hard_frontlabel.mp4", 39.85),
    "FR1": ("Act/FR1/hard.mp4", 14.43),
    "FR2": ("Act/FR2/hard.mp4", 5.84),
    "PR1": ("Act/PR1/PR1__PR1_Hard_control_20260919.mp4", 4.2),
    "PR2": ("Act/PR2/PR2__PR2_Hard_control_20260919.mp4", 7.75),
    "PR3": ("Act/PR3/PR3__PR3_Hard_head_reference_20260919.mp4", 14.76),
    "CP01": ("Mind2Act/CP01/CP01__CP01_hard_adaptive_v2_20260920.mp4", 55.96),
    "CP02": ("Mind2Act/CP02/CP02__CP02_hard_v6_完整示范与运控_20260920.mp4", 63.56),
    "CP03": ("Mind2Act/CP03/CP03__CP03_Hard_7盘_三档20mms_原速.mp4", 75.21),
    "CP04": ("Mind2Act/CP04/hard.mp4", 64.91),
    "CP05": ("Mind2Act/CP05/CP05__CP05_Hard_揭罩与音量调节_12次复奏_20260923.mp4", 89.39),
}
# Vertical offset (source rows) of the 640x334 main-camera window per task.
# Old wall crops used y=0 everywhere; M's cups then sat on the crop's lower edge.
WALL_Y = {"M": 60}


def ff(*args):
    subprocess.run([FF, "-nostdin", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], check=True)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def enc(out):
    return ["-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", out]


def wall(records):
    for code, (rel, start) in HARD.items():
        src = V / rel
        out = OUT / f"wall-{code.lower()}-hard.mp4"
        y = WALL_Y.get(code, 0)
        ff("-ss", start, "-i", src, "-t", 8, "-vf", f"crop=640:334:0:{y},setsar=1", *enc(out))
        records.append({"use": "task wall", "task": code, "level": "Hard", "source": str(src.relative_to(ROOT)), "source_sha256": sha(src), "start": start, "end": start + 8, "speed": 1, "crop": f"640x334 at 0,{y}", "output": str(out.relative_to(ROOT))})


def heroes(records):
    # Mind / M Hard: two source segments joined across a static hold (the cups do
    # not move between them, so the join reads as continuous):
    #   2.0-3.7  six cups lower over the items
    #   6.2-7.5  one adjacent pair swaps positions
    # 3.0 s of source at 1.4x -> 2.143 s on screen. Full 1080p frame, no crop.
    m_src, m_segments, m_speed = HD / "M-Hard-1080p.mp4", [(2.0, 3.7), (6.2, 7.5)], 1.4
    m_out = OUT / "m-cover-swap-hero-1080p.mp4"
    parts = [f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[s{i}]" for i, (a, b) in enumerate(m_segments)]
    parts.append("".join(f"[s{i}]" for i in range(len(m_segments))) + f"concat=n={len(m_segments)}:v=1:a=0,setpts=PTS/{m_speed},fps=30[v]")
    ff("-i", m_src, "-filter_complex", ";".join(parts), "-map", "[v]", *enc(m_out))
    records.append({"use": "scale hero", "task": "M", "level": "Hard", "source": str(m_src.relative_to(ROOT)), "source_sha256": sha(m_src), "segments": m_segments, "speed": m_speed, "crop": None, "action_observed": "Six cups lower over the items, then one adjacent pair swaps positions. Static hold between segments omitted.", "output": str(m_out.relative_to(ROOT))})
    # Act / PR1 Hard: gripper engages the slider and drags it along the 0-40 scale.
    # 640x480 source; main camera is the top 640x360 (wrist strips below excluded).
    p_src, p_start, p_end, p_speed = V / "Act/PR1/PR1__PR1_Hard_control_20260919.mp4", 6.0, 9.8, 2.2
    p_out = OUT / "pr1-slide-hero-1080p.mp4"
    ff("-i", p_src, "-vf", f"trim=start={p_start}:end={p_end},setpts=(PTS-STARTPTS)/{p_speed},crop=640:360:0:0,scale=1920:1080:flags=lanczos,unsharp=5:5:0.5,setsar=1,fps=30", *enc(p_out))
    records.append({"use": "scale hero", "task": "PR1", "level": "Hard", "source": str(p_src.relative_to(ROOT)), "source_sha256": sha(p_src), "start": p_start, "end": p_end, "speed": p_speed, "crop": "640x360 at 0,0, Lanczos upscale to 1920x1080 (source is 640x480)", "action_observed": "Gripper holds the slider and drags it along the scale.", "output": str(p_out.relative_to(ROOT))})


def intro(records):
    # Continuous pull-back plate: a 3x3 grid (1920x1080, 640x360 cells) whose
    # centre cell is the opening piano shot. 1 -> 9 tiles is a camera move on
    # this plate in the composition; the 45-case mosaic then takes over at the
    # same tile scale so the camera keeps receding without a cut.
    piano = ROOT / "assets/generated/clarity-20261010-155258/cases/piano-play.mp4"
    cells = [
        ("Mind/P/P__P_hard_general_012.mp4", 17.09, 1.0),
        ("Act/PR3/PR3__PR3_Easy_head_reference_20260919.mp4", 15.39, 1.0),
        ("Mind/E/E__E_easy.mp4", 24.2, 1.0),
        ("Mind2Act/CP02/CP02__CP02_easy_v6_完整示范与运控_20260920.mp4", 35.33, 1.0),
        None,  # centre: piano
        ("Mind2Act/CP04/CP04__CP04_easy.mp4", 44.63, 1.0),
        ("Act/FR1/easy.mp4", 9.19, 1.0),
        ("Mind/S/S__S_easy.mp4", 25.92, 1.0),
        ("Act/PR2/PR2__PR2_Easy_control_20260919.mp4", 8.19, 1.0),
    ]
    dur = 2.4
    inputs, filters, used = [], [], []
    for i, cell in enumerate(cells):
        if cell is None:
            inputs += ["-t", dur, "-i", piano]
            filters.append(f"[{i}:v]scale=640:360:flags=lanczos,setsar=1,fps=30,trim=duration={dur},setpts=PTS-STARTPTS[c{i}]")
            used.append({"cell": i, "source": str(piano.relative_to(ROOT)), "start": 0})
        else:
            rel, st, _ = cell
            inputs += ["-ss", st, "-t", dur, "-i", V / rel]
            filters.append(f"[{i}:v]crop=640:360:0:0,setsar=1,fps=30,trim=duration={dur},setpts=PTS-STARTPTS[c{i}]")
            used.append({"cell": i, "source": rel, "start": st})
    layout = "|".join(f"{(i % 3) * 640}_{(i // 3) * 360}" for i in range(9))
    filters.append("".join(f"[c{i}]" for i in range(9)) + f"xstack=inputs=9:layout={layout}[v]")
    out = OUT / "intro-zoom-plate-3x3.mp4"
    ff(*inputs, "-filter_complex", ";".join(filters), "-map", "[v]", *enc(out))
    records.append({"use": "intro pull-back plate", "layout": "3x3, 640x360 cells; centre = piano-play", "cells": used, "duration": dur, "output": str(out.relative_to(ROOT))})


def probe():
    for f in sorted(OUT.glob("*.mp4")):
        r = subprocess.run(["/opt/homebrew/bin/ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height,nb_frames:format=duration", "-of", "csv=p=0", f], capture_output=True, text=True)
        print(f.name, r.stdout.replace("\n", " "))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    stages = sys.argv[1:] or ["wall", "heroes", "intro"]
    prov = WORK / "media-provenance.json"
    uses = {"wall": "task wall", "heroes": "scale hero", "intro": "intro pull-back plate"}
    rebuilt = {uses[s] for s in stages if s in uses}
    records = [r for r in (json.loads(prov.read_text()) if prov.exists() else []) if r["use"] not in rebuilt]
    for s in stages:
        if s == "probe":
            probe()
        else:
            globals()[s](records)
    prov.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
