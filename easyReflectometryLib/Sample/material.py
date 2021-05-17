__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy

from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj

MATERIAL_DETAILS = {
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


class Material(BaseObj):
    def __init__(self,
                 sld: Parameter,
                 isld: Parameter,
                 name: str = 'easyMaterial',
                 interface=None):
        super().__init__(name, sld=sld, isld=isld)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Material":
        """
        Default constructor for the reflectometry material. 

        :return: Default material container
        :rtype: Material
        """
        sld = Parameter('sld', **MATERIAL_DETAILS['sld'])
        isld = Parameter('isld', **MATERIAL_DETAILS['isld'])
        return cls(sld, isld, interface=interface)

    @classmethod
    def from_pars(cls,
                  sld: float,
                  isld: float,
                  name: str = 'easyMaterial',
                  interface=None) -> "Material":
        """
        Constructor of a reflectometry material where the parameters are known.

        :param sld: Real scattering length density
        :type sld: float
        :param isld: Imaginary scattering length density
        :type isld: float
        :return: Material container
        :rtype: Material
        """
        default_options = deepcopy(MATERIAL_DETAILS)
        del default_options['sld']['value']
        del default_options['isld']['value']

        sld = Parameter('sld', sld, **default_options['sld'])
        isld = Parameter('isld', isld, **default_options['isld'])

        return cls(sld=sld, isld=isld, name=name, interface=interface)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the material.

        :return: a string representation of the material
        :rtype: str
        """
        return f"<{self.name}: (sld: {self.sld.raw_value:.3f}e-6 {self.sld.unit:~P}, isld: {self.isld.raw_value:.3f}e-6 {self.isld.unit:~P})>"

    # Copying
    def copy(self) -> "Material":
        """
        Get a copy of the material.

        :return: A copy of the material
        :rtype: Material
        """
        return deepcopy(self)
