__author__ = 'github.com/wardsimon'

from abc import ABCMeta
from abc import abstractmethod
from typing import Union

import numpy as np
from easyCore import borg
from easyCore.Objects.core import ComponentSerializer
from easyCore.Objects.Inferface import ItemContainer

from EasyReflectometry.experiment.model import Model
from EasyReflectometry.sample.items.multilayer import MultiLayer
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.material import Material


class CalculatorBase(ComponentSerializer, metaclass=ABCMeta):
    """
    This class is a template and defines all properties that a calculator should have.
    """

    _calculators = []
    #    _borg = borg
    #    _link = {}

    def __init_subclass__(cls, is_abstract: bool = False, **kwargs):
        """
        Initialise all subclasses so that they can be created in the factory

        :param is_abstract: Is this a subclass which shouldn't be dded
        :type is_abstract: bool
        :param kwargs: key word arguments
        :type kwargs: dict
        :return: None
        :rtype: noneType
        """
        super().__init_subclass__(**kwargs)
        if not is_abstract:
            cls._calculators.append(cls)

    @abstractmethod
    def reset_storage(self) -> None:
        """
        Reset the storage for the calculator.
        """
        ...

    @abstractmethod
    def create(self, model: Union[Material, Layer, MultiLayer, Model]) -> list[ItemContainer]:
        """
        Creation function

        :param model: Object to be created
        :return: Item containers of the objects
        """
        ...

    @abstractmethod
    def assign_material_to_layer(self, material_id: str, layer_id: str) -> None:
        """
        Assign a material to a layer.

        :param material_id: the material id
        :param layer_id: the layer id
        """
        ...

    @abstractmethod
    def add_layer_to_item(self, layer_id: str, item_id: str) -> None:
        """
        Add a layer to an item

        :param layer_id: the layer id
        :param item_id: the item id
        """
        ...

    @abstractmethod
    def remove_layer_from_item(self, layer_id: str, item_id: str) -> None:
        """
        Remove a layer from an item

        :param layer_id: the layer id
        :param item_id: the item id
        """
        ...

    @abstractmethod
    def add_item_to_model(self, item_id: str, model_id: str) -> None:
        """
        Add an item to a model

        :param item_id: the item id
        :param model_id: the model id
        """
        ...

    @abstractmethod
    def remove_item_from_model(self, item_id: str, model_id: str) -> None:
        """
        Remove an item from a model

        :param item_id: the item id
        :param model_id: the model id
        """
        ...

    @abstractmethod
    def fit_func(self, x_array: np.ndarray, model_id: str) -> np.ndarray:
        """
        Function to perform a fit

        :param x_array: points to be calculated at
        :param model_id: the model id
        :return: calculated points
        """
        ...

    @abstractmethod
    def sld_profile(self, model_id: str) -> tuple([np.ndarray, np.ndarray]):
        """
        :param model_id: the model id
        """
        ...
