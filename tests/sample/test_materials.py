__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Layers class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.materials import Materials


class TestLayers(unittest.TestCase):
    def test_default(self):
        p = Materials.default()
        assert_equal(p.name, 'easyMaterials')
        assert_equal(p.interface, None)
        assert_equal(len(p), 2)
        assert_equal(p[0].name, 'easyMaterial')
        assert_equal(p[1].name, 'easyMaterial')

    def test_from_pars(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Materials.from_pars(m, k, name='thinBoron')
        assert_equal(p.name, 'thinBoron')
        assert_equal(p.interface, None)
        assert_equal(len(p), 2)
        assert_equal(p[0].name, 'Boron')
        assert_equal(p[1].name, 'Potassium')

    def test_repr(self):
        p = Materials.default()
        assert_equal(
            p.__repr__(),
            '<easyMaterials: A series of 2 materials>\n  - <easyMaterial: (sld: 4.186e-6 1/Å², isld: 0.000e-6 1/Å²)>\n  - <easyMaterial: (sld: 4.186e-6 1/Å², isld: 0.000e-6 1/Å²)>'
        )
