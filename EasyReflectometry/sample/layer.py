__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy

from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj
from EasyReflectometry.sample.material import Material

LAYER_DETAILS = {
    'thickness': {
        'description': 'The thickness of the layer in angstroms',
        'url':
        'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 10.0,
        'units': 'angstrom',
        'min': 0.0,
        'max': np.Inf,
        'fixed': True
    },
    'roughness': {
        'description':
        'The interfacial roughness, Nevot-Croce, for the layer in angstroms.',
        'url': 'https://doi.org/10.1051/rphysap:01980001503076100',
        'value': 3.3,
        'units': 'angstrom',
        'min': 0.0,
        'max': np.Inf,
        'fixed': True
    }
}


class Layer(BaseObj):

    def __init__(self,
                 material: Material,
                 thickness: Parameter,
                 roughness: Parameter,
                 name: str = 'easyLayer',
                 interface=None):
        super().__init__(name,
                         material=material,
                         thickness=thickness,
                         roughness=roughness)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Layer":
        """
        Default constructor for the reflectometry layer. 

        :return: Default layer container
        :rtype: Layer
        """
        material = Material.default()
        thickness = Parameter('thickness', **LAYER_DETAILS['thickness'])
        roughness = Parameter('roughness', **LAYER_DETAILS['roughness'])
        return cls(material, thickness, roughness, interface=interface)

    @classmethod
    def from_pars(cls,
                  material: Material,
                  thickness: float,
                  roughness: float,
                  name: str = 'easyLayer',
                  interface=None) -> "Layer":
        """
        Constructor of a reflectometry layer where the parameters are known.

        :param material: The material that makes up the layer
        :type material: EasyReflectometry.material.Material
        :param thickness: Layer thickness in angstrom
        :type thickness: float
        :param roughness: Layer roughness in angstrom
        :type roughness: float
        :return: Layer container
        :rtype: Layer
        """
        default_options = deepcopy(LAYER_DETAILS)
        del default_options['thickness']['value']
        del default_options['roughness']['value']

        thickness = Parameter('thickness', thickness, **default_options['thickness'])
        roughness = Parameter('roughness', roughness, **default_options['roughness'])

        return cls(material=material,
                   thickness=thickness,
                   roughness=roughness,
                   name=name,
                   interface=interface)

    def assign_material(self, material):
        """
        Assign a material to the layer interface
        """
        self.material = material
        if self.interface is not None:
            self.interface().assign_material_to_layer(self.material.uid, self.uid)

    @property
    def uid(self):
        """
        Return a UID from the borg map
        """
        return self._borg.map.convert_id_to_key(self)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return f"<{self.name}: (material: {self.material.__repr__()}, thickness: {self.thickness.raw_value:.3f} {self.thickness.unit:~P}, roughness: {self.roughness.raw_value:.3f} {self.roughness.unit:~P})>"
