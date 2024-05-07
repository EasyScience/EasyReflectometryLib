"""
Tests for SurfactantLayer class module
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'


import unittest

from easyreflectometry.sample.assemblies.surfactant_layer import SurfactantLayer
from easyreflectometry.sample.elements.layers.layer import Layer
from easyreflectometry.sample.elements.materials.material import Material


class TestSurfactantLayer(unittest.TestCase):
    def test_default(self):
        p = SurfactantLayer()
        assert p.name == 'EasySurfactantLayer'
        assert p._type == 'Surfactant Layer'

        assert p.layers[0].name == 'DPPC Tail'
        assert p.front_layer.name == 'DPPC Tail'
        assert p.tail_layer.name == 'DPPC Tail'
        assert p.tail_layer.molecular_formula == 'C32D64'

        assert p.layers[1].name == 'DPPC Head'
        assert p.back_layer.name == 'DPPC Head'
        assert p.head_layer.name == 'DPPC Head'
        assert p.head_layer.molecular_formula == 'C10H18NO8P'

    @unittest.skip('It is no longer possible to create a surfactant layer without specifying the materials.')
    def test_from_pars(self):
        h2o = Material(-0.561, 0, 'H2O')
        noth2o = Material(0.561, 0, 'nH2O')
        p = SurfactantLayer.from_pars('C8O10H12P', 12, h2o, 0.5, 50, 2, 'C10H24', 10, noth2o, 0.2, 40, 3, name='A Test')
        assert p.layers[0].name == 'A Test Tail Layer'
        assert p.tail_layer.name == 'A Test Tail Layer'
        assert p.tail_layer.molecular_formula == 'C8O10H12P'
        assert p.tail_layer.thickness.raw_value == 12
        assert p.tail_layer.solvent.as_data_dict() == h2o.as_data_dict()
        assert p.tail_layer.solvent_fraction == 0.5
        assert p.tail_layer.area_per_molecule == 50
        assert p.tail_layer.roughness.raw_value == 2
        assert p.layers[1].name == 'A Test Head Layer'
        assert p.head_layer.name == 'A Test Head Layer'
        assert p.head_layer.molecular_formula == 'C10H24'
        assert p.head_layer.thickness.raw_value == 10
        assert p.head_layer.solvent.as_data_dict() == noth2o.as_data_dict()
        assert p.head_layer.solvent_fraction == 0.2
        assert p.head_layer.area_per_molecule == 40
        assert p.name == 'A Test'

    def test_constraint_area_per_molecule(self):
        p = SurfactantLayer()
        p.tail_layer._area_per_molecule.value = 30
        assert p.tail_layer.area_per_molecule == 30.0
        assert p.head_layer.area_per_molecule == 48.2
        assert p.constrain_area_per_molecule is False
        p.constrain_area_per_molecule = True
        assert p.tail_layer.area_per_molecule == 30
        assert p.head_layer.area_per_molecule == 30
        assert p.constrain_area_per_molecule is True
        p.tail_layer._area_per_molecule.value = 40
        assert p.tail_layer.area_per_molecule == 40
        assert p.head_layer.area_per_molecule == 40

    def test_conformal_roughness(self):
        p = SurfactantLayer()
        p.tail_layer.roughness.value = 2
        assert p.tail_layer.roughness.raw_value == 2
        assert p.head_layer.roughness.raw_value == 3
        p.conformal_roughness = True
        assert p.tail_layer.roughness.raw_value == 2
        assert p.head_layer.roughness.raw_value == 2
        assert p.conformal_roughness is True
        p.tail_layer.roughness.value = 4
        assert p.tail_layer.roughness.raw_value == 4
        assert p.head_layer.roughness.raw_value == 4

    def test_constain_solvent_roughness(self):
        p = SurfactantLayer()
        layer = Layer()
        p.tail_layer.roughness.value = 2
        assert p.tail_layer.roughness.raw_value == 2
        assert p.head_layer.roughness.raw_value == 3
        assert layer.roughness.raw_value == 3.3
        p.conformal_roughness = True
        p.constrain_solvent_roughness(layer.roughness)
        assert p.tail_layer.roughness.raw_value == 2
        assert p.head_layer.roughness.raw_value == 2
        assert layer.roughness.raw_value == 2
        assert p.conformal_roughness is True
        p.tail_layer.roughness.value = 4
        assert p.tail_layer.roughness.raw_value == 4
        assert p.head_layer.roughness.raw_value == 4
        assert layer.roughness.raw_value == 4

    def test_dict_repr(self):
        p = SurfactantLayer()
        assert p._dict_repr == {
            'EasySurfactantLayer': {
                'head_layer': {
                    'DPPC Head': {
                        'material': {
                            'C10H18NO8P in D2O': {
                                'solvent_fraction': '0.200 dimensionless',
                                'sld': '2.269e-6 1 / angstrom ** 2',
                                'isld': '0.000e-6 1 / angstrom ** 2',
                                'material': {
                                    'C10H18NO8P': {'sld': '1.246e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}
                                },
                                'solvent': {
                                    'D2O': {'sld': '6.360e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}
                                },
                            }
                        },
                        'thickness': '10.000 angstrom',
                        'roughness': '3.000 angstrom',
                    },
                    'molecular_formula': 'C10H18NO8P',
                    'area_per_molecule': '48.20 angstrom ** 2',
                },
                'tail_layer': {
                    'DPPC Tail': {
                        'material': {
                            'C32D64 in Air': {
                                'solvent_fraction': '0.000 dimensionless',
                                'sld': '8.297e-6 1 / angstrom ** 2',
                                'isld': '0.000e-6 1 / angstrom ** 2',
                                'material': {
                                    'C32D64': {'sld': '8.297e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}
                                },
                                'solvent': {
                                    'Air': {'sld': '0.000e-6 1 / angstrom ** 2', 'isld': '0.000e-6 1 / angstrom ** 2'}
                                },
                            }
                        },
                        'thickness': '16.000 angstrom',
                        'roughness': '3.000 angstrom',
                    },
                    'molecular_formula': 'C32D64',
                    'area_per_molecule': '48.20 angstrom ** 2',
                },
                'area per molecule constrained': False,
                'conformal roughness': False,
            }
        }

    def test_get_head_layer(self):
        # When
        p = SurfactantLayer()

        # Then Expect
        assert p.head_layer == p.back_layer
        assert p.head_layer == p.layers[1]

    def test_set_head_layer(self):
        # When
        p = SurfactantLayer()
        new_layer = Layer()

        # Then
        p.head_layer = new_layer

        # Expect
        assert p.head_layer == new_layer
        assert p.back_layer == new_layer
        assert p.layers[1] == new_layer

    def test_get_tail_layer(self):
        # When
        p = SurfactantLayer()

        # Then Expect
        assert p.tail_layer == p.front_layer
        assert p.tail_layer == p.layers[0]

    def test_set_tail_layer(self):
        # When
        p = SurfactantLayer()
        new_layer = Layer()

        # Then
        p.tail_layer = new_layer

        # Expect
        assert p.tail_layer == new_layer
        assert p.front_layer == new_layer
        assert p.layers[0] == new_layer

    def test_dict_round_trip(self):
        p = SurfactantLayer()
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

    def test_dict_round_trip_area_per_molecule_constraint_enabled(self):
        p = SurfactantLayer()
        p.constrain_area_per_molecule = True
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

    def test_dict_round_trip_area_per_molecule_constraint_disabled(self):
        p = SurfactantLayer()
        p.constrain_area_per_molecule = True
        p.constrain_area_per_molecule = False
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

    def test_dict_round_trip_roughness_constraint_enabled(self):
        p = SurfactantLayer()
        p.conformal_roughness = True
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

    def test_dict_round_trip_roughness_constraint_disabled(self):
        p = SurfactantLayer()
        p.conformal_roughness = True
        p.conformal_roughness = False
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
