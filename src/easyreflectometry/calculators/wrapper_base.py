from abc import abstractmethod

import numpy as np

from easyreflectometry.model import PercentageFhwm
from easyreflectometry.model import ResolutionFunction


class WrapperBase:
    def __init__(self):
        """Constructor."""
        self._magnetism = False
        self.storage = {
            'material': {},
            'layer': {},
            'item': {},
            'model': {},
        }
        self._resolution_function = PercentageFhwm()

    def reset_storage(self):
        """Reset the storage area to blank."""
        self.storage = {
            'material': {},
            'layer': {},
            'item': {},
            'model': {},
        }

    @abstractmethod
    def create_material(self, name: str):
        """Create a material using SLD.

        :param name: The name of the material
        """
        ...

    @abstractmethod
    def create_layer(self, name: str):
        """Create a layer using Slab.

        :param name: The name of the layer
        """
        ...

    @abstractmethod
    def create_item(self, name: str):
        """Create an item using Stack.

        :param name: The name of the item
        """
        ...

    @abstractmethod
    def create_model(self, name: str):
        """Create a model for analysis

        :param name: Name for the model
        """
        ...

    @abstractmethod
    def update_model(self, name: str, **kwargs):
        """Update the non-structural parameters of the model

        :param name: Name for the model
        :param kwargs:

        """
        ...

    @abstractmethod
    def get_model_value(self, name: str, key: str) -> float:
        """A function to get a given model value

        :param name: Name for the model
        :param key: The given value keys
        """
        ...

    @abstractmethod
    def assign_material_to_layer(self, material_name: str, layer_name: str):
        """Assign a material to a layer.

        :param material_name: The material name
        :param layer_name: The layer name
        """
        ...

    @abstractmethod
    def add_layer_to_item(self, layer_name: str, item_name: str):
        """Create a layer from the material of the same name, in a given item.

        :param layer_name: The layer name
        :param item_name: The item name
        """
        ...

    @abstractmethod
    def add_item(self, item_name: str, model_name: str):
        """Add an item to the model.

        :param item_name: items to add to model
        :param model_name: Name for the model
        """
        ...

    @abstractmethod
    def remove_layer_from_item(self, layer_name: str, item_name: str):
        """Remove a layer in a given item.

        :param layer_name: The layer name
        :param item_name: The item name
        """
        ...

    @abstractmethod
    def remove_item(self, item_name: str, model_name: str):
        """Remove a given item.

        :param item_name: The item name
        :param model_name: Name of the model
        """
        ...

    @abstractmethod
    def calculate(self, q_array: np.ndarray, model_name: str) -> np.ndarray:
        """For a given q array calculate the corresponding reflectivity.

        :param q_array: array of data points to be calculated
        :param model_name: the model name
        :return: reflectivity calculated at q
        """
        ...

    @abstractmethod
    def sld_profile(self, model_name: str) -> tuple[np.ndarray, np.ndarray]:
        """Return the scattering length density profile.

        :param model_name: Name for the model
        :return: z and sld(z)
        """
        ...

    def update_material(self, name: str, **kwargs):
        """Update a material.

        :param name: The name of the material
        """
        material = self.storage['material'][name]
        for key in kwargs.keys():
            item = getattr(material, key)
            setattr(item, 'value', kwargs[key])

    def get_material_value(self, name: str, key: str) -> float:
        """A function to get a given material value

        :param name: The material name
        :param key: The given value keys
        :return: The desired value
        """
        material = self.storage['material'][name]
        item = getattr(material, key)
        return getattr(item, 'value')

    def update_layer(self, name: str, **kwargs):
        """Update a layer in a given item.

        :param name: The layer name.
        :param kwargs:
        """
        layer = self.storage['layer'][name]
        for key in kwargs.keys():
            ii = getattr(layer, key)
            setattr(ii, 'value', kwargs[key])

    def get_layer_value(self, name: str, key: str) -> float:
        """A function to get a given layer value

        :param name: The layer name
        :param key: The given value keys
        """
        layer = self.storage['layer'][name]
        ii = getattr(layer, key)
        return getattr(ii, 'value')

    def update_item(self, name: str, **kwargs):
        """Update a layer.

        :param name: The item name
        """
        item = self.storage['item'][name]
        for key in kwargs.keys():
            ii = getattr(item, key)
            setattr(ii, 'value', kwargs[key])

    def get_item_value(self, name: str, key: str) -> float:
        """A function to get a given item value

        :param name: The item name
        :param key: The given value keys
        :return: The desired value
        """
        item = self.storage['item'][name]
        item = getattr(item, key)
        return getattr(item, 'value')

    def set_resolution_function(self, resolution_function: ResolutionFunction) -> None:
        """Set the resolution function for the calculator.

        :param resolution_function: The resolution function
        """
        self._resolution_function = resolution_function

    @property
    def magnetism(self) -> bool:
        return self._magnetism

    @magnetism.setter
    def magnetism(self, magnetism: bool) -> None:
        """Set the magnetism flag.

        :param magnetism: The magnetism flag
        """
        self._magnetism = magnetism
