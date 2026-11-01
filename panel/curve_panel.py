import bpy

class VIEW3D_PT_CURVE(bpy.types.Panel):
    """UI Panel for configuring and generating custom 2D curves."""

    bl_label = "Create Curve"
    bl_idname = "VIEW3D_PT_CURVE"
    bl_parent_id = "VIEW3D_PT_MAIN"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "2D Toolkit"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        scene = context.scene

        # Layout organization for curve parameters
        col = layout.column(align=True)
        col.label(text="Curve Parameters", icon="CURVE_DATA")

        col.prop(scene, "curve_plane", text="Plane")
        col.prop(scene, "curve_radius", text="Radius")
        col.prop(scene, "curve_thickness", text="Thickness")
        col.prop(scene, "curve_arc_angle", text="Arc Angle")
        col.prop(scene, "curve_resolution", text="Resolution")
        col.prop(scene, "curve_cap_type", text="Cap Type")
        col.prop(scene, "curve_cap_resolution", text="Cap Resolution")

        col.separator()
        col.operator(
            "object.create_custom_curve",
            text="Generate Curve",
            icon="ADD",
        )