from __future__ import annotations

from ..elements.layer_collection import LayerCollection
from ..elements.layers.layer import Layer
from .base_assembly import BaseAssembly
from .base_assembly import apply_thickness_constraints


class Bilayer(BaseAssembly):
    def __init__(
        self,
        top_layer: Layer,
        bottom_layer: Layer,
        thickness: float,
        roughness: float,
        name: str = 'EasyBilayer',
        interface=None,
    ):
        super().__init__(
            layers=(top_layer, bottom_layer),
            name=name,
            interface=interface,
        )

        apply_thickness_constraints(self.layers)
        self.thickness = thickness
        self.roughness = roughness

    @classmethod
    def default(cls, interface=None) -> Bilayer:
        """
        Default constructor for the reflectometry bi-layer.

        :return: Default bi-layer container
        :rtype: Bilayer
        """
        layers = LayerCollection.default()
        return cls(
            top_layer=layers[0],
            bottom_layer=layers[1],
            thickness=10.0,
            roughness=1.0,
            interface=interface,
        )

    @classmethod
    def from_pars(
        cls,
        top_layer: Layer,
        bottom_layer: Layer,
        thickness: float,
        roughness: float,
        name: str = 'EasyBilayer',
        interface=None,
    ) -> Bilayer:
        """
        Constructor of a bi-layer item where the parameters are known.

        :param layers: The layers in the multi-layer
        :type layers: EasyReflectometry.layers.Layers
        :return: Bilayer container
        :rtype: Multilayer
        """
        return cls(
            top_layer=top_layer,
            bottom_layer=bottom_layer,
            thickness=thickness,
            roughness=roughness,
            name=name,
            interface=None,
        )

    @LayerCollection.top_layer.setter
    def top_layer(self, layer: Layer) -> None:
        """
        Setter for the top layer
        """
        self.top_layer = layer
        self.top_layer.thickness = self.bottom_layer.thickness

    @LayerCollection.bottom_layer.setter
    def bottom_layer(self, layer: Layer) -> None:
        """
        Setter for the bottom layer
        """
        self.bottom_layer = layer
        self.bottom_layer.thickness = self.top_layer.thickness

    @property
    def thickness(self) -> float:
        """
        :return: The bilayer thickness
        """
        return self.top_layer.thickness.raw_value * 2.0

    @thickness.setter
    def thickness(self, thickness: float) -> None:
        """
        Setter for the bilayer thickness
        """
        if thickness < 0:
            raise ValueError('Thickness must be greater than zero')
        self.top_layer.thickness.raw_value = thickness / 2.0
        self.bottom_layer.thickness.raw_value = thickness / 2.0

    @property
    def roughness(self) -> float:
        """
        :return: The bilayer roughness
        """
        return self.top_layer.roughness.raw_value

    @roughness.setter
    def roughness(self, roughness: float) -> None:
        """
        Setter for the bilayer roughness
        """
        if roughness < 0:
            raise ValueError('Roughness must be greater than zero')
        self.bottom_layer = roughness
        self.top_layer = roughness
