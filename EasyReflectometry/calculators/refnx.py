__author__ = "github.com/arm61"

from typing import Tuple

from easyCore import np
from refnx import reflect


class Refnx:

    def __init__(self):
        self.storage = {
            'material': {},
            'layer': {},
            'item': {},
            'model': {}
        }

    def reset_storage(self):
        """
        Reset the storage area to blank.
        """
        self.storage = {
            'material': {},
            'layer': {},
            'item': {},
            'model': {}
        }

    def create_material(self, name: str):
        """
        Create a material using SLD.

        :param name: The name of the material
        """
        self.storage['material'][name] = reflect.SLD(0, name=name)

    def update_material(self, name: str, **kwargs):
        """
        Update a material.

        :param name: The name of the material
        """
        material = self.storage['material'][name]
        for key in kwargs.keys():
            item = getattr(material, key)
            setattr(item, 'value', kwargs[key])

    def get_material_value(self, name: str, key: str) -> float:
        """
        A function to get a given material value

        :param name: The material name
        :param key: The given value keys
        :return: The desired value
        """
        material = self.storage['material'][name]
        item = getattr(material, key)
        return getattr(item, 'value')

    def create_layer(self, name: str):
        """
        Create a layer using Slab.

        :param name: The name of the layer
        """
        self.storage['layer'][name] = reflect.Slab(0, 0, 0, name=name)

    def update_layer(self, name: str, **kwargs):
        """
        Update a layer in a given item.

        :param name: The layer name
        """
        layer = self.storage['layer'][name]
        for key in kwargs.keys():
            ii = getattr(layer, key)
            setattr(ii, 'value', kwargs[key])

    def get_layer_value(self, name: str, key: str) -> float:
        """
        A function to get a given layer value

        :param name: The layer name
        :param key: The given value keys
        :return: The desired value
        """
        layer = self.storage['layer'][name]
        ii = getattr(layer, key)
        return getattr(ii, 'value')

    def create_item(self, name: str):
        """
        Create an item using Stack.

        :param name: The name of the item
        """
        self.storage['item'][name] = reflect.Stack(name=name)

    def update_item(self, name: str, **kwargs):
        """
        Update a layer.

        :param name: The item name
        """
        item = self.storage['item'][name]
        for key in kwargs.keys():
            ii = getattr(item, key)
            setattr(ii, 'value', kwargs[key])

    def get_item_value(self, name: str, key: str) -> float:
        """
        A function to get a given item value

        :param name: The item name
        :param key: The given value keys
        :return: The desired value
        """
        item = self.storage['item'][name]
        item = getattr(item, key)
        return getattr(item, 'value')

    def create_model(self, name: str):
        """
        Create a model for analysis

        :param name: Name for the model
        """
        self.storage['model'][name] = reflect.ReflectModel(reflect.Structure())

    def update_model(self, name: str, **kwargs):
        """
        Update the non-structural parameters of the model

        :param name: Name for the model
        """
        model = self.storage['model'][name]
        for key in kwargs.keys():
            item = getattr(model, key)
            setattr(item, 'value', kwargs[key])

    def get_model_value(self, name: str, key: str) -> float:
        """
        A function to get a given model value

        :param name: Name for the model
        :param key: The given value keys
        :return: The desired value
        """
        model = self.storage['model'][name]
        item = getattr(model, key)
        return getattr(item, 'value')

    def assign_material_to_layer(self, material_name: str, layer_name: str):
        """
        Assign a material to a layer.

        :param material_name: The material name
        :param layer_name: The layer name
        """
        self.storage['layer'][layer_name].sld = self.storage['material'][material_name]

    def add_layer_to_item(self, layer_name: str, item_name: str):
        """
        Create a layer from the material of the same name, in a given item.

        :param layer_name: The layer name
        :param item_name: The item name
        """
        item = self.storage['item'][item_name]
        item.append(self.storage['layer'][layer_name])

    def add_item(self, item_name: str, model_name: str):
        """
        Add an item to the model.

        :param item_name: items to add to model
        :param model_name: Name for the model
        """
        self.storage['model'][model_name].structure.components.append(
            self.storage['item'][item_name])

    def remove_layer_from_item(self, layer_name: str, item_name: str):
        """
        Remove a layer in a given item.

        :param layer_name: The layer name
        :param item_name: The item name
        """
        layer_idx = self.storage['item'][item_name].components.index(
            self.storage['layer'][layer_name])
        del self.storage['item'][item_name].components[layer_idx]

    def remove_item(self, item_name: str, model_name: str):
        """
        Remove a given item.

        :param item_name: The item name
        :param model_name: Name of the model
        """
        item_idx = self.storage['model'][model_name].structure.components.index(
            self.storage['item'][item_name])
        del self.storage['model'][model_name].structure.components[item_idx]
        del self.storage['item'][item_name]

    def calculate(self, x_array: np.ndarray, model_name: str) -> np.ndarray:
        """
        For a given x calculate the corresponding y.

        :param x_array: array of data points to be calculated
        :param model_name: Name for the model
        :return: points calculated at `x`
        """
        structure = _remove_unecessary_stacks(
            self.storage['model'][model_name].structure)
        model = reflect.ReflectModel(
            structure,
            scale=self.storage['model'][model_name].scale.value,
            bkg=self.storage['model'][model_name].bkg.value,
            dq=self.storage['model'][model_name].dq.value)
        return model(x_array)

    def sld_profile(self, model_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return the scattering length density profile.

        :param model_name: Name for the model
        :return: z and sld(z)
        """
        return _remove_unecessary_stacks(
            self.storage['model'][model_name].structure).sld_profile()


def _remove_unecessary_stacks(
        current_structure: reflect.Structure) -> reflect.Structure:
    """
    Removed unnecessary reflect.Stack objects from the structure.

    :param current_structure: The current structure
    :return: The structre without the unnecessary Stacks
    :rtype: reflect.structure
    """
    structure = []
    for i in current_structure.components:
        if i.repeats.value == 1:
            for j in i.components:
                structure.append(j)
        else:
            structure.append(i)
    return reflect.Structure(structure)
