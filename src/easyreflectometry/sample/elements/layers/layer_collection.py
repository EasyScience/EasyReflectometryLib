__author__ = 'github.com/arm61'

from typing import Optional

from ...base_element_collection import SIZE_DEFAULT_COLLECTION
from ...base_element_collection import BaseElementCollection
from .layer import Layer


class LayerCollection(BaseElementCollection):
    # Added in super().__init__
    layers: list[Layer]

    def __init__(
        self,
        *layers: Optional[list[Layer]],
        name: str = 'EasyLayers',
        interface=None,
        **kwargs,
    ):
        if not layers:
            layers = [Layer(interface=interface) for _ in range(SIZE_DEFAULT_COLLECTION)]

        super().__init__(name, interface, *layers, **kwargs)
