import unittest

import numpy as np
from numpy.testing import assert_almost_equal

from EasyReflectometry.sample.elementals.materials.material_density import MaterialDensity


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
        assert p.as_data_dict() == q.as_data_dict()

