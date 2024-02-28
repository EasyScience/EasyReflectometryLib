from __future__ import annotations

__author__ = 'github.com/arm61'

from copy import deepcopy
from typing import ClassVar

from easyCore import np
from easyCore.Objects.ObjectClasses import Parameter

from ..base_element import BaseElement

MATERIAL_DEFAULTS = {
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


class Material(BaseElement):
    # Added in super().__init__
    sld: ClassVar[Parameter]
    isld: ClassVar[Parameter]

    def __init__(
        self,
        sld: Parameter,
        isld: Parameter,
        name: str = 'EasyMaterial',
        interface=None,
    ):
        """Constructor.

        :param sld: Real scattering length density.
        :param isld: Imaginary scattering length density.
        :param name: Name of the material, defaults to 'EasyMaterial'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        super().__init__(name=name, interface=interface, sld=sld, isld=isld)

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> Material:
        """Default instance of a material."""
        sld = Parameter('sld', **MATERIAL_DEFAULTS['sld'])
        isld = Parameter('isld', **MATERIAL_DEFAULTS['isld'])
        return cls(sld, isld, interface=interface)

    @classmethod
    def from_pars(
        cls,
        sld: float,
        isld: float,
        name: str = 'EasyMaterial',
        interface=None,
    ) -> Material:
        """Instance of a  material where the parameters are known.

        :param sld: Real scattering length density.
        :param isld: Imaginary scattering length density.
        :param name: Name of the material, defaults to 'EasyMaterial'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        default_options = deepcopy(MATERIAL_DEFAULTS)
        del default_options['sld']['value']
        del default_options['isld']['value']

        sld = Parameter('sld', sld, **default_options['sld'])
        isld = Parameter('isld', isld, **default_options['isld'])

        return cls(sld=sld, isld=isld, name=name, interface=interface)

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
