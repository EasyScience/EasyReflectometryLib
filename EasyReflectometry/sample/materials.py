__author__ = 'github.com/arm61'

from typing import List
from typing import Union

import yaml
from easyCore.Objects.Groups import BaseCollection

from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.material import MaterialMixture


class Materials(BaseCollection):

    def __init__(self,
                 *args: List[Union[Material, MaterialMixture]],
                 name: str = 'EasyMaterials',
                 interface=None,
                 **kwargs):
        super().__init__(name, *args, **kwargs)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Materials":
        """
        Default constructor for materials.

        :return: Default materials container
        :rtype: Materials
        """
        material1 = Material.default()
        material2 = Material.default()
        return cls(material1, material2, interface=interface)

    @classmethod
    def from_pars(cls,
                  *args: List[Union[Material, MaterialMixture]],
                  name: str = 'EasyMaterials',
                  interface=None) -> "Materials":
        """
        Constructor of materials where the parameters are known.

        :param args: The series of material
        :type args: List[Union[EasyReflectometry.material.Material]]
        :return: Materials container
        :rtype: Materials
        """
        return cls(*args, name=name, interface=interface)

    @property
    def names(self) -> List:
        """
        :returns: List of names for the materials.
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
