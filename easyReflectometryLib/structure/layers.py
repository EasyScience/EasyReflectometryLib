__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import List, Union, TypeVar

from easyCore.Objects.Groups import BaseCollection
from easyReflectometryLib.structure.layer import Layer

Item = TypeVar("Item")


class Layers(BaseCollection):
    def __init__(self,
                 layers: List[Union[Layer, Item]],
                 name: str = 'easyLayers',
                 interface=None):
        super().__init__(name, *layers)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Layers":
        """
        Default constructor for the reflectometry layers. 

        :return: Default layers container
        :rtype: Layers
        """
        layer1 = Layer.default()
        layer2 = Layer.default()
        return cls([layer1, layer2], interface=interface)

    @classmethod
    def from_pars(cls,
                  layers: List[Layer],
                  name: str = 'easyLayer',
                  interface=None) -> "Layer":
        """
        Constructor of a reflectometry layers where the parameters are known.

        :param layers: The series of layers
        :type layers: List[Union[easyReflectometryLib.layer.Layer, easyReflectometryLib.Item.Item]]
        :return: Layers container
        :rtype: Layers
        """
        return cls(layers=layers, name=name, interface=interface)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return f"<{self.name}: A series of {len(self)} layers>"
