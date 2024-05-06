__author__ = 'github.com/arm61'

import bornagain as ba
import numpy as np
from scipy.stats import norm

from ..wrapper_base import WrapperBase

"""
THIS CODE IS NOT FUNCTIONAL
PLEASE CONSULT ONE OF THE OTHER WRAPPES FOR A FUNCTIONAL EXAMPLE
"""


class BornAgainWrapper(WrapperBase):
    def __init__(self):
        super().__init__()
        self.storage = {
            'layer_material': {},
            'roughness': {},
            'item_repeats': {},
            'model_items': [],
            'model_parameters': {},
        }

    def reset_storage(self):
        """
        Reset the storage area to blank.
        """
        super().reset_storage()
        self.storage = {
            'layer_material': {},
            'roughness': {},
            'item_repeats': {},
            'model_items': [],
            'model_parameters': {},
        }

    def create_material(self, name):
        """
        Create a material using SLD.

        :param name: The name of the material
        :type name: str
        """
        self.storage['material'][name] = ba.MaterialBySLD(str(name), 0.0, 0.0)

    def update_material(self, name, **kwargs):
        """
        Update a material.

        :param name: The name of the material
        :type name: str
        """
        current_value = self.storage['material'][name].materialData()
        real = current_value.real
        imag = current_value.imag
        if 'real' in kwargs.keys():
            real = kwargs['real'] * 1e-6
        if 'imag' in kwargs.keys():
            if kwargs['imag'] < 0:
                raise ValueError('The BornAgain interface does not support negative imaginary scattering length densities')
            imag = kwargs['imag'] * 1e-6
        self.storage['material'][name] = ba.MaterialBySLD(str(name), real, imag)

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
        current_value = self.storage['material'][name].materialData()
        return getattr(current_value, key) / 1e-6

    def create_layer(self, name):
        """
        Create a layer using Slab.

        :param name: The name of the layer
        :type name: str
        """
        self.storage['layer'][name] = ba.Layer(ba.MaterialBySLD('A', 0, 0))
        self.storage['roughness'][name] = ba.LayerRoughness()

    def update_layer(self, name, **kwargs):
        """
        Update a layer in a given item.

        :param name: The layer name
        :type name: str
        """
        if 'thickness' in kwargs.keys():
            thickness = kwargs['thickness']
            self.storage['layer'][name] = ba.Layer(
                self.storage['material'][self.storage['layer_material'][name]], thickness * ba.angstrom
            )
        if 'sigma' in kwargs.keys():
            sigma = kwargs['sigma']
            self.storage['roughness'][name] = ba.LayerRoughness()
            self.storage['roughness'][name].setSigma(sigma * ba.angstrom)

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
        roughness = self.storage['roughness'][name]
        if key == 'thickness':
            return layer.thickness() / ba.angstrom
        if key == 'sigma':
            return roughness.getSigma() / ba.angstrom

    def create_item(self, name):
        """
        Create an item.

        :param name: The name of the item
        :type name: str
        """
        self.storage['item'][name] = []
        self.storage['item_repeats'][name] = 1

    def update_item(self, name, **kwargs):
        """
        Update a layer.

        :param name: The item name
        :type name: str
        """
        if 'repeats' in kwargs.keys():
            self.storage['item_repeats'][name] = kwargs['repeats']

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
        if key == 'repeats':
            return self.storage['item_repeats'][name]

    def create_model(self):
        """
        Create a model for analysis
        """
        self.storage['model'] = ba.Multilayer()
        self.storage['model'].setRoughnessModel(ba.RoughnessModel.NEVOT_CROCE)
        self.storage['model_items'] = []
        self.storage['model_parameters']['scale'] = 1
        self.storage['model_parameters']['background'] = 0
        self.storage['model_parameters']['resolution'] = 0

    def update_model(self, name, **kwargs):
        """
        Update the non-structural parameters of the model
        """
        model = self.storage[name + '_parameters']
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
        model = self.storage[name + '_parameters']
        return model[key]

    def assign_material_to_layer(self, material_name, layer_name):
        """
        Assign a material to a layer.

        :param material_name: The material name
        :type material_name: str
        :param layer_name: The layer name
        :type layer_name: str
        """
        self.storage['layer_material'][layer_name] = material_name

    def add_layer_to_item(self, layer_name, item_name):
        """
        Create a layer from the material of the same name, in a given item.

        :param layer_name: The layer name
        :type layer_name: int
        :param item_name: The item name
        :type item_name: int
        """
        item = self.storage['item'][item_name]
        item.append(layer_name)

    def add_item(self, item_name):
        """
        Add an item to the model.

        :param item_name: items to add to model
        :type item_name: str
        """
        self.storage['model_items'].append(item_name)

    def remove_layer_from_item(self, layer_name, item_name):
        """
        Remove a layer in a given item.

        :param layer_name: The layer name
        :type layer_name: int
        :param item_name: The item name
        :type item_name: int
        """
        layers_idx = self.storage['item'][item_name].index(layer_name)
        del self.storage['layer'][layer_name]
        del self.storage['item'][item_name][layers_idx]
        del self.storage['layer_material'][layer_name]

    def remove_item(self, item_name):
        """
        Remove a given item.

        :param item_name: The item name
        :type item_name: int
        """
        item_idx = self.storage['model_items'].index(item_name)
        del self.storage['model_items'][item_idx]
        del self.storage['item_repeats'][item_name]
        del self.storage['item'][item_name]

    # To conform the base class the signature should be
    # def calculate(self, q_array: np.ndarray, model_name: str) -> np.ndarray:
    def calculate(self, q_array: np.ndarray) -> np.ndarray:
        """For a given q array calculate the corresponding reflectivity.

        :param q_array: array of data points to be calculated
        :param model_name: the model name
        :return: reflectivity calculated at q
        """
        # 3.5 sigma to sync with refnx
        n_sig = 3.5
        n_samples = 21
        distr = ba.RangedDistributionGaussian(n_samples, n_sig)

        scan = ba.QSpecScan(q_array / ba.angstrom)
        scan.setAbsoluteQResolution(
            distr, q_array / ba.angstrom * (self.storage['model_parameters']['resolution'] * 0.5 / 100)
        )

        simulation = ba.SpecularSimulation()
        simulation.setScan(scan)

        total_model = ba.Multilayer()
        for i in self.storage['model_items']:
            for k in range(int(self.storage['item_repeats'][i])):
                for j in self.storage['item'][i]:
                    layer = ba.Layer(
                        self.storage['material'][self.storage['layer_material'][j]],
                        self.storage['layer'][j].thickness(),
                    )
                    total_model.addLayerWithTopRoughness(layer, self.storage['roughness'][j])

        simulation.setSample(total_model)
        simulation.runSimulation()

        return (
            self.storage['model_parameters']['scale'] * simulation.result().array()
            + self.storage['model_parameters']['background']
        )

    def sld_profile(self) -> np.ndarray:
        """
        Return the scattering length density profile.

        This is borrowed from the refnx implementation of the scattering length density.

        :return: z and sld(z)
        :rtype: tuple[np.ndarray, np.ndarray]
        """
        number_of_layers = 0
        for i in self.storage['model_items']:
            number_of_layers += len(self.storage['item'][i]) * self.storage['item_repeats'][i]
        layers = np.zeros((int(number_of_layers), 4))

        count = 0
        for i in self.storage['model_items']:
            for k in range(int(self.storage['item_repeats'][i])):
                for j in self.storage['item'][i]:
                    layers[count, 0] = self.storage['layer'][j].thickness()
                    layers[count, 1] = self.storage['material'][self.storage['layer_material'][j]].materialData().real
                    layers[count, 2] = self.storage['material'][self.storage['layer_material'][j]].materialData().imag
                    layers[count, 3] = self.storage['roughness'][j].getSigma()
                    count += 1

        layers2 = np.copy(layers)
        layers[:, 0] = np.fabs(layers2[:, 0])
        layers[:, 3] = np.fabs(layers2[:, 3])
        # bounding layers should have zero thickness
        layers[0, 0] = layers[-1, 0] = 0

        # distance of each interface from the fronting interface
        dist = np.cumsum(layers[:-1, 0])
        zstart = -5 - 4 * np.fabs(layers2[1, 3])
        zend = 5 + dist[-1] + 4 * layers[-1, 3]

        npnts = 500
        zed = np.linspace(zstart, zend, num=npnts)

        # the output array
        sld = np.ones_like(zed, dtype=float) * layers[0, 1]

        # work out the step in SLD at an interface
        delta_rho = layers[1:, 1] - layers[:-1, 1]

        # use erf for roughness function, but step if the roughness is zero
        def step(z, scale=1, loc=0):
            new_z = z - loc
            f = np.ones_like(new_z) * 0.5
            f[new_z <= -scale] = 0
            f[new_z >= scale] = 1
            return f

        step_f = step
        erf_f = norm.cdf
        sigma = layers[1:, 3]

        # accumulate the SLD of each step.
        for i in range(int(number_of_layers) - 1):
            f = erf_f
            if sigma[i] == 0:
                f = step_f
            sld += delta_rho[i] * f(zed, scale=sigma[i], loc=dist[i])

        return zed / ba.angstrom, sld * 1e6
