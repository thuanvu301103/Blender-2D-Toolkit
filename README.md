# Blender-2D-Toolkit

## Project overview

**Blender 2D Toolkit** is a Blender add-on for creating simple 2D-style geometry and single-cycle idle animations from the 3D Viewport. Its goal is to make common 2D shapes and basic back-and-forth motion quick to generate, while keeping the resulting geometry and animation editable as regular Blender objects, collections, and keyframes.

The add-on currently includes:

- **Create Curve** — generates a flat mesh stroke along a circular arc, with controls for its plane, radius, thickness, sweep, resolution, and end caps. See [docs/Curve.md](docs/Curve.md).
- **Create Face** — assembles a simple face from separate capsule-shaped mesh parts on a selected plane. See [docs/Face.md](docs/Face.md).
- **Idle Loop Animation** — creates back-and-forth **Waving** rotation and **Sliding** translation keyframes for supported objects or armature pose bones. See [docs/Idle Animation.md](docs/Idle%20Animation.md).

The panels are available in the 3D Viewport's **N-panel**, under the **2D Toolkit** tab. The add-on metadata declares Blender 4.0 as its minimum supported version.

## Project structure

```text
Blender-2D-Toolkit/
├── __init__.py                 # Add-on metadata, class registration, and entry point
├── README.md                   # Project overview and structure
├── consts/                     # Shared defaults, limits, and enum options
│   ├── __init__.py
│   ├── curve_const.py          # Curve generation constants
│   ├── face_const.py           # Face component dimensions and positions
│   ├── idle_const.py           # Waving and sliding animation constants
│   ├── plane_const.py          # 2D projection planes
│   └── utils.py                # Shared geometry utility constants
├── docs/                       # User guides for the available tools
│   ├── Curve.md
│   ├── Face.md
│   └── Idle Animation.md
├── operators/                  # Blender actions that create geometry or animation
│   ├── __init__.py
│   ├── curve_operator.py
│   ├── face_operator.py
│   ├── idle_sliding_operator.py
│   ├── idle_waving_operator.py
│   └── utils.py                # Shared mesh and plane transformation helpers
├── panels/                     # 3D Viewport N-panel user interface
│   ├── __init__.py
│   ├── curve_panel.py
│   ├── face_panel.py
│   ├── idle_panel.py
│   ├── main.py
│   └── idle_sub_pannel/        # Waving and Sliding sub-panels
│       ├── __init__.py
│       ├── idle_sliding_panel.py
│       └── idle_waving_panel.py
└── properties/                 # Scene settings exposed by the panels
    ├── __init__.py
    ├── main.py
    ├── curve_property.py
    ├── face_property.py
    ├── idle_property.py
    ├── utils.py                # Shared property helpers (e.g. animation target list)
    └── idle_sub_property/      # Waving and Sliding settings
        ├── idle_sliding_property.py
        └── idle_waving_property.py
```

### Main code areas

- **Operators** implement the actions invoked by the UI, such as creating meshes and inserting animation keyframes.
- **Panels** define where controls appear in Blender.
- **Properties** register the settings stored on the current Scene.
- **Consts** hold shared option lists and default or limit values, keeping the UI and operators consistent.
- **Docs** contain user-facing instructions for the tools.