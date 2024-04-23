__author__ = 'github.com/arm61'
from typing import Optional

from ...base_element_collection import SIZE_DEFAULT_COLLECTION
from ...base_element_collection import BaseElementCollection
from .material import Material
from .material_mixture import MaterialMixture


class MaterialCollection(BaseElementCollection):
    # Added in super().__init__
    matertials: list[Material | MaterialMixture]

    def __init__(
        self,
        *materials: Optional[list[Material | MaterialMixture]],
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
