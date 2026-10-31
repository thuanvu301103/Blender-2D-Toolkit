import bpy

class VIEW_CURVE(bpy.types.Panel):
    bl_label = "Create Curve    "
    bl_idname = "VIEW_CURVE"
    bl_parent_id = "VIEW_MAIN"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "2D Toolkit"

    bl_options = {"DEFAULT_CLOSED"}  # Optional: keep closed by default

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        # Add properties and operators for feature 2 here
        col.label(text="Feature 2 Controls", icon="PROPERTIES")