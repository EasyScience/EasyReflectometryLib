from __future__ import annotations

from numpy import arange

from ..elements.layer_collection import LayerCollection
from ..elements.layers.layer import Layer
from ..elements.materials.material import Material
from .base_assembly import BaseAssembly


class GradientLayer(BaseAssembly):
    """A set of discrete gradient layers changing from the initial to the final material."""

    def __init__(
        self,
        initial_material: Material,
        final_material: Material,
        thickness: float,
        roughness: float,
        discretisation_elements: int = 10,
        name: str = 'EasyGradienLayer',
        interface=None,
    ) -> GradientLayer:
        """
        Constructor.

        :param initial_material: Material of initial "part" of the layer
        :param final_material: Material of final "part" of the layer
        :param thickness: Thicknkess of the layer
        :param roughness: Roughness of the layer
        :param discretisation_elements: Number of discrete layers
        :param name: Name for gradient layer, defaults to 'EasyGradienLayer'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        self._initial_material = initial_material
        self._final_material = final_material
        if discretisation_elements < 2:
            raise ValueError('Discretisation elements must be greater than 2.')
        self._discretisation_elements = discretisation_elements

        gradient_layers = _prepare_gradient_layers(
            initial_material=initial_material,
            final_material=final_material,
            discretisation_elements=discretisation_elements,
            interface=interface,
        )

        super().__init__(
            layers=gradient_layers,
            name=name,
            interface=interface,
            type='Gradient-layer',
        )

        self._setup_thickness_constraints()
        self._enable_thickness_constraints()
        self._setup_roughness_constraints()
        self._enable_roughness_constraints()

        # Set the thickness and roughness properties
        self.thickness = thickness
        self.roughness = roughness

    # Class methods for instance creation
    @classmethod
    def default(cls, name: str = 'Air-Deuterium', interface=None) -> GradientLayer:
        """Default instance  for a gradient layer object. The default is air to deuterium."""
        initial_material = Material.from_pars(0.0, 0.0, 'Air')
        final_material = Material.from_pars(6.36, 0.0, 'D2O')

        return cls(
            initial_material=initial_material,
            final_material=final_material,
            thickness=2.0,
            roughness=0.2,
            discretisation_elements=10,
            name=name,
            interface=interface,
        )

    @classmethod
    def from_pars(
        cls,
        initial_material: Material,
        final_material: Material,
        thickness: float,
        roughness: float,
        discretisation_elements: int,
        name: str = 'EasyGradientLayer',
        interface=None,
    ) -> GradientLayer:
        """Instance for the gradient layer where the parameters are known,
        :py:attr:`initial` is facing the neutron beam.

        :param initial_material: Material of initial "part" of the layer
        :param final_material: Material of final "part" of the layer
        :param thickness: Thicknkess of the layer
        :param roughness: Roughness of the layer
        :param discretisation_elements: Number of dicrete layers
        :param name: Name for gradient layer
        """

        return cls(
            initial_material=initial_material,
            final_material=final_material,
            thickness=thickness,
            roughness=roughness,
            discretisation_elements=discretisation_elements,
            name=name,
            interface=interface,
        )

    @property
    def thickness(self) -> float:
        """Get the thickness of the gradient layer in Angstrom."""
        return self.top_layer.thickness.raw_value * self._discretisation_elements

    @thickness.setter
    def thickness(self, thickness: float) -> None:
        """Set the thickness of the gradient layer.

        :param thickness: Thickness of the gradient layer in Angstroms.
        """
        self.top_layer.thickness.value = thickness / self._discretisation_elements

    @property
    def roughness(self) -> float:
        """Get the Roughness of the gradient layer in Angstrom."""
        return self.top_layer.roughness.raw_value

    @roughness.setter
    def roughness(self, roughness: float) -> None:
        """Set the roughness of the gradient layer.
        :param roughness: Roughness of the gradient layer in Angstroms.
        """
        self.top_layer.roughness.value = roughness

    @property
    def _dict_repr(self) -> dict[str, str]:
        """A simplified dict representation."""
        return {
            'thickness': self.thickness,
            'discretisation_elements': self._discretisation_elements,
            'top_layer': self.top_layer._dict_repr,
            'bottom_layer': self.bottom_layer._dict_repr,
        }

    def as_dict(self, skip: list = None) -> dict:
        """
        Cleaned dictionary. Custom as_dict method to skip generated layers.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        del this_dict['layers']
        return this_dict


def _linear_gradient(
    init_value: float,
    final_value: float,
    discretisation_elements: int,
) -> list[float]:
    discrete_step = (final_value - init_value) / discretisation_elements
    if discrete_step != 0:
        # Both initial and final values are included
        gradient = arange(init_value, final_value + discrete_step, discrete_step)
    else:
        gradient = [init_value] * discretisation_elements
    return gradient


def _prepare_gradient_layers(
    initial_material: Material,
    final_material: Material,
    discretisation_elements: int,
    interface=None,
) -> LayerCollection:
    gradient_sld = _linear_gradient(
        init_value=initial_material.sld.raw_value,
        final_value=final_material.sld.raw_value,
        discretisation_elements=discretisation_elements,
    )
    gradient_isld = _linear_gradient(
        init_value=initial_material.isld.raw_value,
        final_value=final_material.isld.raw_value,
        discretisation_elements=discretisation_elements,
    )
    gradient_layers = []
    for i in range(discretisation_elements):
        layer = Layer.from_pars(
            material=Material.from_pars(gradient_sld[i], gradient_isld[i]),
            thickness=0.0,
            roughness=0.0,
            name=str(i),
            interface=interface,
        )
        gradient_layers.append(layer)
    return LayerCollection(gradient_layers)
