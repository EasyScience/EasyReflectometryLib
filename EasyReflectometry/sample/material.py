__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from collections import defaultdict
from copy import deepcopy

import yaml
from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj
from easyCore.Fitting.Constraints import FunctionalConstraint

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


class MaterialMixture(Material):

    def __init__(self,
                 sld: Parameter,
                 isld: Parameter,
                 material_a: Material,
                 material_b: Material,
                 fraction: Parameter,
                 name: str = "EasyMaterialMixture",
                 interface=None):
        constraint = FunctionalConstraint(sld, self.weighted_average_sld,
                                          [material_a.sld, material_b.sld, fraction])
        material_a.sld.user_constraints['sld'] = constraint
        material_b.sld.user_constraints['sld'] = constraint
        fraction.user_constraints['sld'] = constraint
        iconstraint = FunctionalConstraint(isld, self.weighted_average_sld,
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
        default_options = deepcopy(MATERIAL_DEFAULTS)
        del default_options['sld']['value']
        del default_options['isld']['value']
        sld = Parameter(
            'sld',
            MaterialMixture.weighted_average_sld(material_a.sld.raw_value,
                                                 material_b.sld.raw_value,
                                                 fraction.raw_value),
            **default_options['sld'])
        isld = Parameter(
            'sld',
            MaterialMixture.weighted_average_sld(material_a.isld.raw_value,
                                                 material_b.isld.raw_value,
                                                 fraction.raw_value),
            **default_options['isld'])
        return cls(sld, isld, material_a, material_b, fraction, interface=interface)

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
        del default_options['sld']['value']
        del default_options['isld']['value']
        sld = Parameter(
            'sld',
            MaterialMixture.weighted_average_sld(material_a.sld.raw_value,
                                                 material_b.sld.raw_value,
                                                 fraction.raw_value),
            **default_options['sld'])
        isld = Parameter(
            'sld',
            MaterialMixture.weighted_average_sld(material_a.isld.raw_value,
                                                 material_b.isld.raw_value,
                                                 fraction.raw_value),
            **default_options['isld'])

        return cls(sld=sld,
                   isld=isld,
                   material_a=material_a,
                   material_b=material_b,
                   fraction=fraction,
                   name=name,
                   interface=interface)

    @staticmethod
    def weighted_average_sld(a: Parameter, b: Parameter, p: Parameter) -> Parameter:
        """
        Determine the weighted average SLD between a and b, where p is the weight.
        
        :param a: First sld
        :param b: Second sld
        :param p: Weight
        :return: Weighted average
        """
        return a * (1 - p) + b * p

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
                'sld': f'{self.sld.raw_value}e-6 {self.sld.unit}',
                'isld': f'{self.isld.raw_value}e-6 {self.isld.unit}',
                'material1': self.material_a._dict_repr,
                'material2': self.material_b._dict_repr
            }
        }

    def __repr__(self) -> dict:
        """
        String representation of the material mixture.

        :return: a string representation of the material mixture
        """
        return yaml.dump(self._dict_repr, sort_keys=False)
