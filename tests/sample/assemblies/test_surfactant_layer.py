__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Item class module
"""

import unittest

from EasyReflectometry.sample.assemblies.surfactant_layer import SurfactantLayer
from EasyReflectometry.sample.elements.layers.layer import Layer
from EasyReflectometry.sample.elements.materials.material import Material


class TestSurfactantLayer(unittest.TestCase):

    def test_default(self):
        p = SurfactantLayer.default()
        assert p.name == 'DPPC'
        assert p._type == 'Surfactant Layer'

        assert p.layers[0].name == 'DPPC Tail'
        assert p.bottom_layer.name == 'DPPC Tail'
        assert p.tail_layer.name == 'DPPC Tail'
        assert p.tail_layer.chemical_formula == 'C32D64'

        assert p.layers[1].name == 'DPPC Head'
        assert p.top_layer.name == 'DPPC Head'
        assert p.head_layer.name == 'DPPC Head'
        assert p.head_layer.chemical_formula == 'C10H18NO8P'

    def test_from_pars(self):
        h2o = Material.from_pars(-0.561, 0, 'H2O')
        noth2o = Material.from_pars(0.561, 0, 'nH2O')
        p = SurfactantLayer.from_pars('C8O10H12P',
                                      12,
                                      h2o,
                                      0.5,
                                      50,
                                      2,
                                      'C10H24',
                                      10,
                                      noth2o,
                                      0.2,
                                      40,
                                      3,
                                      name='A Test')
        assert p.layers[0].name == 'A Test Tail Layer'
        assert p.tail_layer.name == 'A Test Tail Layer'
        assert p.tail_layer.chemical_formula == 'C8O10H12P'
        assert p.tail_layer.thickness.raw_value == 12
        assert p.tail_layer.solvent.as_data_dict() == h2o.as_data_dict()
        assert p.tail_layer.solvent_surface_coverage.raw_value == 0.5
        assert p.tail_layer.area_per_molecule.raw_value == 50
        assert p.tail_layer.roughness.raw_value == 2
        assert p.layers[1].name == 'A Test Head Layer'
        assert p.head_layer.name == 'A Test Head Layer'
        assert p.head_layer.chemical_formula == 'C10H24'
        assert p.head_layer.thickness.raw_value == 10
        assert p.head_layer.solvent.as_data_dict() == noth2o.as_data_dict()
        assert p.head_layer.solvent_surface_coverage.raw_value == 0.2
        assert p.head_layer.area_per_molecule.raw_value == 40
        assert p.name == 'A Test'

    def test_constraint_apm(self):
        p = SurfactantLayer.default()
        p.tail_layer.area_per_molecule.value = 30
        assert p.tail_layer.area_per_molecule.raw_value == 30.
        assert p.head_layer.area_per_molecule.raw_value == 48.2
        assert p.constrain_apm == False
        p.constrain_apm = True
        assert p.tail_layer.area_per_molecule.raw_value == 30
        assert p.head_layer.area_per_molecule.raw_value == 30
        assert p.constrain_apm == True
        p.tail_layer.area_per_molecule.value = 40
        assert p.tail_layer.area_per_molecule.raw_value == 40
        assert p.head_layer.area_per_molecule.raw_value == 40

    def test_conformal_roughness(self):
        p = SurfactantLayer.default()
        p.tail_layer.roughness.value = 2
        assert p.tail_layer.roughness.raw_value == 2
        assert p.head_layer.roughness.raw_value == 3
        p.conformal_roughness = True
        assert p.tail_layer.roughness.raw_value == 2
        assert p.head_layer.roughness.raw_value == 2
        assert p.conformal_roughness == True
        p.tail_layer.roughness.value = 4
        assert p.tail_layer.roughness.raw_value == 4
        assert p.head_layer.roughness.raw_value == 4

    def test_constain_solvent_roughness(self):
        p = SurfactantLayer.default()
        l = Layer.default()
        p.tail_layer.roughness.value = 2
        assert p.tail_layer.roughness.raw_value == 2
        assert p.head_layer.roughness.raw_value == 3
        assert l.roughness.raw_value == 3.3
        p.conformal_roughness = True
        p.constrain_solvent_roughness(l.roughness)
        assert p.tail_layer.roughness.raw_value == 2
        assert p.head_layer.roughness.raw_value == 2
        assert l.roughness.raw_value == 2
        assert p.conformal_roughness == True
        p.tail_layer.roughness.value = 4
        assert p.tail_layer.roughness.raw_value == 4
        assert p.head_layer.roughness.raw_value == 4
        assert l.roughness.raw_value == 4

    def test_dict_repr(self):
        p = SurfactantLayer.default()
        assert p._dict_repr == {
            'head_layer': {
                'DPPC Head': {
                    'material': {
                        'C10H18NO8P in D2O': {
                            'solvent_surface_coverage': 0.2,
                            'sld': '2.269e-6 1 / angstrom ** 2',
                            'isld': '0.000e-6 1 / angstrom ** 2',
                            'material': {
                                'C10H18NO8P': {
                                    'sld': '1.246e-6 1 / angstrom ** 2',
                                    'isld': '0.000e-6 1 / angstrom ** 2'
                                }
                            },
                            'solvent': {
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
                
                'chemical_formula': 'C10H18NO8P',
                'area_per_molecule': '48.2 angstrom ** 2'
            },
            'tail_layer': {
                'DPPC Tail': {
                    'material': {
                        'C32D64 in Air': {
                            'solvent_surface_coverage': 0.0,
                            'sld': '8.297e-6 1 / angstrom ** 2',
                            'isld': '0.000e-6 1 / angstrom ** 2',
                            'material': {
                                'C32D64': {
                                    'sld': '8.297e-6 1 / angstrom ** 2',
                                    'isld': '0.000e-6 1 / angstrom ** 2'
                                }
                            },
                            'solvent': {
                                'Air': {
                                    'sld': '0.000e-6 1 / angstrom ** 2',
                                    'isld': '0.000e-6 1 / angstrom ** 2'
                                }
                            }
                        }
                    },
                    'thickness': '16.000 angstrom',
                    'roughness': '3.000 angstrom'
                },
                'chemical_formula': 'C32D64',
                'area_per_molecule': '48.2 angstrom ** 2'
            },            'area per molecule constrained': False,
            'conformal roughness': False
        }
    
    def test_dict_round_trip(self):
        p = SurfactantLayer.default()
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()


    def test_dict_round_trip_apm_constraint_enabled(self):
        p = SurfactantLayer.default()
        p.constrain_apm = True
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
    
    def test_dict_round_trip_apm_constraint_disabled(self):
        p = SurfactantLayer.default()
        p.constrain_apm = True
        p.constrain_apm = False
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

    def test_dict_round_trip_roughness_constraint_enabled(self):
        p = SurfactantLayer.default()
        p.conformal_roughness = True
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

    def test_dict_round_trip_roughness_constraint_disabled(self):
        p = SurfactantLayer.default()
        p.conformal_roughness = True
        p.conformal_roughness = False
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
