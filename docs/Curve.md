# Create Curve

The **Create Curve** tool generates a flat, filled mesh stroke along a circular
arc. The result is a mesh object, not a Blender Curve object.

## Open the tool

In the 3D Viewport, open the **N-panel** and select the **2D Toolkit** tab.
Expand **Create Curve** to configure the stroke.

## Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| Plane | XY | Plane on which the mesh is generated: XY, XZ, or YZ. |
| Radius | 1.0 | Radius of the arc path, in Blender units. |
| Thickness | 0.1 | Width of the planar stroke, in Blender units. |
| Arc Angle | 360° | Sweep from the positive X direction in the selected plane. Values range from 1° to 360°. |
| Resolution | 32 | Segment count for a full 360° sweep. Partial arcs use a proportional count, with at least 4 segments. |
| Cap Type | Round | Endpoint style for arcs shorter than 360°: **Flat** or **Round**. |
| Cap Resolution | 16 | Segment count used to approximate each round cap. This only affects round caps. |

Radius and thickness accept values from 0.000001 to 100 and 0.000001 to 10,
respectively. Resolution and cap resolution range from 4 to 128 and 8 to 128.

## Generate a stroke

1. Choose a projection plane and set the radius, thickness, and arc angle.
2. Set the curve resolution to control the smoothness of the arc. Increase cap
   resolution as well if using round caps and you want smoother endpoints.
3. Choose **Flat** or **Round** caps for an open arc.
4. Click **Generate Curve**.

The stroke starts along the positive X axis and sweeps counter-clockwise in the
selected plane. The mesh is centered around the origin, linked to the active
collection, and selected as the active object after generation.

At 360°, the stroke forms a closed ring and no endpoint caps are created,
regardless of the cap setting. When the radius is very small relative to the
thickness, the inner edge is clamped near the center, so the resulting width may
be less than the requested thickness.
