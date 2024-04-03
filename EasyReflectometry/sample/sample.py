from __future__ import annotations

__author__ = 'github.com/arm61'

import yaml
from easyCore.Objects.Groups import BaseCollection

from .assemblies.base_assembly import BaseAssembly
from .assemblies.multilayer import Multilayer
from .elements.layers.layer import Layer


class Sample(BaseCollection):
    """Collection of assemblies that represent the sample for which experimental measurements exist."""

    def __init__(
        self,
        *args: list[Layer | BaseAssembly],
        name: str = 'EasySample',
        interface=None,
        **kwargs,
    ):
        """Constructor.

        :param args: The assemblies in the sample.
        :param name: Name of the sample, defaults to 'EasySample'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
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

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> Sample:
        """
        Default instance of the reflectometry sample.

        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        item1 = Multilayer.default()
        item2 = Multilayer.default()
        return cls(item1, item2, interface=interface)

    @classmethod
    def from_pars(
        cls,
        *args: list[Layer | BaseAssembly],
        name: str = 'EasyStructure',
        interface=None,
    ) -> Sample:
        """Constructor of a reflectometry sample where the parameters are known.

        :param args: The assemblies in the sample
        :param name: Name of the sample, defaults to 'EasySample'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        return cls(*args, name=name, interface=interface)

    @property
    def uid(self) -> int:
        """The UID from the borg map."""
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """A simplified dict representation."""
        return {self.name: [i._dict_repr for i in self]}

    def __repr__(self) -> str:
        """String representation of the sample."""
        return yaml.dump(self._dict_repr, sort_keys=False)

    def as_dict(self, skip: list = None) -> dict:
        """Produces a cleaned dict using a custom as_dict method to skip necessary things.
        The resulting dict matches the paramters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        for i, layer in enumerate(self.data):
            this_dict['data'][i] = layer.as_dict()
        return this_dict
