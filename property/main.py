import bpy
from .curve_property import register_curve_properties, unregister_curve_properties  

def register_properties() -> None:
    register_curve_properties()


def unregister_properties() -> None:
    unregister_curve_properties()