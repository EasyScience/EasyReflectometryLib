__author__ = 'github.com/arm61'

from typing import Union

import numpy as np
from easyreflectometry.parameter_utils import get_as_parameter
from easyscience.Objects.ObjectClasses import Parameter

from ...base_core import BaseCore

DEFAULTS = {
    'sld': {
        'description': 'The real scattering length density for a material in e-6 per squared angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 4.186,
        'units': '1 / angstrom ** 2',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True,
    },
    'isld': {
        'description': 'The imaginary scattering length density for a material in e-6 per squared angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 0.0,
        'units': '1 / angstrom ** 2',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True,
    },
}


class Material(BaseCore):
    # Added in super().__init__
    sld: Parameter
    isld: Parameter

    def __init__(
        self,
        sld: Union[Parameter, float, None] = None,
        isld: Union[Parameter, float, None] = None,
        name: str = 'EasyMaterial',
        interface=None,
    ):
        """Constructor.

        :param sld: Real scattering length density.
        :param isld: Imaginary scattering length density.
        :param name: Name of the material, defaults to 'EasyMaterial'.
        :param interface: Calculator interface, defaults to `None`.
        """
        sld = get_as_parameter('sld', sld, DEFAULTS)
        isld = get_as_parameter('isld', isld, DEFAULTS)

        super().__init__(name=name, sld=sld, isld=isld, interface=interface)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, str]:
        """A simplified dict representation."""
        return {
            self.name: {
                'sld': f'{self.sld.raw_value:.3f}e-6 {self.sld.unit}',
                'isld': f'{self.isld.raw_value:.3f}e-6 {self.isld.unit}',
            }
        }
