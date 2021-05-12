__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Item class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Sample.material import Material
from easyReflectometryLib.Sample.layer import Layer
from easyReflectometryLib.Sample.layers import Layers
from easyReflectometryLib.Sample.item import Item


class TestItem(unittest.TestCase):
    def test_default(self):
        p = Item.default()
        assert_equal(p.name, 'easyItem')
        assert_equal(p.interface, None)
        assert_equal(len(p.layers), 2)
        assert_equal(p.repetitions.display_name, 'repetitions')
        assert_equal(str(p.repetitions.unit), 'dimensionless')
        assert_equal(p.repetitions.value.n, 1.0)
        assert_equal(p.repetitions.min, 1)
        assert_equal(p.repetitions.max, 9999)
        assert_equal(p.repetitions.fixed, True)
        assert_equal(p.layers.name, 'easyLayers')

    def test_from_pars(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium')
        l = Layers.from_pars([p, q], 'twoLayer')
        o = Item.from_pars(l, 2.0, 'twoLayerItem')
        assert_equal(o.name, 'twoLayerItem')
        assert_equal(o.interface, None)
        assert_equal(o.repetitions.display_name, 'repetitions')
        assert_equal(str(o.repetitions.unit), 'dimensionless')
        assert_equal(o.repetitions.value.n, 2.0)
        assert_equal(o.repetitions.min, 1)
        assert_equal(o.repetitions.max, 9999)
        assert_equal(o.repetitions.fixed, True)
        assert_equal(o.layers.name, 'twoLayer')

    def test_from_pars_layer(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        o = Item.from_pars(p, 2.0, 'twoLayerItem')
        assert_equal(o.name, 'twoLayerItem')
        assert_equal(o.interface, None)
        assert_equal(o.repetitions.display_name, 'repetitions')
        assert_equal(str(o.repetitions.unit), 'dimensionless')
        assert_equal(o.repetitions.value.n, 2.0)
        assert_equal(o.repetitions.min, 1)
        assert_equal(o.repetitions.max, 9999)
        assert_equal(o.repetitions.fixed, True)
        assert_equal(o.layers.name, 'thinBoron')

    def test_repr(self):
        p = Item.default()
        assert_equal(
            p.__repr__(),
            '<easyItem: (1.0 repetitions of <easyLayers: A series of 2 layers>)>'
        )
