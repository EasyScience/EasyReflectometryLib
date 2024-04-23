from __future__ import annotations

__author__ = 'github.com/arm61'

from ..base_element_collection import BaseElementCollection
from .material import Material
from .material_mixture import MaterialMixture

DEFAULT_MATERIALS = (Material(), Material())


class MaterialCollection(BaseElementCollection):
    def __init__(
        self,
        *materials: tuple[Material | MaterialMixture],
        name: str = 'EasyMaterials',
        interface=None,
        **kwargs,
    ):
        if not materials:
            materials = DEFAULT_MATERIALS
        super().__init__(
            name,
            interface,
            *materials,
            **kwargs,
        )

    # # Class methods for instance creation
    # @classmethod
    # def default(cls, interface=None) -> MaterialCollection:
    #     """
    #     Default constructor for materials.

    #     :return: Default materials container
    #     :rtype: Materials
    #     """
    #     material1 = Material()
    #     material2 = Material()
    #     return cls(material1, material2, interface=interface)

    # @classmethod
    # def from_pars(
    #     cls,
    #     *materials: tuple[Material | MaterialMixture],
    #     name: str = 'EasyMaterials',
    #     interface=None,
    # ) -> MaterialCollection:
    #     """
    #     Constructor of materials where the parameters are known.

    #     :param args: The series of material
    #     :type args: list[Material | MaterialMixture]
    #     :return: Materials container
    #     :rtype: Materials
    #     """
    #     return cls(*materials, name=name, interface=interface)

    @property
    def names(self) -> list:
        """
        :returns: list of names for the materials.
        """
        return [i.name for i in self]

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {self.name: [i._dict_repr for i in self]}

    @classmethod
    def from_dict(cls, data: dict) -> MaterialCollection:
        """
        Create a MaterialCollection from a dictionary.

        :param data: dictionary of the MaterialCollection
        :return: MaterialCollection
        """
        material_collection = super().from_dict(data)
        # Remove the default materials
        for i in range(len(DEFAULT_MATERIALS)):
            del material_collection[0]
        return material_collection
