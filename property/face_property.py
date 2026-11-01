import bpy
from ..const import (
    PLANE_2D,
    DEFAULT_PLANE_2D
)

def register_face_properties() -> None:
    bpy.types.Scene.face_plane = bpy.props.EnumProperty(
        name="Projection Plane",
        description="Select spatial orientation plane",
        items=PLANE_2D,
        default=DEFAULT_PLANE_2D,
    )

def unregister_face_properties() -> None:
    del bpy.types.Scene.face_plane