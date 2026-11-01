import bpy

class VIEW3D_PT_FACE(bpy.types.Panel):

    bl_label = "Create Face"
    bl_idname = "VIEW3D_PT_FACE"
    bl_parent_id = "VIEW3D_PT_MAIN"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "2D Toolkit"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.label(text="Face Parameters", icon="OUTLINER_COLLECTION")

        col.prop(scene, "face_plane", text="Plane")

        col.separator()
        col.operator(
            "object.create_custom_face",
            text="Generate Face",
            icon="ADD",
        )