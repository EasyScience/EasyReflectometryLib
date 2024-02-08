from abc import abstractmethod

import numpy as np


class WrapperBase:
    def __init__(self):
        self.storage = {
            'material': {},
            'layer': {},
            'item': {},
            'model': {},
        }

    def reset_storage(self):
        """
        Reset the storage area to blank.
        """
        self.storage = {
            'material': {},
            'layer': {},
            'item': {},
            'model': {},
        }

    @abstractmethod
    def create_material(self, name: str):
        """
        Create a material using SLD.

        :param name: The name of the material
        """
        ...

    @abstractmethod
    def update_material(self, name: str, **kwargs):
        """
        Update a material.

        :param name: The name of the material
        """
        ...

    @abstractmethod
    def get_material_value(self, name: str, key: str) -> float:
        """
        A function to get a given material value

        :param name: The material name
        :param key: The given value keys
        :return: The desired value
        """
        ...

    @abstractmethod
    def create_layer(self, name: str):
        """
        Create a layer using Slab.

        :param name: The name of the layer
        """
        ...

    @abstractmethod
    def update_layer(self, name: str, **kwargs):
        """
        Update a layer in a given item.

        :param name: The layer name
        """
        ...

    @abstractmethod
    def get_layer_value(self, name: str, key: str) -> float:
        """
        A function to get a given layer value

        :param name: The layer name
        :param key: The given value keys
        :return: The desired value
        """
        ...

    @abstractmethod
    def create_item(self, name: str):
        """
        Create an item using Stack.

        :param name: The name of the item
        """
        ...

    @abstractmethod
    def update_item(self, name: str, **kwargs):
        """
        Update a layer.

        :param name: The item name
        """
        ...

    @abstractmethod
    def get_item_value(self, name: str, key: str) -> float:
        """
        A function to get a given item value

        :param name: The item name
        :param key: The given value keys
        :return: The desired value
        """
        ...

    @abstractmethod
    def create_model(self, name: str):
        """
        Create a model for analysis

        :param name: Name for the model
        """
        ...

    @abstractmethod
    def update_model(self, name: str, **kwargs):
        """
        Update the non-structural parameters of the model

        :param name: Name for the model
        """
        ...

    @abstractmethod
    def get_model_value(self, name: str, key: str) -> float:
        """
        A function to get a given model value

        :param name: Name for the model
        :param key: The given value keys
        :return: The desired value
        """
        ...

    @abstractmethod
    def assign_material_to_layer(self, material_name: str, layer_name: str):
        """
        Assign a material to a layer.

        :param material_name: The material name
        :param layer_name: The layer name
        """
        ...

    @abstractmethod
    def add_layer_to_item(self, layer_name: str, item_name: str):
        """
        Create a layer from the material of the same name, in a given item.

        :param layer_name: The layer name
        :param item_name: The item name
        """
        ...

    @abstractmethod
    def add_item(self, item_name: str, model_name: str):
        """
        Add an item to the model.

        :param item_name: items to add to model
        :param model_name: Name for the model
        """
        ...

    @abstractmethod
    def remove_layer_from_item(self, layer_name: str, item_name: str):
        """
        Remove a layer in a given item.

        :param layer_name: The layer name
        :param item_name: The item name
        """
        ...

    @abstractmethod
    def remove_item(self, item_name: str, model_name: str):
        """
        Remove a given item.

        :param item_name: The item name
        :param model_name: Name of the model
        """
        ...

    @abstractmethod
    def calculate(self, x_array: np.ndarray, model_name: str) -> np.ndarray:
        """
        For a given x calculate the corresponding y.

        :param x_array: array of data points to be calculated
        :param model_name: Name for the model
        :return: points calculated at `x`
        """
        ...

    @abstractmethod
    def sld_profile(self, model_name: str) -> tuple[np.ndarray, np.ndarray]:
        """
        Return the scattering length density profile.

        :param model_name: Name for the model
        :return: z and sld(z)
        """
        ...
