# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
# flake8: noqa: E501
"""
Tests for write module
"""

# author: Andrew R. McCluskey (arm61)

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.material import Material
from easyCore.Objects.Base import Parameter 


class TestMaterial(unittest.TestCase):
    def test_default(self):
        p = Material.default()
        assert_equal(p.name, 'easyMaterial')
        assert_equal(p.color, '#96c6df')
        assert_equal(p.interface, None)
        assert_equal(p.sld_value.display_name, 'sld_value')
        assert_equal(str(p.sld_value.unit), '1 / angstrom ** 2')
        assert_equal(p.sld_value.value.n, 4.186)
        assert_equal(p.sld_value.min, -np.Inf)
        assert_equal(p.sld_value.max, np.Inf)
        assert_equal(p.sld_value.fixed, True)
        assert_equal(p.isld_value.display_name, 'isld_value')
        assert_equal(str(p.isld_value.unit), '1 / angstrom ** 2')
        assert_equal(p.isld_value.value.n, 0.0)
        assert_equal(p.isld_value.min, -np.Inf)
        assert_equal(p.isld_value.max, np.Inf)
        assert_equal(p.isld_value.fixed, True)

    def test_from_pars(self):
        p = Material.from_pars(6.908, -0.278, 'Boron')
        assert_equal(p.name, 'Boron')
        assert_equal(p.color, '#59a2cf')
        assert_equal(p.interface, None)
        assert_equal(p.sld_value.display_name, 'sld_value')
        assert_equal(str(p.sld_value.unit), '1 / angstrom ** 2')
        assert_equal(p.sld_value.value.n, 6.908)
        assert_equal(p.sld_value.min, -np.Inf)
        assert_equal(p.sld_value.max, np.Inf)
        assert_equal(p.sld_value.fixed, True)
        assert_equal(p.isld_value.display_name, 'isld_value')
        assert_equal(str(p.isld_value.unit), '1 / angstrom ** 2')
        assert_equal(p.isld_value.value.n, -0.278)
        assert_equal(p.isld_value.min, -np.Inf)
        assert_equal(p.isld_value.max, np.Inf)
        assert_equal(p.isld_value.fixed, True)

    def test_sld_property(self):
        p = Material.default()
        assert_almost_equal(p.sld, 4.186)

    def test_sld_setter(self):
        p = Material.default() 
        p.sld = 6.908
        assert_almost_equal(p.sld_value.value.n, 6.908)

    def test_isld_property(self):
        p = Material.default()
        assert_almost_equal(p.isld, 0.0)

    def test_isld_setter(self):
        p = Material.default() 
        p.isld = -0.278
        assert_almost_equal(p.isld_value.value.n, -0.278)
