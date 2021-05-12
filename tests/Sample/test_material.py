__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Material class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Sample.material import Material


class TestMaterial(unittest.TestCase):
    def test_default(self):
        p = Material.default()
        assert_equal(p.name, 'easyMaterial')
        assert_equal(p.interface, None)
        assert_equal(p.sld.display_name, 'sld')
        assert_equal(str(p.sld.unit), '1 / angstrom ** 2')
        assert_equal(p.sld.value.n, 4.186)
        assert_equal(p.sld.min, -np.Inf)
        assert_equal(p.sld.max, np.Inf)
        assert_equal(p.sld.fixed, True)
        assert_equal(p.isld.display_name, 'isld')
        assert_equal(str(p.isld.unit), '1 / angstrom ** 2')
        assert_equal(p.isld.value.n, 0.0)
        assert_equal(p.isld.min, -np.Inf)
        assert_equal(p.isld.max, np.Inf)
        assert_equal(p.isld.fixed, True)

    def test_from_pars(self):
        p = Material.from_pars(6.908, -0.278, 'Boron')
        assert_equal(p.name, 'Boron')
        assert_equal(p.interface, None)
        assert_equal(p.sld.display_name, 'sld')
        assert_equal(str(p.sld.unit), '1 / angstrom ** 2')
        assert_equal(p.sld.value.n, 6.908)
        assert_equal(p.sld.min, -np.Inf)
        assert_equal(p.sld.max, np.Inf)
        assert_equal(p.sld.fixed, True)
        assert_equal(p.isld.display_name, 'isld')
        assert_equal(str(p.isld.unit), '1 / angstrom ** 2')
        assert_equal(p.isld.value.n, -0.278)
        assert_equal(p.isld.min, -np.Inf)
        assert_equal(p.isld.max, np.Inf)
        assert_equal(p.isld.fixed, True)

    def test_repr(self):
        p = Material.default()
        assert_equal(
            p.__repr__(),
            '<easyMaterial: (sld: 4.186e-6 1/Å², isld: 0.000e-6 1/Å²)>')
