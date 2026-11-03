import math

import bpy
from ..consts.idle_const import (
    DEFAULT_IDLE_WAVING_ANGLE,
    DEFAULT_IDLE_WAVING_DURATION,
    DEFAULT_IDLE_WAVING_EASING,
    DEFAULT_IDLE_WAVING_INTERPOLATION,
    DEFAULT_IDLE_WAVING_LOOP,
    DEFAULT_IDLE_REPEAT_COUNT,
)
from .utils import apply_cycles_modifier
from ..consts.plane_const import DEFAULT_PLANE_2D

from .idle_operator import OT_IDLE_create_idle_template


class OT_IDLE_create_idle_waving(OT_IDLE_create_idle_template):
    """Create a single oscillation cycle on the selected object or pose bone."""

    bl_idname = "object.create_idle_waving"
    bl_label = "Generate Waving Animation"
    bl_options = {"REGISTER", "UNDO"}

    def get_target(self, context: bpy.types.Context) -> str:
        return context.scene.idle_waving_target

    def get_projected_plan(self, context: bpy.types.Context) -> str:
        return context.scene.idle_waving_plane

    def get_duration(self, context: bpy.types.Context) -> float:
        return context.scene.idle_waving_duration

    def get_loop(self, context: bpy.types.Context) -> bool:
        return context.scene.idle_waving_loop
    
    def get_loop_repeat_count(self, context: bpy.types.Context) -> int:
        return context.scene.idle_waving_repeat_count

    def get_interpolation(self, context: bpy.types.Context) -> str:
        return context.scene.idle_waving_interpolation

    def get_easing(self, context: bpy.types.Context) -> str:
        return context.scene.idle_waving_easing


    def resolve_axis_effect(self, context: bpy.types.Context) -> tuple[int, int, int] | None:
        axis_affect = {
            "XY": (0, 0, 1),
            "XZ": (0, 1, 0),
            "YZ": (1, 0, 0),
        }.get(self.get_projected_plan(context))
        if axis_affect is None:
            self.report({"ERROR"}, "Select a valid projection plane.")
        return axis_affect

    def resolve_frames(self, context: bpy.types.Context) ->  tuple[list[float] | None, list[float] | None]:
        scene = context.scene
        fps_base = scene.render.fps_base
        if fps_base <= 0:
            self.report({"ERROR"}, "The scene frame-rate base must be greater than zero.")
            return None, None

        total_frames = max(
            2,
            round(self.get_duration(context) * scene.render.fps / fps_base),
        )
        start_frame = scene.frame_current
        frames = [
            start_frame + total_frames * fraction
            for fraction in (0.0, 0.5, 1.0)
        ]
        offsets = [
            math.radians(scene.idle_waving_angle),
            -math.radians(scene.idle_waving_angle),
            math.radians(scene.idle_waving_angle)
        ]
        return frames, offsets

    def insert_keyframes(
        self,
        animated_target: bpy.types.Object | bpy.types.PoseBone,
        axis_indices: list[int],
        frames: list[float],
        offsets: list[float],
    ) -> bool:
        if len(frames) != len(offsets):
            self.report({"ERROR"}, "Each keyframe must have a matching offset.")
            return False

        base_rotation = list(animated_target.rotation_euler)
        for frame, offset in zip(frames, offsets):
            rotation = base_rotation.copy()
            for index in axis_indices:
                rotation[index] += offset
            animated_target.rotation_euler = rotation
            for index in axis_indices:
                inserted = animated_target.keyframe_insert(
                    data_path="rotation_euler",
                    index=index,
                    frame=frame,
                )
                if not inserted:
                    self.report({"ERROR"}, f"Failed to insert rotation keyframe at frame {frame}.")
                    return False

        return True
    
    def resolve_animation_target(
        self,
        target_obj: bpy.types.Object,
        pose_bone: bpy.types.PoseBone | None = None,
    ) -> tuple[bpy.types.Object | bpy.types.PoseBone, str]:
        animated_target = pose_bone if pose_bone is not None else target_obj
        if animated_target.rotation_mode not in {
            "XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"
        }:
            animated_target.rotation_mode = "XYZ"

        data_path = (
            pose_bone.path_from_id("rotation_euler")
            if pose_bone is not None
            else "rotation_euler"
        )
        return animated_target, data_path


class OT_IDLE_reset_idle_waving_defaults(bpy.types.Operator):
    
    bl_idname = "object.reset_idle_waving_defaults"
    bl_label = "Reset to Default"
    bl_description = "Reset all waving parameters to their default values"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set:
        scene = context.scene
        
        # Reset properties to their default values
        scene.idle_waving_plane = DEFAULT_PLANE_2D
        scene.idle_waving_angle = DEFAULT_IDLE_WAVING_ANGLE
        scene.idle_waving_duration = DEFAULT_IDLE_WAVING_DURATION
        scene.idle_waving_interpolation = DEFAULT_IDLE_WAVING_INTERPOLATION
        scene.idle_waving_easing = DEFAULT_IDLE_WAVING_EASING
        scene.idle_waving_loop = DEFAULT_IDLE_WAVING_LOOP
        scene.idle_waving_repeat_count = DEFAULT_IDLE_REPEAT_COUNT
        
        self.report({'INFO'}, "Waving parameters reset to defaults")
        return {'FINISHED'}