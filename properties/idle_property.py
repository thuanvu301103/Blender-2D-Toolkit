from .idle_sub_property.idle_waving_property import register_idle_waving_properties, unregister_idle_waving_properties
from .idle_sub_property.idle_sliding_property import register_idle_sliding_properties, unregister_idle_sliding_properties


def register_idle_properties() -> None:

    register_idle_waving_properties()
    register_idle_sliding_properties()


def unregister_idle_properties() -> None:

    unregister_idle_waving_properties()
    unregister_idle_sliding_properties()
