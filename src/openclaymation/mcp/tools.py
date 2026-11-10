"""
OpenClaymation MCP Tool Implementations.
Exposes modular building blocks for Claude and other LLM agents.
"""

import json
from pathlib import Path
from ..blender.bridge import run_inline_blender_code


def mcp_stage_clay_scene(theme: str = "warm_studio", backdrop_color: str = "terracotta") -> dict:
    """
    Spawns miniature studio, cyclorama backdrop, warm 3-point lighting, and camera.
    """
    code = f"""
import bpy
from openclaymation.blender.studio_stage import build_miniature_stage
from openclaymation.blender.stop_motion_rig import setup_stop_motion_environment
from openclaymation.blender.clay_shader import CLAY_PALETTES

# Clear default hierarchy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

palette = CLAY_PALETTES.get("{backdrop_color}", CLAY_PALETTES["terracotta"])
stage_info = build_miniature_stage(backdrop_color=palette)
setup_stop_motion_environment(fps=24, step=2)

print("SUCCESS_STAGE")
"""
    output = run_inline_blender_code(code)
    return {"status": "ok", "message": f"Spawned clay miniature stage with theme '{theme}'", "details": output}


def mcp_apply_clay_material(object_name: str, palette: str = "terracotta", fingerprint_scale: float = 28.0) -> dict:
    """
    Applies procedural plasticine shader to specified Blender object.
    """
    code = f"""
import bpy
from openclaymation.blender.clay_shader import apply_clay_to_object

obj = bpy.data.objects.get("{object_name}")
if not obj:
    raise ValueError("Object '{object_name}' not found in current Blender scene.")

apply_clay_to_object(obj, palette_name="{palette}", fingerprint_scale={fingerprint_scale})
print("SUCCESS_MATERIAL")
"""
    output = run_inline_blender_code(code)
    return {"status": "ok", "message": f"Applied '{palette}' clay shader to '{object_name}'", "output": output}


def mcp_bake_stopmotion_physics(step_size: int = 2, camera_jitter: bool = True) -> dict:
    """
    Converts animation into 12 FPS stepped cadence (animating on twos)
    and introduces organic camera bumps.
    """
    code = f"""
import bpy
from openclaymation.blender.stop_motion_rig import bake_stepped_animation, add_camera_chatter

count = 0
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.action:
        if bake_stepped_animation(obj, step_size={step_size}):
            count += 1

if {camera_jitter} and bpy.context.scene.camera:
    add_camera_chatter(bpy.context.scene.camera)

print(f"BAKED_OBJECTS:{{count}}")
"""
    output = run_inline_blender_code(code)
    return {"status": "ok", "message": f"Baked 12 FPS stop-motion stepping on scene objects.", "output": output}


def mcp_render_frames(output_dir: str, start_frame: int = 1, end_frame: int = 48) -> dict:
    """
    Renders claymation frame sequence to PNG.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    code = f"""
import bpy

scene = bpy.context.scene
scene.frame_start = {start_frame}
scene.frame_end = {end_frame}
scene.render.filepath = "{output_dir}/frame_"
scene.render.image_settings.file_format = 'PNG'

bpy.ops.render.render(animation=True)
print("SUCCESS_RENDER")
"""
    output = run_inline_blender_code(code)
    return {"status": "ok", "message": f"Rendered frames {start_frame}-{end_frame} into {output_dir}", "output": output}


def mcp_execute_blender_code(python_code: str) -> dict:
    """
    Executes custom procedural Blender python script. Allows Claude to shape,
    model, and animate custom clay props.
    """
    output = run_inline_blender_code(python_code)
    return {"status": "ok", "output": output}
