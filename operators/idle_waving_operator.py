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

    '''def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene
        target_id = scene.idle_waving_target
        if not target_id or target_id == "NONE":
            self.report({"ERROR"}, "Select a valid object or pose bone.")
            return {"CANCELLED"}

        target_obj = None
        pose_bone = None

        # Determine the target object or pose bone based on the selected target_id
        if target_id.startswith("OBJ_"):
            target_obj = scene.objects.get(target_id[4:])
        elif target_id.startswith("BONE_"):
            # Search for the corresponding armature and pose bone based on the target_id
            for obj in scene.objects:
                if obj.type != "ARMATURE":
                    continue
                bone_prefix = f"BONE_{obj.name}_"
                if target_id.startswith(bone_prefix):
                    candidate = obj.pose.bones.get(target_id[len(bone_prefix):])
                    if candidate is not None:
                        target_obj = obj
                        pose_bone = candidate
                        break

        if target_obj is None:
            self.report({"ERROR"}, "Select a valid object or pose bone.")
            return {"CANCELLED"}

        # Determine the axis index for rotation based on the selected projection plane
        axis_index = {"XY": 2, "XZ": 1, "YZ": 0}.get(scene.idle_waving_plane)
        if axis_index is None:
            self.report({"ERROR"}, "Select a valid projection plane.")
            return {"CANCELLED"}

        # Calculate the total number of frames for the waving cycle based on the scene's frame rate and the specified duration
        fps_base = scene.render.fps_base
        if fps_base <= 0:
            self.report({"ERROR"}, "The scene frame-rate base must be greater than zero.")
            return {"CANCELLED"}

        total_frames = max(
            2,
            round(scene.idle_waving_duration * scene.render.fps / fps_base),
        )
        start_frame = scene.frame_current
        frames = [
            start_frame + total_frames * fraction
            for fraction in (0.0, 0.25, 0.5, 0.75, 1.0)
        ]
        offsets = [
            0.0,
            math.radians(scene.idle_waving_angle),
            0.0,
            -math.radians(scene.idle_waving_angle),
            0.0,
        ]

        # Determine the animated target (pose bone or object) and ensure its rotation mode is compatible with Euler rotations
        animated_target = pose_bone if pose_bone is not None else target_obj
        if animated_target.rotation_mode not in {
            "XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"
        }:
            animated_target.rotation_mode = "XYZ"

        base_rotation = list(animated_target.rotation_euler)
        data_path = (
            pose_bone.path_from_id("rotation_euler")
            if pose_bone is not None
            else "rotation_euler"
        )

        # Ensure the target object has animation data and an action to store the generated keyframes
        if target_obj.animation_data is None:
            target_obj.animation_data_create()

        if target_obj.animation_data.action is None:
            action_name = (
                f"{target_obj.name}_{pose_bone.name}_WavingAction"
                if pose_bone is not None
                else f"{target_obj.name}_WavingAction"
            )
            target_obj.animation_data.action = bpy.data.actions.new(name=action_name)

        # Generate keyframes for the waving animation by modifying the rotation of the animated target at specified frames and offsets
        for frame, offset in zip(frames, offsets):
            rotation = base_rotation.copy()
            rotation[axis_index] += offset
            animated_target.rotation_euler = rotation
            animated_target.keyframe_insert(
                data_path="rotation_euler",
                index=axis_index,
                frame=frame,
            )

        # Retrieve the fcurve corresponding to the generated rotation animation for the specified axis and 
        # apply the selected interpolation and easing modes to the keyframes
        action = target_obj.animation_data.action
        if hasattr(action, "fcurves"):
            fcurves = action.fcurves
        else:
            action_slot = target_obj.animation_data.action_slot
            fcurves = []
            if action_slot is not None:
                for layer in action.layers:
                    for strip in layer.strips:
                        if strip.type != "KEYFRAME":
                            continue
                        channelbag = strip.channelbag(action_slot)
                        if channelbag is not None:
                            fcurves.extend(channelbag.fcurves)

        fcurve = next(
            (
                curve
                for curve in fcurves
                if curve.data_path == data_path and curve.array_index == axis_index
            ),
            None,
        )
        if fcurve is None:
            self.report({"ERROR"}, "Could not find the generated rotation animation curve.")
            return {"CANCELLED"}

        interpolation = scene.idle_waving_interpolation
        easing = scene.idle_waving_easing

        easing_interpolations = {"SINE", "QUAD", "CUBIC"}
        for keyframe in fcurve.keyframe_points:
            if not any(abs(keyframe.co.x - frame) < 1e-4 for frame in frames):
                continue
            keyframe.interpolation = interpolation
            if interpolation in easing_interpolations:
                keyframe.easing = easing

        if scene.idle_waving_loop:
            apply_cycles_modifier(fcurve, scene.idle_waving_repeat_count)

        self.report(
            {"INFO"},
            f"Generated waving animation for {target_obj.name}"
            + (f" > {pose_bone.name}." if pose_bone is not None else "."),
        )
        return {"FINISHED"}
    
    '''


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