__author__ = 'github.com/arm61'

from typing import Tuple

from easyCore import np
from refl1d import model
from refl1d import names

from EasyReflectometry.experiment.resolution_functions import is_constant_resolution_function

from ..wrapper_base import WrapperBase

PADDING_RANGE = 3.5
UPSCALE_FACTOR = 21


class Refl1dWrapper(WrapperBase):
    def create_material(self, name: str):
        """
        Create a material using SLD.

        :param name: The name of the material
        """
        self.storage['material'][name] = names.SLD(str(name))

    def create_layer(self, name: str):
        """
        Create a layer using Slab.

        :param name: The name of the layer
        """
        self.storage['layer'][name] = model.Slab(name=str(name))

    def create_item(self, name: str):
        """
        Create an item using Repeat.

        :param name: The name of the item
        """
        self.storage['item'][name] = model.Repeat(
            model.Stack(model.Slab(names.SLD(), thickness=0, interface=0)), name=str(name)
        )
        del self.storage['item'][name].stack[0]

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
        self.storage['model'][name] = {'scale': 1, 'bkg': 0, 'items': []}

    def update_model(self, name: str, **kwargs):
        """
        Update the non-structural parameters of the model

        :param name: Name of the model
        """
        model = self.storage['model'][name]
        for key in kwargs.keys():
            model[key] = kwargs[key]

    def get_model_value(self, name: str, key: str) -> float:
        """
        A function to get a given model value

        :param name: Name of the model
        :param key: The given value keys
        :return: The desired value
        """
        model = self.storage['model'][name]
        return model[key]

    def assign_material_to_layer(self, material_name: str, layer_name: str):
        """
        Assign a material to a layer.

        :param material_name: The material name
        :param layer_name: The layer name
        """
        self.storage['layer'][layer_name].material = self.storage['material'][material_name]

    def add_layer_to_item(self, layer_name: str, item_name: str):
        """
        Create a layer from the material of the same name, in a given item.

        :param layer_name: The layer name
        :param item_name: The item name
        """
        item = self.storage['item'][item_name]
        item.stack.add(self.storage['layer'][layer_name])

    def add_item(self, item_name: str, model_name: str):
        """
        Add an item to the model.

        :param item_name: items to add to model
        :param model_name: name for the model
        """
        self.storage['model'][model_name]['items'].append(self.storage['item'][item_name])

    def remove_layer_from_item(self, layer_name: str, item_name: str):
        """
        Remove a layer in a given item.

        :param layer_name: The layer name
        :param item_name: The item name
        """
        layer_idx = list(self.storage['item'][item_name].stack).index(self.storage['layer'][layer_name])
        del self.storage['item'][item_name].stack[layer_idx]

    def remove_item(self, item_name: str, model_name: str):
        """
        Remove a given item.

        :param item_name: The item name
        :param model_name: The model name
        """
        item_idx = self.storage['model'][model_name]['items'].index(self.storage['item'][item_name])
        del self.storage['model'][model_name]['items'][item_idx]
        del self.storage['item'][item_name]

    def calculate(self, q_array: np.ndarray, model_name: str) -> np.ndarray:
        """For a given q array calculate the corresponding reflectivity.

        :param q_array: array of data points to be calculated
        :param model_name: the model name
        :return: reflectivity calculated at q
        """
        structure = model.Stack()
        for i in self.storage['model'][model_name]['items'][::-1]:
            if i.repeat.value == 1:
                for j in range(len(i.stack))[::-1]:
                    structure |= i.stack[j]
            else:
                stack = model.Stack()
                for j in range(len(i.stack))[::-1]:
                    stack |= i.stack[j]
                structure |= model.Repeat(stack, repeat=i.repeat.value)

        argmin = np.argmin(q_array)
        argmax = np.argmax(q_array)
        dq_vector = self._resolution_function(q_array)

        if is_constant_resolution_function(self._resolution_function):
            # Compute percentage of Q and normalize
            dq_vector = dq_vector * q_array / 100 / (2 * np.sqrt(2 * np.log(2)))

        q = names.QProbe(
            Q=q_array,
            dQ=dq_vector,
            intensity=self.storage['model'][model_name]['scale'],
            background=self.storage['model'][model_name]['bkg'],
        )
        q.calc_Qo = np.linspace(
            q_array[argmin] - PADDING_RANGE * dq_vector[argmin],
            q_array[argmax] + PADDING_RANGE * dq_vector[argmax],
            UPSCALE_FACTOR * len(q_array),
        )
        R = names.Experiment(probe=q, sample=structure).reflectivity()[1]
        return R

    def sld_profile(self, model_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return the scattering length density profile.

        :param model_name: the model name
        :return: z and sld(z)
        """
        structure = model.Stack()
        for i in self.storage['model'][model_name]['items'][::-1]:
            if i.repeat.value == 1:
                for j in range(len(i.stack))[::-1]:
                    structure |= i.stack[j]
            else:
                stack = model.Stack()
                for j in range(len(i.stack))[::-1]:
                    stack |= i.stack[j]
                structure |= model.Repeat(stack, repeat=i.repeat.value)

        q = names.QProbe(
            np.linspace(0.001, 0.3, 10),
            np.linspace(0.001, 0.3, 10),
            intensity=self.storage['model'][model_name]['scale'],
            background=self.storage['model'][model_name]['bkg'],
        )
        z, sld, _ = names.Experiment(probe=q, sample=structure).smooth_profile()
        return z, sld[::-1]
