"""
Blender Add-on: OpenClaymation Studio UI Panel.
Registers a complete 3D Viewport N-Panel for one-click claymation staging,
procedural plasticine shaders, and stop-motion physics baking.
"""

bl_info = {
    "name": "OpenClaymation Studio",
    "author": "OpenClaymation Contributors",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > ClayStudio",
    "description": "Procedural clay shaders, 12 FPS stop-motion stepper, and miniature lighting for Claude & Blender.",
    "category": "Animation",
}

try:
    import bpy
    from bpy.props import EnumProperty, FloatProperty, BoolProperty, IntProperty
except ImportError:
    bpy = None

if bpy:
    from .clay_shader import apply_clay_to_object, CLAY_PALETTES
    from .stop_motion_rig import setup_stop_motion_environment, bake_stepped_animation, add_camera_chatter, setup_macro_lens
    from .studio_stage import build_miniature_stage

    class CLAY_OT_ApplyShader(bpy.types.Operator):
        bl_idname = "clay.apply_shader"
        bl_label = "Apply Clay Shader"
        bl_description = "Applies tactile plasticine shader with procedural fingerprints"
        bl_options = {'REGISTER', 'UNDO'}

        palette: EnumProperty(
            name="Palette",
            items=[(k, k.replace("_", " ").capitalize(), "") for k in CLAY_PALETTES.keys()],
            default="terracotta"
        )
        fingerprint_scale: FloatProperty(name="Fingerprint Scale", default=28.0, min=5.0, max=100.0)

        def execute(self, context):
            for obj in context.selected_objects:
                if obj.type == 'MESH':
                    apply_clay_to_object(obj, palette_name=self.palette, fingerprint_scale=self.fingerprint_scale)
            self.report({'INFO'}, "Clay shader applied successfully.")
            return {'FINISHED'}

    class CLAY_OT_SetupStudio(bpy.types.Operator):
        bl_idname = "clay.setup_studio"
        bl_label = "Spawn Miniature Studio"
        bl_description = "Creates tabletop cyclorama, warm 3-point lighting, and macro camera"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            build_miniature_stage()
            setup_stop_motion_environment()
            self.report({'INFO'}, "Miniature studio stage spawned.")
            return {'FINISHED'}

    class CLAY_OT_BakeStopMotion(bpy.types.Operator):
        bl_idname = "clay.bake_stopmotion"
        bl_label = "Bake 12 FPS Stepped Cadence"
        bl_description = "Converts smooth curves to authentic 12 FPS (animating on twos) stop-motion"
        bl_options = {'REGISTER', 'UNDO'}

        step_frames: IntProperty(name="Frame Step", default=2, min=1, max=6)

        def execute(self, context):
            count = 0
            for obj in context.selected_objects:
                if bake_stepped_animation(obj, step_size=self.step_frames):
                    count += 1
            if context.scene.camera:
                add_camera_chatter(context.scene.camera)
            self.report({'INFO'}, f"Baked stop-motion stepping on {count} objects.")
            return {'FINISHED'}

    class CLAY_PT_MainPanel(bpy.types.Panel):
        bl_label = "OpenClaymation Studio"
        bl_idname = "CLAY_PT_MainPanel"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = "ClayStudio"

        def draw(self, context):
            layout = self.layout

            # Staging Box
            box = layout.box()
            box.label(text="1. Studio Setup", icon='SCENE_DATA')
            box.operator("clay.setup_studio", text="Spawn Miniature Stage", icon='LIGHT_SUN')

            # Material Box
            box = layout.box()
            box.label(text="2. Plasticine & Shaders", icon='MATERIAL')
            box.operator("clay.apply_shader", text="Apply Clay Material", icon='BRUSH_SOFT')

            # Animation Physics Box
            box = layout.box()
            box.label(text="3. Stop-Motion Physics", icon='ACTION')
            box.operator("clay.bake_stopmotion", text="Bake 12 FPS Stepper", icon='KEYFRAME')


    classes = [
        CLAY_OT_ApplyShader,
        CLAY_OT_SetupStudio,
        CLAY_OT_BakeStopMotion,
        CLAY_PT_MainPanel,
    ]

    def register():
        for cls in classes:
            bpy.utils.register_class(cls)

    def unregister():
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)

    if __name__ == "__main__":
        register()
