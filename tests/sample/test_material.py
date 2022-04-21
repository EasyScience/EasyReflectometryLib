__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Material class module
"""

import unittest
import numpy as np
from numpy.testing import assert_almost_equal
from EasyReflectometry.sample.material import Material, MaterialDensity, MaterialMixture


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
        assert p.to_data_dict() == q.to_data_dict()


class TestMaterialDensity(unittest.TestCase):

    def test_default(self):
        p = MaterialDensity.default()
        assert p.name == 'EasyMaterialDensity'
        assert p.interface == None
        assert p.density.display_name == 'density'
        assert str(p.density.unit) == 'gram / centimeter ** 3'
        assert p.density.value.n == 2.33
        assert p.density.min == 0
        assert p.density.max == np.Inf
        assert p.density.fixed == True

    def test_default_constraint(self):
        p = MaterialDensity.default()
        assert p.density.value.n == 2.33
        assert_almost_equal(p.sld.value.n, 2.073705382)
        p.density.value = 2
        assert_almost_equal(p.sld.value.n, 1.780004619)

    def test_from_pars(self):
        p = MaterialDensity.from_pars('Co', 8.9, 'Cobalt')
        assert p.density.value.n == 8.9
        assert_almost_equal(p.sld.value.n, 2.2645412328256)
        assert p.chemical_structure == 'Co'

    def test_chemical_structure_change(self):
        p = MaterialDensity.from_pars('Co', 8.9, 'Cobolt')
        assert p.density.value.n == 8.9
        assert_almost_equal(p.sld.value.n, 2.2645412328256)
        assert_almost_equal(p.isld.value.n, 0.0)
        assert p.chemical_structure == 'Co'
        p.chemical_structure = 'B'
        assert p.density.value.n == 8.9
        assert_almost_equal(p.sld.value.n, 4.820107844970)
        assert_almost_equal(p.isld.value.n, -0.19098540517806603)
        assert p.chemical_structure == 'B'

    def test_dict_repr(self):
        p = MaterialDensity.default()
        print(p._dict_repr)
        assert p._dict_repr == {
            'EasyMaterialDensity': {
                'sld': '2.074e-6 1 / angstrom ** 2',
                'isld': '0.000e-6 1 / angstrom ** 2'
            },
            'chemical_structure': 'Si',
            'density': '2.33e+00 gram / centimeter ** 3'
        }

    def test_dict_round_trip(self):
        p = MaterialDensity.default()
        q = MaterialDensity.from_dict(p.as_dict())
        assert p.to_data_dict() == q.to_data_dict()


class TestMaterialMixture(unittest.TestCase):

    def test_default(self):
        p = MaterialMixture.default()
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        assert str(p.sld.unit) == '1 / angstrom ** 2'
        assert str(p.isld.unit) == '1 / angstrom ** 2'

    def test_default_constraint(self):
        p = MaterialMixture.default()
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        p.material_a.sld.value = 0
        p.material_b.isld.value = -1
        assert_almost_equal(p.sld.raw_value, 2.093)
        assert_almost_equal(p.isld.raw_value, -0.5)
        assert str(p.sld.unit) == '1 / angstrom ** 2'
        assert str(p.isld.unit) == '1 / angstrom ** 2'
    
    def test_fraction_constraint(self):
        p = Material.default()
        q = Material.from_pars(6.908, -0.278, 'Boron')
        r = MaterialMixture.from_pars(p, q, 0.2)
        assert r.fraction.raw_value == 0.2
        assert_almost_equal(r.sld.raw_value, 4.7304)
        assert_almost_equal(r.isld.raw_value, -0.0556)
        r.fraction.value = 0.5
        assert r.fraction.raw_value == 0.5
        assert_almost_equal(r.sld.raw_value, 5.54700)
        assert_almost_equal(r.isld.raw_value, -0.1390)

    def test_material_a_change(self):
        p = MaterialMixture.default()
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        q = Material.from_pars(6.908, -0.278, 'Boron')
        p.material_a = q
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert_almost_equal(p.sld.raw_value, 5.54700)
        assert_almost_equal(p.isld.raw_value, -0.1390)

    def test_material_b_change(self):
        p = MaterialMixture.default()
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        q = Material.from_pars(6.908, -0.278, 'Boron')
        p.material_b = q
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert_almost_equal(p.sld.raw_value, 5.54700)
        assert_almost_equal(p.isld.raw_value, -0.1390)

    def test_material_b_change_double(self):
        p = MaterialMixture.default()
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        q = Material.from_pars(6.908, -0.278, 'Boron')
        p.material_b = q
        assert p.name == 'EasyMaterial/Boron'
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert_almost_equal(p.sld.raw_value, 5.54700)
        assert_almost_equal(p.isld.raw_value, -0.1390)
        r = Material.from_pars(0.00, 0.00, 'ACMW')
        p.material_b = r
        assert p.name == 'EasyMaterial/ACMW'
        assert p.fraction.raw_value == 0.5
        assert str(p.fraction.unit) == 'dimensionless'
        assert_almost_equal(p.sld.raw_value, 2.0930)
        assert_almost_equal(p.isld.raw_value, 0.0000)

    def test_from_pars(self):
        p = Material.default()
        q = Material.from_pars(6.908, -0.278, 'Boron')
        r = MaterialMixture.from_pars(p, q, 0.2)
        assert r.fraction.raw_value == 0.2
        assert str(r.fraction.unit) == 'dimensionless'
        assert_almost_equal(r.sld.raw_value, 4.7304)
        assert_almost_equal(r.isld.raw_value, -0.0556)
        assert str(r.sld.unit) == '1 / angstrom ** 2'
        assert str(r.isld.unit) == '1 / angstrom ** 2'

    def test_dict_repr(self):
        p = MaterialMixture.default()
        assert p._dict_repr == {
            'EasyMaterial/EasyMaterial': {
                'fraction': 0.5,
                'sld': '4.186e-6 1 / angstrom ** 2',
                'isld': '0.000e-6 1 / angstrom ** 2',
                'material1': {
                    'EasyMaterial': {
                        'sld': '4.186e-6 1 / angstrom ** 2',
                        'isld': '0.000e-6 1 / angstrom ** 2'
                    }
                },
                'material2': {
                    'EasyMaterial': {
                        'sld': '4.186e-6 1 / angstrom ** 2',
                        'isld': '0.000e-6 1 / angstrom ** 2'
                    }
                }
            }
        }

    def test_dict_round_trip(self):
        p = MaterialMixture.default()
        q = MaterialMixture.from_dict(p.as_dict())
        assert p.to_data_dict() == q.to_data_dict()
