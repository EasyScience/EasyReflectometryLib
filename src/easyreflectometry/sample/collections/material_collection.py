__author__ = 'github.com/arm61'
from typing import Optional
from typing import Tuple

from ..elements.materials.material import Material
from .base_element_collection import BaseElementCollection

DEFAULT_COLLECTION = (
    Material(sld=0.0, isld=0.0, name='Air'),
    Material(sld=6.335, isld=0.0, name='D2O'),
    Material(sld=2.074, isld=0.0, name='Si'),
)


class MaterialCollection(BaseElementCollection):
    def __init__(
        self,
        *materials: Tuple[Material],
        name: str = 'EasyMaterials',
        interface=None,
        populate_if_none: bool = True,
        **kwargs,
    ):
        if not materials:  # Empty tuple if no materials are provided
            if populate_if_none:
                materials = DEFAULT_COLLECTION  # (Material(interface=interface) for _ in range(SIZE_DEFAULT_COLLECTION))
            else:
                materials = ()
        # Needed to ensure an empty list is created when saving and instatiating the object as_dict -> from_dict
        # Else collisions might occur in global_object.map
        self.populate_if_none = False

        super().__init__(
            name,
            interface,
            *materials,
            **kwargs,
        )

    def add_material(self, material: Optional[Material] = None):
        """Add a material to the collection.

        :param material: Material to add.
        """
        if material is None:
            material = Material(name='New EasyMaterial', interface=self.interface)
        self.append(material)

    def duplicate_material(self, index: int):
        """Duplicate a material in the collection.

        :param material: Assembly to add.
        """
        to_be_duplicated = self[index]
        duplicate = Material.from_dict(to_be_duplicated.as_dict(skip=['unique_name']))
        duplicate.name = duplicate.name + ' duplicate'
        self.append(duplicate)

    def move_material_up(self, index: int):
        """Move the material at the given index up in the collection.

        :param index: Index of the material to move up.
        """
        if index == 0:
            return
        self.insert(index - 1, self.pop(index))

    def move_material_down(self, index: int):
        """Move the material at the given index down in the collection.

        :param index: Index of the material to move down.
        """
        if index == len(self) - 1:
            return
        self.insert(index + 1, self.pop(index))

    def remove_material(self, index: int):
        """Remove the material at the given index from the collection.

        :param index: Index of the material to remove.
        """
        self.pop(index)
