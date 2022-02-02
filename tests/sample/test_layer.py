__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Layer class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.interface import InterfaceFactory


class TestLayer(unittest.TestCase):

    def test_default(self):
        p = Layer.default()
        assert_equal(p.name, 'EasyLayer')
        assert_equal(p.interface, None)
        assert_equal(p.material.name, 'EasyMaterial')
        assert_equal(p.thickness.display_name, 'thickness')
        assert_equal(str(p.thickness.unit), 'angstrom')
        assert_equal(p.thickness.value.n, 10.0)
        assert_equal(p.thickness.min, 0.0)
        assert_equal(p.thickness.max, np.Inf)
        assert_equal(p.thickness.fixed, True)
        assert_equal(p.roughness.display_name, 'roughness')
        assert_equal(str(p.roughness.unit), 'angstrom')
        assert_equal(p.roughness.value.n, 3.3)
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

    def test_assign_material(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        k = Material.from_pars(2.074, 0.0, 'Silicon')
        assert_almost_equal(p.material.sld.raw_value, 6.908)
        assert_almost_equal(p.material.isld.raw_value, -0.278)
        p.assign_material(k)
        assert_almost_equal(p.material.sld.raw_value, 2.074)
        assert_almost_equal(p.material.isld.raw_value, 0.0)

    def test_assign_material_with_interface_refnx(self):
        interface = InterfaceFactory()
        m = Material.from_pars(6.908, -0.278, 'Boron', interface=interface)
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron', interface=interface)
        k = Material.from_pars(2.074, 0.0, 'Silicon', interface=interface)
        assert_almost_equal(
            p.interface().calculator.storage['layer'][p.uid].sld.real.value, 6.908)
        assert_almost_equal(
            p.interface().calculator.storage['layer'][p.uid].sld.imag.value, -0.278)
        p.assign_material(k)
        assert_almost_equal(
            p.interface().calculator.storage['layer'][p.uid].sld.real.value, 2.074)
        assert_almost_equal(
            p.interface().calculator.storage['layer'][p.uid].sld.imag.value, 0.0)

    def test_dict_repr(self):
        p = Layer.default()
        assert p._dict_repr == {
            'EasyLayer': {
                'material': {
                    'EasyMaterial': {
                        'isld': '0.000e-6 1 / angstrom ** 2',
                        'sld': '4.186e-6 1 / angstrom ** 2'
                    }
                },
                'roughness': '3.300 angstrom',
                'thickness': '10.000 angstrom'
            }
        }

    def test_repr(self):
        p = Layer.default()
        assert p.__repr__(
        ) == 'EasyLayer:\n  material:\n    EasyMaterial:\n      sld: 4.186e-6 1 / angstrom ** 2\n      isld: 0.000e-6 1 / angstrom ** 2\n  thickness: 10.000 angstrom\n  roughness: 3.300 angstrom\n'
