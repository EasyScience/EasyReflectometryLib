"""
Tests for Material class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'


import unittest

import numpy as np
from easyreflectometry.parameter_utils import get_as_parameter
from easyreflectometry.sample.elements.materials.material import DEFAULTS
from easyreflectometry.sample.elements.materials.material import Material


class TestMaterial(unittest.TestCase):
    def test_no_arguments(self):
        p = Material()
        assert p.name == 'EasyMaterial'
        assert p.interface is None
        assert p.sld.display_name == 'sld'
        assert str(p.sld.unit) == '1 / angstrom ** 2'
        assert p.sld.value.value.magnitude == 4.186
        assert p.sld.min == -np.inf
        assert p.sld.max == np.inf
        assert p.sld.fixed is True
        assert p.isld.display_name == 'isld'
        assert str(p.isld.unit) == '1 / angstrom ** 2'
        assert p.isld.value.value.magnitude == 0.0
        assert p.isld.min == -np.inf
        assert p.isld.max == np.inf
        assert p.isld.fixed is True

    def test_shuffled_arguments(self):
        p = Material(name='Boron', sld=6.908, isld=-0.278)
        assert p.name == 'Boron'
        assert p.interface is None
        assert p.sld.display_name == 'sld'
        assert str(p.sld.unit) == '1 / angstrom ** 2'
        assert p.sld.value.value.magnitude == 6.908
        assert p.sld.min == -np.inf
        assert p.sld.max == np.inf
        assert p.sld.fixed is True
        assert p.isld.display_name == 'isld'
        assert str(p.isld.unit) == '1 / angstrom ** 2'
        assert p.isld.value.value.magnitude == -0.278
        assert p.isld.min == -np.inf
        assert p.isld.max == np.inf
        assert p.isld.fixed is True

    def test_only_sld_key(self):
        p = Material(sld=10)
        assert p.sld.display_name == 'sld'
        assert str(p.sld.unit) == '1 / angstrom ** 2'
        assert p.sld.value.value.magnitude == 10
        assert p.sld.min == -np.inf
        assert p.sld.max == np.inf
        assert p.sld.fixed is True

    def test_only_sld_key_parameter(self):
        sld = get_as_parameter('sld', 10, DEFAULTS)
        sld.min = -10.0
        p = Material(sld=sld)
        assert p.sld.value.value.magnitude == 10
        assert p.sld.min == -10

    def test_only_isld_key(self):
        p = Material(isld=10)
        assert p.isld.display_name == 'isld'
        assert str(p.isld.unit) == '1 / angstrom ** 2'
        assert p.isld.value.value.magnitude == 10
        assert p.isld.min == -np.inf
        assert p.isld.max == np.inf
        assert p.isld.fixed is True

    def test_only_isld_key_parameter(self):
        isld = get_as_parameter('isld', 10, DEFAULTS)
        isld.min = -10.0
        p = Material(isld=isld)
        assert p.isld.value.value.magnitude == 10
        assert p.isld.min == -10

    def test_dict_repr(self):
        p = Material()
        assert p._dict_repr == {'EasyMaterial': {'sld': '4.186e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}}

    def test_repr(self):
        p = Material()
        assert p.__repr__() == 'EasyMaterial:\n  sld: 4.186e-6 1 / angstrom ** 2\n  isld: 0.000e-6 1 / angstrom ** 2\n'

    def test_dict_round_trip(self):
        p = Material()
        q = Material.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
