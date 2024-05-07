from typing import Optional

from numpy import arange

from ..elements.layers.layer import Layer
from ..elements.layers.layer_collection import LayerCollection
from ..elements.materials.material import Material
from .base_assembly import BaseAssembly


class GradientLayer(BaseAssembly):
    """A set of discrete gradient layers changing from the front to the back material.
    The front layer is where the neutron beam starts in, it has an index of 0.

    """

    def __init__(
        self,
        front_material: Optional[Material] = None,
        back_material: Optional[Material] = None,
        thickness: Optional[float] = 2.0,
        roughness: Optional[float] = 0.2,
        discretisation_elements: int = 10,
        name: str = 'EasyGradienLayer',
        interface=None,
    ):
        """Constructor.

        :param front_material: Material of front of the layer
        :param back_material: Material of back of the layer
        :param thickness: Thicknkess of the layer
        :param roughness: Roughness of the layer
        :param discretisation_elements: Number of discrete layers
        :param name: Name for gradient layer, defaults to 'EasyGradienLayer'.
        :param interface: Calculator interface, defaults to `None`.
        """

        if front_material is None:
            front_material = Material(0.0, 0.0, 'Air')
        self._front_material = front_material

        if back_material is None:
            back_material = Material(6.36, 0.0, 'D2O')
        self._back_material = back_material

        if discretisation_elements < 2:
            raise ValueError('Discretisation elements must be greater than 2.')
        self._discretisation_elements = discretisation_elements

        gradient_layers = _prepare_gradient_layers(
            front_material=front_material,
            back_material=back_material,
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

    @property
    def thickness(self) -> float:
        """Get the thickness of the gradient layer in Angstrom."""
        return self.front_layer.thickness.raw_value * self._discretisation_elements

    @thickness.setter
    def thickness(self, thickness: float) -> None:
        """Set the thickness of the gradient layer.

        :param thickness: Thickness of the gradient layer in Angstroms.
        """
        self.front_layer.thickness.value = thickness / self._discretisation_elements

    @property
    def roughness(self) -> float:
        """Get the Roughness of the gradient layer in Angstrom."""
        return self.front_layer.roughness.raw_value

    @roughness.setter
    def roughness(self, roughness: float) -> None:
        """Set the roughness of the gradient layer.

        :param roughness: Roughness of the gradient layer in Angstroms.
        """
        self.front_layer.roughness.value = roughness

    @property
    def _dict_repr(self) -> dict[str, str]:
        """A simplified dict representation."""
        return {
            'thickness': self.thickness,
            'discretisation_elements': self._discretisation_elements,
            'back_layer': self.back_layer._dict_repr,
            'front_layer': self.front_layer._dict_repr,
        }

    def as_dict(self, skip: list = None) -> dict:
        """Produces a cleaned dict using a custom as_dict method to skip necessary things.
        The resulting dict matches the parameters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        this_dict = super().as_dict(skip=skip)
        # Determined in __init__
        del this_dict['layers']
        return this_dict


def _linear_gradient(
    front_value: float,
    back_value: float,
    discretisation_elements: int,
) -> list[float]:
    discrete_step = (back_value - front_value) / discretisation_elements
    if discrete_step != 0:
        # Both front and back values are included
        gradient = arange(front_value, back_value + discrete_step, discrete_step)
    else:
        gradient = [front_value] * discretisation_elements
    return gradient


def _prepare_gradient_layers(
    front_material: Material,
    back_material: Material,
    discretisation_elements: int,
    interface=None,
) -> LayerCollection:
    gradient_sld = _linear_gradient(
        front_value=front_material.sld.raw_value,
        back_value=back_material.sld.raw_value,
        discretisation_elements=discretisation_elements,
    )
    gradient_isld = _linear_gradient(
        front_value=front_material.isld.raw_value,
        back_value=back_material.isld.raw_value,
        discretisation_elements=discretisation_elements,
    )
    gradient_layers = []
    for i in range(discretisation_elements):
        material_i = Material(gradient_sld[i], gradient_isld[i], interface=interface)
        layer = Layer(
            material=material_i,
            thickness=0.0,
            roughness=0.0,
            name=str(i),
            interface=interface,
        )
        gradient_layers.append(layer)
    return LayerCollection(gradient_layers)
