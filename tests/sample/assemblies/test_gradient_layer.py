from unittest.mock import MagicMock

import pytest
from numpy.testing import assert_almost_equal

import EasyReflectometry.sample.assemblies.gradient_layer
from EasyReflectometry.sample.assemblies.gradient_layer import GradientLayer
from EasyReflectometry.sample.assemblies.gradient_layer import (
    _apply_thickness_constraints,
    _linear_gradient,
    _prepare_gradient_layers,
)
from EasyReflectometry.sample.elementals.layer import Layer
from EasyReflectometry.sample.elementals.material import Material


class TestGradientLayer():

    @pytest.fixture
    def gradient_layer(self):
        self.init = Material.from_pars(10.0, -10.0, 'Material_1')
        self.final = Material.from_pars(0.0, 0.0, 'Material_2')

        return GradientLayer(
            initial_material=self.init,
            final_material=self.final,
            thickness=1.0,
            roughness=2.0,
            discretisation_elements=10,
            name='Test',
            interface=None
        )

    def test_init(self, gradient_layer):
        # When Then Expect
        assert len(gradient_layer.layers) == 10 
        assert gradient_layer.name, 'Test'
        assert gradient_layer.type, 'Gradient-layer'
        assert gradient_layer.interface is None
        assert gradient_layer.thickness == 1.0
        assert gradient_layer.layers.name == '0/1/2/3/4/5/6/7/8/9'
        assert gradient_layer.layers[0].material.sld.raw_value == 10.0
        assert gradient_layer.layers[5].material.sld.raw_value == 5.0
        assert gradient_layer.layers[0].thickness.raw_value == 0.1
        assert gradient_layer.layers[5].material.isld.raw_value == -5.0
        assert gradient_layer.layers[9].material.isld.raw_value == -1.0

    def test_default(self):
        # When Then
        result = GradientLayer.default()
        
        # Expect
        assert result.name == 'Air-Deuterium'
        assert result.type, 'Gradient-layer'
        assert result.interface is None
        assert len(result.layers) == 10
        assert result.layers.name == '0/1/2/3/4/5/6/7/8/9'

    def test_from_pars(self):
        # When
        init = Material.from_pars(6.908, -0.278, 'Boron')
        final = Material.from_pars(0.487, 0.000, 'Potassium')
        
        # Then
        result = GradientLayer.from_pars(
            initial_material=init,
            final_material=final,
            thickness=10.0,
            roughness=1.0,
            discretisation_elements=5,
            name='gradientItem'
        )

        # Expect
        assert result.name, 'gradientItem'
        assert result.type, 'Gradient-layer'
        assert result.interface is None
        assert len(result.layers) == 5
        assert result.layers.name == '0/1/2/3/4'

    def test_add_layer(self, gradient_layer):
        # When Then Expect
        with pytest.raises(NotImplementedError, match=r".* add .*"):
            gradient_layer.add_layer(Layer.default())

    def test_duplicate_layer(self, gradient_layer):
        # When Then Expect
        with pytest.raises(NotImplementedError, match=r".* duplicate .*"):
            gradient_layer.duplicate_layer(1)

    def test_remove_layer(self, gradient_layer):
        # When Then Expect
        with pytest.raises(NotImplementedError, match=r".* remove .*"):
            gradient_layer.remove_layer(1)

    def test_repr(self, gradient_layer):
        # When Then Expect
        expected_str = "type: Gradient-layer\nthickness: 1.0\ndiscretisation_elements: 10\ninitial_layer:\n  '0':\n    material:\n      EasyMaterial:\n        sld: 10.000e-6 1 / angstrom ** 2\n        isld: -10.000e-6 1 / angstrom ** 2\n    thickness: 0.100 angstrom\n    roughness: 2.000 angstrom\nfinal_layer:\n  '9':\n    material:\n      EasyMaterial:\n        sld: 1.000e-6 1 / angstrom ** 2\n        isld: -1.000e-6 1 / angstrom ** 2\n    thickness: 0.100 angstrom\n    roughness: 2.000 angstrom\n"
        assert gradient_layer.__repr__() == expected_str

    def test_dict_round_trip(self, gradient_layer):
        # When Then
        result = GradientLayer.from_dict(gradient_layer.as_dict())
        
        # Expect
        assert result.as_data_dict() == gradient_layer.as_data_dict()
        assert len(gradient_layer.layers) == len(result.layers)
        # Just one layer of the generated layers is checked
        assert gradient_layer.layers[5].__repr__() == result.layers[5].__repr__()

    def test_thickness_setter(self, gradient_layer):
        # When
        gradient_layer.thickness = 10.0

        # Then
        assert gradient_layer.thickness == 10.0
        assert gradient_layer.layers[0].thickness.raw_value == 1.0
        assert gradient_layer.layers[9].thickness.raw_value == 1.0

    def test_thickness_getter(self, gradient_layer):
        # When
        gradient_layer.layers = MagicMock()
        gradient_layer.layers[0].thickness.raw_value = 10.0

        # Then
        # discretisation_elements * discrete_layer_thickness
        assert gradient_layer.thickness == 10.0

    def test_roughness_setter(self, gradient_layer):
        # When
        gradient_layer.roughness = 10.0

        # Then
        assert gradient_layer.roughness == 10.0
        assert gradient_layer.layers[0].roughness.raw_value == 10.0
        assert gradient_layer.layers[9].roughness.raw_value == 10.0

    def test_thickness_getter(self, gradient_layer):
        # When
        gradient_layer.layers = MagicMock()
        gradient_layer.layers[0].roughness.raw_value = 10.0

        # Then
        # discretisation_elements * discrete_layer_thickness
        assert gradient_layer.roughness == 10.0


