import math
import bpy


# Idle action template class (Template Method Pattern)
class OT_IDLE_create_idle_template(bpy.types.Operator):

    def get_target(self, context: bpy.types.Context) -> str:
        """Return the scene target property name holding the target identifier. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_target().")

    def get_projected_plan(self, context: bpy.types.Context) -> str:
        """Return the scene projected plan property name. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_projected_plan().")

    def get_duration(self, context: bpy.types.Context) -> str:
        """Return the scene duration property name. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_duration().")

    def get_loop(self, context: bpy.types.Context) -> bool:
        """Return the scene loop property name. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_loop().")

    def get_loop_repeat_count(self, context: bpy.types.Context) -> int:
        """Return the scene loop repeat count property name. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_loop_repeat_count().")

    def get_interpolation(self, context: bpy.types.Context) -> str:
        """Return the keyframe interpolation mode (e.g. 'LINEAR', 'SINE'). Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_interpolation().")

    def get_easing(self, context: bpy.types.Context) -> str:
        """Return the keyframe easing mode (e.g. 'EASE_IN_OUT'). Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_easing().")


    def resolve_target(self, context: bpy.types.Context):

        target_obj = None
        pose_bone = None
        
        scene = context.scene
        target_id = self.get_target(context)
        if not target_id or target_id == "NONE":
            self.report({"ERROR"}, "Select a valid object or pose bone.")
            return None, None

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

        return target_obj, pose_bone 


    def resolve_frames(self, context: bpy.types.Context):
        scene = context.scene
        fps_base = scene.render.fps_base
        if fps_base <= 0:
            self.report({"ERROR"}, "The scene frame-rate base must be greater than zero.")
            return None

        total_frames = max(
            2,
            round(self.get_duration(context) * scene.render.fps / fps_base),
        )
        start_frame = scene.frame_current
        frames = [
            start_frame + total_frames * fraction
            for fraction in (0.0, 0.5, 1.0)
        ]
        return frames


    def find_fcurves(self, target_obj: bpy.types.Object, data_path: str, axis_indices) -> list[bpy.types.FCurve]:
        """
        Return the F-curves of the target's action matching the data path and any of the axis indices.

        Args:
            target_obj: The object owning the animation data.
            data_path: The animated property path (e.g. 'rotation_euler' or a pose bone path).
            axis_indices: Array indices of the animated axes (one F-curve per axis).
        """
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

        return [
            curve
            for curve in fcurves
            if curve.data_path == data_path and curve.array_index in axis_indices
        ]


    def apply_interpolation(self, context: bpy.types.Context, fcurves: list[bpy.types.FCurve], frames: list[float]) -> None:
        """
        Apply the selected interpolation (and easing, when supported) to the keyframes of each F-curve
        located at the given frames.

        Args:
            fcurves: The F-curves whose keyframes are updated.
            frames: Frames of the generated keyframes; other keyframes are left untouched.
        """
        interpolation = self.get_interpolation(context)
        easing = self.get_easing(context)

        easing_interpolations = {"SINE", "QUAD", "CUBIC"}
        for fcurve in fcurves:
            for keyframe in fcurve.keyframe_points:
                if not any(abs(keyframe.co.x - frame) < 1e-4 for frame in frames):
                    continue
                keyframe.interpolation = interpolation
                if interpolation in easing_interpolations:
                    keyframe.easing = easing


    def apply_cycles_modifier(self, context: bpy.types.Context, fcurves: list[bpy.types.FCurve]) -> None:
        """
        Make each F-curve repeat after its last keyframe using a Cycles modifier.

        Args:
            fcurves: The F-curves to loop.
        """
        repeat_count = self.get_loop_repeat_count(context)  # 0 = infinite
        for fcurve in fcurves:
            modifier = next((m for m in fcurve.modifiers if m.type == "CYCLES"), None)
            if modifier is None:
                modifier = fcurve.modifiers.new(type="CYCLES")
            modifier.mode_before = "NONE"
            modifier.mode_after = "REPEAT"
            modifier.cycles_after = repeat_count


    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene

        # 1. Get target obj or bone
        target_obj, pose_bone = self.resolve_target(context)
        if target_obj is None:
            return {"CANCELLED"}

        # 2. Determine the axis index for rotation based on the selected projection plane
        axis_index = {"XY": 2, "XZ": 1, "YZ": 0}.get(self.get_projected_plan(context))
        if axis_index is None:
            self.report({"ERROR"}, "Select a valid projection plane.")
            return {"CANCELLED"}

        # 3. Calculate the total number of frames
        frames = self.resolve_frames(context)
        if frames is None:
            return {"CANCELLED"}
        offsets = [
            math.radians(scene.idle_waving_angle),
            -math.radians(scene.idle_waving_angle),
            math.radians(scene.idle_waving_angle)
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

        # 4. Retrieve the generated fcurves (one per animated axis)
        axis_indices = [axis_index]
        target_fcurves = self.find_fcurves(target_obj, data_path, axis_indices)
        if len(target_fcurves) != len(axis_indices):
            self.report({"ERROR"}, "Could not find the generated animation curves.")
            return {"CANCELLED"}

        # 5. Apply Interpolation and Easing
        self.apply_interpolation(context, target_fcurves, frames)

        # 6. Apply Loop - Cycle
        if self.get_loop(context):
            self.apply_cycles_modifier(context, target_fcurves)

        self.report(
            {"INFO"},
            f"Generated animation for {target_obj.name}"
            + (f" > {pose_bone.name}." if pose_bone is not None else "."),
        )
        return {"FINISHED"}