import bpy
from .curve_property import register_curve_properties, unregister_curve_properties  
from .face_property import register_face_properties, unregister_face_properties

def register_properties() -> None:
    register_curve_properties()
    register_face_properties()


def unregister_properties() -> None:
    unregister_curve_properties()
    unregister_face_properties()