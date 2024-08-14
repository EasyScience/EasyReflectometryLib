"""
Tests for LayerCollection class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'

import unittest

from easyreflectometry.sample.assemblies.repeating_multilayer import RepeatingMultilayer
from easyreflectometry.sample.elements.layers.layer import Layer
from easyreflectometry.sample.elements.layers.layer_collection import LayerCollection
from easyreflectometry.sample.elements.materials.material import Material
from easyscience import global_object
from numpy.testing import assert_equal


class TestLayerCollection(unittest.TestCase):
    def test_default(self):
        p = LayerCollection()
        assert_equal(p.name, 'EasyLayers')
        assert_equal(p.interface, None)
        assert_equal(len(p), 2)
        assert_equal(p[0].name, 'EasyLayer')
        assert_equal(p[1].name, 'EasyLayer')

    def test_from_pars(self):
        m = Material(6.908, -0.278, 'Boron')
        k = Material(0.487, 0.000, 'Potassium')
        p = Layer(m, 5.0, 2.0, 'thinBoron')
        q = Layer(k, 50.0, 1.0, 'thickPotassium')
        layers = LayerCollection(p, q, name='twoLayer')
        assert_equal(layers.name, 'twoLayer')
        assert_equal(layers.interface, None)
        assert_equal(len(layers), 2)
        assert_equal(layers[0].name, 'thinBoron')
        assert_equal(layers[1].name, 'thickPotassium')

    def test_from_pars_item(self):
        m = Material(6.908, -0.278, 'Boron')
        p = Layer(m, 5.0, 2.0, 'thinBoron')
        i = RepeatingMultilayer(LayerCollection(), 2)
        layers = LayerCollection(p, i, name='twoLayer')
        assert_equal(layers.name, 'twoLayer')
        assert_equal(layers.interface, None)

    def test_dict_repr(self):
        p = LayerCollection()
        assert p._dict_repr == {
            'EasyLayers': [
                {
                    'EasyLayer': {
                        'material': {'EasyMaterial': {'sld': '4.186e-6 1/Å^2', 'isld': '0.000e-6 1/Å^2'}},
                        'thickness': '10.000 Å',
                        'roughness': '3.300 Å',
                    }
                },
                {
                    'EasyLayer': {
                        'material': {'EasyMaterial': {'sld': '4.186e-6 1/Å^2', 'isld': '0.000e-6 1/Å^2'}},
                        'thickness': '10.000 Å',
                        'roughness': '3.300 Å',
                    }
                },
            ]
        }

    def test_repr(self):
        p = LayerCollection()
        assert (
            p.__repr__()
            == 'EasyLayers:\n- EasyLayer:\n    material:\n      EasyMaterial:\n        sld: 4.186e-6 1/Å^2\n        isld: 0.000e-6 1/Å^2\n    thickness: 10.000 Å\n    roughness: 3.300 Å\n- EasyLayer:\n    material:\n      EasyMaterial:\n        sld: 4.186e-6 1/Å^2\n        isld: 0.000e-6 1/Å^2\n    thickness: 10.000 Å\n    roughness: 3.300 Å\n'  # noqa: E501
        )

    def test_dict_round_trip(self):
        # When
        m = Material(6.908, -0.278, 'Boron')
        k = Material(0.487, 0.000, 'Potassium')
        p = Layer(m, 5.0, 2.0, 'thinBoron')
        q = Layer(k, 50.0, 1.0, 'thickPotassium')
        r = LayerCollection()
        r.insert(0, p)
        r.append(q)
        r_dict = r.as_dict()
        global_object.map._clear()

        # Then
        s = LayerCollection.from_dict(r_dict)

        # Expect
        assert s.as_data_dict() == r.as_data_dict()
