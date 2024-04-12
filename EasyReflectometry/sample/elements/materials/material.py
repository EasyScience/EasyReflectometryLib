from __future__ import annotations

__author__ = 'github.com/arm61'

from numbers import Number
from typing import Union

from easyCore import np
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.parameter_utils import get_as_parameter

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
        sld: Union[Parameter, Number, None] = None,
        isld: Union[Parameter, Number, None] = None,
        name: str = 'EasyMaterial',
        interface=None,
    ):
        """Constructor.

        :param sld: Real scattering length density.
        :param isld: Imaginary scattering length density.
        :param name: Name of the material, defaults to 'EasyMaterial'.
        :param interface: Calculator interface, defaults to `None`.
        """
        sld = get_as_parameter(sld, 'sld', DEFAULTS)
        isld = get_as_parameter(isld, 'isld', DEFAULTS)

        super().__init__(name=name, sld=sld, isld=isld, interface=interface)

    # Class methods for instance creation
    # @classmethod
    # def default(cls, interface=None) -> Material:
    #     """Default instance of a material."""
    #     sld = Parameter('sld', **DEFAULTS['sld'])
    #     isld = Parameter('isld', **DEFAULTS['isld'])
    #     return cls(sld, isld, interface=interface)

    # @classmethod
    # def from_pars(
    #     cls,
    #     sld: float,
    #     isld: float,
    #     name: str = 'EasyMaterial',
    #     interface=None,
    # ) -> Material:
    #     """Instance of a  material where the parameters are known.

    #     :param sld: Real scattering length density.
    #     :param isld: Imaginary scattering length density.
    #     :param name: Name of the material, defaults to 'EasyMaterial'.
    #     :param interface: Calculator interface, defaults to :py:attr:`None`.
    #     """
    #     default_options = deepcopy(DEFAULTS)
    #     del default_options['sld']['value']
    #     del default_options['isld']['value']

    #     sld = Parameter('sld', sld, **default_options['sld'])
    #     isld = Parameter('isld', isld, **default_options['isld'])

    #     return cls(sld=sld, isld=isld, name=name, interface=interface)

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
