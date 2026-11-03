import bpy
from ..consts.idle_const import (
    DEFAULT_IDLE_SLIDING_AXIS,
    DEFAULT_IDLE_SLIDING_DISTANCE,
    DEFAULT_IDLE_SLIDING_DURATION,
    DEFAULT_IDLE_SLIDING_EASING,
    DEFAULT_IDLE_SLIDING_INTERPOLATION,
)


class OT_IDLE_create_idle_sliding(bpy.types.Operator):
    """Create a single back-and-forth sliding cycle on the selected object or pose bone."""

    bl_idname = "object.create_idle_sliding"
    bl_label = "Generate Sliding Animation"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene
        target_id = scene.idle_sliding_target
        if not target_id or target_id == "NONE":
            self.report({"ERROR"}, "Select a valid object or pose bone.")
            return {"CANCELLED"}

        target_obj = None
        pose_bone = None

        if target_id.startswith("OBJ_"):
            target_obj = scene.objects.get(target_id[4:])
        elif target_id.startswith("BONE_"):
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

        axis_index = {"X": 0, "Y": 1, "Z": 2}.get(scene.idle_sliding_axis)
        if axis_index is None:
            self.report({"ERROR"}, "Select a valid slide axis.")
            return {"CANCELLED"}

        fps_base = scene.render.fps_base
        if fps_base <= 0:
            self.report({"ERROR"}, "The scene frame-rate base must be greater than zero.")
            return {"CANCELLED"}

        total_frames = max(
            2,
            round(scene.idle_sliding_duration * scene.render.fps / fps_base),
        )
        start_frame = scene.frame_current
        frames = [
            start_frame + total_frames * fraction
            for fraction in (0.0, 0.25, 0.5, 0.75, 1.0)
        ]
        distance = scene.idle_sliding_distance
        offsets = [0.0, distance, 0.0, -distance, 0.0]

        animated_target = pose_bone if pose_bone is not None else target_obj
        base_location = list(animated_target.location)
        data_path = (
            pose_bone.path_from_id("location")
            if pose_bone is not None
            else "location"
        )

        if target_obj.animation_data is None:
            target_obj.animation_data_create()

        if target_obj.animation_data.action is None:
            action_name = (
                f"{target_obj.name}_{pose_bone.name}_SlidingAction"
                if pose_bone is not None
                else f"{target_obj.name}_SlidingAction"
            )
            target_obj.animation_data.action = bpy.data.actions.new(name=action_name)

        for frame, offset in zip(frames, offsets):
            location = base_location.copy()
            location[axis_index] += offset
            animated_target.location = location
            animated_target.keyframe_insert(
                data_path="location",
                index=axis_index,
                frame=frame,
            )

        # Restore the starting location so the scene is not left at the last keyed value
        animated_target.location = base_location

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
            self.report({"ERROR"}, "Could not find the generated location animation curve.")
            return {"CANCELLED"}

        interpolation = scene.idle_sliding_interpolation
        easing = scene.idle_sliding_easing

        easing_interpolations = {"SINE", "QUAD", "CUBIC"}
        for keyframe in fcurve.keyframe_points:
            if not any(abs(keyframe.co.x - frame) < 1e-4 for frame in frames):
                continue
            keyframe.interpolation = interpolation
            if interpolation in easing_interpolations:
                keyframe.easing = easing

        self.report(
            {"INFO"},
            f"Generated sliding animation for {target_obj.name}"
            + (f" > {pose_bone.name}." if pose_bone is not None else "."),
        )
        return {"FINISHED"}


class OT_IDLE_reset_idle_sliding_defaults(bpy.types.Operator):

    bl_idname = "object.reset_idle_sliding_defaults"
    bl_label = "Reset to Default"
    bl_description = "Reset all sliding parameters to their default values"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set:
        scene = context.scene

        scene.idle_sliding_axis = DEFAULT_IDLE_SLIDING_AXIS
        scene.idle_sliding_distance = DEFAULT_IDLE_SLIDING_DISTANCE
        scene.idle_sliding_duration = DEFAULT_IDLE_SLIDING_DURATION
        scene.idle_sliding_interpolation = DEFAULT_IDLE_SLIDING_INTERPOLATION
        scene.idle_sliding_easing = DEFAULT_IDLE_SLIDING_EASING

        self.report({'INFO'}, "Sliding parameters reset to defaults")
        return {'FINISHED'}
