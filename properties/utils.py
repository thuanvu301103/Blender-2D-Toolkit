import bpy


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
