__author__ = "github.com/arm61"
__version__ = "0.0.1"

from typing import List

import numpy as np

from easyReflectometryLib.Interfaces.interfaceTemplate import InterfaceTemplate
from easyReflectometryLib.Calculators.refnx import Refnx as Refnx_calc


class Refnx(InterfaceTemplate):
    """
    A simple interface using refnx
    """

    _material_link = {
        'sld': 'real',
        'isld': 'imag'
    }

    _layer_link = {
        'thickness': 'thick',
        'roughness': 'rough'
    }

    _item_like = {
        'repetitions': 'repeats'
    }

    _model_link = {
        'scale': 'scale',
        'background': 'bkg',
        'resolution': 'dq'
    }

    name = 'refnx'

    def __init__(self):
        self.calculator = Refnx_calc()
        self._namespace = {}

    def get_material_value(self, name: str, value_label: str) -> float:
        """
        Method to get a material value from the calculator

        :param name: The material name
        :type name: str
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        if value_label in self._material_link.keys():
            value_label = self._material_link[value_label]
        return self.calculator.get_material_value(name, value_label)

    def set_material_value(self, name: str, value_label: str, value: float):
        """
        Method to set a material value from the calculator

        :param name: The material name
        :type name: str
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        if value_label in self._material_link.keys():
            value_label = self._material_link[value_label]
        self.calculator.update_material(name, **{value_label: value})

    def get_layer_value(self, name: str, value_label: str) -> float:
        """
        Method to get a layer value from the calculator

        :param name: The layer name
        :type name: str
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        if value_label in self._layer_link.keys():
            value_label = self._layer_link[value_label]
        return self.calculator.get_layer_value(name, value_label)

    def set_layer_value(self, name: str, value_label: str, value: float):
        """
        Method to set a layer value from the calculator
        
        :param name: The layer name
        :type name: str
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        if value_label in self._layer_link.keys():
            value_label = self._layer_link[value_label]
        self.calculator.update_layer(name, **{value_label: value})

    def add_layer_to_item(self, item_name: str, layer_name: str):
        """
        Method to add a layer to an item from the calculator

        :param item_name: The name of the item to be added to
        :type item_name: str
        :param layer_name: The name of the layer to add
        :type layer_name: str
        """
        self.calculator.add_layer(item_name, layer_name)

    def remove_layer_from_item(self, item_name: str, layer_name: str):
        """
        Method to remove a layer from an item from the calculator

        :param item_name: The name of the item to be removed from
        :type item_name: str
        :param layer_name: The name of the layer to remove
        :type layer_name: str
        """
        self.calculator.remove_layer(item_name, layer_name)

    def move_layer_up(self, item_name: str, layer_name: str):
        """
        Move a layer up in an item stack

        :param item_name: The item name
        :type item_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.calculator.move_layer_up(item_name, layer_name)

    def move_layer_down(self, item_name: str, layer_name: str):
        """
        Move a layer down in an item stack

        :param item_name: The item name
        :type item_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.calculator.move_layer_down(item_name, layer_name)

    def get_item_reps(self, name: str) -> float:
        """
        Method to get an item repeats from the calculator

        :param name: The item name
        :type name: str
        :return: Repeats value
        :rtype: float
        """
        return self.calculator.get_reps(name)

    def set_item_reps(self, name: str, value: float):
        """
        Method to set an item repeats from the calculator

        :param name: The item name
        :type name: str
        :param value: number of repeats
        :type value: float
        """
        self.calculator.update_reps(name, value)

    def get_model_value(self, value_label: str) -> float:
        """
        Method to get a model value from the calculator

        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        if value_label in self._model_link.keys():
            value_label = self._model_link[value_label]
        return self.calculator.get_model_value(value_label)

    def set_model_value(self, value_label: str, value: float):
        """
        Method to set a model value from the calculator
        
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        if value_label in self._model_link.keys():
            value_label = self._model_link[value_label]
        self.calculator.update_model(**{value_label: value})

    def add_item_to_model(self, item_name: str):
        """
        Method to add an item to a model from the calculator

        :param item_name: The name of the item to add
        :type item_name: str
        """
        self.calculator.add_item(item_name)

    def remove_item_from_model(self, item_name: str):
        """
        Method to remove an item from a model from the calculator

        :param item_name: The name of the item to remove
        :type item_name: str
        """
        self.calculator.remove_item(item_name)

    def move_item_up(self, item_name: str):
        """
        Move a item up in a model

        :param item_name: The item name
        :type item_name: str
        """
        self.calculator.move_item_up(item_name)

    def move_item_down(self, item_name: str):
        """
        Move a item down in a model

        :param item_name: The item name
        :type item_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.calculator.move_item_down(item_name)

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
