"""
Automated Video Assembler for Claymation Episodes.
Includes audio narration sync, silence detection, 12->24fps cadence conversion,
and subtitle burn-in.
"""
from .audio_sync import detect_audio_pauses, align_scenes_to_narration
from .video_compiler import compile_claymation_episode

__all__ = [
    "detect_audio_pauses",
    "align_scenes_to_narration",
    "compile_claymation_episode",
]
