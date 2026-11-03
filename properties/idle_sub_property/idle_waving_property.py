import bpy
from ...consts.idle_const import (
    DEFAULT_IDLE_WAVING_ANGLE,
    MIN_IDLE_WAVING_ANGLE,
    MAX_IDLE_WAVING_ANGLE,
    DEFAULT_IDLE_WAVING_DURATION,
    MIN_IDLE_WAVING_DURATION,
    MAX_IDLE_WAVING_DURATION,
    IDLE_WAVING_DURATION_PRECISION,
    IDLE_WAVING_INTERPOLATION_ITEMS,
    DEFAULT_IDLE_WAVING_INTERPOLATION,
    IDLE_WAVING_EASING_ITEMS,
    DEFAULT_IDLE_WAVING_EASING,
    DEFAULT_IDLE_WAVING_LOOP,
    DEFAULT_IDLE_REPEAT_COUNT,
    MIN_IDLE_REPEAT_COUNT,
    MAX_IDLE_REPEAT_COUNT,
)
from ...consts.plane_const import DEFAULT_PLANE_2D, PLANE_2D
from ..utils import get_applicable_targets

def register_idle_waving_properties() -> None:

    bpy.types.Scene.idle_waving_target = bpy.props.EnumProperty(
        name="Animation Target",
        description="Select the object or armature to apply waving and rotation animation",
        items=get_applicable_targets
    )

    bpy.types.Scene.idle_waving_plane = bpy.props.EnumProperty(
        name="Projection Plane",
        description="Select spatial orientation plane",
        items=PLANE_2D,
        default=DEFAULT_PLANE_2D,
    )

    bpy.types.Scene.idle_waving_angle = bpy.props.FloatProperty(
        name="Rotation Angle",
        description="Maximum angular displacement amplitude for the oscillatory rotation",
        default=DEFAULT_IDLE_WAVING_ANGLE,
        min=MIN_IDLE_WAVING_ANGLE,
        max=MAX_IDLE_WAVING_ANGLE
    )

    # Property for complete animation cycle duration (measured in seconds)
    bpy.types.Scene.idle_waving_duration = bpy.props.FloatProperty(
        name="Cycle Duration",
        description="Time duration required to complete a single oscillation cycle",
        default=DEFAULT_IDLE_WAVING_DURATION,
        min=MIN_IDLE_WAVING_DURATION,
        max=MAX_IDLE_WAVING_DURATION,
        precision=IDLE_WAVING_DURATION_PRECISION
    )

    bpy.types.Scene.idle_waving_interpolation = bpy.props.EnumProperty(
        name="Interpolation",
        description="Interpolation method for the generated keyframes",
        items=IDLE_WAVING_INTERPOLATION_ITEMS,
        default=DEFAULT_IDLE_WAVING_INTERPOLATION,
    )

    bpy.types.Scene.idle_waving_easing = bpy.props.EnumProperty(
        name="Easing",
        description="Easing direction for easing interpolation methods",
        items=IDLE_WAVING_EASING_ITEMS,
        default=DEFAULT_IDLE_WAVING_EASING,
    )

    bpy.types.Scene.idle_waving_loop = bpy.props.BoolProperty(
        name="Loop",
        description="Repeat the cycle after the last keyframe using a Cycles F-curve modifier",
        default=DEFAULT_IDLE_WAVING_LOOP,
    )

    bpy.types.Scene.idle_waving_repeat_count = bpy.props.IntProperty(
        name="Repeat Count",
        description="Number of repetitions after the first cycle (0 repeats forever)",
        default=DEFAULT_IDLE_REPEAT_COUNT,
        min=MIN_IDLE_REPEAT_COUNT,
        max=MAX_IDLE_REPEAT_COUNT,
    )


def unregister_idle_waving_properties() -> None:

    del bpy.types.Scene.idle_waving_target
    del bpy.types.Scene.idle_waving_plane
    del bpy.types.Scene.idle_waving_angle
    del bpy.types.Scene.idle_waving_duration
    del bpy.types.Scene.idle_waving_interpolation
    del bpy.types.Scene.idle_waving_easing
    del bpy.types.Scene.idle_waving_loop
    del bpy.types.Scene.idle_waving_repeat_count