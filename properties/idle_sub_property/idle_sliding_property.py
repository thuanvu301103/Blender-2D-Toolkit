import bpy
from ...consts.idle_const import (
    DEFAULT_IDLE_SLIDING_DISTANCE,
    MIN_IDLE_SLIDING_DISTANCE,
    MAX_IDLE_SLIDING_DISTANCE,
    IDLE_SLIDING_DISTANCE_PRECISION,
    DEFAULT_IDLE_SLIDING_DIRECTION,
    MIN_IDLE_SLIDING_DIRECTION,
    MAX_IDLE_SLIDING_DIRECTION,
    DEFAULT_IDLE_SLIDING_DURATION,
    MIN_IDLE_SLIDING_DURATION,
    MAX_IDLE_SLIDING_DURATION,
    IDLE_SLIDING_DURATION_PRECISION,
    IDLE_SLIDING_INTERPOLATION_ITEMS,
    DEFAULT_IDLE_SLIDING_INTERPOLATION,
    IDLE_SLIDING_EASING_ITEMS,
    DEFAULT_IDLE_SLIDING_EASING,
    DEFAULT_IDLE_SLIDING_LOOP,
    DEFAULT_IDLE_REPEAT_COUNT,
    MIN_IDLE_REPEAT_COUNT,
    MAX_IDLE_REPEAT_COUNT,
)
from ...consts.plane_const import DEFAULT_PLANE_2D, PLANE_2D
from ..utils import get_applicable_targets


def register_idle_sliding_properties() -> None:

    bpy.types.Scene.idle_sliding_target = bpy.props.EnumProperty(
        name="Animation Target",
        description="Select the object or armature to apply the sliding animation",
        items=get_applicable_targets,
    )

    bpy.types.Scene.idle_sliding_plane = bpy.props.EnumProperty(
        name="Projection Plane",
        description="Plane in which the target slides",
        items=PLANE_2D,
        default=DEFAULT_PLANE_2D,
    )

    bpy.types.Scene.idle_sliding_direction = bpy.props.FloatProperty(
        name="Slide Direction",
        description="Slide direction angle inside the plane, measured from the first axis of the plane "
                    "(X for XY and XZ, Y for YZ) toward the second axis",
        default=DEFAULT_IDLE_SLIDING_DIRECTION,
        min=MIN_IDLE_SLIDING_DIRECTION,
        max=MAX_IDLE_SLIDING_DIRECTION,
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

    bpy.types.Scene.idle_sliding_loop = bpy.props.BoolProperty(
        name="Loop",
        description="Repeat the cycle after the last keyframe using a Cycles F-curve modifier",
        default=DEFAULT_IDLE_SLIDING_LOOP,
    )

    bpy.types.Scene.idle_sliding_repeat_count = bpy.props.IntProperty(
        name="Repeat Count",
        description="Number of repetitions after the first cycle (0 repeats forever)",
        default=DEFAULT_IDLE_REPEAT_COUNT,
        min=MIN_IDLE_REPEAT_COUNT,
        max=MAX_IDLE_REPEAT_COUNT,
    )


def unregister_idle_sliding_properties() -> None:

    del bpy.types.Scene.idle_sliding_target
    del bpy.types.Scene.idle_sliding_plane
    del bpy.types.Scene.idle_sliding_direction
    del bpy.types.Scene.idle_sliding_distance
    del bpy.types.Scene.idle_sliding_duration
    del bpy.types.Scene.idle_sliding_interpolation
    del bpy.types.Scene.idle_sliding_easing
    del bpy.types.Scene.idle_sliding_loop
    del bpy.types.Scene.idle_sliding_repeat_count
