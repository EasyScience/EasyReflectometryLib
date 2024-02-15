from __future__ import annotations

__author__ = 'github.com/arm61'

from easyCore.Fitting.Constraints import ObjConstraint

from .base_element_collection import BaseElementCollection
from .layers.layer import Layer


class LayerCollection(BaseElementCollection):
    # Added in super().__init__
    layers: list[Layer]

    def __init__(
        self,
        *layers: tuple[Layer],
        name: str = 'EasyLayers',
        interface=None,
        **kwargs,
    ):
        super().__init__(name, interface, *layers, **kwargs)

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> LayerCollection:
        """
        Default constructor for the reflectometry layers.

        :return: Default layers container
        """
        layer1 = Layer.default()
        layer2 = Layer.default()
        return cls(layer1, layer2, interface=interface)

    @classmethod
    def from_pars(
        cls,
        *layers: tuple[Layer],
        name: str = 'EasyLayer',
        interface=None,
    ) -> LayerCollection:
        """
        Constructor of a reflectometry layers where the parameters are known.

        :param args: The series of layers
        :return: Layers container
        """
        return cls(*layers, name=name, interface=interface)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {self.name: [i._dict_repr for i in self]}

    @property
    def top_layer(self) -> Layer:
        """
        :return: The top layer
        """
        return self.layers[0]

    @top_layer.setter
    def top_layer(self, layer: Layer) -> None:
        """
        Setter for the top layer
        """
        self.layers[0] = layer

    @property
    def bottom_layer(self) -> Layer:
        """
        :return: The bottom layer
        """
        return self.layers[-1]

    @bottom_layer.setter
    def bottom_layer(self, layer: Layer) -> None:
        """
        Setter for the bottom layer
        """
        self.layers[-1] = layer


def apply_thickness_constraints(layers: list[Layer]) -> None:
    """
    Add thickness constraint, layer 0 is the deciding layer
    """
    for i in range(1, len(layers)):
        layers[i].thickness.enabled = True
        layer_constraint = ObjConstraint(
            dependent_obj=layers[i].thickness,
            operator='',
            independent_obj=layers[0].thickness,
        )
        layers[0].thickness.user_constraints[f'thickness_{i}'] = layer_constraint
        layers[0].thickness.user_constraints[f'thickness_{i}'].enabled = True

    layers[0].thickness.enabled = True
