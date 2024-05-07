__author__ = 'github.com/arm61'
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
        *materials: Union[list[Union[Material, MaterialMixture]], None],
        name: str = 'EasyMaterials',
        interface=None,
        **kwargs,
    ):
        if not materials:
            materials = [Material(interface=interface) for _ in range(SIZE_DEFAULT_COLLECTION)]
        super().__init__(
            name,
            interface,
            *materials,
            **kwargs,
        )