def test_linear_gradient_increasing():
    # When Then
    result = _linear_gradient(init_value=1.5, final_value=2.5, discretisation_elements=10)

    # Expect
    assert_almost_equal([1.5, 1.6, 1.7, 1.8, 1.9, 2. , 2.1, 2.2, 2.3, 2.4, 2.5], result)


def test_linear_gradient_decreasing():
    # When Then
    result = _linear_gradient(init_value=2.5, final_value=1.5, discretisation_elements=10)

    # Expect
    assert_almost_equal([2.5, 2.4, 2.3, 2.2, 2.1, 2. , 1.9, 1.8, 1.7, 1.6, 1.5], result)


def test_linear_gradient_same():
    # When Then
    result = _linear_gradient(init_value=2.5, final_value=2.5, discretisation_elements=10)

    # Expect
    assert_almost_equal([2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5], result)


def test_prepare_gradient_layers(monkeypatch):
    # When
    mock_material_1 = MagicMock()
    mock_material_2 = MagicMock()
    mock_Layer = MagicMock()
    mock_Material = MagicMock()
    mock_Material.from_pars = MagicMock(return_value='Material_from_pars')
    mock_linear_gradient = MagicMock(return_value=[1.0, 2.0, 3.0])
    monkeypatch.setattr(EasyReflectometry.sample.assemblies.gradient_layer, '_linear_gradient', mock_linear_gradient)
    monkeypatch.setattr(EasyReflectometry.sample.assemblies.gradient_layer, 'Layer', mock_Layer)
    monkeypatch.setattr(EasyReflectometry.sample.assemblies.gradient_layer, 'Material', mock_Material)

    # Then
    result = _prepare_gradient_layers(mock_material_1, mock_material_2, 3, None)

    # When
    assert mock_Material.from_pars.call_count == 3
    assert mock_Material.from_pars.call_args_list[0][0] == (1.0, 1.0)
    assert mock_Material.from_pars.call_args_list[1][0] == (2.0, 2.0)
    assert mock_Material.from_pars.call_args_list[2][0] == (3.0, 3.0)
    assert mock_Layer.from_pars.call_count == 3
    assert mock_Layer.from_pars.call_args_list[0][1]['material'] == 'Material_from_pars'
    assert mock_Layer.from_pars.call_args_list[0][1]['thickness'] == 0.0
    assert mock_Layer.from_pars.call_args_list[0][1]['name'] == '0'
    assert mock_Layer.from_pars.call_args_list[0][1]['interface'] == None

def test_apply_thickness_constraints(monkeypatch):
    # When 
    mock_layer_0 = MagicMock()
    mock_layer_0.thickness = MagicMock()
    mock_layer_0.thickness.user_constraints = {}
    mock_layer_1 = MagicMock()
    layers = [mock_layer_0, mock_layer_1]
    mock_layer_1.thickness = MagicMock()
    mock_obj_constraint = MagicMock()
    mock_ObjConstraint = MagicMock(return_value=mock_obj_constraint)
    monkeypatch.setattr(EasyReflectometry.sample.assemblies.gradient_layer, 'ObjConstraint', mock_ObjConstraint)

    #Then
    _apply_thickness_constraints(layers)

    #Expect
    assert mock_layer_0.thickness.enabled is True
    assert mock_layer_1.thickness.enabled is True
    assert layers[0].thickness.user_constraints['thickness_1'].enabled is True
    assert layers[0].thickness.user_constraints['thickness_1'] == mock_obj_constraint
    mock_ObjConstraint.assert_called_once_with(dependent_obj=mock_layer_1.thickness, operator='', independent_obj=mock_layer_0.thickness)
