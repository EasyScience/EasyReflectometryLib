"""
Tests for SurfactantLayer class module
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'


import unittest

from easyscience import global_object

from easyreflectometry.sample.assemblies.surfactant_layer import SurfactantLayer
from easyreflectometry.sample.elements.layers.layer import Layer
from easyreflectometry.sample.elements.layers.layer_area_per_molecule import LayerAreaPerMolecule
from easyreflectometry.sample.elements.materials.material import Material


class TestSurfactantLayer:
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
        assert p.tail_layer.thickness.value == 12
        assert p.tail_layer.solvent.as_data_dict() == h2o.as_data_dict()
        assert p.tail_layer.solvent_fraction == 0.5
        assert p.tail_layer.area_per_molecule == 50
        assert p.tail_layer.roughness.value == 2
        assert p.layers[1].name == 'A Test Head Layer'
        assert p.head_layer.name == 'A Test Head Layer'
        assert p.head_layer.molecular_formula == 'C10H24'
        assert p.head_layer.thickness.value == 10
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
        assert p.tail_layer.roughness.value == 2
        assert p.head_layer.roughness.value == 3
        p.conformal_roughness = True
        assert p.tail_layer.roughness.value == 2
        assert p.head_layer.roughness.value == 2
        assert p.conformal_roughness is True
        p.tail_layer.roughness.value = 4
        assert p.tail_layer.roughness.value == 4
        assert p.head_layer.roughness.value == 4

    def test_constain_solvent_roughness(self):
        p = SurfactantLayer()
        layer = Layer()
        p.tail_layer.roughness.value = 2
        assert p.tail_layer.roughness.value == 2
        assert p.head_layer.roughness.value == 3
        assert layer.roughness.value == 3.3
        p.conformal_roughness = True
        p.constrain_solvent_roughness(layer.roughness)
        assert p.tail_layer.roughness.value == 2
        assert p.head_layer.roughness.value == 2
        assert layer.roughness.value == 2
        assert p.conformal_roughness is True
        p.tail_layer.roughness.value = 4
        assert p.tail_layer.roughness.value == 4
        assert p.head_layer.roughness.value == 4
        assert layer.roughness.value == 4

        # Seems to be needed to due to the constraint
        global_object.map._clear()

    def test_dict_repr(self):
        p = SurfactantLayer()
        assert p._dict_repr == {
            'EasySurfactantLayer': {
                'head_layer': {
                    'DPPC Head': {
                        'material': {
                            'C10H18NO8P in D2O': {
                                'solvent_fraction': '0.200 dimensionless',
                                'sld': '2.269e-6 1/Å^2',
                                'isld': '0.000e-6 1/Å^2',
                                'material': {'C10H18NO8P': {'sld': '1.246e-6 1/Å^2', 'isld': '0.000e-6 1/Å^2'}},
                                'solvent': {'D2O': {'sld': '6.360e-6 1/Å^2', 'isld': '0.000e-6 1/Å^2'}},
                            }
                        },
                        'thickness': '10.000 Å',
                        'roughness': '3.000 Å',
                    },
                    'molecular_formula': 'C10H18NO8P',
                    'area_per_molecule': '48.20 Å^2',
                },
                'tail_layer': {
                    'DPPC Tail': {
                        'material': {
                            'C32D64 in Air': {
                                'solvent_fraction': '0.000 dimensionless',
                                'sld': '8.297e-6 1/Å^2',
                                'isld': '0.000e-6 1/Å^2',
                                'material': {'C32D64': {'sld': '8.297e-6 1/Å^2', 'isld': '0.000e-6 1/Å^2'}},
                                'solvent': {'Air': {'sld': '0.000e-6 1/Å^2', 'isld': '0.000e-6 1/Å^2'}},
                            }
                        },
                        'thickness': '16.000 Å',
                        'roughness': '3.000 Å',
                    },
                    'molecular_formula': 'C32D64',
                    'area_per_molecule': '48.20 Å^2',
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


def test_dict_round_trip():
    # When
    solvent = Material(-0.561, 0, 'H2O')
    tail_layer = LayerAreaPerMolecule(
        molecular_formula='CO2',
        solvent=solvent,
        solvent_fraction=0.25,
        area_per_molecule=50,
        thickness=10,
        roughness=4,
    )
    head_layer = LayerAreaPerMolecule(
        molecular_formula='CH2',
        solvent_fraction=0.75,
        area_per_molecule=50,
        thickness=5,
        roughness=2,
    )
    p = SurfactantLayer(head_layer=head_layer, tail_layer=tail_layer)
    p_dict = p.as_dict()
    global_object.map._clear()

    # Then
    q = SurfactantLayer.from_dict(p_dict)

    # Expect
    assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())


def test_dict_round_trip_area_per_molecule_constraint_enabled():
    # When
    p = SurfactantLayer()
    p.constrain_area_per_molecule = True
    p_dict = p.as_dict()
    global_object.map._clear()

    # Then
    q = SurfactantLayer.from_dict(p_dict)

    # Expect
    assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())

    # Seems to be needed to due to the constraint
    global_object.map._clear()


def test_dict_round_trip_area_per_molecule_constraint_disabled():
    # When
    p = SurfactantLayer()
    p.constrain_area_per_molecule = True
    p.constrain_area_per_molecule = False
    p_dict = p.as_dict()
    global_object.map._clear()

    # Then
    q = SurfactantLayer.from_dict(p_dict)

    # Expect
    assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())


def test_dict_round_trip_roughness_constraint_enabled():
    # When
    p = SurfactantLayer()
    p.conformal_roughness = True
    p_dict = p.as_dict()
    global_object.map._clear()

    # Then
    q = SurfactantLayer.from_dict(p_dict)

    # Expect
    assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())

    # Seems to be needed to due to the constraint
    global_object.map._clear()


def test_dict_round_trip_roughness_constraint_disabled():
    # When
    p = SurfactantLayer()
    p.conformal_roughness = True
    p.conformal_roughness = False
    p_dict = p.as_dict()
    global_object.map._clear()

    # Then
    q = SurfactantLayer.from_dict(p_dict)

    # Expect
    assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())
