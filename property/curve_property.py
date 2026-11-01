import bpy
from ..const import (
    MIN_RADIUS,

    DEFAULT_RESOLUTION,
    MIN_RESOLUTION,

    DEFAULT_CAP_RESOLUTION,
    MIN_CAP_RESOLUTION
)

def register_curve_properties() -> None:
    bpy.types.Scene.curve_plane = bpy.props.EnumProperty(
        name="Projection Plane",
        description="Select spatial orientation plane",
        items=[
            ("XY", "XY Plane", "Align curve along the XY coordinate plane"),
            ("XZ", "XZ Plane", "Align curve along the XZ coordinate plane"),
            ("YZ", "YZ Plane", "Align curve along the YZ coordinate plane"),
        ],
        default="XY",
    )

    bpy.types.Scene.curve_radius = bpy.props.FloatProperty(
        name="Radius",
        description="Radius value governing the geometric scale",
        default=1.0,
        min=MIN_RADIUS,
        max=100.0,
        unit="LENGTH",
    )

    bpy.types.Scene.curve_thickness = bpy.props.FloatProperty(
        name="Thickness",
        description="Extrusion thickness or stroke width",
        default=0.1,
        min=0.000001,
        max=10.0,
        unit="LENGTH",
    )

    bpy.types.Scene.curve_arc_angle = bpy.props.FloatProperty(
        name="Arc Angle",
        description="Sweep angle distribution in degrees",
        default=360.0,
        min=1.0,
        max=360.0,
    )

    bpy.types.Scene.curve_resolution = bpy.props.IntProperty(
        name="Resolution",
        description="Number of segments proportional to arc angle resolution",
        default=DEFAULT_RESOLUTION,
        min=MIN_RESOLUTION,
        max=128,
    )

    bpy.types.Scene.curve_cap_type = bpy.props.EnumProperty(
        name="Cap Type",
        description="Geometric profile style applied to endpoints",
        items=[
            ("FLAT", "Flat", "Standard flat termination"),
            ("ROUND", "Round", "Semicircular rounded termination"),
        ],
        default="ROUND",
    )

    bpy.types.Scene.curve_cap_resolution = bpy.props.IntProperty(
        name="Cap Resolution",
        description="Number of geometric segments used to approximate curved end caps (ROUND type)",
        default=DEFAULT_CAP_RESOLUTION,
        min=MIN_CAP_RESOLUTION,
        max=128,
    )


def unregister_curve_properties() -> None:
    del bpy.types.Scene.curve_plane
    del bpy.types.Scene.curve_radius
    del bpy.types.Scene.curve_thickness
    del bpy.types.Scene.curve_arc_angle
    del bpy.types.Scene.curve_resolution
    del bpy.types.Scene.curve_cap_type