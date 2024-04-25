"""
Tests for Layer class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'

import unittest

import numpy as np
from numpy.testing import assert_almost_equal
from numpy.testing import assert_equal

from EasyReflectometry.calculators.factory import CalculatorFactory
from EasyReflectometry.parameter_utils import get_as_parameter
from EasyReflectometry.sample.elements.layers.layer import DEFAULTS
from EasyReflectometry.sample.elements.layers.layer import Layer
from EasyReflectometry.sample.elements.materials.material import Material


class TestLayer(unittest.TestCase):
    def test_default(self):
        p = Layer()
        assert_equal(p.name, 'EasyLayer')
        assert_equal(p.interface, None)
        assert_equal(p.material.name, 'EasyMaterial')
        assert_equal(p.thickness.display_name, 'thickness')
        assert_equal(str(p.thickness.unit), 'angstrom')
        assert_equal(p.thickness.value.value.magnitude, 10.0)
        assert_equal(p.thickness.min, 0.0)
        assert_equal(p.thickness.max, np.Inf)
        assert_equal(p.thickness.fixed, True)
        assert_equal(p.roughness.display_name, 'roughness')
        assert_equal(str(p.roughness.unit), 'angstrom')
        assert_equal(p.roughness.value.value.magnitude, 3.3)
        assert_equal(p.roughness.min, 0.0)
        assert_equal(p.roughness.max, np.Inf)
        assert_equal(p.roughness.fixed, True)

    def test_from_pars(self):
        m = Material(6.908, -0.278, 'Boron')
        p = Layer(m, 5.0, 2.0, 'thinBoron')
        assert_equal(p.name, 'thinBoron')
        assert_equal(p.interface, None)
        assert_equal(p.material.name, 'Boron')
        assert_equal(p.thickness.display_name, 'thickness')
        assert_equal(str(p.thickness.unit), 'angstrom')
        assert_equal(p.thickness.value.value.magnitude, 5.0)
        assert_equal(p.thickness.min, 0.0)
        assert_equal(p.thickness.max, np.Inf)
        assert_equal(p.thickness.fixed, True)
        assert_equal(p.roughness.display_name, 'roughness')
        assert_equal(str(p.roughness.unit), 'angstrom')
        assert_equal(p.roughness.value.value.magnitude, 2.0)
        assert_equal(p.roughness.min, 0.0)
        assert_equal(p.roughness.max, np.Inf)
        assert_equal(p.roughness.fixed, True)

    def test_from_roughness_key(self):
        p = Layer(roughness=10.0)
        assert_equal(p.roughness.display_name, 'roughness')
        assert_equal(str(p.roughness.unit), 'angstrom')
        assert_equal(p.roughness.value.value.magnitude, 10.0)
        assert_equal(p.roughness.min, 0.0)
        assert_equal(p.roughness.max, np.Inf)
        assert_equal(p.roughness.fixed, True)

    def test_from_roughness_key_paramter(self):
        roughness = get_as_parameter('roughness', 10, DEFAULTS)
        roughness.min = -10.0
        p = Layer(roughness=roughness)
        assert_equal(p.roughness.value.value.magnitude, 10.0)
        assert_equal(p.roughness.min, -10.0)

    def test_from_thickness_key(self):
        p = Layer(thickness=10.0)
        assert_equal(p.thickness.display_name, 'thickness')
        assert_equal(str(p.thickness.unit), 'angstrom')
        assert_equal(p.thickness.value.value.magnitude, 10.0)
        assert_equal(p.thickness.min, 0.0)
        assert_equal(p.thickness.max, np.Inf)
        assert_equal(p.thickness.fixed, True)

    def test_from_thickness_key_paramter(self):
        thickness = get_as_parameter('thickness', 10, DEFAULTS)
        thickness.min = -10.0
        p = Layer(thickness=thickness)
        assert_equal(p.thickness.value.value.magnitude, 10.0)
        assert_equal(p.thickness.min, -10.0)

    def test_assign_material(self):
        m = Material(6.908, -0.278, 'Boron')
        p = Layer(m, 5.0, 2.0, 'thinBoron')
        k = Material(2.074, 0.0, 'Silicon')
        assert_almost_equal(p.material.sld.raw_value, 6.908)
        assert_almost_equal(p.material.isld.raw_value, -0.278)
        p.assign_material(k)
        assert_almost_equal(p.material.sld.raw_value, 2.074)
        assert_almost_equal(p.material.isld.raw_value, 0.0)

    def test_assign_material_with_interface_refnx(self):
        interface = CalculatorFactory()
        m = Material(6.908, -0.278, 'Boron', interface=interface)
        p = Layer(m, 5.0, 2.0, 'thinBoron', interface=interface)
        k = Material(2.074, 0.0, 'Silicon', interface=interface)
        assert_almost_equal(p.interface()._wrapper.storage['layer'][p.uid].sld.real.value, 6.908)
        assert_almost_equal(p.interface()._wrapper.storage['layer'][p.uid].sld.imag.value, -0.278)
        p.assign_material(k)
        assert_almost_equal(p.interface()._wrapper.storage['layer'][p.uid].sld.real.value, 2.074)
        assert_almost_equal(p.interface()._wrapper.storage['layer'][p.uid].sld.imag.value, 0.0)

    def test_dict_repr(self):
        p = Layer()
        assert p._dict_repr == {
            'EasyLayer': {
                'material': {'EasyMaterial': {'isld': '0.000e-6 1 / angstrom ** 2', 'sld': '4.186e-6 1 / angstrom ** 2'}},
                'roughness': '3.300 angstrom',
                'thickness': '10.000 angstrom',
            }
        }

    def test_repr(self):
        p = Layer()
        assert (
            p.__repr__()
            == 'EasyLayer:\n  material:\n    EasyMaterial:\n      sld: 4.186e-6 1 / angstrom ** 2\n      isld: 0.000e-6 1 / angstrom ** 2\n  thickness: 10.000 angstrom\n  roughness: 3.300 angstrom\n'  # noqa: E501
        )  # noqa: E501

    def test_dict_round_trip(self):
        p = Layer()
        q = Layer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
