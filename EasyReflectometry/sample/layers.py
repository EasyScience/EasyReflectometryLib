__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import List, Union, TypeVar

from easyCore.Objects.Groups import BaseCollection
from EasyReflectometry.sample.layer import Layer

RepeatingMultiLayer = TypeVar("RepeatingMultiLayer")


class Layers(BaseCollection):

    def __init__(self,
                 *args: List[Union[Layer, RepeatingMultiLayer]],
                 name: str = 'easyLayers',
                 interface=None,
                 **kwargs):
        super().__init__(name, *args, **kwargs)
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
        return cls(layer1, layer2, interface=interface)

    @classmethod
    def from_pars(cls,
                  *args: List[Layer],
                  name: str = 'easyLayer',
                  interface=None) -> "Layer":
        """
        Constructor of a reflectometry layers where the parameters are known.

        :param args: The series of layers
        :type args: List[Union[EasyReflectometry.layer.Layer, EasyReflectometry.Item.Item]]
        :return: Layers container
        :rtype: Layers
        """
        return cls(*args, name=name, interface=interface)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        string_return = f"<{self.name}: A series of {len(self)} layers>"
        for i in self:
            string_return += f"\n  - {i}"
        return string_return
