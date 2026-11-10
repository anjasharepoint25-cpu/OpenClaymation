"""
Clay Character Rig & Pivot Builder.
Constructs clay puppet armatures with head and arm rotational pivots:
  Root Empty: {Name}
  Head Pivot: {Name}_Hpiv  at (0, 0, 1.38)
  Left Arm:   {Name}_ALpiv at (-0.36, 0, 1.20)
  Right Arm:  {Name}_ARpiv at (0.36, 0, 1.20)
"""

try:
    import bpy
    from mathutils import Vector
except ImportError:
    bpy = None

from .clay_shader import apply_clay_to_object


def create_clay_character(name: str, palette: str = "terracotta", eye_palette: str = "midnight_blue"):
    """
    Creates a standard stop-motion clay puppet with hierarchical pivot empties.
    Compatible with `anim_lib.armsto`, `headto`, `wave`, `cheer`, and `shakehead`.
    """
    if not bpy:
        raise RuntimeError("Blender (bpy) is not available.")

    # 1. Root Empty
    root = bpy.data.objects.new(name, None)
    root.empty_display_type = 'ARROWS'
    root.empty_display_size = 0.5
    bpy.context.collection.objects.link(root)
    root['asset'] = True
    root['kind'] = 'person'

    # 2. Pivot Empties (Head, Left Arm, Right Arm)
    pivots = {
        f"{name}_Hpiv": (0.0, 0.0, 1.38),
        f"{name}_ALpiv": (-0.36, 0.0, 1.20),
        f"{name}_ARpiv": (0.36, 0.0, 1.20),
    }
    piv_objs = {}
    for piv_name, piv_loc in pivots.items():
        piv = bpy.data.objects.new(piv_name, None)
        piv.empty_display_type = 'SPHERE'
        piv.empty_display_size = 0.15
        piv.location = piv_loc
        piv.parent = root
        bpy.context.collection.objects.link(piv)
        piv_objs[piv_name] = piv

    # 3. Torso (Clay Cone / Cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.85, location=(0, 0, 0.85))
    torso = bpy.context.active_object
    torso.name = f"{name}_Torso"
    torso.parent = root
    apply_clay_to_object(torso, palette_name=palette)

    # 4. Head (Clay Sphere attached to Head Pivot)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=(0, 0, 0.18))
    head = bpy.context.active_object
    head.name = f"{name}_Head"
    head.parent = piv_objs[f"{name}_Hpiv"]
    apply_clay_to_object(head, palette_name=palette)

    # 5. Bead Eyes
    for eye_name, eye_x in [(f"{name}_EyeL", -0.09), (f"{name}_EyeR", 0.09)]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.045, location=(eye_x, -0.25, 0.22))
        eye = bpy.context.active_object
        eye.name = eye_name
        eye.parent = head
        apply_clay_to_object(eye, palette_name=eye_palette)

    # 6. Arms (attached to Arm Pivots)
    for arm_name, parent_piv, arm_sign in [(f"{name}_ArmL", piv_objs[f"{name}_ALpiv"], -1), (f"{name}_ArmR", piv_objs[f"{name}_ARpiv"], 1)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.45, location=(arm_sign * 0.12, 0, -0.22))
        arm = bpy.context.active_object
        arm.name = arm_name
        arm.parent = parent_piv
        apply_clay_to_object(arm, palette_name=palette)

    return root
