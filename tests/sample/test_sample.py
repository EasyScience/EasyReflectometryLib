"""
Tests for Sample class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'

import unittest

from numpy.testing import assert_equal

from EasyReflectometry.sample import Layer
from EasyReflectometry.sample import LayerCollection
from EasyReflectometry.sample import Material
from EasyReflectometry.sample import Multilayer
from EasyReflectometry.sample import RepeatingMultilayer
from EasyReflectometry.sample import Sample
from EasyReflectometry.sample import SurfactantLayer


class TestSample(unittest.TestCase):
    def test_default(self):
        p = Sample()
        assert_equal(p.name, 'EasySample')
        assert_equal(p.interface, None)
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, 'EasyMultilayer')

    def test_from_pars(self):
        m1 = Material(6.908, -0.278, 'Boron')
        m2 = Material(0.487, 0.000, 'Potassium')
        l1 = Layer(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection(l1, l2, name='twoLayer1')
        ls2 = LayerCollection(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer(ls2, 1.0, 'oneLayerItem2')
        d = Sample(o1, o2, name='myModel')
        assert_equal(d.name, 'myModel')
        assert_equal(d.interface, None)
        assert_equal(d[0].name, 'twoLayerItem1')
        assert_equal(d[1].name, 'oneLayerItem2')

    def test_from_pars_layers(self):
        m1 = Material(6.908, -0.278, 'Boron')
        m2 = Material(0.487, 0.000, 'Potassium')
        l1 = Layer(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer(m2, 50.0, 1.0, 'thickPotassium')
        d = Sample(l1, l2, name='myModel')
        assert_equal(d.name, 'myModel')
        assert_equal(d.interface, None)
        assert_equal(d[0].name, 'thinBoron')
        assert_equal(d[1].name, 'thickPotassium')

    def test_from_pars_error(self):
        m1 = Material(6.908, -0.278, 'Boron')
        with self.assertRaises(ValueError):
            _ = Sample(m1, name='myModel')

    def test_repr(self):
        p = Sample()
        assert (
            p.__repr__()
            == 'EasySample:\n- EasyMultilayer:\n    EasyLayers:\n    - EasyLayer:\n        material:\n          EasyMaterial:\n            sld: 4.186e-6 1 / angstrom ** 2\n            isld: 0.000e-6 1 / angstrom ** 2\n        thickness: 10.000 angstrom\n        roughness: 3.300 angstrom\n    - EasyLayer:\n        material:\n          EasyMaterial:\n            sld: 4.186e-6 1 / angstrom ** 2\n            isld: 0.000e-6 1 / angstrom ** 2\n        thickness: 10.000 angstrom\n        roughness: 3.300 angstrom\n- EasyMultilayer:\n    EasyLayers:\n    - EasyLayer:\n        material:\n          EasyMaterial:\n            sld: 4.186e-6 1 / angstrom ** 2\n            isld: 0.000e-6 1 / angstrom ** 2\n        thickness: 10.000 angstrom\n        roughness: 3.300 angstrom\n    - EasyLayer:\n        material:\n          EasyMaterial:\n            sld: 4.186e-6 1 / angstrom ** 2\n            isld: 0.000e-6 1 / angstrom ** 2\n        thickness: 10.000 angstrom\n        roughness: 3.300 angstrom\n'  # noqa: E501
        )

    def test_dict_round_trip(self):
        # When
        p = Sample()
        surfactant = SurfactantLayer()
        p.append(surfactant)
        multilayer = Multilayer()
        p.append(multilayer)
        repeating = RepeatingMultilayer()
        p.append(repeating)

        # Then
        q = Sample.from_dict(p.as_dict())

        # Expect
        assert p.as_data_dict() == q.as_data_dict()
