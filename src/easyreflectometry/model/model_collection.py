from __future__ import annotations

__author__ = 'github.com/arm61'

from typing import List
from typing import Tuple

from easyreflectometry.sample.collections.base_collection import BaseCollection

from .model import Model


class ModelCollection(BaseCollection):
    def __init__(
        self,
        *models: Tuple[Model],
        name: str = 'EasyModels',
        interface=None,
        populate_if_none: bool = True,
        **kwargs,
    ):
        if not models:
            if populate_if_none:
                models = [Model(interface=interface)]
            else:
                models = []
        # Needed to ensure an empty list is created when saving and instatiating the object as_dict -> from_dict
        # Else collisions might occur in global_object.map
        self.populate_if_none = False

        super().__init__(name, interface, *models, **kwargs)

    def add_model(self, new_model: Model):
        """
        Add a model to the models.

        :param new_model: New model to be added.
        """
        self.append(new_model)

    def remove_model(self, index: int):
        """
        Remove an model from the models.

        :param index: Index of the model to remove
        """
        self.pop(index)

    def as_dict(self, skip: List[str] | None = None) -> dict:
        this_dict = super().as_dict(skip=skip)
        this_dict['populate_if_none'] = self.populate_if_none
        return this_dict

    @classmethod
    def from_dict(cls, this_dict: dict) -> ModelCollection:
        """
        Create an instance of a collection from a dictionary.

        :param data: The dictionary for the collection
        :return: An instance of the collection
        """
        collection_dict = this_dict.copy()
        # We neeed to call from_dict on the base class to get the models
        dict_data = collection_dict['data']
        del collection_dict['data']

        collection = super().from_dict(collection_dict)  # type: ModelCollection

        for model_data in dict_data:
            collection.add_model(Model.from_dict(model_data))

        if len(collection) != len(this_dict['data']):
            raise ValueError(f"Expected {len(collection)} models, got {len(this_dict['data'])}")

        return collection
