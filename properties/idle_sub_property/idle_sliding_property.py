import bpy
from ...consts.idle_const import (
    DEFAULT_IDLE_SLIDING_DISTANCE,
    MIN_IDLE_SLIDING_DISTANCE,
    MAX_IDLE_SLIDING_DISTANCE,
    IDLE_SLIDING_DISTANCE_PRECISION,
    IDLE_SLIDING_AXIS_ITEMS,
    DEFAULT_IDLE_SLIDING_AXIS,
    DEFAULT_IDLE_SLIDING_DURATION,
    MIN_IDLE_SLIDING_DURATION,
    MAX_IDLE_SLIDING_DURATION,
    IDLE_SLIDING_DURATION_PRECISION,
    IDLE_SLIDING_INTERPOLATION_ITEMS,
    DEFAULT_IDLE_SLIDING_INTERPOLATION,
    IDLE_SLIDING_EASING_ITEMS,
    DEFAULT_IDLE_SLIDING_EASING,
)
from .idle_waving_property import get_applicable_targets


def register_idle_sliding_properties() -> None:

    bpy.types.Scene.idle_sliding_target = bpy.props.EnumProperty(
        name="Animation Target",
        description="Select the object or armature to apply the sliding animation",
        items=get_applicable_targets,
    )

    bpy.types.Scene.idle_sliding_axis = bpy.props.EnumProperty(
        name="Slide Axis",
        description="Axis along which the target slides",
        items=IDLE_SLIDING_AXIS_ITEMS,
        default=DEFAULT_IDLE_SLIDING_AXIS,
    )

    bpy.types.Scene.idle_sliding_distance = bpy.props.FloatProperty(
        name="Slide Distance",
        description="Maximum displacement in each direction from the starting location",
        default=DEFAULT_IDLE_SLIDING_DISTANCE,
        min=MIN_IDLE_SLIDING_DISTANCE,
        max=MAX_IDLE_SLIDING_DISTANCE,
        precision=IDLE_SLIDING_DISTANCE_PRECISION,
        subtype="DISTANCE",
    )

    bpy.types.Scene.idle_sliding_duration = bpy.props.FloatProperty(
        name="Cycle Duration",
        description="Time duration required to complete a single sliding cycle",
        default=DEFAULT_IDLE_SLIDING_DURATION,
        min=MIN_IDLE_SLIDING_DURATION,
        max=MAX_IDLE_SLIDING_DURATION,
        precision=IDLE_SLIDING_DURATION_PRECISION,
    )

    bpy.types.Scene.idle_sliding_interpolation = bpy.props.EnumProperty(
        name="Interpolation",
        description="Interpolation method for the generated keyframes",
        items=IDLE_SLIDING_INTERPOLATION_ITEMS,
        default=DEFAULT_IDLE_SLIDING_INTERPOLATION,
    )

    bpy.types.Scene.idle_sliding_easing = bpy.props.EnumProperty(
        name="Easing",
        description="Easing direction for easing interpolation methods",
        items=IDLE_SLIDING_EASING_ITEMS,
        default=DEFAULT_IDLE_SLIDING_EASING,
    )


def unregister_idle_sliding_properties() -> None:

    del bpy.types.Scene.idle_sliding_target
    del bpy.types.Scene.idle_sliding_axis
    del bpy.types.Scene.idle_sliding_distance
    del bpy.types.Scene.idle_sliding_duration
    del bpy.types.Scene.idle_sliding_interpolation
    del bpy.types.Scene.idle_sliding_easing
