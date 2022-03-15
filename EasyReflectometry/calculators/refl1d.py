__author__ = "github.com/arm61"

from easyCore import np
from refl1d import names, model, experiment


class Refl1d:

    def __init__(self):
        self.storage = {'material': {}, 'layer': {}, 'item': {}, 'model': {}}

    def reset_storage(self):
        """
        Reset the storage area to blank.
        """
        self.storage = {'material': {}, 'layer': {}, 'item': {}, 'model': {}}

    def create_material(self, name):
        """
        Create a material using SLD.

        :param name: The name of the material
        :type name: str
        """
        self.storage['material'][name] = names.SLD(str(name))

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
        self.storage['layer'][name] = model.Slab(name=str(name))

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
        Create an item using Repeat.

        :param name: The name of the item
        :type name: str
        """
        self.storage['item'][name] = model.Repeat(model.Stack(
            model.Slab(names.SLD(), thickness=0, interface=0)),
                                                  name=str(name))
        del self.storage['item'][name].stack[0]

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

    def create_model(self):
        """
        Create a model for analysis
        """
        self.storage['model'] = {'scale': 1, 'bkg': 0, 'dq': 0, 'items': []}

    def update_model(self, name, **kwargs):
        """
        Update the non-structural parameters of the model
        """
        model = self.storage[name]
        for key in kwargs.keys():
            model[key] = kwargs[key]

    def get_model_value(self, name, key):
        """
        A function to get a given model value

        :param key: The given value keys
        :type name: str
        :return: The desired value
        :rtype: float
        """
        model = self.storage[name]
        return model[key]

    def assign_material_to_layer(self, material_name, layer_name):
        """
        Assign a material to a layer.

        :param material_name: The material name
        :type material_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.storage['layer'][layer_name].material = self.storage['material'][
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
        item.stack.add(self.storage['layer'][layer_name])

    def add_item(self, item_name):
        """
        Add an item to the model.

        :param item_name: items to add to model
        :type item_name: str
        """
        self.storage['model']['items'].append(self.storage['item'][item_name])

    def remove_layer_from_item(self, layer_name, item_name):
        """
        Remove a layer in a given item.

        :param layer_name: The layer name
        :type layer_name: int
        :param item_name: The item name
        :type item_name: int
        """
        layer_idx = list(self.storage['item'][item_name].stack).index(
            self.storage['layer'][layer_name])
        del self.storage['item'][item_name].stack[layer_idx]

    def remove_item(self, item_name):
        """
            Remove a given item.

            :param item_name: The item name
            :type item_name: int
            """
        item_idx = self.storage['model']['items'].index(self.storage['item'][item_name])
        del self.storage['model']['items'][item_idx]
        del self.storage['item'][item_name]

    def calculate(self, x_array: np.ndarray) -> np.ndarray:
        """
        For a given x calculate the corresponding y.

        :param x_array: array of data points to be calculated
        :type x_array: np.ndarray
        :return: points calculated at `x`
        :rtype: np.ndarray
        """
        structure = model.Stack()
        for i in self.storage['model']['items'][::-1]:
            if i.repeat.value == 1:
                for j in range(len(i.stack))[::-1]:
                    structure |= i.stack[j]
            else:
                stack = model.Stack()
                for j in range(len(i.stack))[::-1]:
                    stack |= i.stack[j]
                structure |= model.Repeat(stack, repeat=i.repeat.value)

        argmin = np.argmin(x_array)
        argmax = np.argmax(x_array)
        dq_vector = x_array * self.storage['model']['dq'] / 100 / (
            2 * np.sqrt(2 * np.log(2)))

        q = names.QProbe(x_array,
                         dq_vector,
                         intensity=self.storage['model']['scale'],
                         background=self.storage['model']['bkg'])
        q.calc_Qo = np.linspace(
            x_array[argmin] - 3.5 * dq_vector[argmin],
            x_array[argmax] + 3.5 * dq_vector[argmax],
            21 * len(x_array),
        )
        R = names.Experiment(probe=q, sample=structure).reflectivity()[1]
        return R

    def sld_profile(self) -> np.ndarray:
        """
        Return the scattering length density profile.

        :return: z and sld(z)
        :rtype: tuple[np.ndarray, np.ndarray]
        """
        structure = model.Stack()
        for i in self.storage['model']['items'][::-1]:
            if i.repeat.value == 1:
                for j in range(len(i.stack))[::-1]:
                    structure |= i.stack[j]
            else:
                stack = model.Stack()
                for j in range(len(i.stack))[::-1]:
                    stack |= i.stack[j]
                structure |= model.Repeat(stack, repeat=i.repeat.value)

        q = names.QProbe(np.linspace(0.001, 0.3, 10),
                         np.linspace(0.001, 0.3, 10),
                         intensity=self.storage['model']['scale'],
                         background=self.storage['model']['bkg'])
        z, sld, _ = names.Experiment(probe=q, sample=structure).smooth_profile()
        return z, sld[::-1]
