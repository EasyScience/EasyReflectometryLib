from __future__ import annotations

__author__ = 'github.com/arm61'

import yaml

# from easyCore.Objects.Groups import BaseCollection
from .base import BaseCollection
from .material import Material
from .material import MaterialMixture


class Materials(BaseCollection):
    def __init__(
        self,
        *args: list[Material | MaterialMixture],
        name: str = 'EasyMaterials',
        interface=None,
        **kwargs,
    ):
        super().__init__(name, interface, *args, **kwargs)

    #        super().__init__(name, *args, **kwargs)
    #        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> Materials:
        """
        Default constructor for materials.

        :return: Default materials container
        :rtype: Materials
        """
        material1 = Material.default()
        material2 = Material.default()
        return cls(material1, material2, interface=interface)

    @classmethod
    def from_pars(
        cls,
        *args: list[Material | MaterialMixture],
        name: str = 'EasyMaterials',
        interface=None,
    ) -> Materials:
        """
        Constructor of materials where the parameters are known.

        :param args: The series of material
        :type args: list[Material | MaterialMixture]
        :return: Materials container
        :rtype: Materials
        """
        return cls(*args, name=name, interface=interface)

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

    def __repr__(self) -> str:
        """
        String representation of the materials.

        :return: String representation of the materials
        """
        return yaml.dump(self._dict_repr, sort_keys=False)
