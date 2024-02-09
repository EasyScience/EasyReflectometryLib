__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Material class module
"""

import unittest

import numpy as np

from EasyReflectometry.sample.elementals.materials.material import Material


class TestMaterial(unittest.TestCase):

    def test_default(self):
        p = Material.default()
        assert p.name == 'EasyMaterial'
        assert p.interface == None
        assert p.sld.display_name == 'sld'
        assert str(p.sld.unit) == '1 / angstrom ** 2'
        assert p.sld.value.n == 4.186
        assert p.sld.min == -np.Inf
        assert p.sld.max == np.Inf
        assert p.sld.fixed == True
        assert p.isld.display_name == 'isld'
        assert str(p.isld.unit) == '1 / angstrom ** 2'
        assert p.isld.value.n == 0.0
        assert p.isld.min == -np.Inf
        assert p.isld.max == np.Inf
        assert p.isld.fixed == True

    def test_from_pars(self):
        p = Material.from_pars(6.908, -0.278, 'Boron')
        assert p.name == 'Boron'
        assert p.interface == None
        assert p.sld.display_name == 'sld'
        assert str(p.sld.unit) == '1 / angstrom ** 2'
        assert p.sld.value.n == 6.908
        assert p.sld.min == -np.Inf
        assert p.sld.max == np.Inf
        assert p.sld.fixed == True
        assert p.isld.display_name == 'isld'
        assert str(p.isld.unit) == '1 / angstrom ** 2'
        assert p.isld.value.n == -0.278
        assert p.isld.min == -np.Inf
        assert p.isld.max == np.Inf
        assert p.isld.fixed == True

    def test_dict_repr(self):
        p = Material.default()
        assert p._dict_repr == {
            'EasyMaterial': {
                'sld': '4.186e-6 1 / angstrom ** 2',
                'isld': '0.000e-6 1 / angstrom ** 2'
            }
        }

    def test_repr(self):
        p = Material.default()
        assert p.__repr__(
        ) == 'EasyMaterial:\n  sld: 4.186e-6 1 / angstrom ** 2\n  isld: 0.000e-6 1 / angstrom ** 2\n'

    def test_dict_round_trip(self):
        p = Material.default()
        q = Material.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

