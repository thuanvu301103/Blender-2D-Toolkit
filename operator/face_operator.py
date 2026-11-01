import bpy
from .utils import create_2d_capsule, translate_object_on_plane, rotate_object_on_plane
from ..const.face_const import (
    DEFAULT_FACE_EYE_BROW_LENGTH,
    DEFAULT_FACE_EYE_BROW_WIDTH,
    DEFAULT_FACE_EYE_LENGTH,
    DEFAULT_FACE_EYE_WIDTH,
    DEFAULT_FACE_NOSE_LENGTH,
    DEFAULT_FACE_NOSE_WIDTH,
    DEFAULT_FACE_MOUTH_LENGTH,
    DEFAULT_FACE_MOUTH_WIDTH,
    LEFT_EYE_BROW_POS,
    RIGHT_EYE_BROW_POS,
    LEFT_EYE_POS,
    RIGHT_EYE_POS,
    NOSE_POS,
    MOUTH_POS
)

class OT_FACE_create_custom_face(bpy.types.Operator):
    
    bl_idname = "object.create_custom_face"
    bl_label = "Generate 2D human face"
    bl_options = {"REGISTER", "UNDO"}
    plane: str = None
    root_collection_name = "Custom2DFace"
    root_collection: bpy.types.Collection = None
        

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene

        # Retrieve parameters from scene properties
        self.plane = scene.face_plane

        # Create root collection
        self.root_collection = bpy.data.collections.new(self.root_collection_name)
        bpy.context.scene.collection.children.link(self.root_collection)

        # Create Eye brow
        self.gen_eye_brow()

        # Create Eye
        self.gen_eye()

        # Create Nose
        self.gen_nose()

        # Create Mouth
        self.gen_mouth()

        return {"FINISHED"}


    def gen_eye_brow (self):
        collection_name = f"{self.root_collection_name}_EyeBrow"
        new_collection = bpy.data.collections.new(collection_name)

        left_eye_brow = create_2d_capsule(self.plane, DEFAULT_FACE_EYE_BROW_LENGTH, DEFAULT_FACE_EYE_BROW_WIDTH)
        left_eye_brow.name = f"{self.root_collection_name}_LeftEyeBrow"
        right_eye_brow = create_2d_capsule(self.plane, DEFAULT_FACE_EYE_BROW_LENGTH, DEFAULT_FACE_EYE_BROW_WIDTH)
        right_eye_brow.name = f"{self.root_collection_name}_RightEyeBrow"

        translate_object_on_plane(left_eye_brow, self.plane, LEFT_EYE_BROW_POS[0], LEFT_EYE_BROW_POS[1])
        translate_object_on_plane(right_eye_brow, self.plane, RIGHT_EYE_BROW_POS[0], RIGHT_EYE_BROW_POS[1])

        new_collection.objects.link(left_eye_brow)
        new_collection.objects.link(right_eye_brow)

        self.root_collection.children.link(new_collection)


    def gen_eye (self):
        collection_name = f"{self.root_collection_name}_Eye"
        new_collection = bpy.data.collections.new(collection_name)

        left_eye = create_2d_capsule(self.plane, DEFAULT_FACE_EYE_LENGTH, DEFAULT_FACE_EYE_WIDTH)
        left_eye.name = f"{self.root_collection_name}_LeftEye"
        right_eye = create_2d_capsule(self.plane, DEFAULT_FACE_EYE_LENGTH, DEFAULT_FACE_EYE_WIDTH)
        right_eye.name = f"{self.root_collection_name}_RightEye"

        translate_object_on_plane(left_eye, self.plane, LEFT_EYE_POS[0], LEFT_EYE_POS[1])
        rotate_object_on_plane(left_eye, self.plane, 90.0)
        translate_object_on_plane(right_eye, self.plane, RIGHT_EYE_POS[0], RIGHT_EYE_POS[1])
        rotate_object_on_plane(right_eye, self.plane, 90.0)

        new_collection.objects.link(left_eye)
        new_collection.objects.link(right_eye)

        self.root_collection.children.link(new_collection)


    def gen_nose (self):
        collection_name = f"{self.root_collection_name}_Nose"
        new_collection = bpy.data.collections.new(collection_name)

        nose = create_2d_capsule(self.plane, DEFAULT_FACE_NOSE_LENGTH, DEFAULT_FACE_NOSE_WIDTH)
        nose.name = f"{self.root_collection_name}_Nose"

        translate_object_on_plane(nose, self.plane, NOSE_POS[0], NOSE_POS[1])
        rotate_object_on_plane(nose, self.plane, 90.0)

        new_collection.objects.link(nose)

        self.root_collection.children.link(new_collection)


    def gen_mouth (self):
        collection_name = f"{self.root_collection_name}_Mouth"
        new_collection = bpy.data.collections.new(collection_name)

        mouth = create_2d_capsule(self.plane, DEFAULT_FACE_MOUTH_LENGTH, DEFAULT_FACE_MOUTH_WIDTH)
        mouth.name = f"{self.root_collection_name}_Mouth"

        translate_object_on_plane(mouth, self.plane, MOUTH_POS[0], MOUTH_POS[1])

        new_collection.objects.link(mouth)

        self.root_collection.children.link(new_collection)