from __future__ import annotations

__author__ = 'github.com/arm61'

# import yaml

from .base import BaseElementCollection
from .layer import Layer


class LayerCollection(BaseElementCollection):
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

    # @property
    # def uid(self) -> int:
    #     """
    #     :return: UID from the borg map
    #     """
    #     return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {self.name: [i._dict_repr for i in self]}

    # def __repr__(self) -> str:
    #     """
    #     String representation of the layer.

    #     :return: String representation of the layer
    #     """
    #     return yaml.dump(self._dict_repr, sort_keys=False)
