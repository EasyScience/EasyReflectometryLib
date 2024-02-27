from __future__ import annotations

from copy import deepcopy
from typing import ClassVar

import numpy as np
from easyCore.Fitting.Constraints import FunctionalConstraint
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.special.calculations import density_to_sld
from EasyReflectometry.special.calculations import molecular_weight
from EasyReflectometry.special.calculations import neutron_scattering_length

from .material import MATERIAL_DEFAULTS
from .material import Material

MATERIALDENSITY_DEFAULTS = {
    'chemical_structure': 'Si',
    'sl': {
        'description': 'The real scattering length for a chemical formula in angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 4.1491,
        'units': 'angstrom',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True,
    },
    'isl': {
        'description': 'The real scattering length for a chemical formula in angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 0.0,
        'units': 'angstrom',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True,
    },
    'density': {
        'description': 'The mass density of the material.',
        'url': 'https://en.wikipedia.org/wiki/Density',
        'value': 2.33,
        'units': 'gram / centimeter ** 3',
        'min': 0,
        'max': np.Inf,
        'fixed': True,
    },
    'molecular_weight': {
        'description': 'The molecular weight of a material.',
        'url': 'https://en.wikipedia.org/wiki/Molecular_mass',
        'value': 28.02,
        'units': 'g / mole',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True,
    },
}


class MaterialDensity(Material):
    # Added in __init__
    scattering_length_real: ClassVar[Parameter]
    scattering_length_imag: ClassVar[Parameter]
    molecular_weight: ClassVar[Parameter]
    density: ClassVar[Parameter]

    def __init__(
        self,
        chemical_structure: str,
        density: Parameter,
        name: str = 'EasyMaterialDensity',
        interface=None,
    ) -> MaterialDensity:
        """Constructor.

        :param chemical_structure: Chemical formula for the material.
        :param density: Mass density for the material.
        :param name: Identifier, defaults to :py:attr:`EasyMaterialDensity`.
        :param interface: Interface object, defaults to :py:attr:`None`.
        """
        scattering_length = neutron_scattering_length(chemical_structure)
        default_options = deepcopy(MATERIALDENSITY_DEFAULTS)
        del default_options['molecular_weight']['value']
        del default_options['sl']['value']
        del default_options['isl']['value']
        mw = Parameter('molecular_weight', molecular_weight(chemical_structure), **default_options['molecular_weight'])
        scattering_length_real = Parameter('scattering_length_real', scattering_length.real, **default_options['sl'])
        scattering_length_imag = Parameter('scattering_length_imag', scattering_length.imag, **default_options['isl'])
        default_options = deepcopy(MATERIAL_DEFAULTS)
        del default_options['sld']['value']
        del default_options['isld']['value']
        sld = Parameter(
            'sld',
            density_to_sld(scattering_length_real.raw_value, mw.raw_value, density.raw_value),
            **default_options['sld'],
        )
        isld = Parameter(
            'isld',
            density_to_sld(scattering_length_imag.raw_value, mw.raw_value, density.raw_value),
            **default_options['isld'],
        )

        constraint = FunctionalConstraint(sld, density_to_sld, [scattering_length_real, mw, density])
        scattering_length_real.user_constraints['sld'] = constraint
        mw.user_constraints['sld'] = constraint
        density.user_constraints['sld'] = constraint
        iconstraint = FunctionalConstraint(isld, density_to_sld, [scattering_length_imag, mw, density])
        scattering_length_imag.user_constraints['isld'] = iconstraint
        mw.user_constraints['isld'] = iconstraint
        density.user_constraints['isld'] = iconstraint

        super().__init__(sld, isld, name=name, interface=interface)

        self._add_component('scattering_length_real', scattering_length_real)
        self._add_component('scattering_length_imag', scattering_length_imag)
        self._add_component('molecular_weight', mw)
        self._add_component('density', density)
        self._chemical_structure = chemical_structure
        self.interface = interface

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> MaterialDensity:
        """
        Default constructor for the material defined by density and chemical structure.

        :param interface: Interface object, defaults to :py:attr:`None`
        :return: Material container
        """
        density = Parameter('density', **MATERIALDENSITY_DEFAULTS['density'])
        return cls(MATERIALDENSITY_DEFAULTS['chemical_structure'], density, interface=interface)

    @classmethod
    def from_pars(
        cls,
        chemical_structure: str,
        density: float,
        name: str = 'EasyMaterialDensity',
        interface=None,
    ) -> MaterialDensity:
        """
        Constructor for a material based on the mass density and chemical structure,
        where these are known.
        :param chemical_structure: Chemical formula for the material
        :param density: Mass density for the material
        :param name: Identifier, defaults to :py:attr:`EasyMaterialDensity`
        :param interface: Interface object, defaults to :py:attr:`None`
        :return: Material container
        """
        default_options = deepcopy(MATERIALDENSITY_DEFAULTS)
        del default_options['density']['value']

        density = Parameter('density', density, **default_options['density'])

        return cls(chemical_structure, density, name=name, interface=interface)

    @property
    def chemical_structure(self) -> str:
        """
        :returns: Chemical structure string
        """
        return self._chemical_structure

    @chemical_structure.setter
    def chemical_structure(self, structure_string: str) -> None:
        """
        :param structure_string: String that defines the chemical structure.
        """
        self._chemical_structure = structure_string
        scattering_length = neutron_scattering_length(structure_string)
        self.scattering_length_real.value = scattering_length.real
        self.scattering_length_imag.value = scattering_length.imag

    @property
    def _dict_repr(self) -> dict[str, str]:
        """
        Dictionary representation of the :py:class:`MaterialDensity` object.

        :return: Simple dictionary
        """
        mat_dict = super()._dict_repr
        mat_dict['chemical_structure'] = self._chemical_structure
        mat_dict['density'] = f'{self.density.raw_value:.2e} {self.density.unit}'
        return mat_dict

    def as_dict(self, skip: list = []) -> dict[str, str]:
        """
        Custom as_dict method to skip necessary things.

        :return: Cleaned dictionary.
        """
        this_dict = super().as_dict(skip=skip)
        del this_dict['sld'], this_dict['isld'], this_dict['scattering_length_real']
        del this_dict['scattering_length_imag'], this_dict['molecular_weight']
        return this_dict
