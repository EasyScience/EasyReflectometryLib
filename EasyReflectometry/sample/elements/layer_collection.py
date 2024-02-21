from __future__ import annotations

__author__ = 'github.com/arm61'

from .base_element_collection import BaseElementCollection
from .layers.layer import Layer


class LayerCollection(BaseElementCollection):
    # Added in super().__init__
    layers: list[Layer]

    def __init__(
        self,
        *layers: tuple[Layer],
        name: str = 'EasyLayers',
        interface=None,
        **kwargs,
    ):
        super().__init__(name, interface, *layers, **kwargs)

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> LayerCollection:
        """
        Default constructor for the reflectometry layers.

        :return: Default layers container
        """
        layer1 = Layer.default()
        layer2 = Layer.default()
        return cls(layer1, layer2, interface=interface)

    @classmethod
    def from_pars(
        cls,
        *layers: tuple[Layer],
        name: str = 'EasyLayer',
        interface=None,
    ) -> LayerCollection:
        """
        Constructor of a reflectometry layers where the parameters are known.

        :param args: The series of layers
        :return: Layers container
        """
        return cls(*layers, name=name, interface=interface)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, list[dict]]:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {self.name: [i._dict_repr for i in self]}
