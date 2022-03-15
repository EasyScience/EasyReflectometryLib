__author__ = 'github.com/arm61'

from ast import Param
from email.policy import default
import re
from typing import ClassVar
from copy import deepcopy

import yaml
from easyCore import np
from easyCore.Objects.ObjectClasses import Parameter, BaseObj
from easyCore.Fitting.Constraints import FunctionalConstraint

from EasyReflectometry.special.calculations import weighted_average_sld, neutron_scattering_length, molecular_weight, density_to_sld

MATERIAL_DEFAULTS = {
    'sld': {
        'description':
        'The real scattering length density for a material in e-6 per squared angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 4.186,
        'units': '1 / angstrom ** 2',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True
    },
    'isld': {
        'description':
        'The imaginary scattering length density for a material in e-6 per squared angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 0.0,
        'units': '1 / angstrom ** 2',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True
    }
}

MATERIALDENSITY_DEFAULTS = {
    'chemical_structure': 'Si',
    'sl': {
        'description': 'The real scattering length for a chemical formula in angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 4.1491,
        'units': 'angstrom',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True
    },
    'isl': {
        'description': 'The real scattering length for a chemical formula in angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 0.0,
        'units': 'angstrom',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True
    },
    'density': {
        'description': 'The mass density of the material.',
        'url': 'https://en.wikipedia.org/wiki/Density',
        'value': 2.33,
        'units': 'gram / centimeter ** 3',
        'min': 0,
        'max': np.Inf,
        'fixed': True
    },
    'molecular_weight': {
        'description': 'The molecular weight of a material.',
        'url': 'https://en.wikipedia.org/wiki/Molecular_mass',
        'value': 28.02,
        'units': 'g / mole',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True
    }
}

MATERIALMIXTURE_DEFAULTS = {
    'fraction': {
        'description': 'The fraction of material b in material a',
        'value': 0.5,
        'units': 'dimensionless',
        'min': 0,
        'max': 1,
        'fixed': True
    }
}


class Material(BaseObj):

    sld: ClassVar[Parameter]
    isld: ClassVar[Parameter]

    def __init__(self,
                 sld: Parameter,
                 isld: Parameter,
                 name: str = 'EasyMaterial',
                 interface=None):
        super().__init__(name, sld=sld, isld=isld)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Material":
        """
        Default constructor for the reflectometry material. 

        :return: Default material container
        """
        sld = Parameter('sld', **MATERIAL_DEFAULTS['sld'])
        isld = Parameter('isld', **MATERIAL_DEFAULTS['isld'])
        return cls(sld, isld, interface=interface)

    @classmethod
    def from_pars(cls,
                  sld: float,
                  isld: float,
                  name: str = 'EasyMaterial',
                  interface=None) -> "Material":
        """
        Constructor of a reflectometry material where the parameters are known.

        :param sld: Real scattering length density
        :param isld: Imaginary scattering length density
        :return: Material container
        """
        default_options = deepcopy(MATERIAL_DEFAULTS)
        del default_options['sld']['value']
        del default_options['isld']['value']

        sld = Parameter('sld', sld, **default_options['sld'])
        isld = Parameter('isld', isld, **default_options['isld'])

        return cls(sld=sld, isld=isld, name=name, interface=interface)

    @property
    def uid(self) -> int:
        """
        Return a UID from the borg map.

        :return: Unique id
        """
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation. 
        
        :return: Simple dictionary
        """
        return {
            self.name: {
                'sld': f'{self.sld.raw_value:.3f}e-6 {self.sld.unit}',
                'isld': f'{self.isld.raw_value:.3f}e-6 {self.isld.unit}'
            }
        }

    def __repr__(self) -> str:
        """
        Representation of the material.

        :return: Dictionary representation of the material
        """
        return yaml.dump(self._dict_repr, sort_keys=False)


class MaterialDensity(Material):

    density: ClassVar[Parameter]

    def __init__(self,
                 chemical_structure: str,
                 density: Parameter,
                 name: str = 'EasyMaterialDensity',
                 interface=None) -> 'MaterialDensity':
        """
        :param chemical_structure: Chemical formula for the material
        :param density: Mass density for the material
        :param name: Identifier, defaults to :py:attr:`EasyMaterialDensity`
        :param interface: Interface object, defaults to :py:attr:`None`
        """
        scattering_length = neutron_scattering_length(chemical_structure)
        default_options = deepcopy(MATERIALDENSITY_DEFAULTS)
        del default_options['molecular_weight']['value']
        del default_options['sl']['value']
        del default_options['isl']['value']
        mw = Parameter('molecular_weight', molecular_weight(chemical_structure),
                       **default_options['molecular_weight'])
        scattering_length_real = Parameter('scattering_length_real',
                                           scattering_length.real,
                                           **default_options['sl'])
        scattering_length_imag = Parameter('scattering_length_imag',
                                           scattering_length.imag,
                                           **default_options['isl'])
        default_options = deepcopy(MATERIAL_DEFAULTS)
        del default_options['sld']['value']
        del default_options['isld']['value']
        sld = Parameter(
            'sld',
            density_to_sld(scattering_length_real.raw_value, mw.raw_value,
                           density.raw_value), **default_options['sld'])
        isld = Parameter(
            'isld',
            density_to_sld(scattering_length_imag.raw_value, mw.raw_value,
                           density.raw_value), **default_options['isld'])

        constraint = FunctionalConstraint(sld, density_to_sld,
                                          [scattering_length_real, mw, density])
        scattering_length_real.user_constraints['sld'] = constraint
        mw.user_constraints['sld'] = constraint
        density.user_constraints['sld'] = constraint
        iconstraint = FunctionalConstraint(isld, density_to_sld,
                                           [scattering_length_imag, mw, density])
        scattering_length_imag.user_constraints['isld'] = iconstraint
        mw.user_constraints['isld'] = iconstraint
        density.user_constraints['isld'] = iconstraint

        super().__init__(sld, isld, name=name, interface=interface)

        self._add_component('scattering_length_real', scattering_length_real)
        self._add_component('scattering_length_imag', scattering_length_imag)
        self._add_component('molecular_weight', mw)
        self._add_component('density', density)
        self.chemical_structure = chemical_structure
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> 'MaterialDensity':
        """
        Default constructor for the material defined by density and chemical structure. 
        
        :param interface: Interface object, defaults to :py:attr:`None`
        :return: Material container
        """
        density = Parameter('density', **MATERIALDENSITY_DEFAULTS['density'])
        return cls(MATERIALDENSITY_DEFAULTS['chemical_structure'],
                   density,
                   interface=interface)

    @classmethod
    def from_pars(cls,
                  chemical_structure: str,
                  density: float,
                  name: str = 'EasyMaterialDensity',
                  interface=None) -> 'MaterialDensity':
        """
        Constructor for a material based on the mass density and chemical structure, where these are known.
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
    def _dict_repr(self) -> dict:
        """
        Dictionary representation of the :py:class:`MaterialDensity` object.
        
        :return: Simple dictionary
        """
        mat_dict = super()._dict_repr
        mat_dict['chemical_structure'] = self.chemical_structure
        mat_dict['density'] = f'{self.density.raw_value:.2e} {self.density.unit}'
        return mat_dict


