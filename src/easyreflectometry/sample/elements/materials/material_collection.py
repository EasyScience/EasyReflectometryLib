__author__ = 'github.com/arm61'
from typing import Tuple
from typing import Union

from ...base_element_collection import SIZE_DEFAULT_COLLECTION
from ...base_element_collection import BaseElementCollection
from .material import Material
from .material_mixture import MaterialMixture


class MaterialCollection(BaseElementCollection):
    # Added in super().__init__
    matertials: list[Union[Material, MaterialMixture]]

    def __init__(
        self,
        *materials: Tuple[Union[Material, MaterialMixture]],
        name: str = 'EasyMaterials',
        interface=None,
        populate_if_none: bool = True,
        **kwargs,
    ):
        if not materials:  # Empty tuple if no materials are provided
            if populate_if_none:
                materials = [Material(interface=interface) for _ in range(SIZE_DEFAULT_COLLECTION)]
            else:
                materials = []
        # Needed to ensure an empty list is created when saving and instatiating the object as_dict -> from_dict
        # Else collisions might occur in global_object.map
        self.populate_if_none = False

        super().__init__(
            name,
            interface,
            *materials,
            **kwargs,
        )
