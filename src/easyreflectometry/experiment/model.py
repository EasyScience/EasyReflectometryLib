from __future__ import annotations

__author__ = 'github.com/arm61'

from numbers import Number
from typing import Union

import numpy as np
import yaml
from easyscience.Objects.ObjectClasses import BaseObj
from easyscience.Objects.ObjectClasses import Parameter

from easyreflectometry.parameter_utils import get_as_parameter
from easyreflectometry.sample import BaseAssembly
from easyreflectometry.sample import Layer
from easyreflectometry.sample import LayerCollection
from easyreflectometry.sample import Sample

from .resolution_functions import PercentageFhwm
from .resolution_functions import ResolutionFunction

DEFAULTS = {
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
        'value': 5.0,
    },
}


class Model(BaseObj):
    """Model is the class that represents the experiment.
    It is used to store the information about the experiment and to perform the calculations.
    """

    # Added in super().__init__
    name: str
    sample: Sample
    scale: Parameter
    background: Parameter

    def __init__(
        self,
        sample: Union[Sample, None] = None,
        scale: Union[Parameter, Number, None] = None,
        background: Union[Parameter, Number, None] = None,
        resolution_function: Union[ResolutionFunction, None] = None,
        name: str = 'EasyModel',
        interface=None,
    ):
        """Constructor.

        :param sample: The sample being modelled.
        :param scale: Scaling factor of profile.
        :param background: Linear background magnitude.
        :param name: Name of the model, defaults to 'EasyModel'.
        :param resolution_function: Resolution function, defaults to PercentageFhwm.
        :param interface: Calculator interface, defaults to `None`.

        """

        if sample is None:
            sample = Sample(interface=interface)
        if resolution_function is None:
            resolution_function = PercentageFhwm(DEFAULTS['resolution']['value'])

        scale = get_as_parameter('scale', scale, DEFAULTS)
        background = get_as_parameter('background', background, DEFAULTS)

        super().__init__(
            name=name,
            sample=sample,
            scale=scale,
            background=background,
        )
        self.resolution_function = resolution_function
        # Must be set after resolution function
        self.interface = interface

    def add_item(self, *assemblies: list[BaseAssembly]) -> None:
        """Add a layer or item to the model sample.

        :param assemblies: Assemblies to add to model sample.
        """
        for arg in assemblies:
            if issubclass(arg.__class__, BaseAssembly):
                self.sample.append(arg)
                if self.interface is not None:
                    self.interface().add_item_to_model(arg.uid, self.uid)
            else:
                raise ValueError(f'Object {arg} is not a valid type, must be a child of BaseAssembly.')

    def duplicate_item(self, idx: int) -> None:
        """Duplicate a given item or layer in a sample.

        :param idx: Index of the item or layer to duplicate
        """
        to_duplicate = self.sample[idx]
        duplicate_layers = []
        for i in to_duplicate.layers:
            duplicate_layers.append(
                Layer(
                    material=i.material,
                    thickness=i.thickness.raw_value,
                    roughness=i.roughness.raw_value,
                    name=i.name + ' duplicate',
                    interface=i.interface,
                )
            )
        duplicate = to_duplicate.__class__(
            LayerCollection(*duplicate_layers, name=to_duplicate.layers.name + ' duplicate'),
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
    def resolution_function(self) -> ResolutionFunction:
        """Return the resolution function."""
        return self._resolution_function

    @resolution_function.setter
    def resolution_function(self, resolution_function: ResolutionFunction) -> None:
        """Set the resolution function for the model."""
        self._resolution_function = resolution_function
        if self.interface is not None:
            self.interface().set_resolution_function(self._resolution_function)

    @property
    def interface(self):
        """
        Get the current interface of the object
        """
        return self._interface

    @interface.setter
    def interface(self, new_interface) -> None:
        """Set the interface for the model."""
        # From super class
        self._interface = new_interface
        if new_interface is not None:
            self.generate_bindings()
            self._interface().set_resolution_function(self._resolution_function)

    @property
    def uid(self) -> int:
        """Return a UID from the borg map."""
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, dict[str, str]]:
        """A simplified dict representation."""
        if isinstance(self._resolution_function, PercentageFhwm):
            resolution_value = self._resolution_function.as_dict()['constant']
            resolution = f'{resolution_value} %'
        else:
            resolution = 'function of Q'

        return {
            self.name: {
                'scale': self.scale.raw_value,
                'background': self.background.raw_value,
                'resolution': resolution,
                'sample': self.sample._dict_repr,
            }
        }

    def __repr__(self) -> str:
        """String representation of the layer."""
        return yaml.dump(self._dict_repr, sort_keys=False)

    def as_dict(self, skip: list = None) -> dict:
        """Produces a cleaned dict using a custom as_dict method to skip necessary things.
        The resulting dict matches the parameters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        this_dict['sample'] = self.sample.as_dict(skip=skip)
        this_dict['resolution_function'] = self.resolution_function.as_dict()
        return this_dict

    @classmethod
    def from_dict(cls, this_dict: dict) -> Model:
        """
        Create a Model from a dictionary.

        :param this_dict: dictionary of the Model
        :return: Model
        """
        resolution_function = ResolutionFunction.from_dict(this_dict['resolution_function'])
        del this_dict['resolution_function']
        sample = Sample.from_dict(this_dict['sample'])
        del this_dict['sample']

        model = super().from_dict(this_dict)

        model.sample = sample
        model.resolution_function = resolution_function
        return model
