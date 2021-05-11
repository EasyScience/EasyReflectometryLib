__author__ = "github.com/arm61"
__version__ = "0.0.1"

from typing import List

import numpy as np

from easyReflectometryLib.interfaces.interfaceTemplate import InterfaceTemplate
from easyReflectometryLib.calculators.refnx import Refnx as Refnx_calc


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

    _sample_link = {
        'cif_str': 'cif_str'}

    _crystal_link = {
        "length_a": "length_a",
        "length_b": "length_b",
        "length_c": "length_c",
        "angle_alpha": "angle_alpha",
        "angle_beta": "angle_beta",
        "angle_gamma": "angle_gamma",
    }

    _instrument_link = {
        'resolution_u': 'u',
        'resolution_v': 'v',
        'resolution_w': 'w',
        'resolution_x': 'x',
        'resolution_y': 'y',
        'wavelength': 'wavelength'
    }

    name = 'refnx'

    def __init__(self):
        self.calculator = Refnx_calc()
        self._namespace = {}

    def get_material_value(self, name, value_label: str) -> float:
        """
        Method to get a material value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        if value_label in self._material_link.keys():
            value_label = self._material_link[value_label]
        return self.calculator.get_material_value(name, value_label)

    def set_material_value(self, name, value_label: str, value: float):
        """
        Method to set a material value from the calculator
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

    def get_layer_value(self, value_label: str) -> float:
        """
        Method to get a layer value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        if value_label in self._layer_link.keys():
            value_label = self._layer_link[value_label]
        return self.calculator['layer'].get(value_label, None)

    def set_layer_value(self, value_label: str, value: float):
        """
        Method to set a layer value from the calculator
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
        self.calculator['layer'][value_label] = value

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

    def get_hkl(self, x_array: np.ndarray = None) -> dict:
        return self.calculator.get_hkl(x_array)
