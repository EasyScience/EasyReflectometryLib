from __future__ import annotations

from numbers import Number
from typing import Optional
from typing import Union

import numpy as np
from easyCore.Fitting.Constraints import FunctionalConstraint
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.parameter_utils import get_as_parameter
from EasyReflectometry.special.calculations import density_to_sld
from EasyReflectometry.special.calculations import molecular_weight
from EasyReflectometry.special.calculations import neutron_scattering_length

from .material import DEFAULTS as MATERIAL_DEFAULTS
from .material import Material

DEFAULTS = {
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
DEFAULTS.update(MATERIAL_DEFAULTS)


class MaterialDensity(Material):
    # Added in __init__
    scattering_length_real: Parameter
    scattering_length_imag: Parameter
    molecular_weight: Parameter
    density: Parameter

    def __init__(
        self,
        chemical_structure: Optional[str] = None,
        density: Union[Parameter, Number, None] = None,
        name: str = 'EasyMaterialDensity',
        interface=None,
    ) -> MaterialDensity:
        """Constructor.

        :param chemical_structure: Chemical formula for the material.
        :param density: Mass density for the material.
        :param name: Identifier, defaults to `EasyMaterialDensity`.
        :param interface: Interface object, defaults to `None`.
        """
        if chemical_structure is None:
            chemical_structure = DEFAULTS['chemical_structure']

        density = get_as_parameter(density, 'density', DEFAULTS)

        scattering_length = neutron_scattering_length(chemical_structure)
        # default_options = deepcopy(DEFAULTS)

        mw = get_as_parameter(molecular_weight(chemical_structure), 'molecular_weight', DEFAULTS)
        scattering_length_real = get_as_parameter(
            value=scattering_length.real,
            name='scattering_length_real',
            default_dict=DEFAULTS['sld'],
        )
        scattering_length_imag = get_as_parameter(
            value=scattering_length.imag,
            name='scattering_length_imag',
            default_dict=DEFAULTS['isld'],
        )

        sld = get_as_parameter(
            density_to_sld(scattering_length_real.raw_value, mw.raw_value, density.raw_value),
            'sld',
            DEFAULTS,
        )
        isld = get_as_parameter(
            density_to_sld(scattering_length_imag.raw_value, mw.raw_value, density.raw_value),
            'isld',
            DEFAULTS,
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

    @property
    def chemical_structure(self) -> str:
        """Get the chemical structure string."""
        return self._chemical_structure

    @chemical_structure.setter
    def chemical_structure(self, structure_string: str) -> None:
        """Set the chemical structure string.

        :param structure_string: String that defines the chemical structure.
        """
        self._chemical_structure = structure_string
        scattering_length = neutron_scattering_length(structure_string)
        self.scattering_length_real.value = scattering_length.real
        self.scattering_length_imag.value = scattering_length.imag

    @property
    def _dict_repr(self) -> dict[str, str]:
        """Dictionary representation of the instance."""
        mat_dict = super()._dict_repr
        mat_dict['chemical_structure'] = self._chemical_structure
        mat_dict['density'] = f'{self.density.raw_value:.2e} {self.density.unit}'
        return mat_dict

    def as_dict(self, skip: list = []) -> dict[str, str]:
        """Produces a cleaned dict using a custom as_dict method to skip necessary things.
        The resulting dict matches the paramters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        this_dict = super().as_dict(skip=skip)
        # From Material
        del this_dict['sld']
        del this_dict['isld']
        # Determined in __init__
        del this_dict['scattering_length_real']
        del this_dict['scattering_length_imag']
        del this_dict['molecular_weight']
        return this_dict
