import bpy
from ...consts.idle_const import (
    DEFAULT_IDLE_WAVING_ANGLE,
    MIN_IDLE_WAVING_ANGLE,
    MAX_IDLE_WAVING_ANGLE,
    DEFAULT_IDLE_WAVING_DURATION,
    MIN_IDLE_WAVING_DURATION,
    MAX_IDLE_WAVING_DURATION,
    IDLE_WAVING_DURATION_PRECISION,
)
from ...consts.plane_const import DEFAULT_PLANE_2D, PLANE_2D

def get_applicable_targets(self, context) -> list[tuple]:
    """
    Collect valid scene-level entities and component-level pose bones 
    with designated icon identifiers for each dropdown menu option.
    """
    items = []
    index_counter = 0
    
    for obj in context.scene.objects:
        if obj.type in {'MESH', 'CURVE', 'ARMATURE'}:
            obj_identifier = f"OBJ_{obj.name}"
            
            # Resolve specific icon identifier based on object type
            if obj.type == 'ARMATURE':
                icon_name = "ARMATURE_DATA"
            elif obj.type == 'CURVE':
                icon_name = "CURVE_DATA"
            else:
                icon_name = "OBJECT_DATA"
            
            items.append((
                obj_identifier, 
                obj.name, 
                f"Apply transformation to object: {obj.name}", 
                icon_name, 
                index_counter
            ))
            index_counter += 1
            
            if obj.type == 'ARMATURE':
                for bone in obj.pose.bones:
                    bone_identifier = f"BONE_{obj.name}_{bone.name}"
                    bone_label = f"{obj.name} > {bone.name}"
                    items.append((
                        bone_identifier, 
                        bone_label, 
                        f"Apply transformation to bone: {bone.name}", 
                        "BONE_DATA", 
                        index_counter
                    ))
                    index_counter += 1
                    
    if not items:
        items.append((
            "NONE", 
            "None Available", 
            "No valid object or bone targets detected", 
            "QUESTION", 
            0
        ))
        
    return items


def register_idle_waving_properties() -> None:

    bpy.types.Scene.idle_waving_target = bpy.props.EnumProperty(
        name="Animation Target",
        description="Select the object or armature to apply waving and rotation animation",
        items=get_applicable_targets
    )

    bpy.types.Scene.idle_waving_plane = bpy.props.EnumProperty(
        name="Projection Plane",
        description="Select spatial orientation plane",
        items=PLANE_2D,
        default=DEFAULT_PLANE_2D,
    )

    bpy.types.Scene.idle_waving_angle = bpy.props.FloatProperty(
        name="Rotation Angle",
        description="Maximum angular displacement amplitude for the oscillatory rotation",
        default=DEFAULT_IDLE_WAVING_ANGLE,
        min=MIN_IDLE_WAVING_ANGLE,
        max=MAX_IDLE_WAVING_ANGLE
    )

    # Property for complete animation cycle duration (measured in seconds)
    bpy.types.Scene.idle_waving_duration = bpy.props.FloatProperty(
        name="Cycle Duration",
        description="Time duration required to complete a single oscillation cycle",
        default=DEFAULT_IDLE_WAVING_DURATION,
        min=MIN_IDLE_WAVING_DURATION,
        max=MAX_IDLE_WAVING_DURATION,
        precision=IDLE_WAVING_DURATION_PRECISION
    )


def unregister_idle_waving_properties() -> None:

    del bpy.types.Scene.idle_waving_target
    del bpy.types.Scene.idle_waving_plane
    del bpy.types.Scene.idle_waving_angle
    del bpy.types.Scene.idle_waving_duration