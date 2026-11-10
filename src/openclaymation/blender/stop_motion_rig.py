"""
Stop-Motion Physics & Keyframe Stepper for Blender.
Converts smooth computer-generated 3D animations into authentic 12 FPS
stop-motion cadence (animating on twos), with organic miniature camera chatter.
Supports Blender 3.6 LTS, 4.x, and 5.x LTS (Slotted Actions).
"""

import math
try:
    import bpy
except ImportError:
    bpy = None


def get_all_fcurves(action):
    """
    Universally retrieves F-Curves across Blender 3.x, 4.x, and 5.x (Slotted Actions).
    """
    if not action:
        return []
    if hasattr(action, "fcurves"):
        return list(action.fcurves)

    fcurves = []
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for cb in getattr(strip, "channelbags", []):
                fcurves.extend(getattr(cb, "fcurves", []))
    return fcurves


def setup_stop_motion_environment(fps=24, step=2, render_resolution=(1080, 1920)):
    """
    Configures Blender scene render settings for vertical (or user-defined)
    stop-motion animation. Default is 1080x1920 (9:16 Shorts/Reels/TikTok).
    """
    if not bpy:
        raise RuntimeError("Blender python (bpy) is not available.")

    scene = bpy.context.scene
    scene.render.fps = fps
    scene.render.resolution_x = render_resolution[0]
    scene.render.resolution_y = render_resolution[1]
    scene.render.resolution_percentage = 100

    # Color Management for vibrant tactile plasticine
    if hasattr(scene.view_settings, "view_transform"):
        try:
            scene.view_settings.view_transform = "AgX"
        except Exception:
            scene.view_settings.view_transform = "Filmic"

    try:
        scene.view_settings.look = "Medium High Contrast"
    except Exception:
        pass

    return scene


def bake_stepped_animation(obj, step_size=2):
    """
    Converts all continuous f-curves of an animated object into stepped
    modifiers or CONSTANT interpolation, replicating physical clay manipulation.
    """
    if not bpy or not obj.animation_data or not obj.animation_data.action:
        return False

    action = obj.animation_data.action
    fcurves = get_all_fcurves(action)

    if not fcurves:
        return False

    for fcurve in fcurves:
        # Add or configure Stepped modifier
        stepped_mod = None
        for mod in fcurve.modifiers:
            if mod.type == "STEPPED":
                stepped_mod = mod
                break
        if not stepped_mod:
            stepped_mod = fcurve.modifiers.new(type="STEPPED")
        
        stepped_mod.frame_step = step_size
        stepped_mod.frame_offset = 0.0

    return True


def add_camera_chatter(camera_obj, location_intensity=0.003, rotation_intensity=0.002):
    """
    Adds subtle organic camera vibration simulating accidental bumps
    and manual camera positioning between stop-motion exposures.
    """
    if not bpy or camera_obj.type != "CAMERA":
        return False

    # Ensure animation data exists
    if not camera_obj.animation_data:
        camera_obj.animation_data_create()
    
    # Insert initial keyframe if none
    if not camera_obj.animation_data.action:
        camera_obj.keyframe_insert(data_path="location", frame=1)
        camera_obj.keyframe_insert(data_path="rotation_euler", frame=1)

    action = camera_obj.animation_data.action
    fcurves = get_all_fcurves(action)

    for fcurve in fcurves:
        # Add Noise Modifier to simulate hand-crafted imperfection
        has_noise = any(m.type == "NOISE" for m in fcurve.modifiers)
        if not has_noise:
            mod = fcurve.modifiers.new(type="NOISE")
            mod.scale = 12.0
            if "location" in fcurve.data_path:
                mod.strength = location_intensity
            else:
                mod.strength = rotation_intensity

            # Add stepped modifier so the camera also steps on twos
            step_mod = fcurve.modifiers.new(type="STEPPED")
            step_mod.frame_step = 2.0

    return True


def setup_clay_boil(last_frame: int = 1080, boil_step: int = 3):
    """
    Sets up the classic stop-motion clay 'boil' effect.
    Animates the 'BoilCtl' empty with CONSTANT interpolation every N frames (default 3)
    to drive displacement modifiers, replicating the organic finger-kneading variations.
    """
    if not bpy:
        return False

    import random
    random.seed(42)

    boil_obj = bpy.data.objects.get("BoilCtl")
    if not boil_obj:
        boil_obj = bpy.data.objects.new("BoilCtl", None)
        boil_obj.empty_display_type = 'SPHERE'
        boil_obj.empty_display_size = 0.2
        bpy.context.collection.objects.link(boil_obj)

    if boil_obj.animation_data:
        boil_obj.animation_data_clear()

    for f in range(1, last_frame + 1, boil_step):
        boil_obj.location = tuple(random.uniform(-0.03, 0.03) for _ in range(3))
        boil_obj.keyframe_insert("location", frame=f)

    # Force CONSTANT interpolation on all BoilCtl keyframes
    action = boil_obj.animation_data.action if boil_obj.animation_data else None
    if action:
        for fcurve in get_all_fcurves(action):
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'CONSTANT'

    return True


def setup_macro_lens(camera_obj, target_obj=None, focal_length=65.0, f_stop=2.8):
    """
    Configures shallow depth of field (DoF) to emphasize the miniature scale
    typical of tabletop claymation sets.
    """
    if not bpy or camera_obj.type != "CAMERA":
        return False

    cam = camera_obj.data
    cam.lens = focal_length
    cam.dof.use_dof = True
    cam.dof.aperture_fstop = f_stop

    if target_obj:
        cam.dof.focus_object = target_obj
    else:
        cam.dof.focus_distance = 1.8

    return True
