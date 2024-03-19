from __future__ import annotations

__author__ = 'github.com/arm61'

from copy import deepcopy

import yaml
from easyCore import np
from easyCore.Objects.ObjectClasses import BaseObj
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.sample import Layer
from EasyReflectometry.sample import LayerCollection
from EasyReflectometry.sample import Multilayer
from EasyReflectometry.sample import RepeatingMultilayer
from EasyReflectometry.sample import Sample

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
    """Model is the class that represents the experiment.
    It is used to store the information about the experiment and to perform the calculations.
    """

    def __init__(
        self,
        sample: Sample,
        scale: Parameter,
        background: Parameter,
        resolution: Parameter,
        name: str = 'EasyModel',
        interface=None,
    ):
        """Constructor.

        :param sample: The sample being modelled.
        :param scale: Scaling factor of profile.
        :param background: Linear background magnitude.
        :param resolution: Constant resolution smearing percentage.
        :param name: Name of the model, defaults to 'EasyModel'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.

        """
        super().__init__(
            name=name,
            sample=sample,
            scale=scale,
            background=background,
            resolution=resolution,
        )
        self.interface = interface

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> Model:
        """Default instance of the reflectometry experiment model.

        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        sample = Sample.default()
        scale = Parameter('scale', **LAYER_DETAILS['scale'])
        background = Parameter('background', **LAYER_DETAILS['background'])
        resolution = Parameter('resolution', **LAYER_DETAILS['resolution'])
        return cls(sample, scale, background, resolution, interface=interface)

    @classmethod
    def from_pars(
        cls,
        sample: Sample,
        scale: Parameter,
        background: Parameter,
        resolution: Parameter,
        name: str = 'EasyModel',
        interface=None,
    ) -> Model:
        """Instance of a reflectometry experiment model where the parameters are known.

        :param sample: The sample being modelled.
        :param scale: Scaling factor of profile.
        :param background: Linear background magnitude.
        :param resolution: Constant resolution smearing percentage.
        :param name: Name of the layer, defaults to 'EasyModel'.
        :param interface: Calculator interface, defaults to :py:attr:`None`.
        """
        default_options = deepcopy(LAYER_DETAILS)
        del default_options['scale']['value']
        del default_options['background']['value']
        del default_options['resolution']['value']

        scale = Parameter('scale', scale, **default_options['scale'])
        background = Parameter('background', background, **default_options['background'])
        resolution = Parameter('resolution', resolution, **default_options['resolution'])

        return cls(
            sample=sample,
            scale=scale,
            background=background,
            resolution=resolution,
            name=name,
            interface=interface,
        )

    def add_item(self, *items: Layer | RepeatingMultilayer) -> None:
        """Add a layer or item to the model sample.

        :param items: Layers or items to add to model sample.
        """
        for arg in items:
            if issubclass(arg.__class__, Multilayer):
                self.sample.append(arg)
                if self.interface is not None:
                    self.interface().add_item_to_model(arg.uid, self.uid)

    def duplicate_item(self, idx: int) -> None:
        """Duplicate a given item or layer in a sample.

        :param idx: Index of the item or layer to duplicate
        """
        to_duplicate = self.sample[idx]
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
            LayerCollection.from_pars(*duplicate_layers, name=to_duplicate.layers.name + ' duplicate'),
            name=to_duplicate.name + ' duplicate',
        )
        self.add_item(duplicate)

    def remove_item(self, idx: int) -> None:
        """Remove an item from the model.

        :param idx: Index of the item to remove.
        """
        if self.interface is not None:
            self.interface().remove_item_from_model(self.sample[idx].uid, self.uid)
        del self.sample[idx]

    @property
    def uid(self) -> int:
        """Return a UID from the borg map."""
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, dict[str, str]]:
        """A simplified dict representation."""
        return {
            self.name: {
                'scale': self.scale.raw_value,
                'background': self.background.raw_value,
                'resolution': f'{self.resolution.raw_value} %',
                'sample': self.sample._dict_repr,
            }
        }

    def __repr__(self) -> str:
        """String representation of the layer."""
        return yaml.dump(self._dict_repr, sort_keys=False)
