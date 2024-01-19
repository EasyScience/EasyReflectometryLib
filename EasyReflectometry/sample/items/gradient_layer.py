from __future__ import annotations

from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import Parameter
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
        thickness: Parameter,
        roughness: Parameter,
        discretisation_thickness: float = 0.5,
        name: str = 'EasyGradienLayer',
        conformal_roughness: bool = False,
        interface = None
    ) -> None:
        """
        :param layers: List with initial and final layer object
        :param final: Final layer object
        :param name: Name for gradient layer
        """
        self._initial_material = initial_material
        self._final_material = final_material
        self._thickness = thickness
        self._roughness = roughness
        self._discretisation_thickness = discretisation_thickness

        # setup gradient layers
        discretisation_elements = int(thickness.raw_value / discretisation_thickness)

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
                thickness=discretisation_thickness,
                roughness=0,
                name=str(i),
                interface=interface
            )
            gradient_layers.append(layer)

        super().__init__(
            layers=gradient_layers,
            name=name,
            interface=interface,
            type='Gradient-layer'
        )

        self.layers[-1].roughness.enabled = True
        roughness = ObjConstraint(self.layers[-1].roughness, '',
                                  self.layers[0].roughness)
        self.layers[0].roughness.user_constraints['roughness'] = roughness
        self.layers[0].roughness.user_constraints['roughness'].enabled = conformal_roughness

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
            thickness=Parameter('thickness', 2),
            roughness=Parameter('roughness', 0.2),
            discretisation_thickness=0.1, 
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
        discretisation_thickness: float,
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
        :param discretisation_thickness: Thickness of each layer in the gradient
        :param name: Name for gradient layer
        """

        return cls(
            initial_material=initial_material,
            final_material=final_material,
            thickness=Parameter('thickness', thickness),
            roughness=Parameter('roughness', roughness),
            discretisation_thickness=discretisation_thickness, 
            name=name, 
            interface=interface
        )


    @property
    def conformal_roughness(self) -> bool:
        """
        :return: is the roughness is the same for both layers.
        """
        return self.layers[0].roughness.user_constraints['roughness'].enabled

    @conformal_roughness.setter
    def conformal_roughness(self, x: bool):
        """
        Set the roughness to be the same for both layers.
        """
        self.layers[0].roughness.user_constraints['roughness'].enabled = x
        self.layers[-1].roughness.value = self.layers[0].roughness.raw_value

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
            'thickness': self._thickness,
            'discretisation_thickness': self._discretisation_thickness,
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