# Create Face

The **Create Face** tool generates a simple 2D face from separate, filled capsule-shaped mesh objects: two eyebrows, two eyes, a nose, and a mouth. The feature exposes a projection-plane setting; the component sizes and positions are built in.

## Open the tool

In the 3D Viewport, open the **N-panel**, select the **2D Toolkit** tab, and expand **Create Face**.

## Parameter

| Parameter | Default | Description |
| --- | --- | --- |
| Plane | XY Plane | Plane on which the face is generated: XY, XZ, or YZ. |

## Generate a face

1. Choose **XY Plane**, **XZ Plane**, or **YZ Plane** from **Plane**.
2. Click **Generate Face**.

The add-on adds a **Custom2DFace** collection to the scene. It contains separate child collections for **EyeBrow**, **Eye**, **Nose**, and **Mouth**, with the individual parts stored in those collections. Each part is a filled mesh object.

## Built-in layout

The following dimensions and positions are fixed by the tool. Dimensions and coordinates are in Blender units, measured in the two-dimensional coordinates of the selected plane.

| Part | Length | Width | Position (u, v) |
| --- | ---: | ---: | ---: |
| Left eyebrow | 1.5 | 0.5 | (-1.0, 1.6) |
| Right eyebrow | 1.5 | 0.5 | (1.0, 1.6) |
| Left eye | 0.8 | 0.6 | (-1.0, 0.8) |
| Right eye | 0.8 | 0.6 | (1.0, 0.8) |
| Nose | 1.1 | 0.5 | (0.0, 0.3) |
| Mouth | 1.3 | 0.4 | (0.0, -0.7) |

The parts are positioned relative to the plane origin. Choosing another plane changes their orientation, not their layout or proportions. The generated parts use capsule-shaped outlines; if a configured length is smaller than its width, the mesh utility expands the effective length to match the width.

## Notes

- The tool creates a new face collection each time **Generate Face** is clicked. If a collection with the same name already exists, Blender assigns a unique suffix to the new collection.
- The tool does not expose controls for changing individual feature sizes, spacing, or shape from the panel; adjust the generated objects after creation if needed.
