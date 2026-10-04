
import bpy
from .panel import VIEW3D_PT_2d_toolkit_main
from .operator import OBJECT_OT_create_2d_outline

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


# Properties Registration
def register_properties() -> None:
    """Registers scene properties used by the 2D Outline Effect tool."""
    bpy.types.Scene.target_collection = (
        bpy.props.PointerProperty(
            name="Target Collection",
            type=bpy.types.Collection,
            description="Root collection containin 2D components"
        )
    )

    bpy.types.Scene.outline_thickness = bpy.props.FloatProperty(
        name="Thickness",
        description="Thickness offset for the 2D mesh outline",
        default=0.05,
        min=0.001,
        max=10.0,
        unit="LENGTH",
    )

    bpy.types.Scene.outline_projection_plane = bpy.props.EnumProperty(
        name="Projection Plane",
        description="Plane used to calculate 2D outward boundary vectors",
        items=[
            ("XY", "XY Plane", "Work on XY 2D plane"),
            ("XZ", "XZ Plane", "Work on XZ 2D plane"),
            ("YZ", "YZ Plane", "Work on YZ 2D plane"),
        ],
        default="XY",
    )


def unregister_properties() -> None:
    """Unregisters scene properties for the 2D Outline Effect tool."""
    if hasattr(bpy.types.Scene, "outline_thickness"):
        del bpy.types.Scene.outline_thickness
    if hasattr(bpy.types.Scene, "outline_projection_plane"):
        del bpy.types.Scene.outline_projection_plane

# Module Classes
classes = (
    OBJECT_OT_create_2d_outline,
    VIEW3D_PT_2d_toolkit_main,
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