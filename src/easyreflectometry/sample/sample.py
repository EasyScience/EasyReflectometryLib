from __future__ import annotations

__author__ = 'github.com/arm61'

from typing import Union

import yaml
from easyscience.Objects.Groups import BaseCollection

from .assemblies.base_assembly import BaseAssembly
from .assemblies.multilayer import Multilayer
from .elements.layers.layer import Layer

NR_DEFAULT_LAYERS = 2


class Sample(BaseCollection):
    """Collection of assemblies that represent the sample for which experimental measurements exist."""

    def __init__(
        self,
        *list_layer_like: list[Union[Layer, BaseAssembly]],
        name: str = 'EasySample',
        interface=None,
        **kwargs,
    ):
        """Constructor.

        :param args: The assemblies in the sample.
        :param name: Name of the sample, defaults to 'EasySample'.
        :param interface: Calculator interface, defaults to `None`.
        """
        new_items = []
        if not list_layer_like:
            list_layer_like = [Multilayer(interface=interface) for _ in range(NR_DEFAULT_LAYERS)]

        for layer_like in list_layer_like:
            if issubclass(type(layer_like), Layer):
                new_items.append(Multilayer(layer_like, name=layer_like.name))
            elif issubclass(type(layer_like), BaseAssembly):
                new_items.append(layer_like)
            else:
                raise ValueError('The items must be either a Layer or an Assembly.')
        super().__init__(name, *new_items, **kwargs)
        self.interface = interface

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
        The resulting dict matches the parameters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        for i, layer in enumerate(self.data):
            this_dict['data'][i] = layer.as_dict(skip=skip)
        return this_dict

    @classmethod
    def from_dict(cls, data: dict) -> Sample:
        """
        Create a Sample from a dictionary.

        :param data: dictionary of the Sample
        :return: Sample
        """
        sample = super().from_dict(data)

        # Remove the default multilayers
        for i in range(NR_DEFAULT_LAYERS):
            sample.__delitem__(0)

        # Ensure that the data is also converted
        # TODO Should probably be handled in easyscience
        for i in range(len(sample.data)):
            sample[i] = sample[i].__class__.from_dict(data['data'][i])

        return sample
