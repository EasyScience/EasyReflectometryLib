__author__ = "github.com/arm61"
__version__ = "0.0.1"

from typing import List

import numpy as np

from easyCore.Objects.Inferface import ItemContainer
from EasyReflectometry.interfaces.interfaceTemplate import InterfaceTemplate
from EasyReflectometry.calculators.bornagain import BornAgain as BornAgain_calc
from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.item import RepeatingMultiLayer, MultiLayer
from EasyReflectometry.experiment.model import Model


class BornAgain(InterfaceTemplate):
    """
    A simple interface using BornAgain
    """

    _material_link = {'sld': 'real', 'isld': 'imag'}

    _layer_link = {'thickness': 'thickness', 'roughness': 'sigma'}

    _item_link = {'repetitions': 'repeats'}

    _model_link = {'scale': 'scale',
                   'background': 'background', 'resolution': 'resolution'}

    name = 'BornAgain'

    def __init__(self):
        self.calculator = BornAgain_calc()
        self._namespace = {}

    def reset_storage(self):
        """
        Reset the storage area of the calculator
        """
        self.calculator.reset_storage()

    def create(self, model):
        """
        Creation function

        :param model: Object to be created
        :type model: Union[Material, Layer, Item, Model]
        :return: Item containers of the objects
        :rtype: List[ItemContainer]
        """
        r_list = []
        t_ = type(model)
        if issubclass(t_, Material):
            key = model.uid
            self.calculator.create_material(key)
            r_list.append(
                ItemContainer(key, self._material_link,
                              self.calculator.get_material_value,
                              self.calculator.update_material))
        elif issubclass(t_, Layer):
            key = model.uid
            self.calculator.create_layer(key)
            r_list.append(
                ItemContainer(key, self._layer_link,
                              self.calculator.get_layer_value,
                              self.calculator.update_layer))
            self.assign_material_to_layer(model.material.uid, key)
        elif (issubclass(t_, RepeatingMultiLayer) or issubclass(t_, MultiLayer)):
            key = model.uid
            self.calculator.create_item(key)
            r_list.append(
                ItemContainer(key, self._item_link,
                              self.calculator.get_item_value,
                              self.calculator.update_item))
            for i in model.layers:
                self.add_layer_to_item(i.uid, model.uid)
        elif issubclass(t_, Model):
            self.calculator.create_model()
            r_list.append(
                ItemContainer('model', self._model_link,
                              self.calculator.get_model_value,
                              self.calculator.update_model))
            for i in model.structure:
                self.add_item_to_model(i.uid)
        return r_list

    def assign_material_to_layer(self, material_id: int, layer_id: int):
        """
        Assign a material to a layer.

        :param material_name: The material name
        :type material_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.calculator.assign_material_to_layer(material_id, layer_id)

    def add_layer_to_item(self, layer_id: int, item_id: int):
        """
        Add a layer to the item stack

        :param item_id: The item id
        :type item_id: int
        :param layer_id: The layer id
        :type layer_id: int
        """
        self.calculator.add_layer_to_item(layer_id, item_id)

    def remove_layer_from_item(self, layer_id: int, item_id: int):
        """
        Remove a layer from an item stack
        
        :param item_id: The item id
        :type item_id: int
        :param layer_id: The layer id
        :type layer_id: int
        """
        self.calculator.remove_layer_from_item(layer_id, item_id)

    def add_item_to_model(self, item_id: int):
        """
        Add a layer to the item stack

        :param item_id: The item id
        :type item_id: int
        """
        self.calculator.add_item(item_id)

    def remove_item_from_model(self, item_id: int):
        """
        Remove a layer from the item stack

        :param item_id: The item id
        :type item_id: int
        :param layer_id: The layer id
        :type layer_id: int
        """
        self.calculator.remove_item(item_id)

    def fit_func(self, x_array: np.ndarray) -> np.ndarray:
        """
        Function to perform a fit
        :param x_array: points to be calculated at
        :type x_array: np.ndarray
        :return: calculated points
        :rtype: np.ndarray
        """
        return self.calculator.calculate(x_array)

    def sld_profile(self) -> tuple:
        """
        Return the scattering length density profile.

        :return: z and sld(z)
        :rtype: tuple[np.ndarray, np.ndarray]
        """
        return self.calculator.sld_profile()
