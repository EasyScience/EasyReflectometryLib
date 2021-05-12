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
        if self._borg.debug:
            print(f'Interface1: Value of {value_label} set to {value}')
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
        if self._borg.debug:
            print(f'Interface1: Value of {value_label} set to {value}')
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
        if self._borg.debug:
            print(f'Interface1: Value of {value_label} set to {value}')
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

    def remove_layer_from_item(self, item_name: str, layer_name: str):
        """
        Method to remove a layer from an item from the calculator

        :param item_name: The name of the item to be added to
        :type item_name: str
        :param layer_name: The name of the layer to add
        :type layer_name: str
        """
        self.calculator.remove_layer(item_name, layer_name)

    def get_background_value(self, background, value_label: int) -> float:
        """
        Method to get a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        self.calculator.background = background
        # if value_label <= len(self.calculator.background):
        #     return self.calculator.background[value_label]
        # else:
        #     raise IndexError

    def set_background_value(self, background, value_label: int, value: float):
        """
        Method to set a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        self.calculator.background = background
        # if value_label <= len(self.calculator.background):
        #     self.calculator.background[value_label].set(value)
        # else:
        #     raise IndexError

    def set_pattern_value(self, pattern, value_label: int, value: float):
        """
        Method to set a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        self.calculator.pattern = pattern

    def bulk_update(self, value_label_list: List[str], value_list: List[float], external: bool):
        """
        Perform an update of multiple values at once to save time on expensive updates

        :param value_label_list: list of parameters to set
        :type value_label_list: List[str]
        :param value_list: list of new numeric values
        :type value_list: List[float]
        :param external: should we lookup a name conversion to internal labeling?
        :type external: bool
        :return: None
        :rtype: noneType
        """
        for label, value in zip(value_label_list, value_list):
            # This is a simple case so we will serially update
            if label in self._sample_link:
                self.set_value(label, value)
            elif label in self._instrument_link:
                self.set_instrument_value(label, value)

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
