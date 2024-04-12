from __future__ import annotations

__author__ = 'github.com/arm61'
from numbers import Number
from typing import Optional
from typing import Union

from easyCore import np
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.parameter_utils import get_as_parameter

from ...base_core import BaseCore
from ..materials.material import Material

DEFAULTS = {
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


class Layer(BaseCore):
    # Added in super().__init__
    #: Material that makes up the layer.
    material: Material
    #: Thickness of the layer in Angstrom.
    thickness: Parameter
    #: Roughness of the layer in Angstrom.
    roughness: Parameter

    def __init__(
        self,
        material: Optional[Material] = None,
        thickness: Union[Parameter, Number, None] = None,
        roughness: Union[Parameter, Number, None] = None,
        name: str = 'EasyLayer',
        interface=None,
    ):
        """Constructor.

        :param material: The material for the layer.
        :param thickness: Layer thickness in Angstrom.
        :param roughness: Upper roughness on the layer in Angstrom.
        :param name: Name of the layer, defaults to 'EasyLayer'
        :param interface: Interface object, defaults to :py:attr:`None`
        """
        if material is None:
            material = Material(interface=interface)

        thickness = get_as_parameter(thickness, 'thickness', DEFAULTS)
        roughness = get_as_parameter(roughness, 'roughness', DEFAULTS)

        super().__init__(
            name=name,
            interface=interface,
            material=material,
            thickness=thickness,
            roughness=roughness,
        )

    # # Class methods for instance creation
    # @classmethod
    # def default(cls, interface=None) -> Layer:
    #     """Default instance of the reflectometry layer.

    #     :param interface: Calculator interface, defaults to :py:attr:`None`.
    #     """
    #     material = Material.default()
    #     thickness = Parameter('thickness', **DEFAULTS['thickness'])
    #     roughness = Parameter('roughness', **DEFAULTS['roughness'])
    #     return cls(
    #         material,
    #         thickness,
    #         roughness,
    #         interface=interface,
    #     )

    # @classmethod
    # def from_pars(
    #     cls,
    #     material: Material,
    #     thickness: float,
    #     roughness: float,
    #     name: str = 'EasyLayer',
    #     interface=None,
    # ) -> Layer:
    #     """Instance of a reflectometry layer where the parameters are known.

    #     :param material: The material that makes up the layer.
    #     :param thickness: Layer thickness in angstrom.
    #     :param roughness: Layer roughness in angstrom.
    #     :param name: Name of the layer, defaults to 'EasyLayer'.
    #     :param interface: Calculator interface, defaults to :py:attr:`None`.
    #     """
    #     default_options = deepcopy(DEFAULTS)
    #     del default_options['thickness']['value']
    #     del default_options['roughness']['value']

    #     thickness = Parameter('thickness', thickness, **default_options['thickness'])
    #     roughness = Parameter('roughness', roughness, **default_options['roughness'])

    #     return cls(
    #         material=material,
    #         thickness=thickness,
    #         roughness=roughness,
    #         name=name,
    #         interface=interface,
    #     )

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
