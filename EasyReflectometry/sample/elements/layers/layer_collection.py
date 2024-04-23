from __future__ import annotations

__author__ = 'github.com/arm61'

from ..base_element_collection import BaseElementCollection
from .layer import Layer

# DEFAULT_LAYERS = (Layer(), Layer())
NR_DEFAULT_LAYERS = 2


class LayerCollection(BaseElementCollection):
    # Added in super().__init__
    layers: list[Layer]

    def __init__(
        self,
        *list_layer_like: tuple[Layer],
        name: str = 'EasyLayers',
        interface=None,
        **kwargs,
    ):
        if not list_layer_like:
            list_layer_like = tuple([Layer(interface=interface) for _ in range(NR_DEFAULT_LAYERS)])
        #            layers = DEFAULT_LAYERS

        super().__init__(name, interface, *list_layer_like, **kwargs)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, list[dict]]:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {self.name: [i._dict_repr for i in self]}

    @classmethod
    def from_dict(cls, data: dict) -> LayerCollection:
        """
        Create a LayerCollection from a dictionary.

        :param data: dictionary of the LayerCollection
        :return: LayerCollection
        """
        layer_collection = super().from_dict(data)
        # Remove the default layers
        for i in range(NR_DEFAULT_LAYERS):
            del layer_collection[0]
        return layer_collection
