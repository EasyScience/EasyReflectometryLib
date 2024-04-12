__author__ = 'github.com/arm61'

from typing import Union

import yaml
from easyCore.Objects.Groups import BaseCollection

from .model import Model


class Models(BaseCollection):
    def __init__(self, *models: Union[list[Model], None], name: str = 'EasyModels', interface=None, **kwargs):
        if models is None:
            models = [Model(), Model()]
        super().__init__(name, *models, **kwargs)
        self.interface = interface

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
