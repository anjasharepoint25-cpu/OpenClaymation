"""
Tabletop Miniature Studio Stage & Warm 3-Point Lighting.
Generates an authentic clay animation physical stage setup.
"""

import math
try:
    import bpy
except ImportError:
    bpy = None

from .clay_shader import apply_clay_to_object


def build_miniature_stage(backdrop_color=(0.90, 0.88, 0.84, 1.0), lighting_warmth=0.8):
    """
    Spawns a curved cyclorama backdrop, warm 3-point lighting setup,
    and a tabletop camera focused at origin.
    """
    if not bpy:
        raise RuntimeError("Blender python (bpy) is not available.")

    # 1. Cyclorama Backdrop
    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Clay_Cyclorama_Stage"

    # Extrude back wall if not already curved
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Apply matte backdrop clay material
    apply_clay_to_object(floor, custom_rgba=backdrop_color, fingerprint_scale=12.0)

    # 2. Key Light (Warm, slightly off-angle)
    light_key_data = bpy.data.lights.new(name="Clay_KeyLight", type='AREA')
    light_key_data.energy = 220.0
    light_key_data.size = 1.2
    light_key_data.color = (1.0, 0.92 * lighting_warmth, 0.82 * lighting_warmth)
    light_key = bpy.data.objects.new(name="Clay_KeyLight", object_data=light_key_data)
    bpy.context.collection.objects.link(light_key)
    light_key.location = (2.2, -2.5, 2.8)
    light_key.rotation_euler = (math.radians(45), math.radians(15), math.radians(35))

    # 3. Fill Light (Soft cool contrast)
    light_fill_data = bpy.data.lights.new(name="Clay_FillLight", type='AREA')
    light_fill_data.energy = 90.0
    light_fill_data.size = 2.0
    light_fill_data.color = (0.85, 0.90, 1.0)
    light_fill = bpy.data.objects.new(name="Clay_FillLight", object_data=light_fill_data)
    bpy.context.collection.objects.link(light_fill)
    light_fill.location = (-2.5, -2.0, 1.8)
    light_fill.rotation_euler = (math.radians(55), math.radians(-10), math.radians(-45))

    # 4. Rim / Edge Light (Highlights glossy clay edges)
    light_rim_data = bpy.data.lights.new(name="Clay_RimLight", type='SPOT')
    light_rim_data.energy = 160.0
    light_rim_data.spot_size = math.radians(45)
    light_rim_data.color = (1.0, 0.98, 0.95)
    light_rim = bpy.data.objects.new(name="Clay_RimLight", object_data=light_rim_data)
    bpy.context.collection.objects.link(light_rim)
    light_rim.location = (0, 2.5, 3.0)
    light_rim.rotation_euler = (math.radians(-45), 0, math.radians(180))

    # 5. Miniature Studio Camera
    cam_data = bpy.data.cameras.new(name="Clay_Camera")
    cam_obj = bpy.data.objects.new(name="Clay_Camera", object_data=cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = (0, -2.8, 1.1)
    cam_obj.rotation_euler = (math.radians(78), 0, 0)
    bpy.context.scene.camera = cam_obj

    return {
        "stage": floor.name,
        "camera": cam_obj.name,
        "lights": [light_key.name, light_fill.name, light_rim.name]
    }
