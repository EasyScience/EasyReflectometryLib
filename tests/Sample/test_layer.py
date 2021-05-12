__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Layer class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Sample.material import Material
from easyReflectometryLib.Sample.layer import Layer


class TestLayer(unittest.TestCase):
    def test_default(self):
        p = Layer.default()
        assert_equal(p.name, 'easyLayer')
        assert_equal(p.interface, None)
        assert_equal(p.material.name, 'easyMaterial')
        assert_equal(p.thickness.display_name, 'thickness')
        assert_equal(str(p.thickness.unit), 'angstrom')
        assert_equal(p.thickness.value.n, 10.0)
        assert_equal(p.thickness.min, 0.0)
        assert_equal(p.thickness.max, np.Inf)
        assert_equal(p.thickness.fixed, True)
        assert_equal(p.roughness.display_name, 'roughness')
        assert_equal(str(p.roughness.unit), 'angstrom')
        assert_equal(p.roughness.value.n, 1.2)
        assert_equal(p.roughness.min, 0.0)
        assert_equal(p.roughness.max, np.Inf)
        assert_equal(p.roughness.fixed, True)

    def test_from_pars(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        assert_equal(p.name, 'thinBoron')
        assert_equal(p.interface, None)
        assert_equal(p.material.name, 'Boron')
        assert_equal(p.thickness.display_name, 'thickness')
        assert_equal(str(p.thickness.unit), 'angstrom')
        assert_equal(p.thickness.value.n, 5.0)
        assert_equal(p.thickness.min, 0.0)
        assert_equal(p.thickness.max, np.Inf)
        assert_equal(p.thickness.fixed, True)
        assert_equal(p.roughness.display_name, 'roughness')
        assert_equal(str(p.roughness.unit), 'angstrom')
        assert_equal(p.roughness.value.n, 2.0)
        assert_equal(p.roughness.min, 0.0)
        assert_equal(p.roughness.max, np.Inf)
        assert_equal(p.roughness.fixed, True)

    def test_repr(self):
        p = Layer.default()
        assert_equal(
            p.__repr__(),
            '<easyLayer: (material: <easyMaterial: (sld: 4.186e-6 1/Å², isld: 0.000e-6 1/Å²)>, thickness: 10.000 Å, roughness: 1.200 Å)>'
        )
