__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Model class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.structure.material import Material
from easyReflectometryLib.structure.layer import Layer
from easyReflectometryLib.structure.layers import Layers
from easyReflectometryLib.structure.item import Item
from easyReflectometryLib.structure.model import Model


class TestItem(unittest.TestCase):
    def test_default(self):
        p = Model.default()
        assert_equal(p.name, 'easyModel')
        assert_equal(p.interface, None)
        assert_equal(p[0].name, 'easyItem')
        assert_equal(p[1].name, 'easyItem')

    def test_from_pars(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = Layers.from_pars([l1, l2], 'twoLayer1')
        ls2 = Layers.from_pars([l2, l1], 'twoLayer2')
        o1 = Item.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = Item.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Model.from_pars([o1, o2], 'myModel')
        assert_equal(d.name, 'myModel')
        assert_equal(d.interface, None)
        assert_equal(d[0].name, 'twoLayerItem1')
        assert_equal(d[1].name, 'oneLayerItem2')

    def test_repr(self):
        p = Model.default()
        assert_equal(p.__repr__(), '<easyModel: A series of 2 items>')
