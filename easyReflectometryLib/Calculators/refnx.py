__author__ = "github.com/arm61"
__version__ = "0.0.1"

from easyCore import np
from refnx import reflect


class Refnx:
    def __init__(self):
        self.storage = {
            'material': {},
            'layer': {},
            'item': {},
            'model': reflect.ReflectModel(reflect.Structure())
        }

    def create_material(self, name):
        """
        Create a material using SLD.

        :param name: The name of the material
        :type name: str
        """
        self.storage['material'][name] = reflect.SLD(0, name=name)

    def update_material(self, name, **kwargs):
        """
        Update a material.

        :param name: The name of the material
        :type name: str
        """
        material = self.storage['material'][name]
        for key in kwargs.keys():
            item = getattr(material, key)
            setattr(item, 'value', kwargs[key])

    def get_material_value(self, name, key):
        """
        A function to get a given material value

        :param name: The material name
        :type name: str
        :param key: The given value keys
        :type name: str
        :return: The desired value
        :rtype: float
        """
        material = self.storage['material'][name]
        item = getattr(material, key)
        return getattr(item, 'value')

    def create_layer(self, name):
        """
        Create a layer using Slab.

        :param name: The name of the layer
        :type name: str
        """
        self.storage['layer'][name] = reflect.Slab(0, 0, 0, name=name)

    def update_layer(self, name, **kwargs):
        """
        Update a layer in a given item.

        :param name: The layer name
        :type name: str
        """
        layer = self.storage['layer'][name]
        for key in kwargs.keys():
            ii = getattr(layer, key)
            setattr(ii, 'value', kwargs[key])

    def get_layer_value(self, name, key):
        """
        A function to get a given layer value

        :param name: The layer name
        :type name: str
        :param key: The given value keys
        :type name: str
        :return: The desired value
        :rtype: float
        """
        layer = self.storage['layer'][name]
        ii = getattr(layer, key)
        return getattr(ii, 'value')

    def create_item(self, name):
        """
        Create an item using Stack.

        :param name: The name of the item
        :type name: str
        """
        self.storage['item'][name] = reflect.Stack(name=name)

    def update_item(self, name, **kwargs):
        """
        Update a layer.

        :param name: The item name
        :type name: str
        """
        item = self.storage['item'][name]
        for key in kwargs.keys():
            ii = getattr(item, key)
            setattr(ii, 'value', kwargs[key])

    def get_item_value(self, name, key):
        """
        A function to get a given item value

        :param name: The item name
        :type name: str
        :param key: The given value keys
        :type name: str
        :return: The desired value
        :rtype: float
        """
        item = self.storage['item'][name]
        item = getattr(item, key)
        return getattr(item, 'value')

    def update_model(self, name, **kwargs):
        """
        Update the non-structural parameters of the model
        """
        model = self.storage[name]
        for key in kwargs.keys():
            item = getattr(model, key)
            setattr(item, 'value', kwargs[key])

    def get_model_value(self, name, key):
        """
        A function to get a given model value

        :param key: The given value keys
        :type name: str
        :return: The desired value
        :rtype: float
        """
        model = self.storage[name]
        item = getattr(model, key)
        return getattr(item, 'value')

    def assign_material_to_layer(self, material_name, layer_name):
        """
        Assign a material to a layer.

        :param material_name: The material name
        :type material_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.storage['layer'][layer_name].sld = self.storage['material'][
            material_name]

    def add_layer_to_item(self, layer_name, item_name):
        """
        Create a layer from the material of the same name, in a given item.

        :param layer_name: The layer name
        :type layer_name: int
        :param item_name: The item name
        :type item_name: int
        """
        item = self.storage['item'][item_name]
        item.append(self.storage['layer'][layer_name])

    def add_item(self, item_name):
        """
        Add an item to the model.

        :param item_name: items to add to model
        :type item_name: str
        """
        self.storage['model'].structure.components.append(
            self.storage['item'][item_name])

    def remove_layer_from_item(self, layer_name, item_name):
        """
        Remove a layer in a given item.

        :param layer_name: The layer name
        :type layer_name: int
        :param item_name: The item name
        :type item_name: int
        """
        layer_idx = self.storage['item'][item_name].components.index(
            self.storage['layer'][layer_name])
        del self.storage['item'][item_name].components[layer_idx]

    def remove_item(self, item_name):
        """
        Remove a given item.

        :param item_name: The item name
        :type item_name: int
        """
        item_idx = self.storage['model'].structure.components.index(
            self.storage['item'][item_name])
        del self.storage['model'].structure.components[item_idx]
        del self.storage['item'][item_name]

    def calculate(self, x_array: np.ndarray) -> np.ndarray:
        """
        For a given x calculate the corresponding y.

        :param x_array: array of data points to be calculated
        :type x_array: np.ndarray
        :return: points calculated at `x`
        :rtype: np.ndarray
        """
        structure = _remove_unecessary_stacks(self.storage['model'].structure)
        model = reflect.ReflectModel(structure,
                                     scale=self.storage['model'].scale.value,
                                     bkg=self.storage['model'].bkg.value,
                                     dq=self.storage['model'].dq.value)
        return model(x_array)

    def sld_profile(self) -> np.ndarray:
        """
        Return the scattering length density profile.

        :return: z and sld(z)
        :rtype: tuple[np.ndarray, np.ndarray]
        """
        return _remove_unecessary_stacks(
            self.storage['model'].structure).sld_profile()


def _remove_unecessary_stacks(current_structure):
    """
    Removed unnecessary reflect.Stack objects from the structure.

    :param current_structure: The current structure
    :type current_structure: reflect.Structure
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
