from __future__ import annotations

from typing import Optional
from typing import Union

from ..collections.layer_collection import LayerCollection
from ..elements.layers.layer import Layer
from .base_assembly import BaseAssembly


class Multilayer(BaseAssembly):
    """A multi layer is build from a single or a list of `Layer` or `LayerCollection`.
    The multi layer will arrange the layers as slabs, allowing the reflectometry to be determined from them.
    The front layer is where the neutron beam starts in, it has an index of 0.

    More information about the usage of this assembly is available in the
    `multilayer documentation`_

    .. _`multilayer documentation`: ../sample/assemblies_library.html#multilayer
    """

    def __init__(
        self,
        layers: Union[Layer, list[Layer], LayerCollection, None] = None,
        name: str = 'EasyMultilayer',
        unique_name: Optional[str] = None,
        interface=None,
        type: str = 'Multi-layer',
        populate_if_none: Optional[bool] = True,
    ):
        """Constructor.

        :param layers: The layers that make up the multi-layer.
        :param name: Name for multi layer, defaults to 'EasyMultilayer'.
        :param interface: Calculator interface, defaults to `None`.
        :param type: Type of the constructed instance, defaults to 'Multi-layer'
        """
        if layers is None:
            if populate_if_none:
                layers = LayerCollection([Layer(interface=interface)])
            else:
                layers = LayerCollection()
        elif isinstance(layers, Layer):
            layers = LayerCollection(layers, name=layers.name)
        elif isinstance(layers, list):
            layers = LayerCollection(*layers, name='/'.join([layer.name for layer in layers]))
        # Needed to ensure an empty list is created when saving and instatiating the object as_dict -> from_dict
        # Else collisions might occur in global_object.map
        self.populate_if_none = False

        super().__init__(name, unique_name=unique_name, layers=layers, type=type, interface=interface)

    def add_layer(self, *layers: tuple[Layer]) -> None:
        """Add a layer to the multi layer.

        :param layers: Layers to add to the multi layer.
        """
        for arg in layers:
            if issubclass(arg.__class__, Layer):
                self.layers.append(arg)
                if self.interface is not None:
                    self.interface().add_layer_to_item(arg.unique_name, self.unique_name)

    def duplicate_layer(self, idx: int) -> None:
        """Duplicate a given layer.

        :param idx: index of layer to duplicate.
        :type idx: int
        """
        to_duplicate = self.layers[idx]
        duplicate_layer = Layer(
            material=to_duplicate.material,
            thickness=to_duplicate.thickness.value,
            roughness=to_duplicate.roughness.value,
            name=to_duplicate.name + ' duplicate',
        )
        self.add_layer(duplicate_layer)

    def remove_layer(self, idx: int) -> None:
        """Remove a layer from the item.

        :param idx: index of layer to remove
        """
        if self.interface is not None:
            self.interface().remove_layer_from_item(self.layers[idx].unique_name, self.unique_name)
        del self.layers[idx]

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """A simplified dict representation."""
        return {self.name: self.layers._dict_repr}

    @classmethod
    def from_dict(cls, data: dict) -> Multilayer:
        """
        Create a Multilayer from a dictionary.

        :param data: dictionary of the Multilayer
        :return: Multilayer
        """
        multilayer = super().from_dict(data)
        return multilayer
