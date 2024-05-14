from typing import Union

from easyreflectometry.parameter_utils import get_as_parameter
from easyscience.Objects.ObjectClasses import Parameter

from ..elements.layers.layer import Layer
from ..elements.layers.layer_collection import LayerCollection
from .multilayer import Multilayer

DEFAULTS = {
    'repetitions': {
        'description': 'Number of repetitions of the given series of layers',
        'value': 1,
        'min': 1,
        'max': 9999,
        'fixed': True,
    }
}


class RepeatingMultilayer(Multilayer):
    """
    A repeating multi layer is build from a `Multilayer` and which it repeats
    for a given number of times. This enables a computational efficiency in many
    reflectometry engines as the operation can be performed for a single
    `Multilayer` and cheaply combined for the appropriate number of
    `repetitions`.

    More information about the usage of this assembly is available in the
    `repeating multilayer documentation`_

    .. _`repeating multilayer documentation`: ../sample/assemblies_library.html#repeatingmultilayer
    """

    def __init__(
        self,
        layers: Union[LayerCollection, Layer, list[Layer], None] = None,
        repetitions: Union[Parameter, int, None] = None,
        name: str = 'EasyRepeatingMultilayer',
        interface=None,
    ):
        """Constructor.

        :param layers: The layers that make up the multi-layer that will be repeated.
        :param repetitions: Number of repetitions of the given series of layers
        :param name: Name for the repeating multi layer, defaults to 'EasyRepeatingMultilayer'.
        :param interface: Calculator interface, defaults to `None`.
        """

        if layers is None:
            layers = LayerCollection()
        elif isinstance(layers, Layer):
            layers = LayerCollection(layers, name=layers.name)
        elif isinstance(layers, list):
            layers = LayerCollection(*layers, name='/'.join([layer.name for layer in layers]))

        repetitions = get_as_parameter('repetitions', repetitions, DEFAULTS)

        super().__init__(
            layers=layers,
            name=name,
            interface=interface,
            type='Repeating Multi-layer',
        )
        self._add_component('repetitions', repetitions)
        self.interface = interface

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """A simplified dict representation."""
        d_dict = {self.name: self.layers._dict_repr}
        d_dict[self.name]['repetitions'] = self.repetitions.raw_value
        return d_dict
