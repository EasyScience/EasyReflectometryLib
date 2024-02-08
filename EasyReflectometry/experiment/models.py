__author__ = 'github.com/arm61'
import yaml
from easyCore.Objects.Groups import BaseCollection

from EasyReflectometry.experiment.model import Model


class Models(BaseCollection):

    def __init__(self,
                 *args: list[Model],
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
                  *args: list[Model],
                  name: str = 'EasyModels',
                  interface=None) -> 'Models':
        """
        Constructor for the models where models are being given.

        :param args: The series of models
        :return: Models container
        """
        return cls(*args, name=name, interface=interface)

    def add_model(self, new_model: Model):
        """
        Add a model to the models.

        :param new_model: New model to be added.
        """
        self.append(new_model)

    def remove_model(self, idx: int):
        """
        Remove an model from the models.

        :param idx: Index of the model to remove
        """
        del self[idx]

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
