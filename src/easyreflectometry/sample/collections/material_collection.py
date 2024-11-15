__author__ = 'github.com/arm61'
from typing import Optional
from typing import Tuple

from ..elements.materials.material import Material
from .base_collection import BaseCollection


# Needs to be a function, elements are added to the global_object.map
def DEFAULT_ELEMENTS(interface):
    return (
        Material(sld=0.0, isld=0.0, name='Air', interface=interface),
        Material(sld=6.335, isld=0.0, name='D2O', interface=interface),
        Material(sld=2.074, isld=0.0, name='Si', interface=interface),
    )


class MaterialCollection(BaseCollection):
    def __init__(
        self,
        *materials: Tuple[Material],
        name: str = 'EasyMaterials',
        interface=None,
        unique_name: Optional[str] = None,
        populate_if_none: bool = True,
        **kwargs,
    ):
        if not materials:  # Empty tuple if no materials are provided
            if populate_if_none:
                materials = DEFAULT_ELEMENTS(interface)
            else:
                materials = []

        super().__init__(
            name,
            interface,
            unique_name=unique_name,
            *materials,
            **kwargs,
        )

    def add_material(self, material: Optional[Material] = None):
        """Add a material to the collection.

        :param material: Material to add.
        """
        if material is None:
            material = Material(sld=0.0, isld=0.0, name='Material added')
        material.interface = self.interface
        self.append(material)

    def duplicate_material(self, index: int):
        """Duplicate a material in the collection.

        :param material: Assembly to add.
        """
        to_be_duplicated = self[index]
        duplicate = Material.from_dict(to_be_duplicated.as_dict(skip=['unique_name']))
        duplicate.name = duplicate.name + ' duplicate'
        self.append(duplicate)
