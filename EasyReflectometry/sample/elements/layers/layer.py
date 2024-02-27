from __future__ import annotations

__author__ = 'github.com/arm61'

from copy import deepcopy

from easyCore import np
from easyCore.Objects.ObjectClasses import Parameter

from ..base_element import BaseElement
from ..materials.material import Material

LAYER_DETAILS = {
    'thickness': {
        'description': 'The thickness of the layer in angstroms',
        'url': 'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 10.0,
        'units': 'angstrom',
        'min': 0.0,
        'max': np.Inf,
        'fixed': True,
    },
    'roughness': {
        'description': 'The interfacial roughness, Nevot-Croce, for the layer in angstroms.',
        'url': 'https://doi.org/10.1051/rphysap:01980001503076100',
        'value': 3.3,
        'units': 'angstrom',
        'min': 0.0,
        'max': np.Inf,
        'fixed': True,
    },
}


class Layer(BaseElement):
    # Added in super().__init__
    #: Material that makes up the layer.
    material: Material
    #: Thickness of the layer in Angstrom.
    thickness: Parameter
    #: Roughness of the layer in Angstrom.
    roughness: Parameter

    def __init__(
        self,
        material: Material,
        thickness: Parameter,
        roughness: Parameter,
        name: str = 'EasyLayer',
        interface=None,
    ):
        """Constructor for the reflectometry layer.

        :param material: Material that makes up the layer.
        :param thickness: Thickness of the layer in angstrom.
        :param roughness:Roughness of the layer in angstrom.
        :param name: Name of the layer, defaults to 'EasyLayer'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        super().__init__(
            name=name,
            interface=interface,
            material=material,
            thickness=thickness,
            roughness=roughness,
        )

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> Layer:
        """Default instance of the reflectometry layer.

        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        material = Material.default()
        thickness = Parameter('thickness', **LAYER_DETAILS['thickness'])
        roughness = Parameter('roughness', **LAYER_DETAILS['roughness'])
        return cls(
            material,
            thickness,
            roughness,
            interface=interface,
        )

    @classmethod
    def from_pars(
        cls,
        material: Material,
        thickness: float,
        roughness: float,
        name: str = 'EasyLayer',
        interface=None,
    ) -> Layer:
        """Instance of a reflectometry layer where the parameters are known.

        :param material: The material that makes up the layer.
        :param thickness: Layer thickness in angstrom.
        :param roughness: Layer roughness in angstrom.
        :param name: Name of the layer, defaults to 'EasyLayer'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        default_options = deepcopy(LAYER_DETAILS)
        del default_options['thickness']['value']
        del default_options['roughness']['value']

        thickness = Parameter('thickness', thickness, **default_options['thickness'])
        roughness = Parameter('roughness', roughness, **default_options['roughness'])

        return cls(
            material=material,
            thickness=thickness,
            roughness=roughness,
            name=name,
            interface=interface,
        )

    def assign_material(self, material: Material) -> None:
        """Assign a material to the layer interface.

        :param material: The material to assign to the layer.
        """
        self.material = material
        if self.interface is not None:
            self.interface().assign_material_to_layer(self.material.uid, self.uid)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, str]:
        """A simplified dict representation."""
        return {
            self.name: {
                'material': self.material._dict_repr,
                'thickness': f'{self.thickness.raw_value:.3f} {self.thickness.unit}',
                'roughness': f'{self.roughness.raw_value:.3f} {self.roughness.unit}',
            }
        }
