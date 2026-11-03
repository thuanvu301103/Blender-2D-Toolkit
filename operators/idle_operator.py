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


    # --- Step 1: Resolve target ---
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


    # --- Step 2: Resolve axis affect ---
    def resolve_axis_effect(self, context: bpy.types.Context) -> tuple[int, int, int] | None:
        raise NotImplementedError("Subclasses must implement resolve_axis_effect().")

    def resolve_axis_indices(self, axis_effect: tuple[int, int, int]) -> list[int] | None:
        if len(axis_effect) != 3 or any(axis not in (0, 1) for axis in axis_effect):
            self.report({"ERROR"}, "Axis effect must contain three 0/1 values for X, Y, and Z.")
            return None

        axis_indices = [
            index
            for index, affects_axis in enumerate(axis_effect)
            if affects_axis == 1
        ]
        if not axis_indices:
            self.report({"ERROR"}, "At least one axis must be selected.")
            return None
        return axis_indices


    # --- Step 3: Resolve frames and offset of each frame ---
    def resolve_frames(self, context: bpy.types.Context) -> tuple[list[float] | None, list[float] | None]:
        raise NotImplementedError("Subclasses must implement resolve_frames().")


    def insert_keyframes(
        self,
        animated_target: bpy.types.Object | bpy.types.PoseBone,
        axis_indices: list[int],
        frames: list[float],
        offsets: list[float],
    ) -> bool:
        raise NotImplementedError("Subclasses must implement insert_keyframes().")


    def ensure_animation_action(
        self,
        target_obj: bpy.types.Object,
        pose_bone: bpy.types.PoseBone | None = None,
    ) -> bpy.types.Action:
        if target_obj.animation_data is None:
            target_obj.animation_data_create()

        if target_obj.animation_data.action is None:
            action_name = (
                f"{target_obj.name}_{pose_bone.name}_IdleAction"
                if pose_bone is not None
                else f"{target_obj.name}_IdleAction"
            )
            target_obj.animation_data.action = bpy.data.actions.new(name=action_name)

        return target_obj.animation_data.action


    def resolve_animation_target(
        self,
        target_obj: bpy.types.Object,
        pose_bone: bpy.types.PoseBone | None = None,
    ) -> tuple[bpy.types.Object | bpy.types.PoseBone, str]:
        raise NotImplementedError("Subclasses must implement resolve_animation_target().")


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
            modifier.mode_before = "REPEAT"
            modifier.mode_after = "REPEAT"
            modifier.cycles_after = repeat_count


    # --- MAIN FUNCTION ---
    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene

        # Step 1: Resolve the selected object or pose bone.
        target_obj, pose_bone = self.resolve_target(context)
        if target_obj is None:
            return {"CANCELLED"}

        # Step 2: Resolve the axes affected by the selected projection plane.
        axis_effect = self.resolve_axis_effect(context)
        if axis_effect is None:
            return {"CANCELLED"}
        axis_indices = self.resolve_axis_indices(axis_effect)
        if axis_indices is None:
            return {"CANCELLED"}

        # Step 3: Calculate the keyframe times and animation offsets.
        frames, offsets = self.resolve_frames(context)
        if frames is None or offsets is None:
            return {"CANCELLED"}

        # Step 4: Resolve the animated property and its F-Curve data path.
        animated_target, data_path = self.resolve_animation_target(target_obj, pose_bone)

        # Step 5: Ensure the object has an action to store the keyframes.
        self.ensure_animation_action(target_obj, pose_bone)

        # Step 6: Insert keyframes for each affected axis.
        if not self.insert_keyframes(
            animated_target,
            axis_indices,
            frames,
            offsets,
        ):
            return {"CANCELLED"}

        # Step 7: Find the F-Curves created for the animated axes.
        target_fcurves = self.find_fcurves(target_obj, data_path, axis_indices)
        if len(target_fcurves) != len(axis_indices):
            self.report({"ERROR"}, "Could not find the generated animation curves.")
            return {"CANCELLED"}

        # Step 8: Apply interpolation and easing to the generated keyframes.
        self.apply_interpolation(context, target_fcurves, frames)

        # Step 9: Add cycle modifiers when looping is enabled.
        if self.get_loop(context):
            self.apply_cycles_modifier(context, target_fcurves)

        self.report(
            {"INFO"},
            f"Generated animation for {target_obj.name}"
            + (f" > {pose_bone.name}." if pose_bone is not None else "."),
        )
        return {"FINISHED"}