class MaterialMixture(Material):

    material_a: ClassVar[Material]
    material_b: ClassVar[Material]
    fraction: ClassVar[Parameter]

    def __init__(self,
                 material_a: Material,
                 material_b: Material,
                 fraction: Parameter,
                 name: str = "EasyMaterialMixture",
                 interface=None):
        default_options = deepcopy(MATERIAL_DEFAULTS)
        del default_options['sld']['value']
        del default_options['isld']['value']
        sld = Parameter(
            'sld',
            weighted_average_sld(material_a.sld.raw_value, material_b.sld.raw_value,
                                 fraction.raw_value), **default_options['sld'])
        isld = Parameter(
            'sld',
            weighted_average_sld(material_a.isld.raw_value, material_b.isld.raw_value,
                                 fraction.raw_value), **default_options['isld'])
        constraint = FunctionalConstraint(sld, weighted_average_sld,
                                          [material_a.sld, material_b.sld, fraction])
        material_a.sld.user_constraints['sld'] = constraint
        material_b.sld.user_constraints['sld'] = constraint
        fraction.user_constraints['sld'] = constraint
        iconstraint = FunctionalConstraint(isld, weighted_average_sld,
                                           [material_a.isld, material_b.isld, fraction])
        material_a.isld.user_constraints['isld'] = iconstraint
        material_b.isld.user_constraints['isld'] = iconstraint
        fraction.user_constraints['isld'] = iconstraint
        super().__init__(sld, isld, name, interface)
        self._add_component('material_a', material_a)
        self._add_component('material_b', material_b)
        self._add_component('fraction', fraction)
        self.interface = interface

    #Class constructors
    @classmethod
    def default(cls, interface=None) -> "MaterialMixture":
        """
        Default constructor for a mixture of two materials.
        
        :return: Default material mixture container.
        """
        material_a = Material.default()
        material_b = Material.default()
        fraction = Parameter('fraction', **MATERIALMIXTURE_DEFAULTS['fraction'])
        return cls(material_a, material_b, fraction, interface=interface)

    @classmethod
    def from_pars(cls,
                  material_a: Material,
                  material_b: Material,
                  fraction: float,
                  name: str = "EasyMaterialMixture",
                  interface=None) -> "MaterialMixture":
        """
        Constructor of a mixture of two materials where the parameters are known. 
        
        :param material_a: The first material
        :param material_b: The second material
        :param fraction: The fraction of material_b in material_a
        :return: MaterialMixture container.
        """
        default_options = deepcopy(MATERIALMIXTURE_DEFAULTS)
        del default_options['fraction']['value']

        fraction = Parameter('fraction', fraction, **default_options['fraction'])
        default_options = deepcopy(MATERIAL_DEFAULTS)

        return cls(material_a=material_a,
                   material_b=material_b,
                   fraction=fraction,
                   name=name,
                   interface=interface)

    @property
    def uid(self) -> int:
        """
        Return a UID from the borg map.

        :return: Unique id
        """
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation. 
        
        :return: Simple dictionary
        """
        return {
            self.name: {
                'fraction': self.fraction.raw_value,
                'sld': f'{self.sld.raw_value:.3f}e-6 {self.sld.unit}',
                'isld': f'{self.isld.raw_value:.3f}e-6 {self.isld.unit}',
                'material1': self.material_a._dict_repr,
                'material2': self.material_b._dict_repr
            }
        }
