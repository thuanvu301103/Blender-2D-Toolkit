import bpy
import bmesh
from mathutils import Vector
import math

def create_2d_capsule(plan: str, length: float, width: float, resolution: int = 16) -> bpy.types.Object:
    """
    Generates a 2D capsule mesh on the specified orientation plane with defined length and width.
    
    Args:
        plan (str): Target projection plane identifier ('XY', 'XZ', or 'YZ').
        length (float): Total length of the capsule along the primary longitudinal axis.
        width (float): Total width (diameter) of the capsule.
        resolution (int): Segment resolution for the semicircular extremities.
        
    Returns:
        bpy.types.Object: The instantiated Blender mesh object.
    """
    # Enforce geometric constraint where length must be greater than or equal to width
    if length < width:
        length = width
        
    radius = width / 2.0
    rect_length = length - width
    half_rect_len = rect_length / 2.0
    
    # Initialize BMesh container and mesh data block
    bm = bmesh.new()
    mesh_data = bpy.data.meshes.new("Capsule_2D_Data")
    obj = bpy.data.objects.new("Capsule_2D", mesh_data)
    
    verts = []
    
    # Map 2D local coordinates (u, v) into 3D Cartesian coordinates based on the selected plane
    def map_coordinates(u: float, v: float) -> tuple[float, float, float]:
        if plan == "XZ":
            return (u, 0.0, v)
        elif plan == "YZ":
            return (0.0, u, v)
        else:  # Default configuration for XY plane
            return (u, v, 0.0)

    # Generate vertices for the right semicircular cap
    for i in range(resolution + 1):
        theta = -math.pi / 2.0 + (i / resolution) * math.pi
        u = half_rect_len + radius * math.cos(theta)
        v = radius * math.sin(theta)
        verts.append(bm.verts.new(map_coordinates(u, v)))
        
    # Generate vertices for the left semicircular cap
    for i in range(resolution + 1):
        theta = math.pi / 2.0 + (i / resolution) * math.pi
        u = -half_rect_len + radius * math.cos(theta)
        v = radius * math.sin(theta)
        verts.append(bm.verts.new(map_coordinates(u, v)))
        
    bm.verts.ensure_lookup_table()
    
    # Construct a single face bounded by the generated vertex loop
    bm.faces.new(verts)
    
    # Transfer BMesh topology to the Blender mesh data structure
    bm.to_mesh(mesh_data)
    bm.free()
    
    return obj


def translate_object_on_plane(obj: bpy.types.Object, plan: str, delta_x: float, delta_y: float) -> None:
    """
    Translates a Blender object along a specified 2D projection plane using local delta coordinates.
    
    Args:
        obj (bpy.types.Object): The target Blender object to be translated.
        plan (str): Target projection plane identifier ('XY', 'XZ', or 'YZ').
        delta_x (float): Displacement along the primary local axis of the plane.
        delta_y (float): Displacement along the secondary local axis of the plane.
    """
    # Map 2D displacement components (delta_x, delta_y) to 3D Cartesian translation vectors
    if plan == "XZ":
        translation_vector = Vector((delta_x, 0.0, delta_y))
    elif plan == "YZ":
        translation_vector = Vector((0.0, delta_x, delta_y))
    else:  # Default configuration for XY plane
        translation_vector = Vector((delta_x, delta_y, 0.0))
        
    # Apply the translation vector to the object's global location
    obj.location += translation_vector


def rotate_object_on_plane(obj: bpy.types.Object, plan: str, degrees: float) -> None:
    """
    Rotates a Blender object around the normal axis corresponding to the specified 2D projection plane by a given angle in degrees.
    
    Args:
        obj (bpy.types.Object): The target Blender object to be rotated.
        plan (str): Target projection plane identifier ('XY', 'XZ', or 'YZ').
        degrees (float): Rotation angle measured in degrees.
    """
    # Convert the rotation angle from degrees to radians required by Blender Euler rotation
    radians = math.radians(degrees)
    
    # Apply rotation around the orthogonal axis corresponding to the selected plane
    if plan == "XZ":
        obj.rotation_euler.y += radians
    elif plan == "YZ":
        obj.rotation_euler.x += radians
    else:  # Default configuration for XY plane
        obj.rotation_euler.z += radians