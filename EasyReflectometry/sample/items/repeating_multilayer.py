from copy import deepcopy
from typing import (
    List,
    Union,
)

from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.layers import Layers

from .multilayer import MultiLayer

REPEATINGMULTILAYER_DETAILS = {
    'repetitions': {
        'description': 'Number of repetitions of the given series of layers',
        'value': 1,
        'min': 1,
        'max': 9999,
        'fixed': True
    }
}


class RepeatingMultiLayer(MultiLayer):
    """
    A :py:class:`RepeatingMultiLayer` takes a :py:class:`MultiLayer` and repeats
    it a some number of times. This enables a computational efficiency in many
    reflectometry engines as the operation can be performed for a single
    :py:class:`MultiLayer` and cheaply combined for the appropriate number of
    :py:attr:`repetitions`.

    More information about the usage of this item is available in the
    `item library documentation`_

    .. _`item library documentation`: ./item_library.html#repeatingmultilayer
    """

    def __init__(self,
                 layers: Union[Layers, Layer, List[Layer]],
                 repetitions: Parameter,
                 name: str = 'EasyRepeatingMultiLayer',
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
    def default(cls, interface=None) -> "RepeatingMultiLayer":
        """
        Default constructor for the reflectometry repeating multi layer.

        :return: Default repeating multi-layer container
        """
        layers = Layers.default()
        repetitions = Parameter('repetitions',
                                **REPEATINGMULTILAYER_DETAILS['repetitions'])
        return cls(layers, repetitions, interface=interface)

    @classmethod
    def from_pars(cls,
                  layers: Layers,
                  repetitions: float = 1.0,
                  name: str = 'EasyRepeatingMultiLayer',
                  interface=None) -> "RepeatingMultiLayer":
        """
        Constructor of a reflectometry repeating multi layer where the
        parameters are known.

        :param layers: The layers in the repeating multi layer
        :param repetitions: Number of repetitions, defaults to :py:attr`1`.
        :return: Repeating multi-layer container
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
    def uid(self) -> int:
        """
        :return: UID from the borg map
        """
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        d_dict = {self.name: self.layers._dict_repr}
        d_dict[self.name]['repetitions'] = self.repetitions.raw_value
        return d_dict
