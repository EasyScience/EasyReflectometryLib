__author__ = 'github.com/arm61'

from typing import List, Union

import yaml
from easyCore.Objects.Groups import BaseCollection
from EasyReflectometryLib.sample.item import MultiLayer
from EasyReflectometryLib.sample.layer import Layer


class Structure(BaseCollection):

    def __init__(self,
                 *args: List[Union[Layer, MultiLayer]],
                 name: str = 'EasyStructure',
                 interface=None,
                 **kwargs):
        new_items = []
        for i in args:
            if issubclass(type(i), Layer):
                new_items.append(MultiLayer.from_pars(i, name=i.name))
            elif issubclass(type(i), MultiLayer):
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
        item1 = MultiLayer.default()
        item2 = MultiLayer.default()
        return cls(item1, item2, interface=interface)

    @classmethod
    def from_pars(cls,
                  *args: List[Union[MultiLayer]],
                  name: str = 'EasyStructure',
                  interface=None) -> "Structure":
        """
        Constructor of a reflectometry structure where the parameters are known.

        :param args: The items in the structure
        :type args: List[EasyReflectometry.item.Item]
        :return: Structure container
        :rtype: Structure
        """
        return cls(*args, name=name, interface=interface)

    @property
    def uid(self) -> int:
        """
        :return: UID from the borg map
        """
        return self._borg.map.convert_id_to_key(self)

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
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return yaml.dump(self._dict_repr, sort_keys=False)
