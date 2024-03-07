"""
Tests for LayerAreaPerMolecule class.
"""
import unittest

from numpy.testing import assert_almost_equal

from EasyReflectometry.sample.elements.layers.layer_area_per_molecule import LayerAreaPerMolecule
from EasyReflectometry.sample.elements.materials.material import Material


class TestLayerAreaPerMolecule(unittest.TestCase):
    def test_default(self):
        p = LayerAreaPerMolecule.default()
        assert p.molecular_formula == 'C10H18NO8P'
        assert p.area_per_molecule.raw_value == 48.2
        assert str(p.area_per_molecule.unit) == 'angstrom ** 2'
        assert p.area_per_molecule.fixed is True
        assert p.thickness.raw_value == 10.0
        assert str(p.thickness.unit) == 'angstrom'
        assert p.thickness.fixed is True
        assert p.roughness.raw_value == 3.3
        assert str(p.roughness.unit) == 'angstrom'
        assert p.roughness.fixed is True
        assert_almost_equal(p.material.sld.raw_value, 2.2691419)
        assert_almost_equal(p.material.isld.raw_value, 0)
        assert p.material.name == 'C10H18NO8P in D2O'
        assert p.solvent.sld.raw_value == 6.36
        assert p.solvent.isld.raw_value == 0
        assert p.solvent.name == 'D2O'
        assert p.solvent_fraction.raw_value == 0.2
        assert str(p.solvent_fraction.unit) == 'dimensionless'
        assert p.solvent_fraction.fixed is True

    def test_from_pars(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        p = LayerAreaPerMolecule.from_pars(
            molecular_formula='C8O10H12P',
            thickness=12,
            solvent=h2o,
            solvent_fraction=0.5,
            area_per_molecule=50,
            roughness=2,
            name='PG/H2O',
        )
        assert p.molecular_formula == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvent_fraction.raw_value == 0.5

    def test_from_pars_constraint(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        p = LayerAreaPerMolecule.from_pars(
            molecular_formula='C8O10H12P',
            thickness=12,
            solvent=h2o,
            solvent_fraction=0.5,
            area_per_molecule=50,
            roughness=2,
            name='PG/H2O',
        )
        assert p.molecular_formula == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        assert_almost_equal(p.material.sld.raw_value, 0.31513666667)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvent_fraction.raw_value == 0.5
        p.area_per_molecule.value = 30
        assert p.area_per_molecule.raw_value == 30
        assert_almost_equal(p.material.sld.raw_value, 0.712227778)
        p.thickness.value = 10
        assert p.thickness.raw_value == 10
        assert_almost_equal(p.material.sld.raw_value, 0.910773333)

    def test_solvent_change(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        p = LayerAreaPerMolecule.from_pars(
            molecular_formula='C8O10H12P',
            thickness=12,
            solvent=h2o,
            solvent_fraction=0.5,
            area_per_molecule=50,
            roughness=2,
            name='PG/H2O',
        )
        assert p.molecular_formula == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        print(p.material)
        assert_almost_equal(p.material.sld.raw_value, 0.31513666667)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvent_fraction.raw_value == 0.5
        d2o = Material.from_pars(6.335, 0, 'D2O')
        p.solvent = d2o
        assert p.molecular_formula == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        assert_almost_equal(p.material.sld.raw_value, 3.7631366667)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == 6.335
        assert p.solvent.isld.raw_value == 0
        assert p.solvent_fraction.raw_value == 0.5

    def test_molecular_formula_change(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        p = LayerAreaPerMolecule.from_pars(
            molecular_formula='C8O10H12P',
            thickness=12,
            solvent=h2o,
            solvent_fraction=0.5,
            area_per_molecule=50,
            roughness=2,
            name='PG/H2O',
        )
        assert p.molecular_formula == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        assert_almost_equal(p.material.sld.raw_value, 0.31513666667)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2

        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvent_fraction.raw_value == 0.5
        assert p.material.name == 'C8O10H12P in H2O'
        p.molecular_formula = 'C8O10D12P'
        assert p.molecular_formula == 'C8O10D12P'
        assert p.area_per_molecule.raw_value == 50
        assert_almost_equal(p.material.sld.raw_value, 1.3566266666666666)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvent_fraction.raw_value == 0.5
        assert p.material.name == 'C8O10D12P in H2O'

    def test_dict_repr(self):
        p = LayerAreaPerMolecule.default()
        assert p._dict_repr == {
            'EasyLayerAreaPerMolecule': {
                'material': {
                    'C10H18NO8P in D2O': {
                        'solvent_fraction': 0.2,
                        'sld': '2.269e-6 1 / angstrom ** 2',
                        'isld': '0.000e-6 1 / angstrom ** 2',
                        'material': {
                            'C10H18NO8P': {'sld': '1.246e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}
                        },
                        'solvent': {'D2O': {'sld': '6.360e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}},
                    }
                },
                'thickness': '10.000 angstrom',
                'roughness': '3.300 angstrom',
            },
            'molecular_formula': 'C10H18NO8P',
            'area_per_molecule': '48.2 angstrom ** 2',
        }

    def test_dict_round_trip(self):
        p = LayerAreaPerMolecule.default()
        q = LayerAreaPerMolecule.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
