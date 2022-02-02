"""The :py:mod:`item` library is the backbone of :py:mod:`EasyReflectometry`.
An :py:mod:`EasyReflectometry.sample.item` allows for the inclusion of physical and 
chemical parameterisation into our reflectometry model.  

Current :py:mod:`item` options include: 

* :py:class:`MultiLayer`
* :py:class:`RepeatingMultiLayer`
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from typing import Union, List

from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.layers import Layers

REPEATINGMULTILAYER_DETAILS = {
    'repetitions': {
        'description': 'Number of repetitions of the given series of layers',
        'value': 1,
        'min': 1,
        'max': 9999,
        'fixed': True
    }
}


class MultiLayer(BaseObj):
    """
    A :py:class:`MultiLayer` consists of a series of 
    :py:class:`EasyReflectometry.sample.layer.Layer` or 
    :py:class:`EasyReflectometry.sample.layers.Layers`. 
    This :py:mod:`item` will arrange the layers as slabs, one on top of another, 
    allowing the reflectometry to be determined from them. 
    """
    def __init__(self,
                 layers: Union[Layers, Layer, List[Layer]],
                 name: str = 'easyMultiLayer',
                 interface=None):
        if isinstance(layers, Layer):
            layers = Layers(layers, name=layers.name)
        elif isinstance(layers, list):
            layers = Layers(*layers, name='/'.join([layer.name for layer in layers]))
        self.type = 'Multi-layer'
        super().__init__(name, layers=layers)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "MultiLayer":
        """
        Default constructor for a multi-layer item.

        :return: MultiLayer container
        :rtype: MultiLayer
        """
        layers = Layers.default()
        return cls(layers, interface=interface)

    @classmethod
    def from_pars(cls,
                  layers: Layers,
                  name: str = "easyMultiLayer",
                  interface=None) -> "MultiLayer":
        """
        Constructor of a multi-layer item where the parameters are known.

        :param layers: The layers in the multi-layer
        :type layers: EasyReflectometry.layers.Layers
        :return: MultiLayer container
        :rtype: MultiLayer
        """
        return cls(layers=layers, name=name, interface=interface)

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
        duplicate_layer = Layer.from_pars(material=to_duplicate.material,
                                          thickness=to_duplicate.thickness.raw_value,
                                          roughness=to_duplicate.roughness.raw_value,
                                          name=to_duplicate.name + ' duplicate')
        self.add_layer(duplicate_layer)

    def remove_layer(self, idx):
        """
        Remove a layer from the item.

        :param idx: index of layer to remove
        :type idx: int
        """
        if self.interface is not None:
            self.interface().remove_layer_from_item(self.layers[idx].uid, self.uid)
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
        return f"<{self.name}: ({self.layers.__repr__()})>"


class RepeatingMultiLayer(MultiLayer):
    """
    A :py:class:`RepeatingMultiLayer` takes a :py:class:`MultiLayer` and repeats
    it a some number of times. This enables a computational efficiency in many 
    reflectometry engines as the operation can be performed for a single 
    :py:class:`MultiLayer` and cheaply combined for the appropriate number of 
    :py:attr:`repetitions`. 
    """
    def __init__(self,
                 layers: Union[Layers, Layer, List[Layer]],
                 repetitions: Parameter,
                 name: str = 'easyRepeatingMultiLayer',
                 interface=None):
        if isinstance(layers, Layer):
            layers = Layers(layers, name=layers.name)
        elif isinstance(layers, list):
            layers = Layers(*layers, name='/'.join([layer.name for layer in layers]))
        super().__init__(layers, name, interface)
        self._add_component("repetitions", repetitions)
        self.interface = interface
        self.type = 'Repeating Multi-layer'

    # Class constructors
    @classmethod
    def default(cls, type='Multi-layer', interface=None) -> "RepeatingMultiLayer":
        """
        Default constructor for the reflectometry repeating multi layer. 

        :return: Default repeating multi-layer container
        :rtype: RepeatingMultiLayer
        """
        layers = Layers.default()
        repetitions = Parameter('repetitions',
                                **REPEATINGMULTILAYER_DETAILS['repetitions'])
        return cls(layers, repetitions, interface=interface)

    @classmethod
    def from_pars(cls,
                  layers: Layers,
                  repetitions: float = 1.0,
                  name: str = 'easyRepeatingMultiLayer',
                  interface=None) -> "RepeatingMultiLayer":
        """
        Constructor of a reflectometry repeating multi layer where the parameters are known.

        :param layers: The layers in the repeating multi layer
        :type layers: EasyReflectometry.layers.Layers
        :param repetitions: Number of repetitions 
        :type repetitions: float
        :return: Repeating multi-layer container
        :rtype: RepeatingMultiLayer
        """
        default_options = deepcopy(REPEATINGMULTILAYER_DETAILS)
        del default_options['repetitions']['value']

        repetitions = Parameter('repetitions', repetitions,
                                **default_options['repetitions'])

        return cls(layers=layers,
                   repetitions=repetitions,
                   name=name,
                   interface=interface)

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
