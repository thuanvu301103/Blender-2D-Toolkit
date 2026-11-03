# Idle Loop Animation

The **Idle Loop Animation** panel contains two tools: **Waving** (rotation) and **Sliding** (translation). Each generates a single cycle of keyframes starting at the current frame.

- [Waving](#waving)
- [Sliding](#sliding)

# Waving

The **Waving** tool creates one oscillation cycle by keyframing an object's or pose bone's Euler rotation. It inserts five keyframes on the rotation axis normal to the selected plane: the starting rotation, positive angle, starting rotation, negative angle, and starting rotation. The cycle begins at the current frame.

## Open the tool

In the 3D Viewport, open the **N-panel**, select the **2D Toolkit** tab, expand **Idle Loop Animation**, then expand **Waving**.

## Parameters

| Parameter | Default | Range / options | Description |
| --- | --- | --- | --- |
| Target | No fixed default | Mesh, Curve, or Armature objects; pose bones of Armatures | Object or armature pose bone to animate. The list is built from objects in the current scene. |
| Plane | XY | XY, XZ, YZ | Selects the rotation axis: Z for XY, Y for XZ, and X for YZ. |
| Rotation Angle | 1° | -360° to 360° | Maximum angular offset in each direction from the starting rotation. |
| Cycle Duration | 2 seconds | 0.01 to 60 seconds | Duration of the full cycle, converted to frames using the scene frame rate. |
| Interpolation | Bezier | Bezier, Linear, Sine, Quadratic, Cubic | Interpolation mode assigned to the generated keyframes. |
| Easing | Ease In Out | Automatic, Ease In, Ease Out, Ease In Out | Easing direction, applied when Interpolation is Sine, Quadratic, or Cubic. |
| Loop | Off | On / Off | Repeats the cycle after its last keyframe by adding a Cycles modifier to the generated F-curves. |
| Repeat Count | 0 | 0 to 10000 | Number of repetitions after the first cycle; 0 repeats forever. Only used when Loop is on. |

## Generate a waving cycle

1. Select the object or pose bone in **Target**. Eligible objects are Mesh, Curve, and Armature; for an armature, its pose bones are also listed.
2. Choose a **Plane**, then set the **Rotation Angle** and **Cycle Duration**.
3. Choose an **Interpolation** mode. For Sine, Quadratic, or Cubic, choose the desired **Easing** direction.
4. Put the current frame at the desired cycle start.
5. Click **Generate Waving Animation**.

The add-on inserts five rotation keyframes at 0%, 25%, 50%, 75%, and 100% of the cycle duration. Their offsets from the starting rotation are 0, the chosen angle, 0, the negative chosen angle, and 0. The keys are written to the target object's active Action; for a pose bone, they animate that bone's rotation channel. If no Action exists, the tool creates one. The selected rotation axis is switched to an Euler mode if it was previously set to a non-Euler mode.

## Reset settings

Use the refresh button beside **Waving Parameters** to restore the default Plane, Rotation Angle, Cycle Duration, Interpolation, Easing, Loop, and Repeat Count values. It does not change the selected Target.

## Notes and limitations

- The tool always creates one cycle of keyframes. Enable **Loop** to repeat it with a Cycles modifier; the modifier is only added when Loop is on, and turning Loop off later does not remove an existing modifier (delete it in the Graph Editor).
- Generating again at overlapping frames writes keyframes on the same rotation channel and may replace or affect existing animation at those frames.
- A target must still exist in the scene when generation runs. If no valid target is selected or found, the operator cancels and reports an error.
- The **Easing** setting only affects the Sine, Quadratic, and Cubic interpolation modes; it is not used for Bezier or Linear.

---

# Sliding

The **Sliding** tool creates one back-and-forth cycle by keyframing an object's or pose bone's location. It inserts five keyframes along a direction inside the selected plane: the starting location, a positive offset, the starting location, a negative offset, and the starting location. The cycle begins at the current frame.

## Open the tool

In the 3D Viewport, open the **N-panel**, select the **2D Toolkit** tab, expand **Idle Loop Animation**, then expand **Sliding**.

## Parameters

| Parameter | Default | Range / options | Description |
| --- | --- | --- | --- |
| Target | No fixed default | Mesh, Curve, or Armature objects; pose bones of Armatures | Object or armature pose bone to animate. The list is built from objects in the current scene. |
| Plane | XY | XY, XZ, YZ | Plane in which the target slides. |
| Direction Angle | 0° | -360° to 360° | Slide direction inside the plane, measured from the plane's first axis toward its second axis (X toward Y for XY, X toward Z for XZ, Y toward Z for YZ). |
| Slide Distance | 0.1 | -1000 to 1000 | Maximum offset in each direction from the starting location, in Blender units. |
| Cycle Duration | 2 seconds | 0.01 to 60 seconds | Duration of the full cycle, converted to frames using the scene frame rate. |
| Interpolation | Bezier | Bezier, Linear, Sine, Quadratic, Cubic | Interpolation mode assigned to the generated keyframes. |
| Easing | Ease In Out | Automatic, Ease In, Ease Out, Ease In Out | Easing direction, applied when Interpolation is Sine, Quadratic, or Cubic. |
| Loop | Off | On / Off | Repeats the cycle after its last keyframe by adding a Cycles modifier to the generated F-curves. |
| Repeat Count | 0 | 0 to 10000 | Number of repetitions after the first cycle; 0 repeats forever. Only used when Loop is on. |

## Generate a sliding cycle

1. Select the object or pose bone in **Target**.
2. Choose a **Plane**, then set the **Direction Angle**, **Slide Distance**, and **Cycle Duration**.
3. Choose an **Interpolation** mode. For Sine, Quadratic, or Cubic, choose the desired **Easing** direction.
4. Put the current frame at the desired cycle start.
5. Click **Generate Sliding Animation**.

The add-on inserts five location keyframes at 0%, 25%, 50%, 75%, and 100% of the cycle duration. Their offsets from the starting location are 0, the chosen distance, 0, the negative chosen distance, and 0, applied along the direction `(cos θ, sin θ)` in the selected plane, where θ is the Direction Angle. Both location axes of the plane are keyframed, so for angles that are multiples of 90° one of the two curves stays constant. The keys are written to the target object's active Action; for a pose bone, they animate that bone's location channels. If no Action exists, the tool creates one. After generation, the target's location is restored to its starting value.

## Reset settings

Use the refresh button beside **Sliding Parameters** to restore the default Plane, Direction Angle, Slide Distance, Cycle Duration, Interpolation, Easing, Loop, and Repeat Count values. It does not change the selected Target.

## Notes and limitations

- The tool always creates one cycle of keyframes. Enable **Loop** to repeat it with a Cycles modifier; the modifier is only added when Loop is on, and turning Loop off later does not remove an existing modifier (delete it in the Graph Editor).
- Generating again at overlapping frames writes keyframes on the same location channels and may replace or affect existing animation at those frames.
- For a pose bone, location is in the bone's local space, so the plane and direction are relative to the bone rather than the world.
- A target must still exist in the scene when generation runs. If no valid target is selected or found, the operator cancels and reports an error.
- The **Easing** setting only affects the Sine, Quadratic, and Cubic interpolation modes; it is not used for Bezier or Linear.
