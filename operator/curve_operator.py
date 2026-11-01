import math
import bpy
import bmesh
from mathutils import Vector
from ..const import (
    MIN_RADIUS,
    MIN_RESOLUTION

)

class OT_CURVE_create_custom_curve(bpy.types.Operator):
    """Operator to generate a 2D flat stroke mesh with flat or round terminal caps."""

    bl_idname = "object.create_custom_curve"
    bl_label = "Generate 2D Stroke"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene

        # Retrieve parameters from scene properties
        plane = scene.curve_plane
        radius = scene.curve_radius
        thickness = scene.curve_thickness
        arc_angle_deg = scene.curve_arc_angle
        resolution = scene.curve_resolution
        cap_type = scene.curve_cap_type
        cap_resolution = scene.curve_cap_resolution

        # Convert arc angle from degrees to radians
        arc_angle_rad = math.radians(arc_angle_deg)

        # Calculate radii for inner and outer boundaries
        half_thickness = thickness * 0.5
        r_inner = max(MIN_RADIUS, radius - half_thickness)
        r_outer = radius + half_thickness
        mean_radius = (r_inner + r_outer) * 0.5

        # Initialize BMesh instance for procedural geometry construction
        bm = bmesh.new()

        # Calculate segment count proportional to arc angle resolution
        segments = max(MIN_RESOLUTION, int(resolution * (arc_angle_rad / (2 * math.pi))))

        inner_verts = []
        outer_verts = []

        # Generate inner and outer boundary vertices along the arc path
        for i in range(segments + 1):
            fraction = i / segments if segments > 0 else 0.0
            current_angle = fraction * arc_angle_rad

            cos_a = math.cos(current_angle)
            sin_a = math.sin(current_angle)

            pos_inner = Vector((r_inner * cos_a, r_inner * sin_a, 0.0))
            pos_outer = Vector((r_outer * cos_a, r_outer * sin_a, 0.0))

            inner_verts.append(bm.verts.new(pos_inner))
            outer_verts.append(bm.verts.new(pos_outer))

        bm.verts.ensure_lookup_table()

        # Construct quad strip faces along the main arc body
        for i in range(segments):
            v0 = inner_verts[i]
            v1 = outer_verts[i]
            v2 = outer_verts[i + 1]
            v3 = inner_verts[i + 1]
            bm.faces.new((v0, v1, v2, v3))

        # Handle terminal caps based on user selection (flat or round)
        if cap_type == "ROUND" and arc_angle_rad < 2 * math.pi:

            # --- Start Round Cap ---
            # Calculate start cap center position and create vertex
            start_center_pos = Vector((mean_radius * math.cos(0.0), mean_radius * math.sin(0.0), 0.0))
            start_center_vert = bm.verts.new(start_center_pos)

            # Create vertices for the start cap by sweeping from inner to outer edge
            start_cap_verts = [inner_verts[0]]
            for c in range(cap_resolution - 1, 0, -1):
                cap_frac = c / cap_resolution
                cap_angle = math.pi * 0.5 - cap_frac * math.pi
                # Base orientation for start cap points along negative X direction (-pi)
                cx = start_center_pos.x + half_thickness * math.sin(cap_angle)
                cy = start_center_pos.y - half_thickness * math.cos(cap_angle)
                start_cap_verts.append(bm.verts.new(Vector((cx, cy, 0.0))))
            start_cap_verts.append(outer_verts[0])

            bm.verts.ensure_lookup_table()
            for c in range(len(start_cap_verts) - 1):
                bm.faces.new((start_center_vert, start_cap_verts[c], start_cap_verts[c + 1]))

            # --- End Round Cap ---
            end_angle_base = arc_angle_rad
            end_center_pos = Vector((mean_radius * math.cos(end_angle_base), mean_radius * math.sin(end_angle_base), 0.0))
            end_center_vert = bm.verts.new(end_center_pos)

            end_cap_verts = [outer_verts[-1]]
            for c in range(1, cap_resolution):
                cap_frac = c / cap_resolution
                cap_angle = cap_frac * math.pi
                # Calculate local offset rotated by end_angle_base. Cap sweeps outwards along the forward tangent direction
                local_x = half_thickness * math.sin(cap_angle)
                local_y = half_thickness * math.cos(cap_angle)
                
                # Apply 2D rotation matrix for end_angle_base
                cx = end_center_pos.x + (-local_x * math.sin(end_angle_base) + local_y * math.cos(end_angle_base))
                cy = end_center_pos.y + (local_x * math.cos(end_angle_base) + local_y * math.sin(end_angle_base))
                end_cap_verts.append(bm.verts.new(Vector((cx, cy, 0.0))))
            end_cap_verts.append(inner_verts[-1])

            bm.verts.ensure_lookup_table()
            for c in range(len(end_cap_verts) - 1):
                bm.faces.new((end_center_vert, end_cap_verts[c], end_cap_verts[c + 1]))

        # Transform vertex coordinates according to the selected projection plane
        for v in bm.verts:
            x, y, z = v.co.x, v.co.y, v.co.z
            if plane == "XY":
                v.co = Vector((x, y, 0.0))
            elif plane == "XZ":
                v.co = Vector((x, 0.0, y))
            elif plane == "YZ":
                v.co = Vector((0.0, x, y))
            else:
                v.co = Vector((x, y, 0.0))

        # Create mesh data block from BMesh instance
        mesh_data = bpy.data.meshes.new("Custom2DStrokeData")
        bm.to_mesh(mesh_data)
        bm.free()

        # Instantiate mesh object and link to active collection
        mesh_obj = bpy.data.objects.new("Custom2DStroke", mesh_data)
        context.collection.objects.link(mesh_obj)

        # Update viewport selection state
        context.view_layer.objects.active = mesh_obj
        mesh_obj.select_set(True)

        self.report(
            {"INFO"},
            f"2D flat stroke generated successfully on plane {plane} with {cap_type.lower()} caps.",
        )
        return {"FINISHED"}