__author__ = 'github.com/arm61'

from typing import Optional

from ...base_element_collection import BaseElementCollection
from .layer import Layer


class LayerCollection(BaseElementCollection):
    # Added in super().__init__
    layers: list[Layer]

    def __init__(
        self,
        *layers: Optional[list[Layer]],
        name: str = 'EasyLayerCollection',
        interface=None,
        **kwargs,
    ):
        if not layers:
            layers = []

        super().__init__(name, interface, *layers, **kwargs)
