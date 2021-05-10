__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Layers class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.structure.material import Material
from easyReflectometryLib.structure.layer import Layer
from easyReflectometryLib.structure.layers import Layers


class TestLayers(unittest.TestCase):
    def test_default(self):
        p = Layers.default()
        assert_equal(p.name, 'easyLayers')
        assert_equal(p.interface, None)
        assert_equal(len(p), 2)
        assert_equal(p[0].name, 'easyLayer')
        assert_equal(p[1].name, 'easyLayer')
    
    def test_from_pars(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium')
        l = Layers.from_pars([p, q], 'twoLayer')
        assert_equal(l.name, 'twoLayer')
        assert_equal(l.interface, None)
        assert_equal(len(l), 2)
        assert_equal(l[0].name, 'thinBoron')
        assert_equal(l[1].name, 'thickPotassium')

    def test_repr(self):
        p = Layers.default()
        assert_equal(p.__repr__(), '<easyLayers: A series of 2 layers>')
