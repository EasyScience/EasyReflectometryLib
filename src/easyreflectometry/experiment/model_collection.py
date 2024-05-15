__author__ = 'github.com/arm61'

from typing import Optional

from easyreflectometry.sample.base_element_collection import SIZE_DEFAULT_COLLECTION
from easyreflectometry.sample.base_element_collection import BaseElementCollection

from .model import Model


class ModelCollection(BaseElementCollection):
    # Added in super().__init__
    models: list[Model]

    def __init__(
        self,
        *models: Optional[list[Model]],
        name: str = 'EasyModels',
        interface=None,
        **kwargs,
    ):
        if models == ():
            models = [Model(interface=interface) for _ in range(SIZE_DEFAULT_COLLECTION)]
        super().__init__(name, interface, *models, **kwargs)
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
