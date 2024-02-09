__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Item class module
"""

import unittest

from EasyReflectometry.sample.assemblies.surfactant_layer import SurfactantLayer
from EasyReflectometry.sample.elementals.layer import Layer
from EasyReflectometry.sample.elementals.material import Material


class TestSurfactantLayer(unittest.TestCase):

    def test_default(self):
        p = SurfactantLayer.default()
        assert p.name == 'DPPC'
        assert p.layers[0].name == 'DPPC Tail'
        assert p.layers[1].name == 'DPPC Head'
        assert p.layers[0].chemical_structure == 'C32D64'
        assert p.layers[1].chemical_structure == 'C10H18NO8P'
        assert p.type == 'Surfactant Layer'

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
        assert p.layers[0].name == 'A Test Layer 1'
        assert p.layers[0].chemical_structure == 'C8O10H12P'
        assert p.layers[0].thickness.raw_value == 12
        assert p.layers[0].solvent.as_data_dict() == h2o.as_data_dict()
        assert p.layers[0].solvation.raw_value == 0.5
        assert p.layers[0].area_per_molecule.raw_value == 50
        assert p.layers[0].roughness.raw_value == 2
        assert p.layers[1].name == 'A Test Layer 2'
        assert p.layers[1].chemical_structure == 'C10H24'
        assert p.layers[1].thickness.raw_value == 10
        assert p.layers[1].solvent.as_data_dict() == noth2o.as_data_dict()
        assert p.layers[1].solvation.raw_value == 0.2
        assert p.layers[1].area_per_molecule.raw_value == 40
        assert p.name == 'A Test'

    def test_constraint_apm(self):
        p = SurfactantLayer.default()
        p.layers[0].area_per_molecule.value = 30
        assert p.layers[0].area_per_molecule.raw_value == 30.
        assert p.layers[1].area_per_molecule.raw_value == 48.2
        assert p.constrain_apm == False
        p.constrain_apm = True
        assert p.layers[0].area_per_molecule.raw_value == 30
        assert p.layers[1].area_per_molecule.raw_value == 30
        assert p.constrain_apm == True
        p.layers[0].area_per_molecule.value = 40
        assert p.layers[0].area_per_molecule.raw_value == 40
        assert p.layers[1].area_per_molecule.raw_value == 40

    def test_conformal_roughness(self):
        p = SurfactantLayer.default()
        p.layers[0].roughness.value = 2
        assert p.layers[0].roughness.raw_value == 2
        assert p.layers[1].roughness.raw_value == 3
        p.conformal_roughness = True
        assert p.layers[0].roughness.raw_value == 2
        assert p.layers[1].roughness.raw_value == 2
        assert p.conformal_roughness == True
        p.layers[0].roughness.value = 4
        assert p.layers[0].roughness.raw_value == 4
        assert p.layers[1].roughness.raw_value == 4

    def test_constain_solvent_roughness(self):
        p = SurfactantLayer.default()
        l = Layer.default()
        p.layers[0].roughness.value = 2
        assert p.layers[0].roughness.raw_value == 2
        assert p.layers[1].roughness.raw_value == 3
        assert l.roughness.raw_value == 3.3
        p.conformal_roughness = True
        p.constrain_solvent_roughness(l.roughness)
        assert p.layers[0].roughness.raw_value == 2
        assert p.layers[1].roughness.raw_value == 2
        assert l.roughness.raw_value == 2
        assert p.conformal_roughness == True
        p.layers[0].roughness.value = 4
        assert p.layers[0].roughness.raw_value == 4
        assert p.layers[1].roughness.raw_value == 4
        assert l.roughness.raw_value == 4

    def test_dict_repr(self):
        p = SurfactantLayer.default()
        assert p._dict_repr == {
            'layer1': {
                'DPPC Tail': {
                    'material': {
                        'C32D64/Air': {
                            'fraction': 0.0,
                            'sld': '8.297e-6 1 / angstrom ** 2',
                            'isld': '0.000e-6 1 / angstrom ** 2',
                            'material1': {
                                'C32D64': {
                                    'sld': '8.297e-6 1 / angstrom ** 2',
                                    'isld': '0.000e-6 1 / angstrom ** 2'
                                }
                            },
                            'material2': {
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
                'chemical_structure': 'C32D64',
                'area_per_molecule': '48.2 angstrom ** 2'
            },
            'layer2': {
                'DPPC Head': {
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
            },
            'area per molecule constrained': False,
            'conformal roughness': False
        }
    
    def test_dict_round_trip(self):
        p = SurfactantLayer.default()
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()


    def test_dict_round_trip_apm(self):
        p = SurfactantLayer.default()
        p.constrain_apm = True
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
    
    def test_dict_round_trip_apm2(self):
        p = SurfactantLayer.default()
        p.constrain_apm = True
        p.constrain_apm = False
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

    def test_dict_round_trip_roughness(self):
        p = SurfactantLayer.default()
        p.conformal_roughness = True
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()

    def test_dict_round_trip_roughness2(self):
        p = SurfactantLayer.default()
        p.conformal_roughness = True
        p.conformal_roughness = False
        q = SurfactantLayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()
