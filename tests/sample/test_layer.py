__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Layer class module
"""

import os
import unittest

import numpy as np
from numpy.testing import assert_almost_equal
from numpy.testing import assert_equal

from EasyReflectometry.interface import InterfaceFactory
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.layer import LayerApm
from EasyReflectometry.sample.material import Material
from EasyReflectometry.special.calculations import apm_to_sld
from EasyReflectometry.special.calculations import neutron_scattering_length


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

    def test_dict_round_trip(self):
        p = Layer.default()
        q = Layer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()


class TestLayerApm(unittest.TestCase):

    def test_default(self):
        p = LayerApm.default()
        assert p.chemical_structure == 'C10H18NO8P'
        assert p.area_per_molecule.raw_value == 48.2
        assert str(p.area_per_molecule.unit) == 'angstrom ** 2'
        assert p.area_per_molecule.fixed is True
        assert p.thickness.raw_value == 10.
        assert str(p.thickness.unit) == 'angstrom'
        assert p.thickness.fixed is True
        assert p.roughness.raw_value == 3
        assert str(p.roughness.unit) == 'angstrom'
        assert p.roughness.fixed is True
        assert p.solvent.sld.raw_value == 6.36
        assert p.solvent.isld.raw_value == 0
        assert p.solvent.name == 'D2O'
        assert p.solvation.raw_value == 0.2
        assert str(p.solvation.unit) == 'dimensionless'
        assert p.solvation.fixed is True

    def test_from_pars(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        p = LayerApm.from_pars('C8O10H12P', 12, h2o, 0.5, 50, 2, name='PG/H2O')
        assert p.chemical_structure == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvation.raw_value == 0.5

    def test_from_pars_constraint(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        p = LayerApm.from_pars('C8O10H12P', 12, h2o, 0.5, 50, 2, name='PG/H2O')
        assert p.chemical_structure == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        assert_almost_equal(p.material.sld.raw_value, 0.31513666667)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvation.raw_value == 0.5
        p.area_per_molecule.value = 30
        assert p.area_per_molecule.raw_value == 30
        assert_almost_equal(p.material.sld.raw_value, 0.712227778)
        p.thickness.value = 10
        assert p.thickness.raw_value == 10
        assert_almost_equal(p.material.sld.raw_value, 0.910773333)

    def test_solvent_change(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        p = LayerApm.from_pars('C8O10H12P', 12, h2o, 0.5, 50, 2, name='PG/H2O')
        assert p.chemical_structure == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        print(p.material)
        assert_almost_equal(p.material.sld.raw_value, 0.31513666667)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvation.raw_value == 0.5
        d2o = Material.from_pars(6.335, 0, 'D2O')
        p.solvent = d2o
        assert p.chemical_structure == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        assert_almost_equal(p.material.sld.raw_value, 3.7631366667)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == 6.335
        assert p.solvent.isld.raw_value == 0
        assert p.solvation.raw_value == 0.5

    def test_chemical_structure_change(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        p = LayerApm.from_pars('C8O10H12P', 12, h2o, 0.5, 50, 2)
        assert p.chemical_structure == 'C8O10H12P'
        assert p.area_per_molecule.raw_value == 50
        assert_almost_equal(p.material.sld.raw_value, 0.31513666667)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvation.raw_value == 0.5
        assert p.material.name == 'C8O10H12P/H2O'
        p.chemical_structure = 'C8O10D12P'
        assert p.chemical_structure == 'C8O10D12P'
        assert p.area_per_molecule.raw_value == 50
        assert_almost_equal(p.material.sld.raw_value, 1.3566266666666666)
        assert p.thickness.raw_value == 12
        assert p.roughness.raw_value == 2
        assert p.solvent.sld.raw_value == -0.561
        assert p.solvent.isld.raw_value == 0
        assert p.solvation.raw_value == 0.5 
        assert p.material.name == 'C8O10D12P/H2O'

    def test_dict_repr(self):
        p = LayerApm.default()
        print(p.material.sld)
        print(p.material.isld)
        assert p._dict_repr == {
            'EasyLayerApm': {
                'material': {
                    'C10H18NO8P/D2O': {
                        'fraction': 0.2,
                        'sld': '2.269e-6 1 / angstrom ** 2',
                        'isld': '0.000e-6 1 / angstrom ** 2',
                        'material1': {
                            'C10H18NO8P': {
                                'sld': '1.246e-6 1 / angstrom ** 2',
                                'isld': '0.000e-6 1 / angstrom ** 2'
                            }
                        },
                        'material2': {
                            'D2O': {
                                'sld': '6.360e-6 1 / angstrom ** 2',
                                'isld': '0.000e-6 1 / angstrom ** 2'
                            }
                        }
                    }
                },
                'thickness': '10.000 angstrom',
                'roughness': '3.000 angstrom'
            },
            'chemical_structure': 'C10H18NO8P',
            'area_per_molecule': '48.2 angstrom ** 2'
        }

    def test_dict_round_trip(self):
        p = LayerApm.default()
        q = LayerApm.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()