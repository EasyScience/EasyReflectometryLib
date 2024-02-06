__author__ = 'github.com/arm61'

from copy import deepcopy
from typing import Union

import yaml
from easyCore import np
from easyCore.Objects.ObjectClasses import BaseObj
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.sample.items import MultiLayer
from EasyReflectometry.sample.items import RepeatingMultiLayer
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.layers import Layers
from EasyReflectometry.sample.structure import Structure

LAYER_DETAILS = {
    'scale': {
        'description': 'Scaling of the reflectomety profile',
        'url': 'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 1.0,
        'min': 0,
        'max': np.Inf,
        'fixed': True,
    },
    'background': {
        'description': 'Linear background to include in reflectometry data',
        'url': 'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 1e-8,
        'min': 0.0,
        'max': np.Inf,
        'fixed': True,
    },
    'resolution': {
        'description': 'Percentage constant dQ/Q resolution smearing.',
        'url': 'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 5.0,
        'min': 0.0,
        'max': 100.0,
        'fixed': True,
    },
}


class Model(BaseObj):
    def __init__(
        self,
        structure: Structure,
        scale: Parameter,
        background: Parameter,
        resolution: Parameter,
        name: str = 'EasyModel',
        interface=None,
    ):
        super().__init__(
            name,
            structure=structure,
            scale=scale,
            background=background,
            resolution=resolution,
        )
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> 'Model':
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
    def from_pars(
        cls,
        structure: Structure,
        scale: Parameter,
        background: Parameter,
        resolution: Parameter,
        name: str = 'EasyModel',
        interface=None,
    ) -> 'Model':
        """
        Constructor of a reflectometry experiment model where the parameters are known.

        :param structure: The structure being modelled
        :param scale: Scaling factor of profile
        :param background: Linear background magnitude
        :param background: Constant resolution smearing percentage
        :return: Model container
        """
        default_options = deepcopy(LAYER_DETAILS)
        del default_options['scale']['value']
        del default_options['background']['value']
        del default_options['resolution']['value']

        scale = Parameter('scale', scale, **default_options['scale'])
        background = Parameter('background', background, **default_options['background'])
        resolution = Parameter('resolution', resolution, **default_options['resolution'])

        return cls(
            structure=structure,
            scale=scale,
            background=background,
            resolution=resolution,
            name=name,
            interface=interface,
        )

    def add_item(self, *items: Union[Layer, RepeatingMultiLayer]):
        """
        Add a layer or item to the model structure.

        :param *items: Layers or items to add to model structure
        """
        for arg in items:
            if issubclass(arg.__class__, MultiLayer):
                self.structure.append(arg)
                if self.interface is not None:
                    self.interface().add_item_to_model(arg.uid, self.uid)

    def duplicate_item(self, idx: int):
        """
        Duplicate a given item or layer in a structure.

        :param idx: Index of the item or layer to duplicate
        """
        to_duplicate = self.structure[idx]
        duplicate_layers = []
        for i in to_duplicate.layers:
            duplicate_layers.append(
                Layer.from_pars(
                    material=i.material,
                    thickness=i.thickness.raw_value,
                    roughness=i.roughness.raw_value,
                    name=i.name + ' duplicate',
                )
            )
        duplicate = to_duplicate.__class__.from_pars(
            Layers.from_pars(*duplicate_layers, name=to_duplicate.layers.name + ' duplicate'),
            name=to_duplicate.name + ' duplicate',
        )
        self.add_item(duplicate)

    def remove_item(self, idx):
        """
        Remove an item from the model.

        :param idx: Index of the item to remove
        :type idx: int
        """
        if self.interface is not None:
            self.interface().remove_item_from_model(self.structure[idx].uid, self.uid)
        del self.structure[idx]

    @property
    def uid(self):
        """
        Return a UID from the borg map
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
                'scale': self.scale.raw_value,
                'background': self.background.raw_value,
                'resolution': f'{self.resolution.raw_value} %',
                'structure': self.structure._dict_repr,
            }
        }

    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return yaml.dump(self._dict_repr, sort_keys=False)
