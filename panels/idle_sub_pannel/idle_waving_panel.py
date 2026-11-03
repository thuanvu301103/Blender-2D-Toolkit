
import bpy

class VIEW3D_PT_IDLE_WAVING(bpy.types.Panel):
    
    bl_label = "Waving"
    bl_idname = "VIEW3D_PT_IDLE_WAVING"
    bl_parent_id = "VIEW3D_PT_IDLE"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "2D Toolkit"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.label(text="Waving Parameters", icon="MOD_WAVE")
        row.operator(
            "object.reset_idle_waving_defaults",
            text="",
            icon="FILE_REFRESH"
        )

        col = layout.column(align=True)
        col.prop(scene, "idle_waving_target", text="Target")
        col.prop(scene, "idle_waving_plane", text="Plane")
        col.prop(scene, "idle_waving_angle", text="Rotation Angle")
        col.prop(scene, "idle_waving_duration", text="Cycle Duration")
        col.separator()

        col.prop(scene, "idle_waving_interpolation", text="Interpolation")
        col.prop(scene, "idle_waving_easing", text="Easing")

        col.separator()
        col.operator(
            "object.create_idle_waving",
            text="Generate Waving Animation",
            icon="ADD",
        )