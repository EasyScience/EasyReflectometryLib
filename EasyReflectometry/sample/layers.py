__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import List, Union, TypeVar

import yaml
from easyCore.Objects.Groups import BaseCollection
from EasyReflectometry.sample.layer import Layer

RepeatingMultiLayer = TypeVar("RepeatingMultiLayer")


class Layers(BaseCollection):

    def __init__(self,
                 *args: List[Union[Layer, RepeatingMultiLayer]],
                 name: str = 'EasyLayers',
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
                  name: str = 'EasyLayer',
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

        :return: String representation of the layer
        """
        return yaml.dump(self._dict_repr, sort_keys=False)
