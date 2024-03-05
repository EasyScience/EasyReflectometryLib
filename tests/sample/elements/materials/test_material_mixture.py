import unittest
from unittest.mock import MagicMock

from numpy.testing import assert_almost_equal

from EasyReflectometry.sample.elements.materials.material import Material
from EasyReflectometry.sample.elements.materials.material_mixture import MaterialMixture


class TestMaterialMixture(unittest.TestCase):

    def test_default(self):
        p = MaterialMixture.default()
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        assert str(p.sld.unit) == '1 / angstrom ** 2'
        assert str(p.isld.unit) == '1 / angstrom ** 2'

    def test_default_constraint(self):
        p = MaterialMixture.default()
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
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
        assert r._fraction.raw_value == 0.2
        assert_almost_equal(r.sld.raw_value, 4.7304)
        assert_almost_equal(r.isld.raw_value, -0.0556)
        r._fraction.value = 0.5
        assert r._fraction.raw_value == 0.5
        assert_almost_equal(r.sld.raw_value, 5.54700)
        assert_almost_equal(r.isld.raw_value, -0.1390)

    def test_material_a_change(self):
        p = MaterialMixture.default()
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        q = Material.from_pars(6.908, -0.278, 'Boron')
        p.material_a = q
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
        assert_almost_equal(p.sld.raw_value, 5.54700)
        assert_almost_equal(p.isld.raw_value, -0.1390)

    def test_material_b_change(self):
        p = MaterialMixture.default()
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        q = Material.from_pars(6.908, -0.278, 'Boron')
        p.material_b = q
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
        assert_almost_equal(p.sld.raw_value, 5.54700)
        assert_almost_equal(p.isld.raw_value, -0.1390)

    def test_material_b_change_double(self):
        p = MaterialMixture.default()
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
        assert p.sld.raw_value == Material.default().sld.raw_value
        assert p.isld.raw_value == Material.default().isld.raw_value
        q = Material.from_pars(6.908, -0.278, 'Boron')
        p.material_b = q
        assert p.name == 'EasyMaterial/Boron'
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
        assert_almost_equal(p.sld.raw_value, 5.54700)
        assert_almost_equal(p.isld.raw_value, -0.1390)
        r = Material.from_pars(0.00, 0.00, 'ACMW')
        p.material_b = r
        assert p.name == 'EasyMaterial/ACMW'
        assert p._fraction.raw_value == 0.5
        assert str(p._fraction.unit) == 'dimensionless'
        assert_almost_equal(p.sld.raw_value, 2.0930)
        assert_almost_equal(p.isld.raw_value, 0.0000)

    def test_from_pars(self):
        p = Material.default()
        q = Material.from_pars(6.908, -0.278, 'Boron')
        r = MaterialMixture.from_pars(p, q, 0.2)
        assert r._fraction.raw_value == 0.2
        assert str(r._fraction.unit) == 'dimensionless'
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
                'material_a': {
                    'EasyMaterial': {
                        'sld': '4.186e-6 1 / angstrom ** 2',
                        'isld': '0.000e-6 1 / angstrom ** 2'
                    }
                },
                'material_b': {
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
        assert p.as_data_dict() == q.as_data_dict()
    
    def test_update_name(self):
        # When
        p = MaterialMixture.default()
        mock_material_a = MagicMock()
        mock_material_a.name = 'name_a'
        p._material_a = mock_material_a
        mock_material_b = MagicMock()
        mock_material_b.name = 'name_b'
        p._material_b = mock_material_b

        # Then
        p._update_name()

        # Expect
        assert p.name == 'name_a/name_b'
