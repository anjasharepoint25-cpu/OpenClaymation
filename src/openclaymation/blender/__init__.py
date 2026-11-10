"""
Blender procedural clay and stop-motion animation pipeline.
"""
from .clay_shader import create_clay_material, apply_clay_to_object, CLAY_PALETTES
from .stop_motion_rig import setup_stop_motion_environment, bake_stepped_animation, add_camera_chatter
from .studio_stage import build_miniature_stage

__all__ = [
    "create_clay_material",
    "apply_clay_to_object",
    "CLAY_PALETTES",
    "setup_stop_motion_environment",
    "bake_stepped_animation",
    "add_camera_chatter",
    "build_miniature_stage",
]
