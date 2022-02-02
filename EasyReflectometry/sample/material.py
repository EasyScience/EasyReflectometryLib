__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from collections import defaultdict
from copy import deepcopy

import yaml
from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj

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

MATERIAL_B_DEFAULTS = {
    'sld': {
        'description':
        'The real scattering length density for a material in e-6 per squared angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 6.908,
        'units': '1 / angstrom ** 2',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True
    },
    'isld': {
        'description':
        'The imaginary scattering length density for a material in e-6 per squared angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': -0.278,
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


class MaterialMixture(BaseObj):

    def __init__(self,
                 material_a: Material,
                 material_b: Material,
                 fraction: Parameter,
                 name: str = "EasyMaterialMixture",
                 interface=None):
        super().__init__(name,
                         material_a=material_a,
                         material_b=material_b,
                         fraction=fraction)
        self.interface = interface

    #Class constructors
    @classmethod
    def default(cls, interface=None) -> "MaterialMixture":
        """
        Default constructor for a mixture of two materials.
        
        :return: Default material mixture container.
        """
        material_a = Material('material_a', **MATERIAL_DEFAULTS)
        material_b = Material('material_b', **MATERIAL_B_DEFAULTS)
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
                'fraction': f'{self.fraction.raw_value}',
                'material1': self.material_a.__repr__(),
                'material2': self.material_b.__repr__()
            }
        }

    def __repr__(self) -> dict:
        """
        String representation of the material mixture.

        :return: a string representation of the material mixture
        """
        return yaml.dump(self._dict_repr, sort_keys=False)
