import bpy

# Operator Definition
class OBJECT_OT_create_2d_outline(bpy.types.Operator):
    """Generates an extruded outline for 2D mesh objects along boundary vertices."""

    bl_idname = "mesh.create_2d_outline"
    bl_label = "Generate Outline"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def execute(self, context: bpy.types.Context) -> dict:
        scene = context.scene
        thickness = scene.outline_thickness
        plane = scene.outline_projection_plane
        obj = context.active_object

        # Invoke core outline generation logic
        success = self._generate_outline(obj, thickness, plane)

        if not success:
            self.report({"WARNING"}, "No boundary edges found to generate outline.")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Outline successfully generated with thickness {thickness}.")
        return {"FINISHED"}

    def _generate_outline(
        self, obj: bpy.types.Object, thickness: float, plane: str
    ) -> bool:
        """Core algorithm to calculate boundary offsets and build outline geometry."""
        import bmesh
        from mathutils import Vector

        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(obj.data)
        bm.normal_update()

        boundary_verts = [v for v in bm.verts if v.is_boundary]
        if not boundary_verts:
            bpy.ops.object.mode_set(mode="OBJECT")
            return False

        # Select projection coordinates based on chosen plane
        vert_directions = {}
        for v in boundary_verts:
            dir_vector = Vector((0.0, 0.0, 0.0))
            boundary_edges = [e for e in v.link_edges if e.is_boundary]

            for e in boundary_edges:
                face = e.link_faces[0]
                other_v = e.other_vert(v)

                if plane == "XY":
                    edge_vec = (other_v.co - v.co).xy
                    face_center = (face.calc_center_median() - v.co).xy
                elif plane == "XZ":
                    edge_vec = Vector(((other_v.co - v.co).x, (other_v.co - v.co).z))
                    face_center = Vector(
                        ((face.calc_center_median() - v.co).x, (face.calc_center_median() - v.co).z)
                    )
                else:  # YZ
                    edge_vec = Vector(((other_v.co - v.co).y, (other_v.co - v.co).z))
                    face_center = Vector(
                        ((face.calc_center_median() - v.co).y, (face.calc_center_median() - v.co).z)
                    )

                if edge_vec.length == 0:
                    continue

                perp = Vector((-edge_vec.y, edge_vec.x)).normalized()
                if perp.dot(face_center) > 0:
                    perp = -perp

                if plane == "XY":
                    dir_vector += Vector((perp.x, perp.y, 0.0))
                elif plane == "XZ":
                    dir_vector += Vector((perp.x, 0.0, perp.y))
                else:  # YZ
                    dir_vector += Vector((0.0, perp.x, perp.y))

            if dir_vector.length > 0:
                vert_directions[v] = dir_vector.normalized()

        # Duplicate geometry for outline generation
        out_bmesh = bmesh.ops.duplicate(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:])
        new_verts = [
            elem for elem in out_bmesh["geom"] if isinstance(elem, bmesh.types.BMVert)
        ]

        vert_map = dict(zip(bm.verts, new_verts))
        for orig_v, new_v in vert_map.items():
            if orig_v in vert_directions:
                new_v.co += vert_directions[orig_v] * thickness

        bmesh.update_edit_mesh(obj.data)
        bpy.ops.object.mode_set(mode="OBJECT")
        return True