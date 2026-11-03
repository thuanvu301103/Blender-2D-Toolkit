# Idle Loop Animation — Waving

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

## Generate a waving cycle

1. Select the object or pose bone in **Target**. Eligible objects are Mesh, Curve, and Armature; for an armature, its pose bones are also listed.
2. Choose a **Plane**, then set the **Rotation Angle** and **Cycle Duration**.
3. Choose an **Interpolation** mode. For Sine, Quadratic, or Cubic, choose the desired **Easing** direction.
4. Put the current frame at the desired cycle start.
5. Click **Generate Waving Animation**.

The add-on inserts five rotation keyframes at 0%, 25%, 50%, 75%, and 100% of the cycle duration. Their offsets from the starting rotation are 0, the chosen angle, 0, the negative chosen angle, and 0. The keys are written to the target object's active Action; for a pose bone, they animate that bone's rotation channel. If no Action exists, the tool creates one. The selected rotation axis is switched to an Euler mode if it was previously set to a non-Euler mode.

## Reset settings

Use the refresh button beside **Waving Parameters** to restore the default Plane, Rotation Angle, Cycle Duration, Interpolation, and Easing values. It does not change the selected Target.

## Notes and limitations

- The tool creates one cycle of keyframes; it does not set the Action to repeat automatically. Configure repetition separately in Blender if a continuous loop is needed.
- Generating again at overlapping frames writes keyframes on the same rotation channel and may replace or affect existing animation at those frames.
- A target must still exist in the scene when generation runs. If no valid target is selected or found, the operator cancels and reports an error.
- The **Easing** setting only affects the Sine, Quadratic, and Cubic interpolation modes; it is not used for Bezier or Linear.
