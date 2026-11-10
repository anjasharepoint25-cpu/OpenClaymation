"""
Example Standalone Script: Generate a Complete Clay Character Scene in Blender.
Can be run via:
    blender -b -P examples/generate_demo_scene.py
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import bpy
from openclaymation.blender.studio_stage import build_miniature_stage
from openclaymation.blender.clay_shader import apply_clay_to_object
from openclaymation.blender.stop_motion_rig import setup_stop_motion_environment, add_camera_chatter, bake_stepped_animation

def run():
    print("🎬 Initializing OpenClaymation Standalone Generator...")

    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Build Stage
    build_miniature_stage()
    setup_stop_motion_environment(fps=24, step=2)

    # 1. Base Clay Character Body
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(0, 0, 0.75))
    body = bpy.context.active_object
    body.name = "Clay_Hero_Body"
    apply_clay_to_object(body, palette_name="terracotta", fingerprint_scale=24.0)

    # 2. Clay Bead Eyes
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(-0.16, -0.52, 0.95))
    eye_l = bpy.context.active_object
    eye_l.name = "Clay_Eye_Left"
    apply_clay_to_object(eye_l, palette_name="midnight_blue", fingerprint_scale=32.0)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(0.16, -0.52, 0.95))
    eye_r = bpy.context.active_object
    eye_r.name = "Clay_Eye_Right"
    apply_clay_to_object(eye_r, palette_name="midnight_blue", fingerprint_scale=32.0)

    # 3. Simple Stop-Motion Bounce Keyframe
    body.keyframe_insert(data_path="location", frame=1)
    body.location.z = 1.1
    body.keyframe_insert(data_path="location", frame=12)
    body.location.z = 0.75
    body.keyframe_insert(data_path="location", frame=24)

    # Bake stepped physics on twos (12 FPS)
    bake_stepped_animation(body, step_size=2)

    # Add camera chatter
    if bpy.context.scene.camera:
        add_camera_chatter(bpy.context.scene.camera)

    output_blend = "openclaymation_demo.blend"
    bpy.ops.wm.save_as_mainfile(filepath=output_blend)
    print(f"✅ Scene successfully generated and saved to: {output_blend}")

if __name__ == "__main__":
    run()
