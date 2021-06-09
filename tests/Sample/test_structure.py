__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Model class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Sample.material import Material
from easyReflectometryLib.Sample.layer import Layer
from easyReflectometryLib.Sample.layers import Layers
from easyReflectometryLib.Sample.item import RepeatingMultiLayer
from easyReflectometryLib.Sample.structure import Structure


class TestStructure(unittest.TestCase):
    def test_default(self):
        p = Structure.default()
        assert_equal(p.name, 'easyStructure')
        assert_equal(p.interface, None)
        assert_equal(p[0].name, 'easyRepeatingMultiLayer')
        assert_equal(p[1].name, 'easyRepeatingMultiLayer')

    def test_from_pars(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
        ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultiLayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultiLayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Structure.from_pars(o1, o2, name='myModel')
        assert_equal(d.name, 'myModel')
        assert_equal(d.interface, None)
        assert_equal(d[0].name, 'twoLayerItem1')
        assert_equal(d[1].name, 'oneLayerItem2')

    def test_from_pars_layers(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        d = Structure.from_pars(l1, l2, name='myModel')
        assert_equal(d.name, 'myModel')
        assert_equal(d.interface, None)
        assert_equal(d[0].name, 'thinBoron')
        assert_equal(d[1].name, 'thickPotassium')

    def test_from_pars_error(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        with self.assertRaises(ValueError):
            _ = Structure.from_pars(m1, name='myModel')

    def test_repr(self):
        p = Structure.default()
        assert_equal(
            p.__repr__(),
            '<easyStructure: A series of 2 items>\n  - <easyRepeatingMultiLayer: (1.0 repetitions of <easyLayers: A series of 2 layers>\n  - <easyLayer: (material: <easyMaterial: (sld: 4.186e-6 1/Å², isld: 0.000e-6 1/Å²)>, thickness: 10.000 Å, roughness: 3.300 Å)>\n  - <easyLayer: (material: <easyMaterial: (sld: 4.186e-6 1/Å², isld: 0.000e-6 1/Å²)>, thickness: 10.000 Å, roughness: 3.300 Å)>)>\n  - <easyRepeatingMultiLayer: (1.0 repetitions of <easyLayers: A series of 2 layers>\n  - <easyLayer: (material: <easyMaterial: (sld: 4.186e-6 1/Å², isld: 0.000e-6 1/Å²)>, thickness: 10.000 Å, roughness: 3.300 Å)>\n  - <easyLayer: (material: <easyMaterial: (sld: 4.186e-6 1/Å², isld: 0.000e-6 1/Å²)>, thickness: 10.000 Å, roughness: 3.300 Å)>)>'
        )
