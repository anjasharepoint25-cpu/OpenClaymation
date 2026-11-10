"""
Audio Sync & Silence Detection for Stop-Motion Storytelling.
Detects narrative pauses to automatically segment episodes into cohesive visual acts.
"""

import re
import shutil
import subprocess
from pathlib import Path


def detect_audio_pauses(audio_path: str, noise_threshold_db: float = -35.0, min_duration: float = 0.35) -> list[float]:
    """
    Uses ffmpeg silencedetect filter to discover breath and paragraph pauses.
    Returns list of silence midpoint timestamps (in seconds).
    """
    if not shutil.which("ffmpeg"):
        # Fallback when ffmpeg is not locally installed
        return []

    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={noise_threshold_db}dB:d={min_duration}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)

    silence_starts = []
    silence_ends = []

    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([\d\.]+)", line)
            if m:
                silence_starts.append(float(m.group(1)))
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s*([\d\.]+)", line)
            if m:
                silence_ends.append(float(m.group(1)))

    # Midpoints of silences
    midpoints = []
    for s, e in zip(silence_starts, silence_ends):
        midpoints.append(round((s + e) / 2.0, 3))

    return midpoints


def align_scenes_to_narration(total_audio_duration: float, scene_count: int, pause_timestamps: list[float] = None) -> list[dict]:
    """
    Divides total duration into scene blocks aligned with natural audio pauses.
    Each block contains: { 'scene_idx': int, 'start': float, 'end': float, 'duration': float, 'target_frames_12fps': int }
    """
    boundaries = [0.0]
    if pause_timestamps and len(pause_timestamps) >= scene_count - 1:
        # Use detected pause midpoints
        boundaries.extend(pause_timestamps[:scene_count - 1])
    else:
        # Uniform fallback
        step = total_audio_duration / scene_count
        boundaries.extend([round(step * i, 2) for i in range(1, scene_count)])

    boundaries.append(total_audio_duration)

    scenes = []
    for i in range(len(boundaries) - 1):
        start = boundaries[i]
        end = boundaries[i + 1]
        dur = round(end - start, 2)
        frames_12 = int(round(dur * 12))
        scenes.append({
            "scene_idx": i + 1,
            "start": start,
            "end": end,
            "duration": dur,
            "target_frames_12fps": frames_12,
            "output_frames_24fps": frames_12 * 2
        })

    return scenes
