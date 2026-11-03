
import bpy
from .panels import (
    #VIEW3D_PT_MAIN,
    VIEW3D_PT_CURVE,
    VIEW3D_PT_FACE,
    VIEW3D_PT_IDLE,
    VIEW3D_PT_IDLE_WAVING
)
from .operators import (
    OT_CURVE_create_custom_curve,
    OT_FACE_create_custom_face,
    OT_IDLE_create_idle_waving,
)
from .properties import register_properties, unregister_properties

# Add-on Metadata for Blender 2D Toolkit

bl_info = {
    "name": "Blender 2D Toolkit",
    "author": "Vu Ngoc Thuan",
    "version": "1.0.0",
    "blender": (4, 0, 0),
    "location": "View3D > N-Panel > 2D Toolkit",
    "description": "A collection of 2D geometry processing and rigging tools for Blender.",
    "category": "Mesh",
}

# Module Classes
classes = (
    OT_CURVE_create_custom_curve,
    OT_FACE_create_custom_face,
    OT_IDLE_create_idle_waving,
    #VIEW3D_PT_MAIN,
    VIEW3D_PT_CURVE,
    VIEW3D_PT_FACE,
    VIEW3D_PT_IDLE,
    VIEW3D_PT_IDLE_WAVING
)


def register() -> None:
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception:
            pass
    register_properties()


def unregister() -> None:
    unregister_properties()
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass


if __name__ == "__main__":
    try:
        unregister()
    except Exception:
        pass
    register()