__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy
from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj

MATERIAL_DETAILS = {
    'sld_value': {
        'description': 'The real scattering length density for a material in e-6 per squared angstrom.',
        'url':         'https://www.ncnr.nist.gov/resources/activation/',
        'value':       4.186,
        'units':       '1 / angstrom ** 2',
        'min':         -np.Inf,
        'max':         np.Inf,
        'fixed':       True
    },
    'isld_value':  {
        'description': 'The imaginary scattering length density for a material in e-6 per squared angstrom.',
        'url':         'https://www.ncnr.nist.gov/resources/activation/',
        'value':       0.0,
        'units':       '1 / angstrom ** 2',
        'min':         -np.Inf,
        'max':         np.Inf,
        'fixed':       True
    }
}


class Material(BaseObj):
    def __init__(self, sld_value: Parameter, isld_value: Parameter, label: str='easyMaterial', interface=None):
        super().__init__(label, sld_value=sld_value, isld_value=isld_value)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Material": 
        """
        Default constructor for the reflectometry material. 

        :return: Default material container
        :rtype: Material
        """
        sld_value = Parameter('sld_value', **MATERIAL_DETAILS['sld_value'])
        isld_value = Parameter('isld_value', **MATERIAL_DETAILS['isld_value'])
        return cls(sld_value, isld_value, interface=interface)

    @classmethod
    def from_pars(cls, sld_value: float, isld_value: float, label: str='easyMaterial', interface=None) -> "Material":
        """
        Constructor of a reflectometry material where the parameters are known.

        :param sld_value: Real scattering length density
        :type sld_value: float
        :param isld_value: Imaginary scattering length density
        :type isld_value: float
        :return: Material container
        :rtype: Material
        """
        default_options = deepcopy(MATERIAL_DETAILS)
        del default_options['sld_value']['value']
        del default_options['isld_value']['value']

        sld_value = Parameter('sld_value', sld_value, **default_options['sld_value'])
        isld_value = Parameter('isld_value', isld_value, **default_options['isld_value'])

        return cls(sld_value=sld_value, isld_value=isld_value, label=label, interface=interface)

    # Dynamic properties
    @property
    def sld(self) -> float:
        """
        Get the *sld_value* parameter.

        :return: *sld_value* parameter
        :rtype: float
        """
        return self.sld_value.raw_value

    @sld.setter
    def sld(self, new_sld_value: float): 
        """
        Set the *sld_value* parameter.

        :param new_sld_value: new *sld_value* lattice parameter
        :type new_sld_value: float
        :return: noneType
        :rtype: None
        """
        self.sld_value.raw_value = new_sld_value

    @property
    def isld(self) -> float:
        """
        Get the *isld_value* parameter.

        :return: *isld_value* parameter
        :rtype: float
        """
        return self.isld_value.raw_value

    @isld.setter
    def isld(self, new_isld_value: float): 
        """
        Set the *isld_value* parameter.

        :param new_isld_value: new *isld_value* lattice parameter
        :type new_isld_value: float
        :return: noneType
        :rtype: None
        """
        self.isld_value.raw_value = new_isld_value
