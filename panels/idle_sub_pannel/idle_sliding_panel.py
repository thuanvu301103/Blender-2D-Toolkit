import bpy


class VIEW3D_PT_IDLE_SLIDING(bpy.types.Panel):

    bl_label = "Sliding"
    bl_idname = "VIEW3D_PT_IDLE_SLIDING"
    bl_parent_id = "VIEW3D_PT_IDLE"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "2D Toolkit"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.label(text="Sliding Parameters", icon="ARROW_LEFTRIGHT")
        row.operator(
            "object.reset_idle_sliding_defaults",
            text="",
            icon="FILE_REFRESH"
        )

        col = layout.column(align=True)
        col.prop(scene, "idle_sliding_target", text="Target")
        col.prop(scene, "idle_sliding_axis", text="Axis")
        col.prop(scene, "idle_sliding_distance", text="Slide Distance")
        col.prop(scene, "idle_sliding_duration", text="Cycle Duration")
        col.separator()

        col.prop(scene, "idle_sliding_interpolation", text="Interpolation")
        col.prop(scene, "idle_sliding_easing", text="Easing")

        col.separator()
        col.operator(
            "object.create_idle_sliding",
            text="Generate Sliding Animation",
            icon="ADD",
        )
