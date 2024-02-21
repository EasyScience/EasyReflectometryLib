from __future__ import annotations

__author__ = 'github.com/arm61'

import yaml
from easyCore.Objects.Groups import BaseCollection

from .assemblies.base_assembly import BaseAssembly
from .assemblies.multilayer import Multilayer
from .elements.layers.layer import Layer


class Sample(BaseCollection):
    def __init__(
        self,
        *args: list[Layer | BaseAssembly],
        name: str = 'EasySample',
        interface=None,
        **kwargs,
    ):
        new_items = []
        for layer_like in args:
            if issubclass(type(layer_like), Layer):
                new_items.append(Multilayer.from_pars(layer_like, name=layer_like.name))
            elif issubclass(type(layer_like), BaseAssembly):
                new_items.append(layer_like)
            else:
                raise ValueError('The items must be either a Layer or an Assembly.')
        super().__init__(name, *new_items, **kwargs)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> Sample:
        """
        Default constructor for the reflectometry sample.

        :return: Default sample container
        :rtype: Structure
        """
        item1 = Multilayer.default()
        item2 = Multilayer.default()
        return cls(item1, item2, interface=interface)

    @classmethod
    def from_pars(
        cls,
        *args: list[Multilayer],
        name: str = 'EasyStructure',
        interface=None,
    ) -> Sample:
        """
        Constructor of a reflectometry sample where the parameters are known.

        :param args: The items in the sample
        :type args: list[EasyReflectometry.item.Item]
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
