__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import List, Union, TypeVar

from easyCore.Objects.Groups import BaseCollection
from EasyReflectometry.sample.material import Material


class Materials(BaseCollection):
    def __init__(self,
                 *args: List[Material],
                 name: str = 'easyMaterials',
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
                  *args: List[Material],
                  name: str = 'easyMaterials',
                  interface=None) -> "Materials":
        """
        Constructor of materials where the parameters are known.

        :param args: The series of material
        :type args: List[Union[EasyReflectometry.material.Material]]
        :return: Materials container
        :rtype: Materials
        """
        return cls(*args, name=name, interface=interface)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the materials.

        :return: a string representation of the materials
        :rtype: str
        """
        string_return = f"<{self.name}: A series of {len(self)} materials>"
        for i in self:
            string_return += f"\n  - {i}"
        return string_return
