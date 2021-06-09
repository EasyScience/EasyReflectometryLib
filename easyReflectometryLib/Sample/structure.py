__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import List, Union

from easyCore import np
from easyCore.Objects.Groups import BaseCollection
from easyReflectometryLib.Sample.item import RepeatingMultiLayer
from easyReflectometryLib.Sample.layer import Layer


class Structure(BaseCollection):
    def __init__(self,
                 *args: List[Union[Layer, RepeatingMultiLayer]],
                 name: str = 'easyStructure',
                 interface=None,
                 **kwargs):
        new_items = []
        for i in args:
            if isinstance(i, Layer):
                new_items.append(RepeatingMultiLayer.from_pars(i, name=i.name))
            elif isinstance(i, RepeatingMultiLayer):
                new_items.append(i)
            else:
                raise ValueError('The items must be either a Layer or an Item')
        super().__init__(name, *new_items, **kwargs)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Structure":
        """
        Default constructor for the reflectometry structure. 

        :return: Default structure container
        :rtype: Structure
        """
        item1 = RepeatingMultiLayer.default()
        item2 = RepeatingMultiLayer.default()
        return cls(item1, item2, interface=interface)

    @classmethod
    def from_pars(cls,
                  *args: List[RepeatingMultiLayer],
                  name: str = 'easyStructure',
                  interface=None) -> "Structure":
        """
        Constructor of a reflectometry structure where the parameters are known.

        :param args: The items in the structure
        :type args: List[easyReflectometryLib.item.Item]
        :return: Structure container
        :rtype: Structure
        """
        return cls(*args, name=name, interface=interface)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        string_return = f"<{self.name}: A series of {len(self)} items>"
        for i in self:
            string_return += f"\n  - {i}"
        return string_return
