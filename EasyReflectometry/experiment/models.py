__author__ = 'github.com/arm61'

from copy import deepcopy
from typing import List, Union, TypeVar

import yaml
from easyCore.Objects.Groups import BaseCollection
from EasyReflectometry.experiment.model import Model


class Models(BaseCollection):

    def __init__(self,
                 *args: List[Model],
                 name: str = 'EasyModels',
                 interface=None,
                 **kwargs):
        super().__init__(name, *args, **kwargs)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> 'Models':
        """
        Default constructor for the models
        
        :return: Default models container
        """
        model1 = Model.default()
        model2 = Model.default()
        return cls(model1, model2, interface=interface)

    @classmethod
    def from_pars(cls,
                  *args: List[Model],
                  name: str = 'EasyModels',
                  interface=None) -> 'Models':
        """
        Constructor for the models where models are being given. 
        
        :param args: The series of models
        :return: Models container
        """
        return cls(*args, name=name, interface=interface)

    @property
    def uid(self) -> int:
        """
        :return: UID from borg map
        """
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation. 
        
        :return: Simple dictionary
        """
        return {self.name: [i._dict_repr for i in self]}

    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: String representation of the layer
        """
        return yaml.dump(self._dict_repr, sort_keys=False)
