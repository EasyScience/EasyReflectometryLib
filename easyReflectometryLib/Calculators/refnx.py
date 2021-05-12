__author__ = "github.com/arm61"
__version__ = "0.0.1"

from easyCore import np 
from easyCore import borg
from refnx import reflect


class Refnx:
    def __init__(self):
        self.storage = {
            'material': {},
            'layer': {},
            'item': {}
        }

    def create_material(self, name):
        """
        Create a material using SLD.

        :param name: The name of the material
        :type name: str
        """
        self.storage['material'][name] = reflect.SLD(0)

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

    def create_layer(self, layer_name, material_name):
        """
        Create a layer from the material of the same name.

        :param layer_name: The name of the layer
        :type layer_name: str
        :param material_name: The name of the layer
        :type material_name: str
        """
        self.storage['layer'][layer_name] = self.storage['material'][material_name]()
        
    def update_layer(self, name, **kwargs):
        """
        Update a layer.

        :param name: The layer's name
        :type name: str
        """
        layer = self.storage['layer'][name]
        for key in kwargs.keys():
            item = getattr(layer, key)
            setattr(item, 'value', kwargs[key])

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
        item = getattr(layer, key)
        return getattr(item, 'value')

    def create_item(self, name):
        """
        Create an item.

        :param name: The item name
        :type name: str
        """
        self.storage['item'][name] = reflect.Stack()
    
    def add_layer(self, item_name, layer_name):
        """
        Add a layer to the item stack

        :param item_name: The item name
        :type item_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.storage['item'][item_name].components.append(self.storage['layer'][layer_name])

    def remove_layer(self, item_name, layer_name):
        """
        Remove a layer from the item stack

        :param item_name: The item name
        :type item_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.storage['item'][item_name].components.pop(self.storage['item'][item_name].components.index(self.storage['layer'][layer_name]))
    
    def move_layer_up(self, item_name, layer_name):
        """
        Move a layer up in an item stack

        :param item_name: The item name
        :type item_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        item_list = self.storage['item'][item_name].components
        layer_list = self.storage['layer'][layer_name]
        old_index = item_list.index(layer_list)
        item_list.insert(old_index-1, item_list.pop(old_index))

    def move_layer_down(self, item_name, layer_name):
        """
        Move a layer down in an item stack

        :param item_name: The item name
        :type item_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        item_list = self.storage['item'][item_name].components
        layer_list = self.storage['layer'][layer_name]
        old_index = item_list.index(layer_list)
        item_list.insert(old_index+1, item_list.pop(old_index))

    def update_reps(self, name, reps):
        """
        Update the number of repeats for the stack

        :param name: The item name
        :type name: str
        :param reps: Number of repeats
        :type reps: float
        """
        self.storage['item'][name].repeats.value = reps

    def get_reps(self, name):
        """
        Get the number of repeats for the stack

        :param name: The item name
        :type name: str
        """
        return self.storage['item'][name].repeats.value

    def create_model(self):
        """
        Create a model.
        """
        self.storage['model'] = reflect.ReflectModel(reflect.Structure())

    def add_item(self, item_name):
        """
        Add a item to the model structure

        :param item_name: The item or layer name
        :type item_name: str
        """
        try: 
            self.storage['model'].structure.components.append(self.storage['item'][item_name])
        except KeyError:
            self.storage['model'].structure.components.append(self.storage['layer'][item_name])

    def remove_item(self, item_name):
        """
        Remove an item or layer from the model structure

        :param item_name: The item or layer name
        :type item_name: str
        """
        try:
            self.storage['model'].structure.components.pop(self.storage['model'].structure.components.index(self.storage['item'][item_name]))
        except KeyError:
            self.storage['model'].structure.components.pop(self.storage['model'].structure.components.index(self.storage['layer'][item_name]))
 
    def move_item_up(self, item_name):
        """
        Move an item up in a model

        :param item_name: The item name
        :type item_name: str
        """
        structure_list = self.storage['model'].structure.components
        item_list = self.storage['item'][item_name]
        old_index = structure_list.index(item_list)
        structure_list.insert(old_index-1, structure_list.pop(old_index))

    def move_item_down(self, item_name):
        """
        Move an item down in a model

        :param item_name: The item name
        :type item_name: str
        """
        structure_list = self.storage['model'].structure.components
        item_list = self.storage['item'][item_name]
        old_index = structure_list.index(item_list)
        structure_list.insert(old_index+1, structure_list.pop(old_index))

    def update_model(self, **kwargs):
        """
        Update the non-structural parameters of the model
        """
        model = self.storage['model']
        for key in kwargs.keys():
            item = getattr(model, key)
            setattr(item, 'value', kwargs[key])
            
    def get_model_value(self, key):
        """
        A function to get a given model value

        :param name: The model name
        :type name: str
        :param key: The given value keys
        :type name: str
        :return: The desired value
        :rtype: float
        """
        model = self.storage['model']
        item = getattr(model, key)
        return getattr(item, 'value')

    def calculate(self, x_array: np.ndarray) -> np.ndarray:
        """
        For a given x calculate the corresponding y.

        :param x_array: array of data points to be calculated
        :type x_array: np.ndarray
        :return: points calculated at `x`
        :rtype: np.ndarray
        """
        return self.storage['model'](x_array)

    def sld_profile(self) -> np.ndarray:
        """
        Return the scattering length density profile.

        :return: z and sld(z)
        :rtype: tuple[np.ndarray, np.ndarray]
        """
        return self.storage['model'].structure.sld_profile()
