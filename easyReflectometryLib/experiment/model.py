__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from copy import deepcopy

from easyCore import np
from easyCore.Objects.Base import Parameter, BaseObj
from easyReflectometryLib.sample.structure import Structure

LAYER_DETAILS = {
    'scale': {
        'description': 'Scaling of the reflectomety profile',
        'url':
        'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 1.0,
        'min': 0,
        'max': np.Inf,
        'fixed': True
    },
    'background': {
        'description':
        'Linear background to include in reflectometry data',
        'url': 'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 1e-7,
        'min': 0.0,
        'max': np.Inf,
        'fixed': True
    },
    'resolution': {
        'description':
        'Percentage constant dQ/Q resolution smearing.',
        'url': 'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 5.0,
        'min': 0.0,
        'max': np.Inf,
        'fixed': True
    }
}


class Model(BaseObj):
    def __init__(self,
                 structure: Structure,
                 scale: Parameter,
                 background: Parameter,
                 resolution: Parameter,
                 name: str = 'easyModel',
                 interface=None):
        super().__init__(name,
                         structure=structure,
                         scale=scale,
                         background=background,
                         resolution=resolution)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Model":
        """
        Default constructor for the reflectometry experiment model. 

        :return: Default model container
        :rtype: Model
        """
        structure = Structure.default()
        scale = Parameter('scale', **LAYER_DETAILS['scale'])
        background = Parameter('background', **LAYER_DETAILS['background'])
        resolution = Parameter('resolution', **LAYER_DETAILS['resolution'])
        return cls(structure, scale, background, resolution, interface=interface)

    @classmethod
    def from_pars(cls,
                  structure: Structure,
                  scale: Parameter,
                  background: Parameter,
                  resolution: Parameter,
                  name: str = 'easyModel',
                  interface=None) -> "Model":
        """
        Constructor of a reflectometry experiment model where the parameters are known.

        :param structure: The structure being modelled
        :type structure: easyReflectometryLib.structure.Structure
        :param scale: Scaling factor of profile
        :type scale: float
        :param background: Linear background magnitude
        :type background: float
        :param background: Constant resolution smearing percentage 
        :type background: float
        :return: Model container
        :rtype: Model
        """
        default_options = deepcopy(LAYER_DETAILS)
        del default_options['scale']['value']
        del default_options['background']['value']
        del default_options['resolution']['value']

        scale = Parameter('scale', scale,
                              **default_options['scale'])
        background = Parameter('background', background,
                              **default_options['background'])
        resolution = Parameter('resolution', resolution,
                              **default_options['resolution'])

        return cls(structure=structure,
                   scale=scale,
                   background=background,
                   resolution=resolution,
                   name=name,
                   interface=interface)

    # Representation
    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return f"<{self.name}: (structure: {self.structure.name}, scale: {self.scale.raw_value:.3f}, background: {self.background.raw_value:.3e}, resolution: {self.resolution.raw_value:.2f})>"