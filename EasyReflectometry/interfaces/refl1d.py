__author__ = "github.com/arm61"

from typing import List
from typing import Tuple
from typing import Union

import numpy as np
from easyCore.Objects.Inferface import ItemContainer

from EasyReflectometry.calculators.refl1d import Refl1d as Refl1d_calc
from EasyReflectometry.experiment.model import Model
from EasyReflectometry.interfaces.interfaceTemplate import InterfaceTemplate
from EasyReflectometry.sample.item import MultiLayer
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.material import MaterialMixture


class Refl1d(InterfaceTemplate):
    """
    A simple interface using refl1
    """

    _material_link = {"sld": "rho", "isld": "irho"}

    _layer_link = {"thickness": "thickness", "roughness": "interface"}

    _item_link = {"repetitions": "repeat"}

    _model_link = {"scale": "scale", "background": "bkg", "resolution": "dq"}

    name = "refl1d"

    def __init__(self):
        self.calculator = Refl1d_calc()
        self._namespace = {}

    def reset_storage(self):
        """
        Reset the storage area of the calculator
        """
        self.calculator.reset_storage()

    def create(self, model: Union[Material, Layer, MultiLayer, Model]) -> List[ItemContainer]:
        """
        Creation function

        :param model: Object to be created
        :return: Item containers of the objects
        """
        r_list = []
        t_ = type(model)
        if issubclass(t_, Material):
            key = model.uid
            if key not in self.calculator.storage["material"].keys():
                self.calculator.create_material(key)
            r_list.append(
                ItemContainer(key, self._material_link, self.calculator.get_material_value, self.calculator.update_material)
            )
        elif issubclass(t_, MaterialMixture):
            key = model.uid
            if key not in self.calculator.storage["material"].keys():
                self.calculator.create_material(key)
            r_list.append(
                ItemContainer(key, self._material_link, self.calculator.get_material_value, self.calculator.update_material)
            )
        elif issubclass(t_, Layer):
            key = model.uid
            if key not in self.calculator.storage["layer"].keys():
                self.calculator.create_layer(key)
            r_list.append(ItemContainer(key, self._layer_link, self.calculator.get_layer_value, self.calculator.update_layer))
            self.assign_material_to_layer(model.material.uid, key)
        elif issubclass(t_, MultiLayer):
            key = model.uid
            self.calculator.create_item(key)
            r_list.append(ItemContainer(key, self._item_link, self.calculator.get_item_value, self.calculator.update_item))
            for i in model.layers:
                self.add_layer_to_item(i.uid, model.uid)
        elif issubclass(t_, Model):
            key = model.uid
            self.calculator.create_model(key)
            r_list.append(ItemContainer(key, self._model_link, self.calculator.get_model_value, self.calculator.update_model))
            for i in model.structure:
                self.add_item_to_model(i.uid, key)
        return r_list

    def assign_material_to_layer(self, material_id: str, layer_id: str):
        """
        Assign a material to a layer.

        :param material_name: The material name
        :param layer_name: The layer name
        """
        self.calculator.assign_material_to_layer(material_id, layer_id)

    def add_layer_to_item(self, layer_id: str, item_id: str):
        """
        Add a layer to the item stack

        :param item_id: The item id
        :param layer_id: The layer id
        """
        self.calculator.add_layer_to_item(layer_id, item_id)

    def remove_layer_from_item(self, layer_id: str, item_id: str):
        """
        Remove a layer from an item stack

        :param item_id: The item id
        :type item_id: int        :param layer_id: The layer id
        """
        self.calculator.remove_layer_from_item(layer_id, item_id)

    def add_item_to_model(self, item_id: str, model_id: str):
        """
        Add a layer to the item stack

        :param item_id: The item id
        :param model_id: The model id
        """
        self.calculator.add_item(item_id, model_id)

    def remove_item_from_model(self, item_id: str, model_id: str):
        """
        Remove a layer from the item stack

        :param item_id: The item id
        :param model_id: The model id
        """
        self.calculator.remove_item(item_id, model_id)

    def fit_func(self, x_array: np.ndarray, model_id: str) -> np.ndarray:
        """
        Function to perform a fit

        :param x_array: points to be calculated at
        :param model_id: The name of the model
        :return: calculated points
        """
        return self.calculator.calculate(x_array, model_id)

    def sld_profile(self, model_id: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return the scattering length density profile.

        :return: z and sld(z)
        """
        return self.calculator.sld_profile(model_id)
