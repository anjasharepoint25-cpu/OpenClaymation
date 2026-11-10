"""
Blender procedural clay and stop-motion animation pipeline.
"""
from .clay_shader import create_clay_material, apply_clay_to_object, CLAY_PALETTES
from .stop_motion_rig import setup_stop_motion_environment, bake_stepped_animation, add_camera_chatter, setup_clay_boil
from .studio_stage import build_miniature_stage
from .character_rig import create_clay_character

__all__ = [
    "create_clay_material",
    "apply_clay_to_object",
    "CLAY_PALETTES",
    "setup_stop_motion_environment",
    "bake_stepped_animation",
    "add_camera_chatter",
    "setup_clay_boil",
    "build_miniature_stage",
    "create_clay_character",
]
