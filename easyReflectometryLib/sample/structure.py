__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import List, Union

from easyCore import np
from easyCore.Objects.Groups import BaseCollection
from easyReflectometryLib.sample.item import Item
from easyReflectometryLib.sample.layer import Layer


class Structure(BaseCollection):
    def __init__(self,
                 items: List[Union[Layer, Item]],
                 name: str = 'easyStructure',
                 interface=None):
        new_items = []
        for i in items:
            if isinstance(i, Layer):
                new_items.append(Item.from_pars(i))
            elif isinstance(i, Item):
                new_items.append(i)
            else:
                raise ValueError('The items must be either a Layer or an Item')
        super().__init__(name, *new_items)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Structure":
        """
        Default constructor for the reflectometry structure. 

        :return: Default structure container
        :rtype: Structure
        """
        item1 = Item.default()
        item2 = Item.default()
        return cls([item1, item2], interface=interface)

    @classmethod
    def from_pars(cls,
                  items: List[Item],
                  name: str = 'easyStructure',
                  interface=None) -> "Structure":
        """
        Constructor of a reflectometry structure where the parameters are known.

        :param items: The items in the structure
        :type items: List[easyReflectometryLib.item.Item]
        :return: Structure container
        :rtype: Structure
        """
        return cls(items, name=name, interface=interface)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return f"<{self.name}: A series of {len(self)} items>"
