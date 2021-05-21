__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import Union

from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj
from easyReflectometryLib.Sample.layer import Layer
from easyReflectometryLib.Sample.layers import Layers

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
                 type: str = 'Layer',
                 interface=None):
        if isinstance(layers, Layer):
            layers = Layers([layers], name=layers.name)
            type = 'Layer'
        super().__init__(name, layers=layers, repetitions=repetitions)
        self.interface = interface
        self.type = type

    # Class constructors
    @classmethod
    def default(cls, type='Layer', interface=None) -> "Item":
        """
        Default constructor for the reflectometry item. 

        :return: Default item container
        :rtype: Item
        """
        layers = Layers.default()
        repetitions = Parameter('repetitions', **ITEM_DETAILS['repetitions'])
        return cls(layers, repetitions, type=type, interface=interface)

    @classmethod
    def from_pars(cls,
                  layers: Layers,
                  repetitions: float = 1.0,
                  name: str = 'easyItem',
                  type: str = 'Layer',
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
                   type=type,
                   interface=interface)

    def add_layer(self, *layers):
        """
        Add a layer to the item.

        :param *layers: Layers to add to item
        :type layers: Layer
        """
        for arg in layers:
            if issubclass(arg.__class__, Layer):
                self.layers.append(arg)
                if self.interface is not None:
                    self.interface().add_layer_to_item(arg.uid, self.uid)

    def duplicate_layer(self, idx):
        """
        Duplicate a given layer.

        :param idx: index of layer to duplicate
        :type idx: int
        """
        to_duplicate = self.layers[idx]
        duplicate_layer = Layer.from_pars(
            material=to_duplicate.material,
            thickness=to_duplicate.thickness.raw_value,
            roughness=to_duplicate.roughness.raw_value,
            name=to_duplicate.name,
            interface=to_duplicate.interface)
        self.add_layer(duplicate_layer)

    def remove_layer(self, idx):
        """
        Remove a layer from the item.

        :param idx: index of layer to remove
        :type idx: int
        """
        if self.interface is not None:
            self.interface().remove_layer_from_item(self.layers[idx].uid,
                                                    self.uid)
        del self.layers[idx]

    @property
    def uid(self):
        """
        Return a UID from the borg map
        """
        return self._borg.map.convert_id_to_key(self)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return f"<{self.name}: ({self.repetitions.raw_value} repetitions of {self.layers.__repr__()})>"
