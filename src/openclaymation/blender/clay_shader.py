"""
Procedural Clay / Plasticine Shader Generator for Blender.
Supports Blender 3.6 LTS, 4.x, and 5.x LTS.
Creates tactile handmade clay textures with procedural fingerprints,
subsurface scattering (SSS), and matte micro-imperfections.
"""

import math
try:
    import bpy
except ImportError:
    bpy = None

CLAY_PALETTES = {
    "terracotta": (0.76, 0.38, 0.24, 1.0),
    "midnight_blue": (0.08, 0.12, 0.28, 1.0),
    "olive_green": (0.32, 0.42, 0.20, 1.0),
    "mustard_yellow": (0.85, 0.65, 0.15, 1.0),
    "plasticine_red": (0.80, 0.18, 0.16, 1.0),
    "plasticine_cyan": (0.15, 0.55, 0.75, 1.0),
    "sculpting_grey": (0.50, 0.50, 0.50, 1.0),
    "porcelain_white": (0.92, 0.90, 0.88, 1.0),
}


def create_clay_material(name="Clay_Plasticine", color=(0.76, 0.38, 0.24, 1.0), fingerprint_scale=28.0, roughness=0.65, sss_weight=0.25):
    """
    Creates a procedural clay material with fingerprint whorls and tactile bump.
    Returns the created bpy.types.Material.
    """
    if not bpy:
        raise RuntimeError("Blender python (bpy) is not available.")

    # Check if material already exists
    if name in bpy.data.materials:
        mat = bpy.data.materials[name]
    else:
        mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output node
    node_output = nodes.new(type="ShaderNodeOutputMaterial")
    node_output.location = (600, 0)

    # Principled BSDF
    node_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    node_bsdf.location = (200, 0)

    # Base Color & Roughness
    node_bsdf.inputs["Base Color"].default_value = color
    if "Roughness" in node_bsdf.inputs:
        node_bsdf.inputs["Roughness"].default_value = roughness

    # SSS configuration across Blender versions
    if "Subsurface Weight" in node_bsdf.inputs:
        # Blender 4.0+ / 5.0+
        node_bsdf.inputs["Subsurface Weight"].default_value = sss_weight
        if "Subsurface Radius" in node_bsdf.inputs:
            node_bsdf.inputs["Subsurface Radius"].default_value = (0.7, 0.3, 0.2)
    elif "Subsurface" in node_bsdf.inputs:
        # Blender 3.6 LTS
        node_bsdf.inputs["Subsurface"].default_value = sss_weight
        if "Subsurface Color" in node_bsdf.inputs:
            node_bsdf.inputs["Subsurface Color"].default_value = color

    # Texture Coordinate & Mapping
    node_coord = nodes.new(type="ShaderNodeTexCoord")
    node_coord.location = (-1000, 0)

    node_mapping = nodes.new(type="ShaderNodeMapping")
    node_mapping.location = (-800, 0)
    links.new(node_coord.outputs["Object"], node_mapping.inputs["Vector"])

    # 1. Micro Roughness & Noise (organic clay kneading marks)
    node_noise = nodes.new(type="ShaderNodeTexNoise")
    node_noise.location = (-550, 150)
    node_noise.inputs["Scale"].default_value = 18.0
    node_noise.inputs["Detail"].default_value = 4.0
    node_noise.inputs["Roughness"].default_value = 0.7
    links.new(node_mapping.outputs["Vector"], node_noise.inputs["Vector"])

    # 2. Fingerprint Texture Simulation (Wave + Voronoi combination)
    node_wave = nodes.new(type="ShaderNodeTexWave")
    node_wave.location = (-550, -150)
    node_wave.inputs["Scale"].default_value = fingerprint_scale
    node_wave.inputs["Distortion"].default_value = 7.5
    node_wave.inputs["Detail"].default_value = 2.0
    links.new(node_mapping.outputs["Vector"], node_wave.inputs["Vector"])

    # ColorRamp for subtle fingerprint grooves
    node_ramp = nodes.new(type="ShaderNodeValToRGB")
    node_ramp.location = (-300, -150)
    node_ramp.color_ramp.elements[0].position = 0.42
    node_ramp.color_ramp.elements[1].position = 0.58
    links.new(node_wave.outputs["Fac"], node_ramp.inputs["Fac"])

    # Bump node
    node_bump = nodes.new(type="ShaderNodeBump")
    node_bump.location = (-50, -100)
    node_bump.inputs["Strength"].default_value = 0.12  # Subtle handmade thumbprint
    node_bump.inputs["Distance"].default_value = 0.05
    links.new(node_ramp.outputs["Color"], node_bump.inputs["Height"])

    # Connect Normal & BSDF to Output
    links.new(node_bump.outputs["Normal"], node_bsdf.inputs["Normal"])
    links.new(node_bsdf.outputs["BSDF"], node_output.inputs["Surface"])

    return mat


def apply_clay_to_object(obj, palette_name="terracotta", custom_rgba=None, fingerprint_scale=28.0):
    """
    Applies procedural clay material to a given Blender object.
    """
    if not bpy:
        raise RuntimeError("Blender python (bpy) is not available.")

    color = custom_rgba if custom_rgba else CLAY_PALETTES.get(palette_name, CLAY_PALETTES["terracotta"])
    mat_name = f"Clay_{palette_name.capitalize()}"
    mat = create_clay_material(name=mat_name, color=color, fingerprint_scale=fingerprint_scale)

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return mat
