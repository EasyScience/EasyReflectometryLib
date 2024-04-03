from __future__ import annotations

from copy import deepcopy

from easyCore.Objects.ObjectClasses import Parameter

from ..elements.layers.layer import Layer
from ..elements.layers.layer_collection import LayerCollection
from .multilayer import Multilayer

REPEATINGMULTILAYER_DETAILS = {
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
        layers: LayerCollection | Layer | list[Layer],
        repetitions: Parameter,
        name: str = 'EasyRepeatingMultilayer',
        interface=None,
    ):
        """Constructor.

        :param layers: The layers that make up the multi-layer that will be repeated.
        :param repetitions: Number of repetitions of the given series of layers
        :param name: Name for the repeating multi layer, defaults to 'EasyRepeatingMultilayer'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """

        if isinstance(layers, Layer):
            layers = LayerCollection(layers, name=layers.name)
        elif isinstance(layers, list):
            layers = LayerCollection(*layers, name='/'.join([layer.name for layer in layers]))
        super().__init__(
            layers=layers,
            name=name,
            interface=interface,
            type='Repeating Multi-layer',
        )
        self._add_component('repetitions', repetitions)
        self.interface = interface

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> RepeatingMultilayer:
        """Default instance of a repeating multi layer.

        :return: Default repeating multi-layer container
        """
        layers = LayerCollection.default()
        repetitions = Parameter('repetitions', **REPEATINGMULTILAYER_DETAILS['repetitions'])
        return cls(
            layers,
            repetitions,
            interface=interface,
        )

    @classmethod
    def from_pars(
        cls,
        layers: LayerCollection,
        repetitions: float = 1.0,
        name: str = 'EasyRepeatingMultilayer',
        interface=None,
    ) -> RepeatingMultilayer:
        """Instance of a repeating multi layer where the
        parameters are known.

        :param layers: The layers in the repeating multi layer.
        :param repetitions: Number of repetitions, defaults to :py:attr`1`.
        :param name: Name of the layer, defaults to 'EasyRepeatingMultilayer'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        default_options = deepcopy(REPEATINGMULTILAYER_DETAILS)
        del default_options['repetitions']['value']

        repetitions = Parameter('repetitions', repetitions, **default_options['repetitions'])

        return cls(
            layers=layers,
            repetitions=repetitions,
            name=name,
            interface=interface,
        )

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """A simplified dict representation."""
        d_dict = {self.name: self.layers._dict_repr}
        d_dict[self.name]['repetitions'] = self.repetitions.raw_value
        return d_dict
