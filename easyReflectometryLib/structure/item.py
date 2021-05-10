__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import Union

from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj
from easyReflectometryLib.structure.layer import Layer
from easyReflectometryLib.structure.layers import Layers

ITEM_DETAILS = {
    'repetitions': {
        'description': 'Number of repetitions of the given series of layers',
        'value': 1,
        'min': 1,
        'max': 9999,
        'fixed': True
    }
}


class Item(BaseObj):
    def __init__(self,
                 layers: Union[Layers, Layer],
                 repetitions: Parameter,
                 name: str = 'easyItem',
                 interface=None):
        if isinstance(layers, Layer):
            layers = Layers([layers])
        super().__init__(name, layers=layers, repetitions=repetitions)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Item":
        """
        Default constructor for the reflectometry item. 

        :return: Default item container
        :rtype: Item
        """
        layers = Layers.default()
        repetitions = Parameter('repetitions', **ITEM_DETAILS['repetitions'])
        return cls(layers, repetitions, interface=interface)

    @classmethod
    def from_pars(cls,
                  layers: Layers,
                  repetitions: float = 1.0,
                  name: str = 'easyItem',
                  interface=None) -> "Item":
        """
        Constructor of a reflectometry item where the parameters are known.

        :param layers: The layers in the item
        :type layers: easyReflectometryLib.layers.Layers
        :param repetitions: Number of repetitions 
        :type repetitions: float
        :return: Item container
        :rtype: Item
        """
        default_options = deepcopy(ITEM_DETAILS)
        del default_options['repetitions']['value']

        repetitions = Parameter('repetitions', repetitions,
                                **default_options['repetitions'])

        return cls(layers=layers,
                   repetitions=repetitions,
                   name=name,
                   interface=interface)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return f"<{self.name}: ({self.repetitions.raw_value} repetitions of {self.layers.__repr__()})>"
