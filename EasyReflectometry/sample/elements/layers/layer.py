from __future__ import annotations

__author__ = 'github.com/arm61'

from copy import deepcopy
from typing import ClassVar

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
    thickness: ClassVar[Parameter]
    roughness: ClassVar[Parameter]

    def __init__(
        self,
        material: Material,
        thickness: Parameter,
        roughness: Parameter,
        name: str = 'EasyLayer',
        interface=None,
    ):
        super().__init__(
            name=name,
            interface=interface,
            material=material,
            thickness=thickness,
            roughness=roughness,
        )

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> Layer:
        """
        Default constructor for the reflectometry layer.

        :return: Default layer container
        :rtype: Layer
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
        """
        Constructor of a reflectometry layer where the parameters are known.

        :param material: The material that makes up the layer
        :type material: EasyReflectometry.material.Material
        :param thickness: Layer thickness in angstrom
        :type thickness: float
        :param roughness: Layer roughness in angstrom
        :type roughness: float
        :return: Layer container
        :rtype: Layer
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
        """
        Assign a material to the layer interface
        """
        self.material = material
        if self.interface is not None:
            self.interface().assign_material_to_layer(self.material.uid, self.uid)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, str]:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        return {
            self.name: {
                'material': self.material._dict_repr,
                'thickness': f'{self.thickness.raw_value:.3f} {self.thickness.unit}',
                'roughness': f'{self.roughness.raw_value:.3f} {self.roughness.unit}',
            }
        }
