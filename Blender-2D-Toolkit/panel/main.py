import bpy

# Panel Definition
class VIEW3D_PT_2d_toolkit_main(bpy.types.Panel):
    """Main UI Panel for Blender 2D Toolkit in 3D View Sidebar."""

    bl_label = "2D Toolkit"
    bl_idname = "VIEW3D_PT_2d_toolkit_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "2D Toolkit"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        scene = context.scene

        # Outline Effect Section
        box = layout.box()
        box.label(text="Outline Effect", icon="STROKE")

        col = box.column(align=True)
        col.prop(scene, "outline_thickness")
        col.prop(scene, "outline_projection_plane")

        col.separator()
        col.operator("mesh.create_2d_outline", text="Generate Outline", icon="OUTLINER")
