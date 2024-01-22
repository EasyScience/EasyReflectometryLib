from __future__ import annotations

from easyCore.Fitting.Constraints import ObjConstraint
from numpy import arange

from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.material import Material

from .multilayer import MultiLayer


class GradientLayer(MultiLayer):
    """
    A :py:class:`GradientLayer` constructs a gradient multilayer for the
    provided initial and final material.
    """
    def __init__(
        self,
        initial_material: Material,
        final_material: Material,
        thickness: float,
        roughness: float,
        discretisation_elements: int = 10,
        name: str = 'EasyGradienLayer',
        interface=None
    ) -> GradientLayer:
        """
        :param initial_material: Material of initial "part" of the layer
        :param final_material: Material of final "part" of the layer
        :param thickness: Thicknkess of the layer
        :param roughness: Roughness of the layer
        :param discretisation_elements: Number of dicrete layers
        :param name: Name for gradient layer
        :param interface: Interface to use for the layer
        """
        self.initial_material = initial_material
        self.final_material = final_material
        self.roughness = roughness
        self.discretisation_elements = discretisation_elements

        gradient_layers = self._prepare_gradient_layers(
            initial_material=initial_material,
            final_material=final_material,
            discretisation_elements=discretisation_elements,
            interface=interface)

        super().__init__(
            layers=gradient_layers,
            name=name,
            interface=interface,
            type='Gradient-layer'
        )

        self._apply_thickness_constraints(thickness, discretisation_elements)

    def _prepare_gradient_layers(
            self,
            initial_material: Material,
            final_material: Material,
            discretisation_elements: int,
            interface=None
        ) -> list[Layer]:
        gradient_sld = _linear_gradient(
            init_value=initial_material.sld.raw_value,
            final_value=final_material.sld.raw_value,
            discretisation_elements=discretisation_elements
        )
        gradient_isld = _linear_gradient(
            init_value=initial_material.isld.raw_value,
            final_value=final_material.isld.raw_value,
            discretisation_elements=discretisation_elements
        )
        gradient_layers = []
        for i in range(discretisation_elements):
            layer = Layer.from_pars(
                material=Material.from_pars(gradient_sld[i], gradient_isld[i]),
                thickness=0.0,
                roughness=0.0,
                name=str(i),
                interface=interface
            )
            gradient_layers.append(layer)
        return gradient_layers

    def _apply_thickness_constraints(self, thickness: float, discretisation_elements: int) -> None:
        # Add thickness constraint, layer 0 is the deciding layer
        for i in range(discretisation_elements):
            if i != 0:
                self.layers[i].thickness.enabled = True
                layer_constraint = ObjConstraint(
                    dependent_obj=self.layers[i].thickness,
                    operator='',
                    independent_obj=self.layers[0].thickness
                )
                self.layers[0].thickness.user_constraints[f'thickness_{i}'] = layer_constraint
                self.layers[0].thickness.user_constraints[f'thickness_{i}'].enabled = True

        # Trigger the constraint to be applied
        self.layers[0].thickness.value = thickness / discretisation_elements
        self.layers[0].thickness.enabled = True

    @property
    def thickness(self) -> float:
        """
        :return: Thickness of the layer
        """
        return self.layers[0].thickness.raw_value * self.discretisation_elements

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> GradientLayer:
        """
        Default constructor for a gradient layer object. The default is air to deuterium.

        :return: Gradient layer object.
        """
        initial_material = Material.from_pars(0.0, 0.0, 'Air')
        final_material = Material.from_pars(6.36, 0.0, 'D2O')

        return cls(
            initial_material=initial_material,
            final_material=final_material,
            thickness=2.,
            roughness=0.2,
            discretisation_elements=10, 
            name='Air-Deuterium', 
            interface=interface
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
        interface=None
    ) -> GradientLayer:
        """
        Constructor for the gradient layer where the parameters are known,
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
            interface=interface
        )

    def add_layer(self, layer: Layer) -> None:
        raise NotImplementedError("Cannot add layers to a gradient layer.")

    def duplicate_layer(self, idx: int) -> None:
        raise NotImplementedError("Cannot duplicate a layer for a gradient layer.")

    def remove_layer(self, idx: int) -> None:
        raise NotImplementedError("Cannot remove layer from a gradient layer.")

    @property
    def _dict_repr(self) -> dict[str, str]:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {
            'type': self.type,
            'thickness': self.thickness,
            'discretisation_elements': self.discretisation_elements,
            'initial_layer': self.layers[0]._dict_repr,
            'final_layer': self.layers[-1]._dict_repr
        }

    def as_dict(self, skip: list = None) -> dict:
        """
        Custom as_dict method to skip generated layers.

        :return: Cleaned dictionary.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        del this_dict['layers']
        return this_dict


def _linear_gradient(
        init_value: float,
        final_value: float,
        discretisation_elements: int
    ) -> list[float]:
    discrete_step = (final_value - init_value) / discretisation_elements
    if discrete_step != 0:
        # Both initial and final values are included
        gradient = arange(init_value, final_value + discrete_step, discrete_step)
    else:
        gradient = [init_value] * discretisation_elements
    return gradient
