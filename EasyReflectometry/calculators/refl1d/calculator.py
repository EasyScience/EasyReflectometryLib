__author__ = 'github.com/arm61'

# import numpy as np
# from easyCore.Objects.Inferface import ItemContainer

# from EasyReflectometry.experiment.model import Model
# from EasyReflectometry.sample.items import MultiLayer
# from EasyReflectometry.sample.layer import Layer
# from EasyReflectometry.sample.material import Material
# from EasyReflectometry.sample.material import MaterialMixture

from ..calculator_base import CalculatorBase
from .wrapper import Refl1dWrapper


class Refl1d(CalculatorBase):
    """
    Calculator for refl1
    """

    name = 'refl1d'

    _material_link = {
        'sld': 'rho',
        'isld': 'irho',
    }

    _layer_link = {
        'thickness': 'thickness',
        'roughness': 'interface',
    }

    _item_link = {
        'repetitions': 'repeat',
    }

    _model_link = {
        'scale': 'scale',
        'background': 'bkg',
        'resolution': 'dq',
    }

    def __init__(self):
        super().__init__()
        self._wrapper = Refl1dWrapper()
        # self._namespace = {}

    # def reset_storage(self) -> None:
    #     """
    #     Reset the storage area of the calculator
    #     """
    #     self._wrapper.reset_storage()

    # def create(self, model: Material | Layer | MultiLayer | Model) -> list[ItemContainer]:
    #     """
    #     Creation function

    #     :param model: Object to be created
    #     :return: Item containers of the objects
    #     """
    #     r_list = []
    #     t_ = type(model)
    #     if issubclass(t_, Material):
    #         key = model.uid
    #         if key not in self._wrapper.storage['material'].keys():
    #             self._wrapper.create_material(key)
    #         r_list.append(
    #             ItemContainer(
    #                 key,
    #                 self._material_link,
    #                 self._wrapper.get_material_value,
    #                 self._wrapper.update_material,
    #             )
    #         )
    #     elif issubclass(t_, MaterialMixture):
    #         key = model.uid
    #         if key not in self._wrapper.storage['material'].keys():
    #             self._wrapper.create_material(key)
    #         r_list.append(
    #             ItemContainer(
    #                 key,
    #                 self._material_link,
    #                 self._wrapper.get_material_value,
    #                 self._wrapper.update_material,
    #             )
    #         )
    #     elif issubclass(t_, Layer):
    #         key = model.uid
    #         if key not in self._wrapper.storage['layer'].keys():
    #             self._wrapper.create_layer(key)
    #         r_list.append(
    #             ItemContainer(
    #                 key,
    #                 self._layer_link,
    #                 self._wrapper.get_layer_value,
    #                 self._wrapper.update_layer,
    #             )
    #         )
    #         self.assign_material_to_layer(model.material.uid, key)
    #     elif issubclass(t_, MultiLayer):
    #         key = model.uid
    #         self._wrapper.create_item(key)
    #         r_list.append(
    #             ItemContainer(
    #                 key,
    #                 self._item_link,
    #                 self._wrapper.get_item_value,
    #                 self._wrapper.update_item,
    #             )
    #         )
    #         for i in model.layers:
    #             self.add_layer_to_item(i.uid, model.uid)
    #     elif issubclass(t_, Model):
    #         key = model.uid
    #         self._wrapper.create_model(key)
    #         r_list.append(
    #             ItemContainer(
    #                 key,
    #                 self._model_link,
    #                 self._wrapper.get_model_value,
    #                 self._wrapper.update_model,
    #             )
    #         )
    #         for i in model.structure:
    #             self.add_item_to_model(i.uid, key)
    #     return r_list

    # def assign_material_to_layer(self, material_id: str, layer_id: str) -> None:
    #     """
    #     Assign a material to a layer.

    #     :param material_name: The material name
    #     :param layer_name: The layer name
    #     """
    #     self._wrapper.assign_material_to_layer(material_id, layer_id)

    # def add_layer_to_item(self, layer_id: str, item_id: str) -> None:
    #     """
    #     Add a layer to the item stack

    #     :param item_id: The item id
    #     :param layer_id: The layer id
    #     """
    #     self._wrapper.add_layer_to_item(layer_id, item_id)

    # def remove_layer_from_item(self, layer_id: str, item_id: str) -> None:
    #     """
    #     Remove a layer from an item stack

    #     :param item_id: The item id
    #     :type item_id: int        :param layer_id: The layer id
    #     """
    #     self._wrapper.remove_layer_from_item(layer_id, item_id)

    # def add_item_to_model(self, item_id: str, model_id: str) -> None:
    #     """
    #     Add a layer to the item stack

    #     :param item_id: The item id
    #     :param model_id: The model id
    #     """
    #     self._wrapper.add_item(item_id, model_id)

    # def remove_item_from_model(self, item_id: str, model_id: str) -> None:
    #     """
    #     Remove a layer from the item stack

    #     :param item_id: The item id
    #     :param model_id: The model id
    #     """
    #     self._wrapper.remove_item(item_id, model_id)

    # def fit_func(self, x_array: np.ndarray, model_id: str) -> np.ndarray:
    #     """
    #     Function to perform a fit

    #     :param x_array: points to be calculated at
    #     :param model_id: The name of the model
    #     :return: calculated points
    #     """
    #     return self._wrapper.calculate(x_array, model_id)

    # def sld_profile(self, model_id: str) -> tuple[np.ndarray, np.ndarray]:
    #     """
    #     Return the scattering length density profile.

    #     :return: z and sld(z)
    #     """
    #     return self._wrapper.sld_profile(model_id)
