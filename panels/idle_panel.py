import bpy

class VIEW3D_PT_IDLE(bpy.types.Panel):
    
    bl_label = "Idle Loop Animation"
    bl_idname = "VIEW3D_PT_IDLE"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "2D Toolkit"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: bpy.types.Context) -> None:
        pass