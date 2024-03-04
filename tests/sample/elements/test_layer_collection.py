"""
Tests for LayerCollection class.
"""
__author__ = 'github.com/arm61'
__version__ = '0.0.1'

import unittest

from numpy.testing import assert_equal

from EasyReflectometry.sample.assemblies.repeating_multilayer import RepeatingMultilayer
from EasyReflectometry.sample.elements.layer_collection import LayerCollection
from EasyReflectometry.sample.elements.layers.layer import Layer
from EasyReflectometry.sample.elements.materials.material import Material


class TestLayerCollection(unittest.TestCase):
    def test_default(self):
        p = LayerCollection.default()
        assert_equal(p.name, 'EasyLayers')
        assert_equal(p.interface, None)
        assert_equal(len(p), 2)
        assert_equal(p[0].name, 'EasyLayer')
        assert_equal(p[1].name, 'EasyLayer')

    def test_from_pars(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium')
        layers = LayerCollection.from_pars(p, q, name='twoLayer')
        assert_equal(layers.name, 'twoLayer')
        assert_equal(layers.interface, None)
        assert_equal(len(layers), 2)
        assert_equal(layers[0].name, 'thinBoron')
        assert_equal(layers[1].name, 'thickPotassium')

    def test_from_pars_item(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        i = RepeatingMultilayer.from_pars(LayerCollection.default(), 2)
        layers = LayerCollection.from_pars(p, i, name='twoLayer')
        assert_equal(layers.name, 'twoLayer')
        assert_equal(layers.interface, None)

    def test_dict_repr(self):
        p = LayerCollection.default()
        print(p._dict_repr)
        assert p._dict_repr == {
            'EasyLayers': [
                {
                    'EasyLayer': {
                        'material': {
                            'EasyMaterial': {'sld': '4.186e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}
                        },
                        'thickness': '10.000 angstrom',
                        'roughness': '3.300 angstrom',
                    }
                },
                {
                    'EasyLayer': {
                        'material': {
                            'EasyMaterial': {'sld': '4.186e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}
                        },
                        'thickness': '10.000 angstrom',
                        'roughness': '3.300 angstrom',
                    }
                },
            ]
        }

    def test_repr(self):
        p = LayerCollection.default()
        assert (
            p.__repr__()
            == 'EasyLayers:\n- EasyLayer:\n    material:\n      EasyMaterial:\n        sld: 4.186e-6 1 / angstrom ** 2\n        isld: 0.000e-6 1 / angstrom ** 2\n    thickness: 10.000 angstrom\n    roughness: 3.300 angstrom\n- EasyLayer:\n    material:\n      EasyMaterial:\n        sld: 4.186e-6 1 / angstrom ** 2\n        isld: 0.000e-6 1 / angstrom ** 2\n    thickness: 10.000 angstrom\n    roughness: 3.300 angstrom\n'  # noqa: E501
        )

    def test_dict_round_trip(self):
        p = LayerCollection.default()
        q = LayerCollection.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
