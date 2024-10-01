"""
Tests for Material class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'

import numpy as np
from easyscience import global_object

from easyreflectometry.parameter_utils import get_as_parameter
from easyreflectometry.sample.elements.materials.material import DEFAULTS
from easyreflectometry.sample.elements.materials.material import Material


class TestMaterial:
    def test_no_arguments(self):
        p = Material()
        assert p.name == 'EasyMaterial'
        assert p.interface is None
        assert p.sld.display_name == 'sld'
        assert str(p.sld.unit) == '1/Å^2'
        assert p.sld.value == 4.186
        assert p.sld.min == -np.Inf
        assert p.sld.max == np.Inf
        assert p.sld.fixed is True
        assert p.isld.display_name == 'isld'
        assert str(p.isld.unit) == '1/Å^2'
        assert p.isld.value == 0.0
        assert p.isld.min == -np.Inf
        assert p.isld.max == np.Inf
        assert p.isld.fixed is True

    def test_shuffled_arguments(self):
        p = Material(name='Boron', sld=6.908, isld=-0.278)
        assert p.name == 'Boron'
        assert p.interface is None
        assert p.sld.display_name == 'sld'
        assert str(p.sld.unit) == '1/Å^2'
        assert p.sld.value == 6.908
        assert p.sld.min == -np.Inf
        assert p.sld.max == np.Inf
        assert p.sld.fixed is True
        assert p.isld.display_name == 'isld'
        assert str(p.isld.unit) == '1/Å^2'
        assert p.isld.value == -0.278
        assert p.isld.min == -np.Inf
        assert p.isld.max == np.Inf
        assert p.isld.fixed is True

    def test_only_sld_key(self):
        p = Material(sld=10)
        assert p.sld.display_name == 'sld'
        assert str(p.sld.unit) == '1/Å^2'
        assert p.sld.value == 10
        assert p.sld.min == -np.Inf
        assert p.sld.max == np.Inf
        assert p.sld.fixed is True

    def test_only_sld_key_parameter(self):
        sld = get_as_parameter('sld', 10, DEFAULTS)
        sld.min = -10.0
        p = Material(sld=sld)
        assert p.sld.value == 10
        assert p.sld.min == -10

    def test_only_isld_key(self):
        p = Material(isld=10)
        assert p.isld.display_name == 'isld'
        assert str(p.isld.unit) == '1/Å^2'
        assert p.isld.value == 10
        assert p.isld.min == -np.Inf
        assert p.isld.max == np.Inf
        assert p.isld.fixed is True

    def test_only_isld_key_parameter(self):
        isld = get_as_parameter('isld', 10, DEFAULTS)
        isld.min = -10.0
        p = Material(isld=isld)
        assert p.isld.value == 10
        assert p.isld.min == -10

    def test_dict_repr(self):
        p = Material()
        assert p._dict_repr == {'EasyMaterial': {'sld': '4.186e-6 1/Å^2', 'isld': '0.000e-6 1/Å^2'}}

    def test_repr(self):
        p = Material()
        assert p.__repr__() == 'EasyMaterial:\n  sld: 4.186e-6 1/Å^2\n  isld: 0.000e-6 1/Å^2\n'

    def test_dict_round_trip(self):
        p = Material()
        p_dict = p.as_dict()
        global_object.map._clear()

        q = Material.from_dict(p_dict)

        assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())
