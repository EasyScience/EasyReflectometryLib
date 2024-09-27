__author__ = 'github.com/arm61'

from typing import Optional

from ..elements.layers.layer import Layer
from .base_collection import BaseCollection


class LayerCollection(BaseCollection):
    def __init__(
        self,
        *layers: Optional[list[Layer]],
        name: str = 'EasyLayerCollection',
        interface=None,
        unique_name: Optional[str] = None,
        populate_if_none: bool = True,  # Needed to match as_dict signature from BaseCollection
        **kwargs,
    ):
        if not layers:
            layers = []

        super().__init__(name, interface, unique_name=unique_name, *layers, **kwargs)
