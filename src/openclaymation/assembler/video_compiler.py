"""
Video Compiler for Stop-Motion Claymation Episodes.
Compiles sequential PNG frames into 24 FPS MP4 with 12 FPS hold cadence,
audio narration sync, and subtitle burn-in.
"""

import os
import shutil
import subprocess
from pathlib import Path


def compile_claymation_episode(
    frames_dir: str,
    output_mp4: str,
    audio_path: str = None,
    srt_path: str = None,
    fps_display: int = 24,
    fps_source: int = 12,
    resolution: str = "1080:1920"
) -> bool:
    """
    Renders frame sequence into an MP4 file.
    Duplicating 12 FPS frames into 24 FPS produces authentic stop-motion cadence
    while complying with social media container standards.
    """
    if not shutil.which("ffmpeg"):
        raise EnvironmentError(
            "ffmpeg is required for episode compilation. "
            "Please install ffmpeg (e.g. `brew install ffmpeg` on macOS)."
        )

    frames_path = Path(frames_dir)
    pattern = str(frames_path / "frame_%04d.png")

    # Base ffmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps_source),
        "-i", pattern,
    ]

    if audio_path and os.path.exists(audio_path):
        cmd.extend(["-i", str(audio_path)])

    # Video filters
    vf_filters = [
        f"scale={resolution}:flags=lanczos",
        f"fps={fps_display}",
        "format=yuv420p"
    ]

    if srt_path and os.path.exists(srt_path):
        vf_filters.append(f"subtitles='{srt_path}':force_style='FontName=Liberation Sans,FontSize=18,Outline=2'")

    cmd.extend([
        "-vf", ",".join(vf_filters),
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "veryfast"
    ])

    if audio_path and os.path.exists(audio_path):
        cmd.extend(["-c:a", "aac", "-b:a", "192k", "-shortest"])

    cmd.append(str(output_mp4))

    subprocess.run(cmd, check=True)
    return True
