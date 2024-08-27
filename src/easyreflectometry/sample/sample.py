from __future__ import annotations

__author__ = 'github.com/arm61'

from typing import Union

from easyscience.Objects.Groups import BaseCollection

from easyreflectometry.parameter_utils import yaml_dump

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
        populate_if_none: bool = True,
        **kwargs,
    ):
        """Constructor.

        :param args: The assemblies in the sample.
        :param name: Name of the sample, defaults to 'EasySample'.
        :param interface: Calculator interface, defaults to `None`.
        """
        new_items = []
        if not list_layer_like:
            if populate_if_none:
                list_layer_like = [Multilayer(interface=interface) for _ in range(NR_DEFAULT_LAYERS)]
            else:
                list_layer_like = []

        for layer_like in list_layer_like:
            if issubclass(type(layer_like), Layer):
                new_items.append(Multilayer(layer_like, name=layer_like.name))
            elif issubclass(type(layer_like), BaseAssembly):
                new_items.append(layer_like)
            else:
                raise ValueError('The items must be either a Layer or an Assembly.')
        super().__init__(name, *new_items, **kwargs)
        self.interface = interface

        # Needed by the as_dict functionality
        self.populate_if_none = False

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """A simplified dict representation."""
        return {self.name: [i._dict_repr for i in self]}

    def __repr__(self) -> str:
        """String representation of the sample."""
        return yaml_dump(self._dict_repr)

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
        this_dict['populate_if_none'] = self.populate_if_none
        return this_dict
